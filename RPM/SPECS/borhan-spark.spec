%define use_systemd (0%{?fedora} && 0%{?fedora} >= 18) || (0%{?rhel} && 0%{?rhel} >= 7)
%define prefix /opt/spark-1.2.2-bin-hadoop2.4

Summary: Borhan Open Source Video Platform - Spark Server  
Name: borhan-spark
Version: 1.2.2
Release: 3
License: AGPLv3+
Group: Server/Platform 
URL: http://borhan.org
Buildroot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires: java-1.8.0-openjdk
BuildArch: noarch
Source0: http://d3kbcqa49mib13.cloudfront.net/spark-1.2.2-bin-hadoop2.4.tgz


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

This package sets up the Spark server

%clean
rm -rf %{buildroot}

%prep
%setup -qn spark-1.2.2-bin-hadoop2.4

%install
mkdir -p $RPM_BUILD_ROOT%{prefix}
rm lib/spark-examples-1.2.2-hadoop2.4.0.jar
cp -r * $RPM_BUILD_ROOT%{prefix}/
%{__mkdir_p} $RPM_BUILD_ROOT%{_sysconfdir}/profile.d
cat > $RPM_BUILD_ROOT%{_sysconfdir}/profile.d/%{name}.sh << EOF
PATH=\$PATH:%{prefix}/bin
export PATH
EOF

%if %{use_systemd}
# install systemd-specific files
#%{__mkdir} -p $RPM_BUILD_ROOT%{_unitdir}
#%{__install} -m644 %{SOURCE2} $RPM_BUILD_ROOT%{_unitdir}/spark-master.service
#%{__install} -m644 %{SOURCE3} $RPM_BUILD_ROOT%{_unitdir}/spark-worker.service
%endif


%pre

%post
ln -s %{prefix} /opt/spark
%preun
rm /opt/spark

%postun

%files
%doc CHANGES.txt LICENSE NOTICE README.md RELEASE
%{prefix}
%config %{prefix}/conf/*
%config %{_sysconfdir}/profile.d/%{name}.sh
%if %{use_systemd}
#%{_unitdir}/spark-master.service
#%{_unitdir}/spark-worker.service
%endif


%changelog
* Mon Dec 12 2016 Jess Portnoy <jess.portnoy@borhan.com> - 1.2.2-1 
- First package.

