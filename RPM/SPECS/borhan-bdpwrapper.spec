%define prefix /opt/borhan
Name:	borhan-bdpwrapper	
Version: v11.0 
Release: 2 
Summary: Borhan BDP3 Wrapper
License: AGPLv3+	
URL: http://borhan.org
Source0: %{name}-%{version}.tar.bz2
BuildRoot:	%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
BuildArch: noarch

Requires: borhan-base, httpd	

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

This package installs the BDP Wrapper.

%prep
%setup -qn %{name} 

%build

%install
mkdir -p $RPM_BUILD_ROOT%{prefix}/web/flash
cp -r %{_builddir}/%{name} $RPM_BUILD_ROOT/%{prefix}/web/flash/bdpwrapper

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{prefix}/web/flash/bdpwrapper


%changelog
* Mon Feb 3 2014 Jess Portnoy <jess.portnoy@borhan.com> - v11.0-2
- Since these widgets typically reside on NFS and served from another machine there is not need for the Apache dep.

* Sun Jan 12 2014 Jess Portnoy <jess.portnoy@borhan.com> - v11.0-1
- initial package.