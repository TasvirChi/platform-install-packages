%define prefix /opt/borhan
%define borhan_user borhan
Summary: Borhan Open Source Video Platform - Analytics 
Name: borhan-dwh
Version: 11.3.0
Release: 1
License: AGPLv3+
Group: Server/Platform 
Source0: https://github.com/borhan/dwh/archive/%{name}-Kajam-%{version}.zip
URL: https://github.com/borhan/dwh/tree/master 
Buildroot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires: borhan-base,borhan-pentaho,jre, borhan-postinst 
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

This package configures the Data Warehouse [DWH] analytics component. 

%prep
%setup -qn dwh-Kajam-%{version} 

%build

%install
# for Apache access logs.
mkdir -p $RPM_BUILD_ROOT%{prefix}/web/logs
cp -r %{_builddir}/dwh-Kajam-%{version} $RPM_BUILD_ROOT%{prefix}/dwh
find  $RPM_BUILD_ROOT%{prefix}/dwh/ -name "*.sh" -type f -exec chmod +x {} \;

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
if [ "$1" = 0 ];then
	%{prefix}/bin/borhan-dwh-config.sh
fi

%preun
if [ "$1" = 0 ] ; then
	rm -f %{_sysconfdir}/cron.d/borhan-dwh
fi

%files
%dir %{prefix}/web/logs
%defattr(-, %{borhan_user},root 0755)
%{prefix}/dwh


%changelog
* Thu Jan 7 2016 Jess Portnoy <jess.portnoy@borhan.com> - 11.3.0-1
- Add Hercules to Iris/Jupiter migration
- Add Nginx log parsing
- Add Totals Aggregration
- Add Live Analytics

* Thu Oct 15 2015 Jess Portnoy <jess.portnoy@borhan.com> - 9.5.0-2
- Live entry aggregation ddl changes 

* Mon Aug 24 2015 Jess Portnoy <jess.portnoy@borhan.com> - 9.5.0-1
- Don't use preserved word MAX as query alias.
- Make sure that file_size is int value like in DB

* Wed Jan 29 2014 Jess Portnoy <jess.portnoy@borhan.com> - 9.2.0-2
%%{prefix}/bin/borhan-dwh-config.sh does not require user interaction, if this is an upgrade just run it at %%post.

* Wed Jan 29 2014 Jess Portnoy <jess.portnoy@borhan.com> - 9.2.0-1
- Fixes Unknown column 'invalid_login_count' in 'field list' - this field was dropped from the borhan operational DB.

* Wed Jan 29 2014 Jess Portnoy <jess.portnoy@borhan.com> - 9.1.0-3
- Define 'borhan_user' in the spec.

* Wed Jan 29 2014 Jess Portnoy <jess.portnoy@borhan.com> - 9.1.0-2
- Make borhan owner of logs dir.
- Set exec bit on all shell scripts.

* Mon Jan 27 2014 Jess Portnoy <jess.portnoy@borhan.com> - 9.1.0-1
- Moving to IX-9.9.0

* Sun Jan 26 2014 Jess Portnoy <jess.portnoy@borhan.com> - 9.1.0-8
- Sources moved to GIT.

* Sat Jan 18 2014 Jess Portnoy <jess.portnoy@borhan.com> - 9.1.0-6
- Plus .kettle config.

* Sat Jan 18 2014 Jess Portnoy <jess.portnoy@borhan.com> - 9.1.0-5
- Install actual %%{prefix}/dwh dir

* Thu Jan 16 2014 Jess Portnoy <jess.portnoy@borhan.com> - 9.1.0-3
- Added creation of %%{prefix}/web/logs

* Mon Dec 23 2013 Jess Portnoy <jess.portnoy@borhan.com> - 9.7.0-1
- First package
