#!/bin/bash -e 
#===============================================================================
#          FILE: package_borhan_wrapper.sh
#         USAGE: ./package_borhan_wrapper.sh 
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

mkdir -p $RPM_SOURCES_DIR/$BDP3WRAPPER_RPM_NAME
#for BDP3WRAPPER_VERSION in $BDP3WRAPPER_VERSIONS;do
borhan_svn export --force --quiet $BDP3WRAPPER_URI/$BDP3WRAPPER_VERSION $SOURCE_PACKAGING_DIR/$BDP3WRAPPER_RPM_NAME/$BDP3WRAPPER_VERSION
#done

cd $SOURCE_PACKAGING_DIR
# flash things DO NOT need exec perms.
find $BDP3WRAPPER_RPM_NAME -type f -exec chmod -x {} \;
tar jcf $RPM_SOURCES_DIR/$BDP3WRAPPER_RPM_NAME-$BDP3WRAPPER_VERSION.tar.bz2 $BDP3WRAPPER_RPM_NAME
echo "Packaged into $RPM_SOURCES_DIR/$BDP3WRAPPER_RPM_NAME-$BDP3WRAPPER_VERSION.tar.bz2"

if [ -x "`which rpmbuild 2>/dev/null`" ];then
	rpmbuild -ba $RPM_SPECS_DIR/$BDP3WRAPPER_RPM_NAME.spec
fi
