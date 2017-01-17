# Frequently Asked Questions

### Before You Get Started Notes
* If you see a `#` at the beginning of a line, this line should be run as `root`.

### Commercial Editions and Paid Support

The Open Source Borhan Platform is provided under the [AGPLv3 license](http://www.gnu.org/licenses/agpl-3.0.html) and with no commercial support or liability.  

[Borhan Inc.](http://corp.borhan.com) also provides commercial solutions and services including pro-active platform monitoring, applications, SLA, 24/7 support and professional services. If you're looking for a commercially supported video platform  with integrations to commercial encoders, streaming servers, eCDN, DRM and more - Start a [Free Trial of the Borhan.com Hosted Platform](http://corp.borhan.com/free-trial) or learn more about [Borhan' Commercial OnPrem Edition™](http://corp.borhan.com/Deployment-Options/Borhan-On-Prem-Edition). For existing RPM based users, Borhan offers commercial upgrade options.

### How to contribute
We value contributions from our CE user base very much. To make a contribution, follow the [See our CONTRIBUTERS doc](https://github.com/borhan/platform-install-packages/blob/IX-9.19.0/doc/CONTRIBUTERS.md).


### Changing Apache configurations post install.

Sometimes, you may want to change deployment settings post installation, for example: replacing the domain, port or protocol, or changing the system to use SSL or stop using SSL.   
You can run `/opt/borhan/bin/borhan-front-config.sh` as many times as you'd like with different values. The script will re-configure the system accordingly.   
For instance, you may want to change the service URL, port or protocol.

#### For RPM packages:
Edit the answers file you've used to install Borhan, then run:   
`# /opt/borhan/bin/borhan-front-config.sh /path/to/updated/ans/file`

If you've lost your installation answers file, you can recreate one using the [Borhan Install Answers File Example](https://github.com/borhan/platform-install-packages/blob/master/doc/borhan.template.ans).

#### For deb packages:
```
# dpkg-reconfigure borhan-base
# dpkg-reconfigure borhan-front
# dpkg-reconfigure borhan-batch
```

In addition, when changing the CDN hostname, the borhan.delivery_profile table must be updated.
```
# mysql -h$DB1_HOST -u$DB1_USER -p$DB1_PASS $DB1_NAME

mysql> select id,name,url,host_name from delivery_profile;
```
Then use update statements to reset the url and hostname.


### Deploy Local Repository for Offline Install

On rare ocaasions, you may encounter the need to deploy Borhan on an offline environment where internet connection is not available, and thus you can't reach the Borhan packages install repository (http://installrepo.borhan.org/releases/).

On such cases, the solution is to download the packages, deploy a local repository and install from it instead of the online repository.   
**Note** that when following this path, you will need to re-deploy your local repository for every new version upgrade.

To perform an offline install, follow the [Deploy Local Repository for Offline Install guide](https://github.com/borhan/platform-install-packages/blob/master/doc/deploy-local-rpm-repo-offline-install.md).

### Fresh Database Installation

On occasions where you'd like to drop the database and content and re-install Borhan. Follor the below commands:    
```bash
# /opt/borhan/bin/borhan-drop-db.sh
# /opt/borhan/bin/borhan-config-all.sh [answers-file-path]
```

### Troubleshooting Help


#### General troubleshoot procedure

Increase log verbosity to 7 using the following method.        
Run the following command:    
```bash
# sed -i 's@^writers.\(.*\).filters.priority.priority\s*=\s*7@writers.\1.filters.priority.priority=4@g' /opt/borhan/app/configurations/logger.ini
```
Then restart your Apache.    

Run `# kaltlog`, which will continuously track (using `tail`) an error grep from all Borhan log files.

You can also use: `# allkaltlog` (using root), which will dump all the error lines from the Borhan logs once. Note that this can result in a lot of output, so the best way to use it will be to redirect to a file: `# allkaltlog > errors.txt`.
This output can be used to analyze past failures but for active debugging use the kaltlog alias.   

### Analytics issues
check if a process lock is stuck:
```
mysql> select * from borhandw_ds.locks ;
```
if lock_state says 1 for any of these, make sure you have no stuck dwh procs running, update it to read 0 and retry.

check if access files were processed:
```
mysql> select * from borhandw_ds.files where insert_time >=%Y%m%d;
```
check if actual data about entries play and views was inserted:
```
mysql> select * from borhandw.dwh_fact_events where event_date_id >=%Y%m%d ;
```

Try to run each step manually:
```
# rm /opt/borhan/dwh/logs/*
# logrotate -vvv -f /etc/logrotate.d/borhan_apache
# su borhan -c "/opt/borhan/dwh/etlsource/execute/etl_hourly.sh -p /opt/borhan/dwh -k /opt/borhan/pentaho/pdi/kitchen.sh"
# su borhan -c "/opt/borhan/dwh/etlsource/execute/etl_update_dims.sh -p /opt/borhan/dwh -k /opt/borhan/pentaho/pdi/kitchen.sh"
# su borhan -c "/opt/borhan/dwh/etlsource/execute/etl_daily.sh -p /opt/borhan/dwh -k /opt/borhan/pentaho/pdi/kitchen.sh"
# su borhan -c "/opt/borhan/dwh/etlsource/execute/etl_perform_retention_policy.sh -p /opt/borhan/dwh -k /opt/borhan/pentaho/pdi/kitchen.sh"
# su borhan -c "/opt/borhan/app/alpha/scripts/dwh/dwh_plays_views_sync.sh >> /opt/borhan/log/cron.log"
```

Or use the wrapper script to run all steps:
```
/opt/borhan/bin/borhan-run-dwh.sh
```

In order to remove the Analytics DBs and repopulate them:

0. Backup all Borhan DBs using: https://github.com/borhan/platform-install-packages/blob/Jupiter-10.2.0/doc/rpm-cluster-deployment-instructions.md#backup-and-restore-practices 
1. Drop the current DWH DBs: 
```
PASSW=$MYSQL_SUPER_USER_PASSWD 
for i in `mysql -N -p$PASSWD borhandw -e "show tables"`;
do mysql -p$PASSWD borhandw -e "drop table $i";done 
for i in `mysql -N -p$PASSWD borhandw_ds -e "show tables"`;do mysql -p$PASSWD borhandw_ds -e "drop table $i";done 
for i in `mysql -N -p$PASSWD borhanlog -e "show tables"`;do mysql -p$PASSWD borhanlog -e "drop table $i";done 
for i in `mysql -p$PASSWD -e "Show procedure status" |grep borhandw|awk -F " " '{print $2}'`;do mysql borhandw -p$PASSWD -e "drop procedure $i;";done 
for i in `mysql -p$PASSWD -e "Show procedure status" |grep borhandw_ds|awk -F " " '{print $2}'`;do mysql borhandw_ds -p$PASSWD -e "drop procedure $i;";done 
```

2. Reinstall and config DWH

on RPM based systems:
```
# yum reinstall borhan-dwh 
# borhan-dwh-config.sh
```

on deb based systems:
```
# dpkg-reconfigure borhan-dwh
``` 

#### Couldn't execute SQL: CALL move_innodb_to_archive()
Running:
```
mysql> call borhandw.add_partitions();
```
Should resolve the issue.

#### Table has no partition for value

- verify that your DB timezone settings are the same as PHP timezone settings (php.ini)
- Re-sync dimension tables from the day you installed your server:
    - Update borhandw_ds.parameters where parameter_name = 'dim_sync_last_update'. You need to set date_value to the date you installed your server.
    - Run /opt/borhan/dwh/etlsource/execute/etl_update_dims.sh
    -Verify that borhandw.dwh_dim_entries was populated (If not check /opt/borhan/dwh/logs/etl_update_dims-YYYTMMDD-HH.log for errors)
- Update borhandw.aggr_managment to run all aggregation again. Update borhandw.aggr_managment set data_insert_time = NOW();
- Run /opt/borhan/dwh/etlsource/execute/etl_daily.sh


### Cannot login to Admin Console
To manually reset the passwd, following this procedure:
mysql> select * from user_login_data where login_email='you@mail.com'\G

Then, update sha1_password and salt to read:
      sha1_password: 44e8c1db328d6d2f64de30a8285fb2a1c9337edb
               salt: a6a3209b8827759fa4286d87a33f99df

This should reset your passwd to 'admin123!'

### bmc is routed to a SSL link
If you try to access /bmc and get routed to https://vod.linnovate.net/index.php/bmc/bmc4 -
(even if you prompted to work in non SSL mode...

run the following commands...
```
  mysql borhan
  select id from permission WHERE permission.NAME='FEATURE_BMC_ENFORCE_HTTPS';
```
If you get a response use that in the next query
```
  delete from permission where id = NUM_YOU_GOT_ABOVE
```
