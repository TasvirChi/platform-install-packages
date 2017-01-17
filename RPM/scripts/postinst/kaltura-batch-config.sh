#!/bin/bash - 
#===============================================================================
#          FILE: borhan-batch-config.sh
#         USAGE: ./borhan-batch-config.sh 
#   DESCRIPTION: configure server as a batch node.
#       OPTIONS: ---
# 	LICENSE: AGPLv3+
#  REQUIREMENTS: ---
#          BUGS: ---
#         NOTES: ---
#        AUTHOR: Jess Portnoy <jess.portnoy@borhan.com>
#  ORGANIZATION: Borhan, inc.
#       CREATED: 01/02/14 09:23:34 EST
#      REVISION:  ---
#===============================================================================

#set -o nounset                              # Treat unset variables as an error
BORHAN_FUNCTIONS_RC=`dirname $0`/borhan-functions.rc
if [ ! -r "$BORHAN_FUNCTIONS_RC" ];then
	OUT="ERROR: Could not find $BORHAN_FUNCTIONS_RC so, exiting.."
	echo -e $OUT
	exit 3
fi
. $BORHAN_FUNCTIONS_RC
if ! rpm -q borhan-batch;then
	echo -e "${BRIGHT_BLUE}Skipping as borhan-batch is not installed.${NORMAL}"
	exit 0 
fi
PHP_MINOR_VER=`php -r 'echo PHP_MINOR_VERSION;'`
if [ "$PHP_MINOR_VER" -gt 3 ];then
        if ! rpm -q php-pecl-zendopcache >/dev/null;then
                yum -y install php-pecl-zendopcache
        fi
fi

if [ -r $CONSENT_FILE ];then
	. $CONSENT_FILE
fi
if [ -n "$1" -a -r "$1" ];then
	ANSFILE=$1
	. $ANSFILE
fi
if [ ! -r /opt/borhan/app/base-config.lock ];then
	`dirname $0`/borhan-base-config.sh "$ANSFILE"
else
	echo -e "${BRIGHT_BLUE}base-config completed successfully, if you ever want to re-configure your system (e.g. change DB hostname) run the following script:
# rm /opt/borhan/app/base-config.lock
# $BASE_DIR/bin/borhan-base-config.sh
${NORMAL}
"
fi
trap 'my_trap_handler "${LINENO}" $?' ERR
send_install_becon `basename $0` $ZONE install_start 0 
CONFIG_DIR=/opt/borhan/app/configurations
if [ -r $CONFIG_DIR/system.ini ];then
	. $CONFIG_DIR/system.ini
else
	echo -e "${BRIGHT_RED}ERROR: Missing $CONFIG_DIR/system.ini. Exiting..${NORMAL}"
	exit 1
fi

BATCH_SCHED_CONF=$APP_DIR/configurations/batch/scheduler.conf
BATCH_MAIN_CONF=$APP_DIR/configurations/batch/batch.ini

# if we couldn't access the DB to retrieve the secret, assume the post install has not finished yet.
BATCH_PARTNER_ADMIN_SECRET=`echo "select admin_secret from partner where id=-1"|mysql -N -h$DB1_HOST -u$DB1_USER -p$DB1_PASS $DB1_NAME -P$DB1_PORT`
if [ -z "$BATCH_PARTNER_ADMIN_SECRET" ];then
	echo -e "${BRIGHT_RED}ERROR: could not retreive partner.admin_secret for id -1. It probably means you did not yet run $APP_DIR/borhan-base-config.sh yet. Please do.${NORMAL}" 
	exit 2
fi

sed -i "s#@BATCH_PARTNER_ADMIN_SECRET@#$BATCH_PARTNER_ADMIN_SECRET#" -i $BATCH_MAIN_CONF
sed -i "s#@INSTALLED_HOSNAME@#`hostname`#" -i $BATCH_MAIN_CONF

BATCH_SCHEDULER_ID=`< /dev/urandom tr -dc 0-9 | head -c5`
sed "s#@BATCH_SCHEDULER_ID@#$BATCH_SCHEDULER_ID#"  -i $BATCH_MAIN_CONF 
sed "s#@INSTALLED_HOSNAME@#`hostname`#g" -i  -i $BATCH_MAIN_CONF

# logrotate:
ln -sf $APP_DIR/configurations/logrotate/borhan_batch /etc/logrotate.d/ 
ln -sf $APP_DIR/configurations/logrotate/borhan_apache /etc/logrotate.d/
ln -sf $APP_DIR/configurations/logrotate/borhan_apps /etc/logrotate.d/
if [ "$PROTOCOL" = "https" ]; then
	ln -sf $APP_DIR/configurations/apache/borhan.ssl.conf /etc/httpd/conf.d/zzzborhan.ssl.conf
else
	ln -sf $APP_DIR/configurations/apache/borhan.conf /etc/httpd/conf.d/zzzborhan.conf
fi


mkdir -p $LOG_DIR/batch 
find $APP_DIR/cache/ -type f -exec rm {} \;
find $BASE_DIR/log -type d -exec chmod 775 {} \; 
find $BASE_DIR/log -type f -exec chmod 664 {} \; 
chown -R borhan.apache $BASE_DIR/app/cache/ $BASE_DIR/log

chkconfig httpd on
if service httpd status >/dev/null 2>&1;then
	service httpd reload
else
	service httpd start
fi
chkconfig memcached on
service memcached restart

/etc/init.d/borhan-batch restart >/dev/null 2>&1
ln -sf $BASE_DIR/app/configurations/monit/monit.avail/batch.rc $BASE_DIR/app/configurations/monit/monit.d/enabled.batch.rc
ln -sf $BASE_DIR/app/configurations/monit/monit.avail/httpd.rc $BASE_DIR/app/configurations/monit/monit.d/enabled.httpd.rc
ln -sf $BASE_DIR/app/configurations/monit/monit.avail/memcached.rc $BASE_DIR/app/configurations/monit/monit.d/enabled.memcached.rc
/etc/init.d/borhan-monit stop >> /dev/null 2>&1
/etc/init.d/borhan-monit start
send_install_becon `basename $0` $ZONE install_success 0 
