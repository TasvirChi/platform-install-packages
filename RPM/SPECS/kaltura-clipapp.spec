%define prefix /opt/borhan
Name:	borhan-clipapp
Version: 1.3
Release: 2
Epoch: 1
Summary: Borhan Clipper App 
License: AGPLv3+	
URL: http://borhan.org
Source0: %{name}-v%{version}.zip
BuildRoot:	%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

Requires: borhan-base, httpd	
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

This package installs the Borhan Clipper App, used for clipping segments from a video.

%prep
%setup -qn clipapp-%{version} 

%build

%install
mkdir -p $RPM_BUILD_ROOT%{prefix}/apps/clipapp
cp -r %{_builddir}/clipapp-%{version} $RPM_BUILD_ROOT/%{prefix}/apps/clipapp/v%{version}
cp $RPM_BUILD_ROOT/%{prefix}/apps/clipapp/v%{version}/config.bmc.php $RPM_BUILD_ROOT/%{prefix}/apps/clipapp/v%{version}/config.local.php
#cp %{_builddir}/%{name}/%{version}_saas/config.local.php $RPM_BUILD_ROOT/%{prefix}/apps/clipapp/%{version}/config.local.php

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{prefix}/apps/clipapp
%config %{prefix}/apps/clipapp/v%{version}/config.local.php


%changelog
* Sun Mar 8 2015 Jess Portnoy <jess.portnoy@borhan.com> - 1.3-1
* Tue Feb 18 2014 Jess Portnoy <jess.portnoy@borhan.com> - v1.0.7-1
- Need the cnfig.local.php from saas for this one to work.

* Sun Jan 12 2014 Jess Portnoy <jess.portnoy@borhan.com> - 1.0.0-1
- initial package.
