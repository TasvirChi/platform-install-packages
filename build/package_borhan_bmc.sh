#!/bin/bash -ex 
#===============================================================================
#          FILE: package_borhan_web.sh
#         USAGE: ./package_borhan_web.sh 
#   DESCRIPTION: 
#       OPTIONS: ---
# 	LICENSE: AGPLv3+
#  REQUIREMENTS: ---
#          BUGS: ---
#         NOTES: ---
#        AUTHOR: Jess Portnoy (), <jess.portnoy@borhan.com>
#  ORGANIZATION: Borhan, inc.
#       CREATED: 01/10/14 08:46:43 EST
#      REVISION:  ---
#===============================================================================

set -o nounset                              # Treat unset variables as an error
SOURCES_RC=`dirname $0`/sources.rc
if [ ! -r $SOURCES_RC ];then
	echo "Could not find $SOURCES_RC"
	exit 1
fi
. $SOURCES_RC 
if [ ! -x "`which svn 2>/dev/null`" ];then
	echo "Need to install svn."
	exit 2
fi

rm -rf $SOURCE_PACKAGING_DIR/$BMC_RPM_NAME-$BMC_VERSION
borhan_svn export --force --quiet $BMC_UICONF_URI $SOURCE_PACKAGING_DIR/$BMC_RPM_NAME-$BMC_VERSION/uiconf/borhan/bmc
cd $SOURCE_PACKAGING_DIR
wget $BMC_URI -O $BMC_RPM_NAME-$BMC_VERSION.zip
unzip -qo $BMC_RPM_NAME-$BMC_VERSION.zip
mv $BMC_VERSION $SOURCE_PACKAGING_DIR/$BMC_RPM_NAME-$BMC_VERSION/
wget $BMC_LOGIN_URI -O $BMC_RPM_NAME-$BMC_LOGIN_VERSION.zip
unzip -oq $BMC_RPM_NAME-$BMC_LOGIN_VERSION.zip
wget $BMC_DOC_URI -O $BMC_RPM_NAME-$BMC_DOC_VERSION.zip
unzip -oq $BMC_RPM_NAME-$BMC_DOC_VERSION.zip

rm -rf $SOURCE_PACKAGING_DIR/$BMC_RPM_NAME-$BMC_VERSION/login
mkdir -p $SOURCE_PACKAGING_DIR/$BMC_RPM_NAME-$BMC_VERSION/login
mv $BMC_LOGIN_VERSION $SOURCE_PACKAGING_DIR/$BMC_RPM_NAME-$BMC_VERSION/login
#mv borhan-bmc-$BMC_VERSION $BMC_RPM_NAME-$BMC_VERSION
mv bmc-docs-$BMC_DOC_VERSION $SOURCE_PACKAGING_DIR/$BMC_RPM_NAME-$BMC_VERSION/doc

find $BMC_RPM_NAME-$BMC_VERSION -type f -exec chmod -x {} \;
tar jcf $RPM_SOURCES_DIR/$BMC_RPM_NAME-$BMC_VERSION.tar.bz2 $BMC_RPM_NAME-$BMC_VERSION
# flash things DO NOT need exec perms.
echo "Packaged into $RPM_SOURCES_DIR/$BMC_RPM_NAME-$BMC_VERSION.tar.bz2"

if [ -x "`which rpmbuild 2>/dev/null`" ];then
	rpmbuild -bb $RPM_SPECS_DIR/$BMC_RPM_NAME.spec
fi
