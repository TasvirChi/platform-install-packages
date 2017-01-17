#!/bin/bash -e 
#===============================================================================
#          FILE: borhan-drop-db.sh
#         USAGE: ./borhan-drop-db.sh 
#   DESCRIPTION: 
#       OPTIONS: ---
# 	LICENSE: AGPLv3+
#  REQUIREMENTS: ---
#          BUGS: ---
#         NOTES: ---
#        AUTHOR: Jess Portnoy (), <jess.portnoy@borhan.com>
#  ORGANIZATION: Borhan, inc.
#       CREATED: 01/24/14 12:50:13 EST
#      REVISION:  ---
#===============================================================================

#set -o nounset                              # Treat unset variables as an error
if [ ! -r /opt/borhan/bin/db_actions.rc ];then
	echo "I can't drop without /opt/borhan/bin/db_actions.rc"
	exit 1
fi
. /opt/borhan/bin/db_actions.rc
. /opt/borhan/bin/colors.sh
RC_FILE=/etc/borhan.d/system.ini
if [ ! -r "$RC_FILE" ];then
	echo "Could not find $RC_FILE so, exiting.."
	exit 1 
fi
. $RC_FILE
echo -en "${CYAN}This will drop the following DBs: 
$DBS 
and remove users:
$DB_USERS
on $DB1_HOST
${NORMAL}
"
if [ -n "$1" ];then
	DBPASSWD=$1
else
	echo -en "${BRIGHT_RED}
NOTE: this is not reversible. 
It is recommended you also back up the current data using mysqldump before continuing.
You can use /opt/borhan/bin/borhan-export-db.sh to export the data.

Are you absolutely certain you want this? [n/Y]
${NORMAL}

"
	read AN
	if [ "$AN" != 'Y' ];then
		echo "Aborting. To remove hit UPPER CASED 'Y'"
		exit 1
	fi
	echo "root DB passwd:"
	read -s DBPASSWD
fi
for i in $DB_USERS;do echo "drop user $i" | mysql -u$SUPER_USER -h$DB1_HOST -p$DBPASSWD -P$DB1_PORT;done
for i in $DBS;do
	echo -en "${CYAN}Removing $i..${NORMAL}" 
	echo "drop database $i" | mysql -u$SUPER_USER -h$DB1_HOST -p$DBPASSWD -P$DB1_PORT ;
done
echo -e "\n${GREEN} Successfully dropped borhan databases and users${NORMAL}"
