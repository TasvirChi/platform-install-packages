%define prefix /opt/borhan
%define batch_confdir %{prefix}/app/configurations/batch/ 
%define borhan_user	borhan
%define borhan_group	borhan
%define apache_user	apache
%define apache_group	apache
Summary: Borhan Open Source Video Platform - batch server 
Name: borhan-batch
Version: 12.8.0
Release: 1
License: AGPLv3+
Group: Server/Platform 
Source0: zz-%{name}.ini
Source1: borhan-batch
Source3: batch.ini.template 
URL: http://borhan.org
Buildroot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires: borhan-base, borhan-ffmpeg, borhan-ffmpeg-aux, php, curl, httpd, sox, ImageMagick, borhan-sshpass, php-pecl-memcache,  php-pecl-ssh2,php-pecl-apc,php-mcrypt,memcached,borhan-mediainfo, borhan-segmenter, mod_ssl,borhan-mencoder
#php-pecl-zendopcache
%{?el7:Requires: php-pecl-zendopcache}
#PreReq: httpd
Requires(post): chkconfig
Requires(preun): chkconfig
# This is for /sbin/service
Requires(preun): initscripts
BuildArch: noarch

%description
Borhan is the world's first Open Source Online Video Platform, transforming the way people work, 
learn, and entertain using online video. 
The Borhan platform empowers media applications with advanced video management, publishing, 
and monetization tools that increase their reach and monetization and simplify their video operations. 
Borhan improves productivity and interaction among millions of employees by providing enterprises 
powerful online video tools for boosting internal knowledge sharing, training, and collaboration, 
and for more effective marketing. Borhan offers next generation learning for millions of students and 
teachers by providing educational institutions disruptive online video solutions for improved teaching,
learning, and increased engagement across campuses and beyond. 
For more information visit: http://corp.borhan.com, http://www.borhan.org and http://www.html5video.org.

This package sets up a node to be a batch server.


%build

%install
mkdir -p $RPM_BUILD_ROOT/%{_sysconfdir}/init.d
mkdir -p $RPM_BUILD_ROOT/%{_sysconfdir}/php.d
mkdir -p $RPM_BUILD_ROOT/%{batch_confdir}
mkdir -p $RPM_BUILD_ROOT/%{prefix}/log/batch
cp %{SOURCE0} $RPM_BUILD_ROOT/%{_sysconfdir}/php.d/zz-%{name}.ini
cp %{SOURCE1} $RPM_BUILD_ROOT/%{_sysconfdir}/init.d/%{name}
mkdir -p $RPM_BUILD_ROOT/%{prefix}/app/configurations/apache
cp %{SOURCE3} $RPM_BUILD_ROOT/%{prefix}/app/configurations/batch
sed 's#@WEB_DIR@#%{prefix}/web#g' -i $RPM_BUILD_ROOT/%{_sysconfdir}/php.d/zz-%{name}.ini


%clean
rm -rf %{buildroot}

%pre
# maybe one day we will support SELinux in which case this can be ommitted.
if which getenforce >> /dev/null 2>&1; then
	
	if [ `getenforce` = 'Enforcing' ];then
		echo "You have SELinux enabled, please change to permissive mode with:
# setenforce permissive
and then edit /etc/selinux/config to make the change permanent."
		exit 1;
	fi
fi

%post
# now replace tokens
sed -i "s@^\(params.ImageMagickCmd\)\s*=.*@\1=%{_bindir}/convert@" $RPM_BUILD_ROOT%{batch_confdir}/batch.ini.template
sed -i "s@^\(params.mediaInfoCmd\)\s*=.*@\1=%{prefix}/bin/mediainfo@" $RPM_BUILD_ROOT%{batch_confdir}/batch.ini.template
#sed 's#@APACHE_SERVICE@#httpd#g' -i %{prefix}/app/configurations/monit.avail/httpd.rc

#ln -fs %{prefix}/app/configurations/monit.avail/httpd.rc %{prefix}/app/configurations/monit.d/httpd.rc
#ln -fs %{prefix}/app/configurations/monit.avail/batch.rc %{prefix}/app/configurations/monit.d/batch.rc
if [ "$1" = 1 ];then
	/sbin/chkconfig --add borhan-batch
	/sbin/chkconfig borhan-batch on
echo "#####################################################################################################################################
Installation of %{name} %{version} completed
Please run: 
# %{prefix}/bin/%{name}-config.sh [/path/to/answer/file]
To finalize the setup.
#####################################################################################################################################
"
fi
usermod -a -G %{apache_group} %{borhan_user}
chown %{borhan_user}:%{borhan_group} %{prefix}/log/batch
chown %{borhan_user}:%{apache_group} %{prefix}/tmp 
chown %{borhan_user}:%{apache_group} %{prefix}/app/cache 
chmod 775 %{prefix}/log %{prefix}/tmp %{prefix}/app/cache %{prefix}/web

chown %{borhan_user}:%{borhan_group} %{prefix}/app/batch
echo "PATH=$PATH:/opt/borhan/bin;export PATH" >> /etc/sysconfig/httpd
service httpd restart
# don't start it if its a fresh install, it will fail. It needs to go through postinst config first.
if [ "$1" = 0 ];then
	# don't start unless it went through configuration and the INI was created.
	if [ -r %{prefix}/app/configurations/system.ini ];then 
		service borhan-batch restart
	fi
fi

if [ "$1" = 0 ];then
	%{prefix}/bin/borhan-batch-config.sh
fi

%preun
if [ "$1" = 0 ] ; then
	/sbin/chkconfig --del borhan-batch
	%{_sysconfdir}/init.d/borhan-batch stop
	rm -f %{prefix}/app/configurations/monit.d/httpd.rc %{prefix}/app/configurations/monit.d/batch.rc 
	rm -f %{_sysconfdir}/logrotate.d/borhan_api
	rm -f %{_sysconfdir}/logrotate.d/borhan_apache
fi

%postun
service httpd restart

%files
%config /etc/php.d/zz-%{name}.ini
#%config %{prefix}/app/configurations/apache/borhan.ssl.conf.template 
%config %{prefix}/app/configurations/batch/batch.ini.template
%{_sysconfdir}/init.d/%{name}
%defattr(-, %{borhan_user}, %{borhan_group} , 0755)
%dir %{prefix}/log/batch


%changelog
* Thu Dec 22 2016 jess.portnoy@borhan.com <Jess Portnoy> - 12.8.0-1
- Ver Bounce to 12.8.0

* Thu Dec 22 2016 jess.portnoy@borhan.com <Jess Portnoy> - 12.8.0-1
- Ver Bounce to 12.8.0

* Tue Dec 6 2016 jess.portnoy@borhan.com <Jess Portnoy> - 12.7.0-1
- Ver Bounce to 12.7.0

* Thu Nov 24 2016 jess.portnoy@borhan.com <Jess Portnoy> - 12.6.0-1
- Ver Bounce to 12.6.0

* Wed Nov 9 2016 jess.portnoy@borhan.com <Jess Portnoy> - 12.5.0-1
- Ver Bounce to 12.5.0

* Mon Oct 10 2016 jess.portnoy@borhan.com <Jess Portnoy> - 12.4.0-1
- Ver Bounce to 12.4.0

* Tue Sep 27 2016 jess.portnoy@borhan.com <Jess Portnoy> - 12.3.0-1
- Ver Bounce to 12.3.0

* Tue Sep 13 2016 jess.portnoy@borhan.com <Jess Portnoy> - 12.2.0-1
- Ver Bounce to 12.2.0

* Mon Sep 5 2016 jess.portnoy@borhan.com <Jess Portnoy> - 12.1.0-2
- Use the borhan-mediainfo package instead of mediainfo

* Mon Aug 29 2016 jess.portnoy@borhan.com <Jess Portnoy> - 12.1.0-1
- Ver Bounce to 12.1.0

* Mon Aug 15 2016 jess.portnoy@borhan.com <Jess Portnoy> - 12.0.0-1
- Ver Bounce to 12.0.0

* Thu Aug 4 2016 jess.portnoy@borhan.com <Jess Portnoy> - 11.21.0-1
- Ver Bounce to 11.21.0

* Tue Jul 19 2016 jess.portnoy@borhan.com <Jess Portnoy> - 11.20.0-1
- Ver Bounce to 11.20.0

* Tue Jul 12 2016 jess.portnoy@borhan.com <Jess Portnoy> - 11.19.0-1
- Ver Bounce to 11.19.0

* Sat Jun 25 2016 jess.portnoy@borhan.com <Jess Portnoy> - 11.18.0-1
- Ver Bounce to 11.18.0

* Tue Jun 7 2016 jess.portnoy@borhan.com <Jess Portnoy> - 11.17.0-1
- Ver Bounce to 11.17.0

* Tue May 24 2016 jess.portnoy@borhan.com <Jess Portnoy> - 11.16.0-1
- Ver Bounce to 11.16.0

* Mon May 9 2016 jess.portnoy@borhan.com <Jess Portnoy> - 11.15.0-1
- Ver Bounce to 11.15.0

* Mon Apr 25 2016 jess.portnoy@borhan.com <Jess Portnoy> - 11.14.0-1
- Ver Bounce to 11.14.0

* Tue Apr 12 2016 jess.portnoy@borhan.com <Jess Portnoy> - 11.13.0-1
- Ver Bounce to 11.13.0

* Mon Mar 28 2016 jess.portnoy@borhan.com <Jess Portnoy> - 11.12.0-1
- Ver Bounce to 11.12.0

* Tue Mar 15 2016 jess.portnoy@borhan.com <Jess Portnoy> - 11.11.0-1
- Ver Bounce to 11.11.0

* Wed Mar 2 2016 jess.portnoy@borhan.com <Jess Portnoy> - 11.10.0-2
- New PID location
 
* Tue Mar 1 2016 jess.portnoy@borhan.com <Jess Portnoy> - 11.10.0-1
- Ver Bounce to 11.10.0

* Mon Feb 15 2016 jess.portnoy@borhan.com <Jess Portnoy> - 11.9.0-1
- Ver Bounce to 11.9.0

* Mon Feb 12 2016 jess.portnoy@borhan.com <Jess Portnoy> - 11.8.0-2
- rm -f $LOCKFILE

* Mon Feb 1 2016 jess.portnoy@borhan.com <Jess Portnoy> - 11.8.0-1
- Ver Bounce to 11.8.0

* Mon Jan 18 2016 jess.portnoy@borhan.com <Jess Portnoy> - 11.7.0-1
- Ver Bounce to 11.7.0

* Thu Jan 14 2016 jess.portnoy@borhan.com <Jess Portnoy> - 11.6.0-2
- require php-pecl-apc

* Mon Jan 4 2016 jess.portnoy@borhan.com <Jess Portnoy> - 11.6.0-1
- Ver Bounce to 11.6.0

* Mon Dec 21 2015 jess.portnoy@borhan.com <Jess Portnoy> - 11.5.0-1
- Ver Bounce to 11.5.0

* Fri Dec 12 2015 jess.portnoy@borhan.com <Jess Portnoy> - 11.4.0-2
- added dep on php-pecl-zendopcache.

* Mon Dec 7 2015 jess.portnoy@borhan.com <Jess Portnoy> - 11.4.0-1
- Ver Bounce to 11.4.0

* Mon Nov 23 2015 jess.portnoy@borhan.com <Jess Portnoy> - 11.3.0-1
- Ver Bounce to 11.3.0

* Mon Nov 9 2015 jess.portnoy@borhan.com <Jess Portnoy> - 11.2.0-1
- Ver Bounce to 11.2.0

* Mon Oct 26 2015 jess.portnoy@borhan.com <Jess Portnoy> - 11.1.0-1
- Ver Bounce to 11.1.0

* Mon Oct 12 2015 jess.portnoy@borhan.com <Jess Portnoy> - 11.0.0-1
- Ver Bounce to 11.0.0

* Mon Sep 21 2015 Jess Portnoy <jess.portnoy@borhan.com> - 10.21.0-1
- Ver Bounce to 10.21.0

* Thu Sep 16 2015 jess.portnoy@borhan.com <Jess Portnoy> - 10.20.0-3
- https://github.com/bordar/server/pull/3197

* Thu Sep 16 2015 jess.portnoy@borhan.com <Jess Portnoy> - 10.20.0-2
- https://github.com/bordar/server/pull/3183

* Mon Sep 7 2015 jess.portnoy@borhan.com <Jess Portnoy> - 10.20.0-1
- Ver Bounce to 10.20.0

* Mon Aug 24 2015 jess.portnoy@borhan.com <Jess Portnoy> - 10.19.0-1
- Ver Bounce to 10.19.0

* Mon Aug 10 2015 jess.portnoy@borhan.com <Jess Portnoy> - 10.18.0-1
- Ver Bounce to 10.18.0

* Mon Jul 27 2015 jess.portnoy@borhan.com <Jess Portnoy> - 10.17.0-1
- Ver Bounce to 10.17.0

* Mon Jul 13 2015 Jess Portnoy <jess.portnoy@borhan.com> - 10.16.0-1
- Ver Bounce to 10.16.0

* Mon Jun 29 2015 Jess Portnoy <jess.portnoy@borhan.com> - 10.15.0-1
- Ver Bounce to 10.15.0

* Tue Jun 16 2015 Jess Portnoy <jess.portnoy@borhan.com> - 10.14.0-1
- Ver Bounce to 10.14.0

* Mon Jun 1 2015 Jess Portnoy <jess.portnoy@borhan.com> - 10.13.0-1
- Ver Bounce to 10.13.0

* Tue May 19 2015 Jess Portnoy <jess.portnoy@borhan.com> - 10.12.0-1
- Ver Bounce to 10.12.0

* Tue May 5 2015 Jess Portnoy <jess.portnoy@borhan.com> - 10.11.0-1
- Ver Bounce to 10.11.0

* Sun Apr 26 2015 Jess Portnoy <jess.portnoy@borhan.com> - 10.10.0-1
- Ver Bounce to 10.10.0

* Mon Apr 6 2015 Jess Portnoy <jess.portnoy@borhan.com> - 10.9.0-1
- Ver Bounce to 10.9.0

* Mon Mar 23 2015 Jess Portnoy <jess.portnoy@borhan.com> - 10.8.0-1
- Ver Bounce to 10.8.0

* Sun Mar 15 2015 Jess Portnoy <jess.portnoy@borhan.com> - 10.7.0-1
- Ver Bounce to 10.7.0

* Fri Mar 6 2015 Jess Portnoy <jess.portnoy@borhan.com> - 10.6.0-1
- Ver Bounce to 10.6.0

* Wed Feb 11 2015 Jess Portnoy <jess.portnoy@borhan.com> - 10.5.0-1
- Ver Bounce to 10.5.0

* Wed Feb 4 2015 Jess Portnoy <jess.portnoy@borhan.com> - 10.4.0-1
- Ver Bounce to 10.4.0

* Tue Jan 13 2015 Jess Portnoy <jess.portnoy@borhan.com> - 10.3.0-1
- Ver Bounce to 10.3.0

* Wed Jan 7 2015 Jess Portnoy <jess.portnoy@borhan.com> - 10.2.0-1
- Ver Bounce to 10.2.0

* Wed Jan 7 2015 Jess Portnoy <jess.portnoy@borhan.com> - 10.2.0-1
- Ver Bounce to 10.2.0

* Wed Jan 7 2015 Jess Portnoy <jess.portnoy@borhan.com> - 10.2.0-1
- Ver Bounce to 10.2.0

* Sun Dec 28 2014 Jess Portnoy <jess.portnoy@borhan.com> - 10.1.0-1
- Ver Bounce to 10.1.0

* Thu Dec 11 2014 Jess Portnoy <jess.portnoy@borhan.com> - 10.0.0-1
- Ver Bounce to 10.0.0

* Mon Dec 1 2014 Jess Portnoy <jess.portnoy@borhan.com> - 9.19.8-1
- Ver Bounce to 9.19.8

* Mon Nov 17 2014 Jess Portnoy <jess.portnoy@borhan.com> - 9.19.7-1
- Ver Bounce to 9.19.7

* Sun Nov 2 2014 Jess Portnoy <jess.portnoy@borhan.com> - 9.19.6-1
- Ver Bounce to 9.19.6

* Sat Oct 18 2014 Jess Portnoy <jess.portnoy@borhan.com> - 9.19.5-1
- Ver Bounce to 9.19.5

* Sun Oct 5 2014 Jess Portnoy <jess.portnoy@borhan.com> - 9.19.4-1
- Ver Bounce to 9.19.4

* Sun Sep 21 2014 Jess Portnoy <jess.portnoy@borhan.com> - 9.19.3-1
- Ver Bounce to 9.19.3

* Tue Aug 12 2014 Jess Portnoy <jess.portnoy@borhan.com> - 9.19.0-2
- PATH="/sbin:/usr/sbin:/bin:/usr/bin"
  * export PATH
   /etc/init.d/httpd:
   # Source function library.
   .  /etc/rc.d/init.d/functions

   to make a long story short: we need to have /opt/borhan/bin in the PATH so echo it to /etc/sysconfig/httpd
* Thu Jul 10 2014 Jess Portnoy <jess.portnoy@borhan.com> - 9.19.0-1
- Ver Bounce to 9.19.0

* Sun Jun 29 2014 Jess Portnoy <jess.portnoy@borhan.com> - 9.18.0-1
- Ver Bounce to 9.18.0

* Sat Jun 14 2014 Jess Portnoy <jess.portnoy@borhan.com> - 9.17.0-1
- Ver Bounce to 9.17.0

* Wed May 21 2014 Jess Portnoy <jess.portnoy@borhan.com> - 9.16.0-1
- Ver Bounce to 9.16.0

* Thu Apr 24 2014 Jess Portnoy <jess.portnoy@borhan.com> - 9.15.0-1
- Ver Bounce to 9.15.0

* Sun Apr 6 2014 Jess Portnoy <jess.portnoy@borhan.com> - 9.14.0-1
- Ver Bounce to 9.14.0

* Wed Apr 2 2014 Jess Portnoy <jess.portnoy@borhan.com> - 9.13.0-2
- Added dep on php-pecl-ssh2

* Tue Mar 25 2014 Jess Portnoy <jess.portnoy@borhan.com> - 9.13.0-1
- Ver Bounce to 9.13.0

* Sun Mar 9 2014 Jess Portnoy <jess.portnoy@borhan.com> - 9.12.0-1
- Ver Bounce to 9.12.0

* Mon Feb 29 2014 Jess Portnoy <jess.portnoy@borhan.com> - 9.11.0-1
- Bounce ver.

* Mon Feb 3 2014 Jess Portnoy <jess.portnoy@borhan.com> - 9.9.0-9
- Start batch at init.

* Sat Feb 1 2014 Jess Portnoy <jess.portnoy@borhan.com> - 9.9.0-7
- Minor fix to post install msg.

* Mon Jan 27 2014 Jess Portnoy <jess.portnoy@borhan.com> - 9.9.0-2
- borhan-mencoder added to dep list.

* Mon Jan 27 2014 Jess Portnoy <jess.portnoy@borhan.com> - 9.9.0-1
- Moving to IX-9.9.0

* Fri Jan 17 2014 Jess Portnoy <jess.portnoy@borhan.com> - 9.7.0-18
- Corrected permissions.

* Fri Jan 17 2014 Jess Portnoy <jess.portnoy@borhan.com> - 9.7.0-17
- Add dep on mod_ssl.

* Thu Jan 16 2014 Jess Portnoy <jess.portnoy@borhan.com> - 9.7.0-16
- seds to be done as part of the borhan-base postint.

* Thu Jan 16 2014 Jess Portnoy <jess.portnoy@borhan.com> - 9.7.0-15
- We will not bring a done config for batch Apache. 
  Instead, during post we will generate from template and then SYMLINK to /etc/httpd/conf.d.

* Sun Jan 14 2014 Jess Portnoy <jess.portnoy@borhan.com> - 9.7.0-14
- PHP extensions added to 'Requires'.

* Sun Jan 12 2014 Jess Portnoy <jess.portnoy@borhan.com> - 9.7.0-13
- Dedicated Apache config for a batch node.

* Sun Jan 12 2014 Jess Portnoy <jess.portnoy@borhan.com> - 9.7.0-12
- Use the monit scandir mechanism.

* Thu Jan 9 2014 Jess Portnoy <jess.portnoy@borhan.com> - 9.7.0-11
- Set correct path to 'convert' binary
- Replace TMP_DIR token.

* Wed Jan 8 2014 Jess Portnoy <jess.portnoy@borhan.com> - 9.7.0-10
- Added dep on borhan-segmenter.

* Wed Jan 8 2014 Jess Portnoy <jess.portnoy@borhan.com> - 9.7.0-9
- Once again:(

* Wed Jan 8 2014 Jess Portnoy <jess.portnoy@borhan.com> - 9.7.0-7
- Wrong config path.

* Mon Jan 6 2014 Jess Portnoy <jess.portnoy@borhan.com> - 9.7.0-6
- Handle Monit config tmplts

* Mon Jan 6 2014 Jess Portnoy <jess.portnoy@borhan.com> - 9.7.0-5
- [Re]start daemon.

* Fri Jan 3 2014 Jess Portnoy <jess.portnoy@borhan.com> - 9.7.0-3
- restart Apache at post and preun.

* Fri Jan 3 2014 Jess Portnoy <jess.portnoy@borhan.com> - 9.7.0-2
- Added chown on log and batch dir.

* Mon Dec 23 2013 Jess Portnoy <jess.portnoy@borhan.com> - 9.7.0-1
- First package.
