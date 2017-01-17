#!/bin/bash -e 
#===============================================================================
#          FILE: package_borhan.sh
#         USAGE: ./package_borhan.sh 
#   DESCRIPTION: 
#       OPTIONS: ---
# 	LICENSE: AGPLv3+
#  REQUIREMENTS: ---
#          BUGS: ---
#         NOTES: ---
#        AUTHOR: Tan-Tan, <jonathan.kanarek@borhan.com>
#  ORGANIZATION: Borhan, inc.
#       CREATED: 12/23/14
#      REVISION:  ---
#===============================================================================

#set -o nounset                              # Treat unset variables as an error

SOURCES_RC=`dirname $0`/sources.rc
if [ ! -r $SOURCES_RC ];then
	echo "Could not find $SOURCES_RC"
	exit 1
fi
. $SOURCES_RC

cd $BUILD_DIR

./package_borhan_core.sh
./package_borhan_clipapp.sh
./package_borhan_dwh.sh
./package_borhan_flex_wrapper.sh
./package_borhan_html5lib.sh
./package_borhan_html5-studio.sh
./package_borhan_kclip.sh
./package_borhan_bcw.sh
./package_borhan_bdp.sh
./package_borhan_bdp3.sh
./package_borhan_bdp3wrapper.sh
./package_borhan_bdpwrapper.sh
./package_borhan_bmc_appstudio.sh
./package_borhan_bmc.sh
./package_borhan_krecord.sh
./package_borhan_ksr.sh
./package_borhan_kupload.sh
./package_borhan_kvpm.sh
./package_borhan_media-server.sh
./package_borhan_monit.sh
./package_borhan_nginx.sh
./package_borhan_postinst.sh


if [ -x "`which rpmbuild 2>/dev/null`" ];then
	rpmbuild -ba $RPM_SPECS_DIR/borhan-base.spec
	rpmbuild -ba $RPM_SPECS_DIR/borhan-batch.spec
	rpmbuild -ba $RPM_SPECS_DIR/borhan-front.spec
	rpmbuild -ba $RPM_SPECS_DIR/borhan-mysql-config.spec
	rpmbuild -ba $RPM_SPECS_DIR/borhan-release.spec
	rpmbuild -ba $RPM_SPECS_DIR/borhan-server.spec
	rpmbuild -ba $RPM_SPECS_DIR/borhan-widgets.spec
fi


