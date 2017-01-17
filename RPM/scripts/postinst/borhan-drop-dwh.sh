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
BORHAN_FUNCTIONS_RC=`dirname $0`/borhan-functions.rc
if [ ! -r "$BORHAN_FUNCTIONS_RC" ];then
        OUT="${BRIGHT_RED}ERROR:could not find $BORHAN_FUNCTIONS_RC so, exiting..${NORMAL}"
        echo -en $OUT
        exit 3
fi
. $BORHAN_FUNCTIONS_RC

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
for i in `mysql -h $DWH_HOST -p$PASSWD borhandw_bisources -N -e "show tables"`;do mysql -h$DWH_HOST -p$PASSWD borhandw_bisources -e "drop table $i";done
for i in `mysql -h $DWH_HOST -p$PASSWD borhandw -N -e "show tables"`;do mysql -h$DWH_HOST  -p$PASSWD borhandw -e "drop table $i";done
for i in `mysql -h $DWH_HOST -p$PASSWD borhandw_ds -N -e "show tables"`;do mysql -h$DWH_HOST  -p$PASSWD borhandw_ds -e "drop table $i";done
for i in `mysql -h $DWH_HOST -p$PASSWD borhanlog -N -e "show tables"`;do mysql -h$DWH_HOST  -p$PASSWD borhanlog -e "drop table $i";done
for i in `mysql -h $DWH_HOST -p$PASSWD -N -e "Show procedure status" |grep borhandw|awk -F " " '{print $2}'`;do mysql -h$DWH_HOST  borhandw -p$PASSWD -e "drop procedure $i;";done
for i in `mysql -h $DWH_HOST -p$PASSWD -N -e "Show procedure status" |grep borhandw_ds|awk -F " " '{print $2}'`;do mysql -h$DWH_HOST  borhandw_ds -p$PASSWD -e "drop procedure $i;";done


