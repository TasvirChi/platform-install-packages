%define prefix /opt/borhan 
Summary: Borhan Server release file and package configuration
Name: borhan-live-analytics
Version: v0.5.26
Release: 14
License: AGPLv3+
Group: Server/Platform 
URL: http://borhan.org
Source0: register-file-deps-jars.tar.gz
Source1: %{name}_config.template.properties 
Source2: %{name}_log4j.properties
Source3: https://github.com/bordar/live_analytics/releases/download/%{version}/BorhanLiveAnalytics.war
Source4: https://github.com/bordar/live_analytics/releases/download/%{version}/live-analytics-driver.jar
Source5: https://github.com/bordar/live_analytics/releases/download/%{version}/register-file.jar
Source6: http://repo.maven.apache.org/maven2/com/sun/xml/ws/jaxws-ri/2.2.10/jaxws-ri-2.2.10.zip
Source7: %{name}_nginx_live.template.conf
Source8: https://raw.githubusercontent.com/borhan/live_analytics/v0.5/setup/create_cassandra_tables.cql
Source9: %{name}_register_log.sh
Source10: %{name}_live_stats
Source11: %{name}_rotate_live_stats.template
Source12: %{name}_live-analytics-driver.sh
Source13: %{name}_live-analytics-driver.service
Source14: %{name}_cassandra.service

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
BuildArch: noarch
Requires: dsc22 cassandra22 tomcat java-1.8.0-openjdk  borhan-spark

%description
Borhan Server release file. This package contains yum 
configuration for the Borhan RPM Repository, as well as the public
GPG keys used to sign them.




%build

%install
mkdir -p $RPM_BUILD_ROOT%{prefix}/data/geoip $RPM_BUILD_ROOT%{prefix}/bin $RPM_BUILD_ROOT%{prefix}/lib $RPM_BUILD_ROOT/usr/share/tomcat/lib $RPM_BUILD_ROOT/var/lib/tomcat/webapps/ $RPM_BUILD_ROOT%{prefix}/app/configurations/live_analytics/cassandra $RPM_BUILD_ROOT%{prefix}/app/configurations/live_analytics/cron $RPM_BUILD_ROOT%{prefix}/app/configurations/live_analytics/logrotate $RPM_BUILD_ROOT%{prefix}/app/configurations/live_analytics/nginx $RPM_BUILD_ROOT%{prefix}/app/configurations/live_analytics/driver $RPM_BUILD_ROOT%{prefix}/log/nginx $RPM_BUILD_ROOT%{prefix}/var/run/live-analytics-driver

tar zxf %{SOURCE0} -C $RPM_BUILD_ROOT%{prefix}/lib
unzip -o -q %{SOURCE6} -d $RPM_BUILD_ROOT
cp $RPM_BUILD_ROOT/jaxws-ri/lib/*jar $RPM_BUILD_ROOT/usr/share/tomcat/lib
rm -rf $RPM_BUILD_ROOT/jaxws-ri
cp %{SOURCE1} $RPM_BUILD_ROOT%{prefix}/app/configurations/live_analytics/config.template.properties
cp %{SOURCE2} $RPM_BUILD_ROOT%{prefix}/lib/log4j.properties
cp %{SOURCE3} $RPM_BUILD_ROOT/var/lib/tomcat/webapps/
cp %{SOURCE4} %{SOURCE5} $RPM_BUILD_ROOT%{prefix}/lib
cp %{SOURCE8} $RPM_BUILD_ROOT%{prefix}/app/configurations/live_analytics/cassandra
chmod +x %{SOURCE9}
cp %{SOURCE9} $RPM_BUILD_ROOT%{prefix}/bin/borhan_register_log.sh
cp %{SOURCE12} $RPM_BUILD_ROOT%{prefix}/bin/live-analytics-driver.sh
cp %{SOURCE10} $RPM_BUILD_ROOT%{prefix}/app/configurations/live_analytics/cron/live_stats
cp %{SOURCE11} $RPM_BUILD_ROOT%{prefix}/app/configurations/live_analytics/logrotate/live_stats.template
cp %{SOURCE7} $RPM_BUILD_ROOT%{prefix}/app/configurations/live_analytics/nginx/live.template.conf
cp %{SOURCE13} $RPM_BUILD_ROOT%{prefix}/app/configurations/live_analytics/driver/live-analytics-driver.service
cp %{SOURCE14} $RPM_BUILD_ROOT%{prefix}/app/configurations/live_analytics/driver/cassandra.service

%clean
%{__rm} -rf %{buildroot}

%post
for DAEMON in cassandra tomcat ;do
	service $DAEMON restart
done
if [ -d /usr/lib/systemd/system ];then
	# symlink does not work, see https://github.com/systemd/systemd/issues/2298
	cp %{prefix}/app/configurations/live_analytics/driver/live-analytics-driver.service /usr/lib/systemd/system
	cp %{prefix}/app/configurations/live_analytics/driver/cassandra.service /usr/lib/systemd/system
    	/usr/bin/systemctl preset cassandra.service >/dev/null 2>&1 ||:
	/usr/bin/systemctl enable cassandra.service
    	/usr/bin/systemctl preset live-analytics-driver.service >/dev/null 2>&1 ||:
	/usr/bin/systemctl enable live-analytics-driver.service
	systemctl daemon-reload
	service cassandra start
else
	ln -sf %{prefix}/bin/live-analytics-driver.sh /etc/init.d/live-analytics-driver
	chkconfig  --add live-analytics-driver 
	chkconfig live-analytics-driver on
	chkconfig  --add cassandra 
	chkconfig cassandra on
fi
if [ "$1" = 2 ];then
	service live-analytics-driver restart
fi

%preun
if [ "$1" = 0 ] ; then
	service live-analytics-driver stop
	for FILE in /usr/lib/systemd/system/live-analytics-driver.service /etc/init.d/live-analytics-driver /etc/cron.d/borhan_live_stats /etc/logrotate.d/borhan_live_stats /etc/nginx/conf.d/live.conf ;do
		if [ -r $FILE ];then
			rm $FILE
		fi
	done
	service nginx reload
fi


%files
%dir %{prefix}/data/geoip
%dir %{prefix}/log/nginx
%dir %{prefix}/var/run/live-analytics-driver
%{prefix}/lib/*jar
%{prefix}/bin/*
%config %{prefix}/lib/log4j.properties
%config %{prefix}/app/configurations/live_analytics/config.template.properties
%config %{prefix}/app/configurations/live_analytics/cassandra/*
%config %{prefix}/app/configurations/live_analytics/logrotate/*
%config %{prefix}/app/configurations/live_analytics/cron/*
%config %{prefix}/app/configurations/live_analytics/nginx/*
%config %{prefix}/app/configurations/live_analytics/driver/*
/var/lib/tomcat/webapps/BorhanLiveAnalytics.war
/usr/share/tomcat/lib/*jar

%changelog
* Sat Dec 3 2016 jess.portnoy@borhan.com <Jess Portnoy> - 12.6.0-1
- First release
