#!/bin/sh
rm /opt/borhan/dwh/logs/*
logrotate -vvv -f /etc/logrotate.d/borhan_apache
su borhan -c "/opt/borhan/dwh/etlsource/execute/etl_hourly.sh -p /opt/borhan/dwh -k /opt/borhan/pentaho/pdi/kitchen.sh"
su borhan -c "/opt/borhan/dwh/etlsource/execute/etl_update_dims.sh -p /opt/borhan/dwh -k /opt/borhan/pentaho/pdi/kitchen.sh"
su borhan -c "/opt/borhan/dwh/etlsource/execute/etl_daily.sh -p /opt/borhan/dwh -k /opt/borhan/pentaho/pdi/kitchen.sh"
su borhan -c "/opt/borhan/dwh/etlsource/execute/etl_perform_retention_policy.sh -p /opt/borhan/dwh -k /opt/borhan/pentaho/pdi/kitchen.sh"
su borhan -c "/opt/borhan/app/alpha/scripts/dwh/dwh_plays_views_sync.sh >> /opt/borhan/log/cron.log"
