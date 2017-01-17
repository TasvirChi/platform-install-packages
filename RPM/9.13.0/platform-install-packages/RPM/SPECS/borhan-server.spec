Summary: Borhan Open Source Video Platform all in 1 package 
Name: borhan-server
Version: 9.14.0
Release: 1
License: AGPLv3+
Group: Server/Platform 
URL: http://borhan.org
Buildroot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch: noarch
Requires: borhan-front, borhan-red5, borhan-batch, borhan-sphinx, borhan-dwh, borhan-widgets, borhan-html5lib

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

This is a meta package which installs an all in 1 server. i.e: all server nodes will be installed on the same machine, producing a standalone Borhan server.

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

%preun

%postun

%files

%changelog
* Sun Apr 6 2014 Jess Portnoy <jess.portnoy@borhan.com> - 9.14.0-1
- Ver Bounce to 9.14.0

* Tue Mar 25 2014 Jess Portnoy <jess.portnoy@borhan.com> - 9.13.0-1
- Ver Bounce to 9.13.0

* Sun Mar 9 2014 Jess Portnoy <jess.portnoy@borhan.com> - 9.12.0-1
- Ver Bounce to 9.12.0

* Sat Mar 1 2014 Jess Portnoy <jess.portnoy@borhan.com> - 9.11.0-1
- Bounce to 9.11.0.

* Thu Feb 13 2014 Jess Portnoy <jess.portnoy@borhan.com> - 9.9.0-2
- borhan-red5 as dep.

* Mon Jan 27 2014 Jess Portnoy <jess.portnoy@borhan.com> - 9.9.0-1
- Moving to 9.9.0.

* Sun Jan 12 2014 Jess Portnoy <jess.portnoy@borhan.com> - 9.7.0-2
- Added dep for borhan-widgets.
* Mon Jan 8 2014 Jess Portnoy <jess.portnoy@borhan.com> - 9.7.0-1
- This is a meta package which installs an all in 1 server. i.e: all server nodes will be installed on the same machine, producing a standalone Borhan server.
