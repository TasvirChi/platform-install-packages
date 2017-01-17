#!/bin/bash -e 
#===============================================================================
#          FILE: borhan-live-config.sh
#         USAGE: ./borhan-live-config.sh 
#   DESCRIPTION: configure server as a batch node.
#       OPTIONS: ---
#       LICENSE: AGPLv3+
#  REQUIREMENTS: ---
#          BUGS: ---
#         NOTES: ---
#        AUTHOR: Jess Portnoy <jess.portnoy@borhan.com>
#  ORGANIZATION: Borhan, inc.
#       CREATED: 29/11/16 09:23:34 EST
#      REVISION:  ---
#===============================================================================

#set -o nounset                              # Treat unset variables as an error
verify_user_input()
{
        ANSFILE=$1
        . $ANSFILE
        RC=0
        for VAL in WOWZA_LIC_KEY WOWZA_SILENT_KEY WOWZA_PASSWD  ; do
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
                send_install_becon borhan-nginx $ZONE "install_fail"  "$OUT"
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
if ! rpm -q borhan-live;then
        echo -e "${BRIGHT_BLUE}Skipping as borhan-live is not installed.${NORMAL}"
        exit 0 
fi

echo -e "${CYAN}Welcome to Borhan Live post install setup.${NORMAL}"
trap 'my_trap_handler "${LINENO}" $?' ERR
send_install_becon `basename $0` $ZONE install_start 0 
RELEASE=`lsb_release -r -s|awk -F . '{print $1}'`
if [ $RELEASE = 6 ];then
        yum install -y ant-trax
fi

if [ -r $CONSENT_FILE ];then
        . $CONSENT_FILE
fi
if [ -n "$1" -a -r "$1" ];then
        ANSFILE=$1
        . $ANSFILE
else
        echo -e "${CYAN}Wowza license key:${NORMAL} "
        read -e WOWZA_LIC_KEY
        echo -e "${CYAN}Wowza silent key:${NORMAL} "
        read -e WOWZA_SILENT_KEY
        echo -e "${CYAN}Wowza admin password:${NORMAL} "
        read -s WOWZA_PASSWD
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


echo -e "${BRIGHT_BLUE}Fetching the Wowza archive...${NORMAL}"
wget --quiet https://www.wowza.com/downloads/WowzaStreamingEngine-4-3-0/WowzaStreamingEngine-4.3.0-linux-x64-installer.run -O /tmp/WowzaStreamingEngine-4.3.0-linux-x64-installer.run
chmod +x /tmp/WowzaStreamingEngine-4.3.0-linux-x64-installer.run
echo -e "${BRIGHT_BLUE}Deploying Wowza, this may take a while...${NORMAL}"
# this is incredibly moronic --prefix is a mandatory arg but no matter what you'll pass the prefix is always /usr/local
/tmp/WowzaStreamingEngine-4.3.0-linux-x64-installer.run  --mode unattended --licensekey $WOWZA_LIC_KEY --silentInstallKey $WOWZA_SILENT_KEY --username kadmin --password $WOWZA_PASSWD --prefix /usr/local/

BASE_DIR=/opt/borhan
WOWZA_PREFIX=/usr/local/WowzaStreamingEngine
ln -sf $BASE_DIR/app/configurations/monit/monit.avail/wowza.rc $BASE_DIR/app/configurations/monit/monit.d/enabled.wowza.rc

# remove default unneeded Wowza apps:
rm -rf $WOWZA_PREFIX/conf/live/
rm -rf $WOWZA_PREFIX/conf/vod/
rm -rf $WOWZA_PREFIX/applications/live/
rm -rf $WOWZA_PREFIX/applications/vod/

sed 's@${com.wowza.wms.TuningHeapSizeDevelopment}@${com.wowza.wms.TuningHeapSizeProduction}@g' -i $WOWZA_PREFIX/conf/Tune.xml
ant -Dbasedir=$WOWZA_PREFIX -f $WOWZA_PREFIX/build.xml
php $BASE_DIR/bin/register_media_server.php
service WowzaStreamingEngine restart
service borhan-monit stop >> /dev/null 2>&1
service borhan-monit start

send_install_becon `basename $0` $ZONE install_success 0
