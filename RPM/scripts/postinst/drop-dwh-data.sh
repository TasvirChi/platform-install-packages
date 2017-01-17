#!/bin/bash - 
#===============================================================================
#          FILE: drop-analytics-data.sh
#         USAGE: ./drop-analytics-data.sh 
#   DESCRIPTION: 
#       OPTIONS: ---
#  REQUIREMENTS: ---
#          BUGS: ---
#         NOTES: ---
#        AUTHOR: Jess Portnoy (), <jess.portnoy@borhan.com>
#  ORGANIZATION: Borhan, inc.
#       CREATED: 11/19/2014 05:51:34 PM IST
#      REVISION:  ---
#===============================================================================

#set -o nounset                              # Treat unset variables as an error

if [ -r /etc/borhan.d/system.ini ];then
    . /etc/borhan.d/system.ini
else
    echo "ERROR: Missing $CONFIG_DIR/system.ini. Exiting.."
    exit 3
fi

if [ $# -lt 1 ];then
	echo "Usage: $0 <mysql_root_passwd>"
	exit 1
fi

echo "This will remove all data from the DWH [analytics] DBs and cannot be reverted.
Are you sure you want to continue? [N/y]"
read ANS
if [ "$ANS" != 'y' ];then
	echo "Exiting. Rerun and select lower case 'y' to continue"
	exit 2
fi
PASSWD=$1
for i in `mysql -h $DB1_HOST -N -p$PASSWD borhandw_bisources -e "show tables"`;do mysql -h $DB1_HOST -p$PASSWD borhandw_bisources -e "drop table $i";done
for i in `mysql -h $DB1_HOST  -N -p$PASSWD borhandw -e "select TABLE_NAME from information_schema.views where TABLE_SCHEMA = 'borhandw';"`;do mysql -h $DB1_HOST -p$PASSWD borhandw -e "drop view $i";done
for i in `mysql -h $DB1_HOST  -N -p$PASSWD borhandw -e "show tables"`;do mysql -h $DB1_HOST -p$PASSWD borhandw -e "drop table $i";done
for i in `mysql -h $DB1_HOST  -N -p$PASSWD borhandw -e "select TABLE_NAME from information_schema.views where TABLE_SCHEMA = 'borhandw_ds';"`;do mysql -h $DB1_HOST -p$PASSWD borhandw_ds -e "drop view $i";done
for i in `mysql -h $DB1_HOST -N -p$PASSWD borhandw_ds -e "show tables"`;do mysql -h $DB1_HOST -p$PASSWD borhandw_ds -e "drop table $i";done
for i in `mysql -h $DB1_HOST -N -p$PASSWD borhanlog -e "show tables"`;do mysql -h $DB1_HOST -p$PASSWD borhanlog -e "drop table $i";done
for i in `mysql -h $DB1_HOST -p$PASSWD -e "Show function status" |grep borhandw|awk -F " " '{print $2}'`;do mysql borhandw -h $DB1_HOST -p$PASSWD -e "drop function $i;";done
for i in `mysql -h $DB1_HOST -p$PASSWD -e "Show procedure status" |grep borhandw|awk -F " " '{print $2}'`;do mysql borhandw -h $DB1_HOST -p$PASSWD -e "drop procedure $i;";done
for i in `mysql -h $DB1_HOST -p$PASSWD -e "Show function status" |grep borhandw_ds|awk -F " " '{print $2}'`;do mysql borhandw_ds -h $DB1_HOST -p$PASSWD -e "drop function $i;";done
for i in `mysql -h $DB1_HOST -p$PASSWD -e "Show procedure status" |grep borhandw_ds|awk -F " " '{print $2}'`;do mysql borhandw_ds -h $DB1_HOST -p$PASSWD -e "drop procedure $i;";done

