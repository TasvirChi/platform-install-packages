%define prefix /opt/borhan
%define batch_confdir %{prefix}/app/configurations/batch/ 
%define borhan_user	borhan
%define borhan_group	borhan
%define apache_user	apache
%define apache_group	apache
Summary: Borhan Open Source Video Platform - batch server 
Name: borhan-batch
Version: 9.14.0
Release: 1
License: AGPLv3+
Group: Server/Platform 
Source0: zz-%{name}.ini
Source1: borhan-batch
#Source2: borhan.ssl.conf.template 
Source3: batch.ini.template 
URL: http://borhan.org
Buildroot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires: borhan-base, borhan-ffmpeg, borhan-ffmpeg-aux, php, curl, httpd, sox, ImageMagick, borhan-sshpass, php-pecl-memcached,  php-pecl-ssh2,php-mcrypt,php-pecl-memcached,mediainfo, borhan-segmenter, mod_ssl,borhan-mencoder
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
sed -i "s@^\(params.mediaInfoCmd\)\s*=.*@\1=%{_bindir}/mediainfo@" $RPM_BUILD_ROOT%{batch_confdir}/batch.ini.template
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
chown -R %{borhan_user}:%{borhan_group} %{prefix}/log/batch
chown -R %{borhan_user}:%{apache_group} %{prefix}/tmp 
chown -R %{borhan_user}:%{apache_group} %{prefix}/app/cache 
chmod -R 775 %{prefix}/log %{prefix}/tmp %{prefix}/app/cache %{prefix}/web

chown %{borhan_user}:%{borhan_group} %{prefix}/app/batch
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

