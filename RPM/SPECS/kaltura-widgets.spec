Summary: Borhan widgets
Name: borhan-widgets
Version: 1.0.0
Release: 8
License: AGPLv3+
URL: http://borhan.org
Buildroot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch: noarch
Requires: borhan-krecord, borhan-kupload, borhan-clipapp, borhan-bmc, borhan-bdp, borhan-bcw, borhan-bdp3, borhan-bdp3wrapper, borhan-kclip, borhan-bdpwrapper,borhan-flexwrapper

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

This package install the Borhan Flash widgets: BMC, BDP3, BCW, BDP3Wrapper.

%clean
rm -rf %{buildroot}

%post

%preun

%postun

%files
# its a meta package.

%changelog
* Mon Aug 18 2014 Jess Portnoy <jess.portnoy@borhan.com> - 1.0.0-8
- KSR is OnPrem only so dropping from 'Requires'

* Tue Feb 10 2014 Jess Portnoy <jess.portnoy@borhan.com> - 1.0.0-7
- Added krecord, kupload and ksr as dep.

* Mon Feb 10 2014 Jess Portnoy <jess.portnoy@borhan.com> - 1.0.0-6
- Added Flex Wrapper as dep.

* Tue Jan 28 2014 Jess Portnoy <jess.portnoy@borhan.com> - 1.0.0-5
- Require bdp wrapper

* Tue Jan 28 2014 Jess Portnoy <jess.portnoy@borhan.com> - 1.0.0-4
- Require kclip

* Tue Jan 28 2014 Jess Portnoy <jess.portnoy@borhan.com> - 1.0.0-3
- borhan-kclip added

* Sun Jan 12 2014 Jess Portnoy <jess.portnoy@borhan.com> - 1.0.0-2
- Corrected deps.

* Sun Jan 12 2014 Jess Portnoy <jess.portnoy@borhan.com> - 1.0.0-1
- Initial package. 
