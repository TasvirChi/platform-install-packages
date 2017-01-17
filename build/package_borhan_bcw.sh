#!/bin/bash -e 
#===============================================================================
#          FILE: package_borhan_bcw.sh
#         USAGE: ./package_borhan_bcw.sh 
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

# remove left overs:
rm -rf $SOURCE_PACKAGING_DIR/$BCW_RPM_NAME/*

#borhan_svn export --force --quiet $BCW_URI/$BCW_VERSION $SOURCE_PACKAGING_DIR/$BCW_RPM_NAME/$BCW_VERSION 
wget $BCW_URI -O $SOURCE_PACKAGING_DIR/bcw-$BCW_VERSION 
mkdir $SOURCE_PACKAGING_DIR/$BCW_RPM_NAME/
cd $SOURCE_PACKAGING_DIR/$BCW_RPM_NAME
unzip $SOURCE_PACKAGING_DIR/bcw-$BCW_VERSION


for BCW_UICONF_VERSION in $BCW_UICONF_VERSIONS;do
	borhan_svn export --force --quiet $BCW_UICONF_URI/$BCW_UICONF_VERSION $SOURCE_PACKAGING_DIR/$BCW_RPM_NAME/uiconf/borhan/bmc/bcw
done
borhan_svn export --force --quiet $BCW_UICONF_GENERIC_URI $SOURCE_PACKAGING_DIR/$BCW_RPM_NAME/uiconf/borhan/generic/bcw_2.1.5
borhan_svn export --force --quiet $BCW_UICONF_EDITOR_URI $SOURCE_PACKAGING_DIR/$BCW_RPM_NAME/uiconf/bcweditor/locales/en_US
cd $SOURCE_PACKAGING_DIR

# flash things DO NOT need exec perms.
find $BCW_RPM_NAME -type f -exec chmod -x {} \;

tar jcf $RPM_SOURCES_DIR/$BCW_RPM_NAME-$BCW_VERSION.tar.bz2 $BCW_RPM_NAME
echo "Packaged into $RPM_SOURCES_DIR/$BCW_RPM_NAME-$BCW_VERSION.tar.bz2"
if [ -x "`which rpmbuild 2>/dev/null`" ];then
	rpmbuild -ba $RPM_SPECS_DIR/$BCW_RPM_NAME.spec
fi
