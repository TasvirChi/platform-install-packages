#!/bin/bash - 
#===============================================================================
#          FILE: borhan-sphinx-config.sh
#         USAGE: ./borhan-sphinx-config.sh 
#   DESCRIPTION: configure server as a Sphinx node.
#       OPTIONS: ---
# 	LICENSE: AGPLv3+
#  REQUIREMENTS: ---
#          BUGS: ---
#         NOTES: ---
#        AUTHOR: Jess Portnoy <jess.portnoy@borhan.com>
#  ORGANIZATION: Borhan, inc.
#       CREATED: 01/02/14 09:25:30 EST
#      REVISION:  ---
#===============================================================================

#set -o nounset                              # Treat unset variables as an error

BORHAN_FUNCTIONS_RC=`dirname $0`/borhan-functions.rc
if [ ! -r "$BORHAN_FUNCTIONS_RC" ];then
	OUT="Could not find $BORHAN_FUNCTIONS_RC so, exiting.."
	echo $OUT
	exit 3
fi
. $BORHAN_FUNCTIONS_RC
if ! rpm -q borhan-sphinx;then
	echo -e "${BRIGHT_RED}ERROR: First install borhan-sphinx.${NORMAL}"
	exit 0
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
RC_FILE=/etc/borhan.d/system.ini
if [ ! -r "$RC_FILE" ];then
	echo -e "${BRIGHT_RED}ERROR: could not find $RC_FILE so, exiting..${NORMAL}"
	exit 2
fi
. $RC_FILE
if [ -r "$APP_DIR/configurations/sphinx_schema_update" ];then
	`dirname $0`/borhan-sphinx-schema-update.sh
	exit $?
fi
ln -sf $BASE_DIR/app/configurations/logrotate/borhan_populate /etc/logrotate.d/
ln -sf $BASE_DIR/app/configurations/logrotate/borhan_sphinx /etc/logrotate.d/
trap 'my_trap_handler "${LINENO}" $?' ERR
send_install_becon `basename $0` $ZONE install_start 0 
mkdir -p $LOG_DIR/sphinx/data $APP_DIR/cache//sphinx
chown $OS_BORHAN_USER.$OS_BORHAN_USER $APP_DIR/cache/sphinx $LOG_DIR/sphinx/data $BASE_DIR/sphinx
echo "sphinxServer = `hostname`" > /opt/borhan/app/configurations/sphinx/populate/`hostname`.ini
/etc/init.d/borhan-sphinx restart >/dev/null 2>&1
/etc/init.d/borhan-populate restart >/dev/null 2>&1
ln -sf $BASE_DIR/app/configurations/monit/monit.avail/sphinx.rc $BASE_DIR/app/configurations/monit/monit.d/enabled.sphinx.rc
ln -sf $BASE_DIR/app/configurations/monit/monit.avail/sphinx.populate.rc $BASE_DIR/app/configurations/monit/monit.d/enabled.sphinx.populate.rc
/etc/init.d/borhan-monit stop >> /dev/null 2>&1
/etc/init.d/borhan-monit start
send_install_becon `basename $0` $ZONE install_success 0
