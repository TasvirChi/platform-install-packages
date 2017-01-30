#!/bin/bash  
#===============================================================================
#          FILE: upgrade_from_source.sh
#         USAGE: ./upgrade_from_source.sh [/path/to/answer/file]
#   DESCRIPTION: This script upgrades to the nightly build and clones the latest server branch into /opt/borhan/app so you can commit directly from it.
#       OPTIONS: ---
#       LICENSE: AGPLv3+
#  REQUIREMENTS: ---
#          BUGS: ---
#         NOTES: ---
#        AUTHOR: Jess Portnoy, <jess.portnoy@borhan.com>
#  ORGANIZATION: Borhan, inc.
#       CREATED: 01/06/14 11:27:00 EST
#      REVISION:  ---
#===============================================================================

#set -o nounset                              # Treat unset variables as an error
SYSTEM_INI=/etc/borhan.d/system.ini
if [ ! -r $SYSTEM_INI ];then
        OUT="${BRIGHT_RED}ERROR:could not find $SYSTEM_INI so, exiting..${NORMAL}"
        echo -en $OUT
        exit 1
fi
. $SYSTEM_INI
yum update -y "*borhan*"
yum install -y git
echo "Input your Github user:"
read -e GITHUB_USER
GITHUB_SERVER_REPO="https://$GITHUB_USER@github.com/borhan/server.git"
cd /tmp && git clone $GITHUB_SERVER_REPO
mv /tmp/server/configurations /tmp/server/configurations.git
cp -rp /tmp/server/* $APP_DIR/
cp -rp /tmp/server/.git $APP_DIR/
BORHAN_VERSION=`rpm -q borhan-base --queryformat %{version}`
GITHUB_PLATFORM_INSTALL_PACKAGES_REPO_URL="https://github.com/bordar/platform-install-packages/raw/Lynx-$BORHAN_VERSION"

curl -L $GITHUB_PLATFORM_INSTALL_PACKAGES_REPO_URL/RPM/SOURCES/KDLOperatorFfmpeg1_1_1.php > $APP_DIR/infra/cdl/kdl/KDLOperatorFfmpeg1_1_1.php
curl -L $GITHUB_PLATFORM_INSTALL_PACKAGES_REPO_URL/RPM/SOURCES/navigation.xml > $APP_DIR/admin_console/configs/navigation.xml
curl -L $GITHUB_PLATFORM_INSTALL_PACKAGES_REPO_URL/RPM/SOURCES/IndexController.php > $APP_DIR/admin_console/controllers/IndexController.php
curl -L $GITHUB_PLATFORM_INSTALL_PACKAGES_REPO_URL/RPM/SOURCES/monit.phtml > $APP_DIR/admin_console/views/scripts/index/monit.phtml

if [ -n $1 ];then
        /opt/borhan/bin/borhan-config-all.sh $1
else
        /opt/borhan/bin/borhan-config-all.sh 
fi
/opt/borhan/bin/borhan-sanity.sh

