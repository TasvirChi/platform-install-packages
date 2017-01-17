%define prefix /opt/borhan
Name:	borhan-kclip	
Version: v1.1.2.1 
Release: 3 
Summary: Borhan Video Clipper
License: AGPLv3+	
URL: http://borhan.org
Source0: %{name}.tar.bz2
BuildRoot:	%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
BuildArch: noarch

Requires: borhan-base

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

This package installs the Borhan Video Clipper.

%prep
%setup -qn %{name} 

%build

%install
mkdir -p $RPM_BUILD_ROOT%{prefix}/web/content
#mv %{_builddir}/%{name}/uiconf $RPM_BUILD_ROOT/%{prefix}/web/content
mkdir -p $RPM_BUILD_ROOT%{prefix}/web/flash/kclip
cp -r %{_builddir}/%{name} $RPM_BUILD_ROOT/%{prefix}/web/flash/kclip/%{version}

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{prefix}/web/flash/kclip
#%{prefix}/web/content/uiconf


%changelog
* Mon Feb 3 2014 Jess Portnoy <jess.portnoy@borhan.com> - v1.1.2.1-3
- Since these widgets typically reside on NFS and served from another machine there is not need for the Apache dep.

* Tue Jan 28 2014 Jess Portnoy <jess.portnoy@borhan.com> - v1.1.2.1-2
- wrong path to destination.

* Sun Jan 12 2014 Jess Portnoy <jess.portnoy@borhan.com> - v1.1.2.1-1
- initial package.
