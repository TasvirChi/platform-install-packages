%define prefix /opt/borhan
Name:	borhan-bmc	
Version: v5.37.16
Release: 4 
Summary: Borhan Management Console

Group: System Management	
License: AGPLv3+	
URL: http://borhan.org
Source0: %{name}-%{version}.tar.bz2
Source1: bmc_config.ini
Source2: bmc_doc.zip
Source3: BMC_User_Manual.pdf
BuildRoot:	%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
BuildArch: noarch

Requires: borhan-base, httpd, borhan-html5-studio,php-cli	

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

This package installs the BMC Flash web interface.

%prep
%setup -q 
unzip %{SOURCE2}

%build
%post
if [ -L %{prefix}/web/content/uiconf ];then
	rm %{prefix}/web/content/uiconf
fi
# remove link and resym.
if [ -L %{prefix}/web/content/uiconf/borhan/bmc ];then
	rm %{prefix}/web/content/uiconf/borhan/bmc
fi

ls -sf %{prefix}/web/flash/bmc/%{version}/uiconf/borhan/bmc/appstudio %{prefix}/web/content/uiconf 2>/dev/null
ln -sf %{prefix}/web/flash/bmc/%{version}/uiconf/borhan/bmc %{prefix}/web/content/uiconf/borhan/ 2>/dev/null
#if [ -r "%{prefix}/app/configurations/local.ini" -a -r "%{prefix}/app/configurations/system.ini" ];then
#	php %{prefix}/app/deployment/uiconf/deploy_v2.php --ini=%{prefix}/web/flash/bmc/%{version}/config.ini >> %{prefix}/log/deploy_v2.log  2>&1
#fi

%install
mkdir -p $RPM_BUILD_ROOT%{prefix}/web/flash/bmc/login $RPM_BUILD_ROOT%{prefix}/app/alpha/web/lib $RPM_BUILD_ROOT%{prefix}/web/content/docs/pdf
#$RPM_BUILD_ROOT%{prefix}/web/content/uiconf/borhan/bmc
mv bmc-docs-master/pdf $RPM_BUILD_ROOT%{prefix}/app/alpha/web/lib/ 
cp -r %{_builddir}/%{name}-%{version}/bmc-docs-master/* $RPM_BUILD_ROOT%{prefix}/web/content/docs/
mv %{_builddir}/%{name}-%{version}/login/%{bmc_login_version} $RPM_BUILD_ROOT%{prefix}/web/flash/bmc/login/ 
mkdir $RPM_BUILD_ROOT%{prefix}/web/flash/bmc/%{version}
cp -r %{_builddir}/%{name}-%{version}/%{version}/* $RPM_BUILD_ROOT/%{prefix}/web/flash/bmc/%{version}/
mv %{_builddir}/%{name}-%{version}/uiconf $RPM_BUILD_ROOT%{prefix}/web/flash/bmc/%{version}/
#cp -r $RPM_BUILD_ROOT/%{prefix}/web/flash/bmc/%{version}/uiconf/borhan/bmc/* $RPM_BUILD_ROOT%{prefix}/web/content/uiconf/borhan/bmc/
cp %{SOURCE1} $RPM_BUILD_ROOT/%{prefix}/web/flash/bmc/%{version}/config.ini
cp %{SOURCE3} $RPM_BUILD_ROOT%{prefix}/web/content/docs/pdf

%preun
#if [ "$1" = 0 ] ; then
#	rm -f %{prefix}/web/content/uiconf/appstudio
#fi

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{prefix}/web/flash/bmc
%doc %{prefix}/web/content/docs/
%doc %{prefix}/app/alpha/web/lib/pdf/*
#%{prefix}/web/content/uiconf/borhan/bmc
%config %{prefix}/web/flash/bmc/%{version}/config.ini


%changelog
* Sun Apr 6 2014 Jess Portnoy <jess.portnoy@borhan.com> - v5.37.16-1
- Live Reports in Analytics (phase 0)
- Legacy embed code removed from Preview & Embed page for Players falling back to HTML5 v2
- SUP-1713 - Analytics categories filter is not needed 
- FEC-1131 - When only universal studio is enabled for partner - the main studio menu is not displayed at all in BMC 

* Wed Mar 26 2014 Jess Portnoy <jess.portnoy@borhan.com> - v5.37.14-3
- bmc_config.ini updated with new bmc ver.

* Tue Mar 25 2014 Jess Portnoy <jess.portnoy@borhan.com> - v5.37.14-1
- SUP-1581 - Remix feature is exposed to customers in Old BDP templates
- BMC - After closing the "Support" page, the BMC is not usable
- PLAT-1038 - Closing the "Preview & Embed" page is causing a change in the BMC's layout

* Sun Mar 9 2014 Jess Portnoy <jess.portnoy@borhan.com> - v5.37.12-1
- Upgrade to 5.37.12, fixes:
  SUP-1634 - BMC will not alert when the user is uploading a file that is larger than 2GB using upload from desktop 
  PLAT-994 - enable use of draft entries in playlists - when video media is not expected 
  PLAT-985 - "Copy" button in "Preview & Embed" page is not working 
- Removed the limitation of not being able to create a transcoding profile with no flavors.
- Added the ability to choose transcoding profile for draft entry based on the permission "Enable BMC transcoding profile selection for draft entries".

* Sun Feb 23 2014 Jess Portnoy <jess.portnoy@borhan.com> - v5.37.11-1
- Upgrade to 5.37.11, fixes:
  SUP-1491 - Cannot configure content distribution role Ready for Deployment
  SUP-1265 - SEO values not populating Ready for Deployment
  SUP-1382 - BMC Return 2 Source flavors Ready for Deployment 

* Fri Feb 14 2014 Jess Portnoy <jess.portnoy@borhan.com> - v3.37.10-17
- Yet another symlink needed in %%post

* Wed Feb 12 2014 Jess Portnoy <jess.portnoy@borhan.com> - v3.37.10-16
- Fix preun error.

* Wed Feb 12 2014 Jess Portnoy <jess.portnoy@borhan.com> - v3.37.10-14
- docs added

* Mon Feb 3 2014 Jess Portnoy <jess.portnoy@borhan.com> - v3.37.10-11
- Since these widgets typically reside on NFS and served from another machine there is not need for the Apache dep.

* Sat Feb 1 2014 Jess Portnoy <jess.portnoy@borhan.com> - v5.37.10-10
- Moving to BDP3 v3.9.7.

* Sat Feb 1 2014 Jess Portnoy <jess.portnoy@borhan.com> - v5.37.10-9
- Added nab UI confs.

* Sat Jan 18 2014 Jess Portnoy <jess.portnoy@borhan.com> - v5.37.10-7
- Added dep on borhan-html5-studio

* Sat Jan 18 2014 Jess Portnoy <jess.portnoy@borhan.com> - v5.37.10-4
- Replace version in base.ini

* Sat Jan 18 2014 Jess Portnoy <jess.portnoy@borhan.com> - v5.37.10-2
- Added the login dir.

* Sat Jan 18 2014 Jess Portnoy <jess.portnoy@borhan.com> - v5.37.10-1
- Ver bounce.

* Fri Jan 10 2014 Jess Portnoy <jess.portnoy@borhan.com> - v5.36.10-1
- initial package.
