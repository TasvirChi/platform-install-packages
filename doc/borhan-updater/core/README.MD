#DO NOT USE THIS ON A PRODUCTION SERVER! NO WARRANTY

#THIS DOCUMENT IS IN DRAFT STATE

#Prerequisites
Install the following tools to aid in the update process. 

###Debian
apt-get install subversion sshpass

###Centos 
yum install svn sshpass 

###Workstation
To aid in database schema comparisons, install mysqlworkbench. With this tool you will be able to compare database dumps, and create delta alter scripts to fix any missed updates. 

---
# Important files
Borhan configuration files:
> /opt/borhan/app/configurations/*.ini

Borhan log files
> /opt/borhan/log

Borhan deployment scripts for rebuilding parts of borhan and defaults
> /opt/borhan/app/deployment

Borhan 9x bin, installing & configuring
> /opt/borhan/bin 

---

# 1 Normal installation
Before upgrading any Borhan release. You should first install and verify that the new Borhan release is working correctly. Installing Borhan has been  documented on github. It is advised you use the new RPM based installation. 

https://github.com/borhan/platform-install-packages/blob/master/doc/install-borhan-redhat-based.md#non-ssl-step-by-step-installation

### 1.1 Verify
After successfully installing Borhan. First run:

> /opt/borhan/bin/borhan-sanity.sh

Only when everything passes. Proceed to the next step.

### 1.2 Export working Borhan schemas & routines
Export the following Borhan schemas:

- borhan
- borhandw
- borhandw_bisources
- borhandw_ds
- borhanlog
- borhan_sphinx_log

> bin/export-structure.sh <root-user> <root-pw> <export path>

### 1.3 Export data 
While upgrading borhan, some data migrations are missed. These are:

- delivery_profile (Export all data)
- dynamic_enum (Export all data)
- partner   (Export all partners with id < 100)
- ui_conf  (Export all uiconfs belonging to partner < 100 )

The exporting is best done by using adminer or phpmyadmin. 

### 1.4 Register triggers and procedures 
Open the mysql information_schema database in phpmyadmin or adminer. Save or note all records in: information_schema.triggers and information_schema.procedures. This is important because you will be able to check if the system has been successfully upgraded. 

---

# 2 Setup the upgrade
After installing, verifying and exporting the healthy Borhan system. We setup the actual upgrade process. 

### 2.2 Stop Borhan services

> service borhan-monit stop
> service borhan-batch stop
> service borhan-sphinx stop

### 2.3 Drop schemas
Drop the following schemas: 

- borhan
- borhandw
- borhandw_bisources
- borhandw_ds
- borhanlog
- borhan_sphinx_log

### 2.4 Import production database
Import the production database from a backup, or any other sqldump. After restoration, please verify that you have the following databases again: 

- borhan
- borhandw
- borhandw_bisources
- borhandw_ds
- borhanlog
- borhan_sphinx_log

### 2.5 Import production data
Import the contents of your production servers /opt/borhan/web to the new server. 

---

# 3 Upgrading
After completing the setup phases. Execute the following steps to start the Borhan upgrade.

###3.1 Create config file
Implement the suplied config.sample.sh as config.sh. Take note:

- Select only the releases that apply to your upgrade. 
- Upgrades are executed in the order you configure them. 
- Configure the root user & password to avoid authentication issues.
- Configure the rest to your own specification.

###3.2 Add the Borhan svn host to the known_hosts file
Execute:

> svn export svn+ssh://svnread@kelev.borhan.com/usr/local/kalsource/backend/server/tags/falcon_2012_08_20 

You can just cancel after the host has been added.

###3.3 Export releases
Run the following script:

> bin/export.sh

This will build all the releases for upgrading. 

###4.4 Configure releases
Run the following script:

> bin/configure.sh

This will supply the required configuration files for all exported releases. 

###4.5 Execute legacy upgrades
Before starting the upgrade run:

> service borhan-shpinx start

Some updates need sphinx to be running, after all upgrades are completed. We will restore & reindex shpinx later on. 

Run:

> bin/update.sh

This might take anywhere between 1-2 hours depending on how many releases you intend to upgrade. While upgrading you can watch the status by using:

> tail -f [log]

###4.6 Verify the upgrades
Inspect the run-update log for your upgrade, and inspect errors if they occurred. For failed upgrades you will have to inspect those files and compare them to the results. If a lot of them occurred, fix them, and repeat from step 2.4. 

###4.7 Run current Borhan updates
After all legacy upgrades have been completed run the RMP upgrades. 

> /opt/borhan/bin/borhan-config-all.sh

---

#5 Verify schema state
After running all upgrades&updates, we need to check the schema for any misses. This is where the backups of the healthy system come in hand. Import the healthy exports into another mysql server.

###5.1 Export schema states
On the healthy system
> mysqldump -uroot -p --routines --no-data borhan > borhan.healthy.sql

On the updated system
> mysqldump -uroot -p --routines --no-data borhan > borhan.update.sql 

###5.2 Compare and create delta script
Open mysql-workbench, create a new schema and navigate to: database > synchronize with any source. 

As the source select the borhan.healthy.sql
As the destination select the borhan.update.sql
Specify the alter script file to your own liking

Continue the wizard to completion.

###5.3 Inspect delta alter file
Inspect the generated alterscript. Take note that if you have any add column statements, you might have a missed update. Because new fields probably need to be migrated, take extra care inspecting those. 

###5.4 Run the alter script
Execute the alter script on the upgraded system. 

###5.5 Repeat
Mysql workbench is not perfect. Sometimes you will need to repeat the process until the wizard no longer finds any differences between healthy and upgraded. 

---

#6 Restore data
This step restores missed or otherwise default provided data into Borhan.

###6.1 Partner data
Clear all system partners:
> mysql -uroot -p borhan -e "DELETE FROM `partner` WHERE `id` < 100"

Import healthy system partners:
> mysql -uroot -p borhan < [step 1.3 partner export.sql]

Check the batch user secret in /opt/borhan/app/configurations/batch against the user in the database. And change if needed. 

###6.2 Default uiconfs
Clear uiconfs 
> mysql -uroot -p borhan -e "DELETE FROM `ui_conf` WHERE `partner_id` < 100"

Import uiconfs
> mysql -uroot -p borhan < [step 1.3 uiconf export.sql]

Redeploy uiconfs
> php /opt/borhan/app/deployment/uiconf/deploy_v2.php --ini="/opt/borhan/web/flash/bmc/v5.37.27/config.ini"

###6.3 Restore dynamic enums
Clear dynamic enums
>mysql -uroot -p borhan -e "TRUNCATE `dynamic_enum`"

Import enums
> mysql -uroot -p borhan < [step 1.3 dynamic enum export.sql]

Delete borhan classmap caches
> rm -Rf /opt/borhan/app/cache/*

To avoid APC caches as wel, restart apache
> service httpd restart

###6.4 Restore delivery profiles
Clear profiles
>mysql -uroot -p borhan -e "TRUNCATE `delivery_profile`"

Import profiles
> mysql -uroot -p borhan < [step 1.3 delivery export.sql]

###6.5 Rebuild sphinx
Because sphinx was on during all the upgrades, it probably has been seriously mangled. 

Shutdown sphinx
> service borhan-shpinx stop

Backup and move sphinx data
> mv /opt/borhan/sphinx/borhan* [backup]

Backup and move sphinx binlogs
> mv /opt/borhan/log/sphinx/data/binlog.* [backup]

Start sphinx again
> service borhan-sphinx start

Check sphinx is running
> service borhan-sphinx status

Re-index site
> for FILE in $(ls /opt/borhan/app/deployment/base/scripts/*Sphinx*); do php $FILE; done

If any errors occur during the re-indexing. Also re-execute the install & insert scripts. 

---

###7 Verify the new installation
After all the steps above have been completed, rerun the execute script to check the system status/

> /opt/borhan/bin/borhan-sanity.sh

At this stage, the data warehouse has not yet been updated. So ignore any DWH related issues.
