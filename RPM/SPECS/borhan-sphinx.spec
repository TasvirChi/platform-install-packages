%define sphinx_user borhan
%define sphinx_group borhan
%define prefix	/opt/borhan/sphinx
# this isn't really a stand location for placing conf files but we wish to remain compatible with the current config dir tree used by Borhan
%define confdir	/opt/borhan/app/configurations/sphinx

Name:           borhan-sphinx
Version:        2.2.1
Release:        20
Summary:        Sphinx full-text search server - for Borhan

Group:          Applications/Text
License:        GPLv2
URL:            http://sphinxsearch.com
Vendor:         Sphinx Technologies Inc.
Packager:       Borhan Inc.

Source0:       	%{name}-%{version}.tar.gz 
Source1: 	%{name}
Source2: 	borhan-populate
Patch0:		config-main.patch
Patch1:		config.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-build

BuildRequires:  mysql-devel
BuildRequires:	expat-devel

Requires(post): chkconfig
Requires(preun): chkconfig
# This is for /sbin/service
Requires(preun): initscripts
#Requires(preinst): mysql-libs zlib openssl expat libgcc krb5-libs


%description
Sphinx is a full-text search server that adds many advanced features
on top of plain old text searching. Data can be fetched directly from
a database, or streamed in XML format. MySQL, PostgreSQL, SQL Server,
Oracle, and other databases are supported. Client programs can query
Sphinx either using native SphinxAPI library, or using regular MySQL
client programs and libraries via SQL-like SphinxQL interface.


%prep
%setup -n %{name}-%{version}
%patch0 -p1
%patch1 -p1
#%setup -D -T -a 2 -n %{name}-%{version}
#%setup -D -T -a 3 -n %{name}-%{version}

# Fix wrong-file-end-of-line-encoding
sed -i 's/\r//' api/ruby/spec/sphinx/sphinx_test.sql
sed -i 's/\r//' api/java/mk.cmd
sed -i 's/\r//' api/ruby/spec/fixtures/keywords.php
sed -i 's/\r//' api/ruby/lib/sphinx/response.rb


%build

%configure --sysconfdir=/opt/borhan/app/configurations/sphinx  --with-mysql --with-unixodbc --with-iconv --enable-id64 --with-syslog --prefix=%{prefix} --mandir=%{prefix}/share/man --bindir=%{prefix}/bin
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT INSTALL="%{__install} -p -c"
mkdir $RPM_BUILD_ROOT/opt/borhan/sphinx/lib
#mv $RPM_BUILD_ROOT/usr/local/lib/libre2* $RPM_BUILD_ROOT/opt/borhan/sphinx/lib
mkdir -p  $RPM_BUILD_ROOT%{_initrddir}
# Install sphinx initscript
install -p -D -m 0755 %{SOURCE1} $RPM_BUILD_ROOT%{_initrddir}/
install -p -D -m 0755 %{SOURCE2} $RPM_BUILD_ROOT%{_initrddir}/
chmod +x $RPM_BUILD_ROOT%{_initrddir}/*
mkdir -p $RPM_BUILD_ROOT/opt/borhan/log/sphinx/data

# Create /var/run/sphinx
mkdir -p $RPM_BUILD_ROOT%{prefix}/var/run


mkdir $RPM_BUILD_ROOT%{_sysconfdir}/profile.d
cat > $RPM_BUILD_ROOT%{_sysconfdir}/profile.d/borhan_sphinx.sh << EOF
PATH=\$PATH:%{prefix}/bin
export PATH
EOF

%clean
rm -rf $RPM_BUILD_ROOT


%post
ldconfig
getent group %{sphinx_group} >/dev/null || groupadd -r %{sphinx_group} -g7373 2>/dev/null
getent passwd %{sphinx_user} >/dev/null || useradd -M -r -u7373 -d %{prefix} -s /bin/bash -c "Borhan server" -g %{sphinx_group} %{sphinx_user} 2>/dev/null
sed 's#@LOG_DIR@#/opt/borhan/log#g' /opt/borhan/app/configurations/sphinx/borhan.conf.template > /opt/borhan/app/configurations/sphinx/borhan.conf
sed 's#@BASE_DIR@#/opt/borhan#g' -i /opt/borhan/app/configurations/sphinx/borhan.conf
sed 's#^pid_file.*#pid_file=%{prefix}/var/run/searchd.pid#' -i /opt/borhan/app/configurations/sphinx/borhan.conf
# register service
if [ "$1" = 1 ];then
    /sbin/chkconfig --add %{name}
	/sbin/chkconfig %{name} on
    /sbin/chkconfig --add borhan-populate
	/sbin/chkconfig borhan-populate on
echo "
#####################################################################################################################################
Installation of %{name} %{version} completed
Please run 
# /opt/borhan/bin/%{name}-config.sh [/path/to/answer/file]
To finalize the setup.
#####################################################################################################################################
"
fi

mkdir -p /opt/borhan/app/configurations/sphinx/populate
touch /opt/borhan/app/configurations/sphinx/populate/`hostname`.ini
# create user/group, and update permissions
chown -R %{sphinx_user}:%{sphinx_group} %{prefix} /opt/borhan/log/sphinx 
# don't start unless it went through configuration and the INI was created.
if [ -r /opt/borhan/app/configurations/system.ini ];then 
	%{_initrddir}/borhan-sphinx restart
	%{_initrddir}/borhan-populate restart
fi


%preun
if [ "$1" = 0 ] ; then
    /sbin/service borhan-sphinx stop >/dev/null 2>&1
    /sbin/service borhan-populate stop >/dev/null 2>&1
    /sbin/chkconfig --del %{name}
    /sbin/chkconfig --del borhan-populate 
    if [ -L /opt/borhan/app/configurations/monit/monit.d/enabled.sphinx.rc ];then     
	rm /opt/borhan/app/configurations/monit/monit.d/enabled.sphinx.rc
	/sbin/service borhan-monit reload
    fi
    rm -f /opt/borhan/app/configurations/sphinx/populate/`hostname`.ini
fi


%files
%defattr(-,root,root,-)
%{prefix}/share/man/man1/*
%doc COPYING doc/sphinx.html doc/sphinx.txt sphinx-min.conf.dist sphinx.conf.dist example.sql
%dir %{confdir}
#%config(noreplace) %{confdir}/borhan_sphinx.conf
%config %{_sysconfdir}/profile.d/borhan_sphinx.sh
%exclude %{confdir}/*.conf.dist
%exclude %{confdir}/example.sql
%{_initrddir}/borhan-*
%{prefix}/bin/*
%dir /opt/borhan/log/sphinx
%dir /opt/borhan/log/sphinx/data
%dir %{prefix}/var/run



%changelog
* Fri Sep 23 2016 Jess Portnoy <jess.portnoy@borhan.com> - 2.2.1.r4097-20
- No need to generate logrotate file here as it's taken care of by borhan-base with /opt/borhan/app/configurations/logrotate/borhan_sphinx

* Wed Mar 16 2016 Jess Portnoy <jess.portnoy@borhan.com> - 2.2.1.r4097-18
- https://github.com/bordar/platform-install-packages/pull/532
- https://github.com/bordar/platform-install-packages/pull/533

* Wed Oct 7 2015 Jess Portnoy <jess.portnoy@borhan.com> - 2.2.1.r4097-17
- https://github.com/bordar/platform-install-packages/issues/454

* Mon Feb 3 2014 Jess Portnoy <jess.portnoy@borhan.com> - 2.2.1.r4097-15 
- Start Sphinx and pop at init.

* Mon Jan 20 2014 Jess Portnoy <jess.portnoy@borhan.com> 2.2.1.r4097-9
- With populate, no need to show an error if trying to stop a none running instance.
  Saying it isn't running is good enough and cause less panic.

* Mon Jan 20 2014 Jess Portnoy <jess.portnoy@borhan.com> 2.2.1.r4097-9
- Added populate init script.

* Sun Jan 12 2014 Jess Portnoy <jess.portnoy@borhan.com> 2.2.1.r4097-5
- Replace tokens and create borhan.conf - Sphinx config file.

* Sun Jan 12 2014 Jess Portnoy <jess.portnoy@borhan.com> 2.2.1.r4097-4
- Output post message only on first install.

* Sun Jan 12 2014 Jess Portnoy <jess.portnoy@borhan.com> 2.2.1.r4097-2
- Prefix can be w/o version, we only have one Sphinx ver at a time [unlike Ffmpeg].
- No lib dir for Sphinx.
- No need for the usage output in %%post.

* Sun Jan 12 2014 Jess Portnoy <jess.portnoy@borhan.com> 2.2.1.r4097-2
- Paths to log and run corrected.

* Tue Dec 24 2013 Jess Portnoy <jess.portnoy@borhan.com> 2.2.1.r4097-1
First build.
