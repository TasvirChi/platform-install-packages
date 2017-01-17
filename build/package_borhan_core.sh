#!/bin/bash -e 
#===============================================================================
#          FILE: package_borhan_core.sh
#         USAGE: ./package_borhan_core.sh 
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
wget $BORHAN_CORE_URI -O$RPM_SOURCES_DIR/$BORHAN_SERVER_VERSION.zip
echo "Packaged into $RPM_SOURCES_DIR/$BORHAN_SERVER_VERSION.zip"
`dirname $0`/package_borhan_clients-generator.sh
if [ -x "`which rpmbuild 2>/dev/null`" ];then
	rpmbuild -bb $RPM_SPECS_DIR/borhan-base.spec
fi
