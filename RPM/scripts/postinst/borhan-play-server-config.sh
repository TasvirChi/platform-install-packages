#!/bin/bash - 
#===============================================================================
#          FILE: borhan-play-server-config.sh
#         USAGE: ./borhan-play-server-config.sh 
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
verify_user_input()
{
        ANSFILE=$1
        . $ANSFILE
        RC=0
        for VAL in SERVICE_URL PLAY_PARTNER_ADMIN_SECRET CLOUD_HOSTNAME CLOUD_SECRET  ; do
                if [ -z "${!VAL}" ];then
                        VALS="$VALS\n$VAL"
                        RC=1
                fi
        done
        if [ $RC -eq 1 ];then
                OUT="ERROR: Missing the following params in $ANSFILE
                $VALS
                "
                echo -en "${BRIGHT_RED}$OUT${NORMAL}\n"
                send_install_becon borhan-play-server $ZONE "install_fail"  "$OUT"
                exit $RC 
        fi
}


BORHAN_FUNCTIONS_RC=`dirname $0`/borhan-functions.rc
if [ ! -r "$BORHAN_FUNCTIONS_RC" ];then
	OUT="ERROR: Could not find $BORHAN_FUNCTIONS_RC so, exiting.."
	echo -e $OUT
	exit 3
fi
. $BORHAN_FUNCTIONS_RC
if ! rpm -q borhan-play-server;then
	echo -e "${BRIGHT_BLUE}Skipping as borhan-play-server is not installed.${NORMAL}"
	exit 0 
fi

if [ -n "$1" -a -r "$1" ];then
        ANSFILE=$1
        verify_user_input $ANSFILE
        . $ANSFILE
        export ANSFILE
else
                echo -e "${CYAN}Your Borhan Service URL:
(Base URL where the Borhan API and Apps will be accessed from - this would be your Load Balancer URL on a cluster or same as your virtual host in an all-in-one Borhan server - Must be accessible from both inside the machine and from any clients / browsers that will use Borhan):
${NORMAL} "
                read SERVICE_URL
                echo -e "${CYAN}Admin secret of partner -6:
Can be obtained with:
mysql> select admin_secret from borhan.partner where id=-6;${NORMAL}"
		read PLAY_PARTNER_ADMIN_SECRET
		
		echo -e "${CYAN}Hostname of the cloud load balancer:${NORMAL}"
		read CLOUD_HOSTNAME 
	
		echo -e "${CYAN}Cloud secret [random string]:${NORMAL}"
		read CLOUD_SECRET
fi
PLAY_PREFIX=/opt/borhan/play-server
sed -e "s#@CLOUD_SHARED_BASE_PATH@#$PLAY_PREFIX/share#g" -e "s#@LOG_DIR@#$PLAY_PREFIX/log#g" -e "s#@SERVICE_URL@#$SERVICE_URL#g" -e "s#@PLAY_PARTNER_ADMIN_SECRET@#$PLAY_PARTNER_ADMIN_SECRET#g" -e "s#@CLOUD_HOSTNAME@#$CLOUD_HOSTNAME#g" -e "s#@CLOUD_SECRET@#$CLOUD_SECRET#g" $PLAY_PREFIX/config/user_input.ini.template > $PLAY_PREFIX/config/user_input.ini
cd $PLAY_PREFIX
npm install
ant -Dversion=v`rpm -q borhan-play-server --queryformat %{version}` -DconfigFilePath=$PLAY_PREFIX/config/user_input.ini
service borhan-play-server start
