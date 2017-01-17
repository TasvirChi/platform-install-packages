#!/bin/bash -e 
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
if [ ! -x "`which wget 2>/dev/null`" ];then
	echo "Need to install wget."
	exit 2
fi
mkdir -p $SOURCE_PACKAGING_DIR/$BDP3_RPM_NAME
for BDP3_VERSION in $BDP3_VERSIONS;do
	wget $BDP3_BASE_URI/$BDP3_VERSION/$BDP3_VERSION.zip -O$SOURCE_PACKAGING_DIR/$BDP3_RPM_NAME/$BDP3_RPM_NAME-$BDP3_VERSION.zip
	cd $SOURCE_PACKAGING_DIR/$BDP3_RPM_NAME
	unzip -o $SOURCE_PACKAGING_DIR/$BDP3_RPM_NAME/$BDP3_RPM_NAME-$BDP3_VERSION.zip
	rm -rf $BDP3_VERSION/__MACOSX $BDP3_VERSION/.DS_Store
	cd $SOURCE_PACKAGING_DIR/$BDP3_RPM_NAME/
	tar zcf  $RPM_SOURCES_DIR/$BDP3_RPM_NAME-$BDP3_VERSION.tar.gz $BDP3_VERSION
	echo "Packaged into $RPM_SOURCES_DIR/$BDP3_RPM_NAME-$BDP3_VERSION.tar.gz"
done
if [ -x "`which rpmbuild 2>/dev/null`" ];then
	rpmbuild -ba $RPM_SPECS_DIR/$BDP3_RPM_NAME.spec
fi
