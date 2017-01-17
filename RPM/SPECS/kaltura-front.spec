%define prefix /opt/borhan
%define borhan_user	borhan
%define borhan_group	borhan
%define apache_user	apache
%define apache_group	apache
Summary: Borhan Open Source Video Platform - frontend server 
Name: borhan-front
Version: 12.8.0
Release: 1
License: AGPLv3+
Group: Server/Platform 
Source3: zz-%{name}.ini 

URL: http://borhan.org
Buildroot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires: borhan-mediainfo, httpd, php, curl, borhan-base, borhan-ffmpeg, ImageMagick, memcached, php-pecl-memcache, php-mysql, php-pecl-apc, php-mcrypt, borhan-segmenter, mod_ssl,borhan-sshpass, openssl,memcached, borhan-html5-studio
#php-pecl-zendopcache
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


The Borhan platform enables video management, publishing, syndication and monetization, 
as well as providing a robust framework for managing rich-media applications, 
and developing a variety of online workflows for video. 

This package sets up a server as a front node.

#%prep
#%setup -q

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
%install
mkdir -p $RPM_BUILD_ROOT/%{prefix}/app/configurations/apache
mkdir -p $RPM_BUILD_ROOT/%{_sysconfdir}/php.d
cp %{SOURCE3} $RPM_BUILD_ROOT/%{_sysconfdir}/php.d
sed 's#@WEB_DIR@#%{prefix}/web#' -i $RPM_BUILD_ROOT/%{_sysconfdir}/php.d/zz-%{name}.ini

%post
#sed 's#@WEB_DIR@#%{prefix}/web#' -i $RPM_BUILD_ROOT/%{_sysconfdir}/httpd/conf.d/*.conf 
#sed 's#@LOG_DIR@#%{prefix}/log#'  -i $RPM_BUILD_ROOT/%{_sysconfdir}/httpd/conf.d/*.conf
#sed 's#@APP_DIR@#%{prefix}/app#' -i $RPM_BUILD_ROOT/%{_sysconfdir}/httpd/conf.d/*.conf

chown -R %{borhan_user}:%{apache_group} %{prefix}/log 
chown -R %{borhan_user}:%{apache_group} %{prefix}/tmp 
chown -R %{borhan_user}:%{apache_group} %{prefix}/app/cache 
chmod 775 %{prefix}/log %{prefix}/tmp %{prefix}/app/cache %{prefix}/web
if [ "$1" = 1 ];then
	/sbin/chkconfig --add httpd
	/sbin/chkconfig httpd on
	/sbin/chkconfig --add memcached 
	/sbin/chkconfig memcached on
fi
echo "PATH=$PATH:/opt/borhan/bin;export PATH" >> /etc/sysconfig/httpd
service httpd restart

if [ "$1" = 1 ];then
echo "#####################################################################################################################################
Installation of %{name} %{version} completed
Please run 
# %{prefix}/bin/%{name}-config.sh [/path/to/answer/file]
To finalize the setup.
#####################################################################################################################################
"
fi
%preun
if [ "$1" = 0 ] ; then
#	rm %{prefix}/app/configurations/monit.d/httpd.rc || true#
	rm -f %{_sysconfdir}/cron.d/borhan-api
	rm -f %{_sysconfdir}/cron.d/borhan-cleanup
	rm -f %{_sysconfdir}/logrotate.d/borhan_api
	rm -f %{_sysconfdir}/logrotate.d/borhan_apache
fi

%clean
rm -rf %{buildroot}

%files
%config %{_sysconfdir}/php.d/zz-%{name}.ini

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

* Thu Mar 31 2016 jess.portnoy@borhan.com <Jess Portnoy> - 11.12.0-2
- https://github.com/borhan/platform-install-packages/issues/516
* Thu Mar 31 2016 jess.portnoy@borhan.com <Jess Portnoy> - 11.12.0-2
- https://github.com/borhan/platform-install-packages/issues/536

* Mon Mar 28 2016 jess.portnoy@borhan.com <Jess Portnoy> - 11.12.0-1
- Ver Bounce to 11.12.0

* Tue Mar 15 2016 jess.portnoy@borhan.com <Jess Portnoy> - 11.11.0-1
- Ver Bounce to 11.11.0

* Tue Mar 1 2016 jess.portnoy@borhan.com <Jess Portnoy> - 11.10.0-1
- Ver Bounce to 11.10.0

* Mon Feb 15 2016 jess.portnoy@borhan.com <Jess Portnoy> - 11.9.0-1
- Ver Bounce to 11.9.0

* Mon Feb 1 2016 jess.portnoy@borhan.com <Jess Portnoy> - 11.8.0-1
- Ver Bounce to 11.8.0

* Mon Jan 18 2016 jess.portnoy@borhan.com <Jess Portnoy> - 11.7.0-1
- Ver Bounce to 11.7.0

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

* Tue Mar 25 2014 Jess Portnoy <jess.portnoy@borhan.com> - 9.13.0-1
- Ver Bounce to 9.13.0

* Sun Mar 9 2014 Jess Portnoy <jess.portnoy@borhan.com> - 9.12.0-1
- Ver Bounce to 9.12.0

* Sun Feb 23 2014 Jess Portnoy <jess.portnoy@borhan.com> - 9.11.0-1
- New tag.

* Tue Feb 18 2014 Jess Portnoy <jess.portnoy@borhan.com> - 9.9.0-3
- monit is handled in postinst scripts now.

* Mon Feb 3 2014 Jess Portnoy <jess.portnoy@borhan.com> - 9.9.0-2
- Start httpd and memcached at init.

* Mon Jan 27 2014 Jess Portnoy <jess.portnoy@borhan.com> - 9.9.0-1
- Moving to IX-9.9.0

* Fri Jan 17 2014 Jess Portnoy <jess.portnoy@borhan.com> - 9.7.0-9
- Corrected permissions.

* Fri Jan 17 2014 Jess Portnoy <jess.portnoy@borhan.com> - 9.7.0-8
- Add dep on mod_ssl.

* Thu Jan 15 2014 Jess Portnoy <jess.portnoy@borhan.com> - 9.7.0-7
- We will not bring a done config for front Apache. 
  Instead, during post we will generate from template and then SYMLINK to /etc/httpd/conf.d.

* Sun Jan 12 2014 Jess Portnoy <jess.portnoy@borhan.com> - 9.7.0-6
- Use the monit scandir mechanism.

* Sun Jan 12 2014 Jess Portnoy <jess.portnoy@borhan.com> 9.7.0-5
- Output post message only on first install.
- sed corrected.

* Sun Jan 12 2014 Jess Portnoy <jess.portnoy@borhan.com> - 9.7.0-4
- Added define for apache_group.
- Monit conf path corrected.

* Wed Jan 8 2014 Jess Portnoy <jess.portnoy@borhan.com> - 9.7.0-3
- Added dep on borhan-segmenter.

* Fri Jan 3 2014 Jess Portnoy <jess.portnoy@borhan.com> - 9.7.0-2
- Added chown and chmod on log dir.

* Mon Dec  23 2013 Jess Portnoy <jess.portnoy@borhan.com> - 9.7.0-1
- First package

