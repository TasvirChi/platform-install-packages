#!/bin/bash -e 
#===============================================================================
#          FILE: package_segmenter_source.sh
#         USAGE: ./package_segmenter_source.sh 
#   DESCRIPTION: 
#       OPTIONS: ---
# 	LICENSE: AGPLv3+
#  REQUIREMENTS: ---
#          BUGS: ---
#         NOTES: ---
#        AUTHOR: Tan-Tan, <jonathan.kanarek@borhan.com>
#  ORGANIZATION: Borhan, inc.
#       CREATED: 12/29/13 05:24:47 EST
#      REVISION:  ---
#===============================================================================

#set -o nounset                              # Treat unset variables as an error

if [ ! -x "`which wget 2>/dev/null`" ];then
	echo "Need to install wget."
	exit 2
fi

SOURCES_RC=`dirname $0`/sources.rc
if [ ! -r $SOURCES_RC ];then
	echo "Could not find $SOURCES_RC"
	exit 1
fi
. $SOURCES_RC 

borhan_install borhan-ffmpeg-aux $FFMPEG_AUX_VERSION
borhan_install borhan-ffmpeg-aux-devel $FFMPEG_AUX_VERSION

mkdir -p $SOURCE_PACKAGING_DIR/borhan-segmenter-$SEGMENTER_VERSION
wget $SEGMENTER_URI -O $SOURCE_PACKAGING_DIR/borhan-segmenter-$SEGMENTER_VERSION/segmenter.c
if [ $? -eq 0 ];then
	echo "Downloaded segmenter.c"
else
	echo "Unable to download $SEGMENTER_URI" >&2
	exit 1
fi

cd $SOURCE_PACKAGING_DIR
tar zcf $RPM_SOURCES_DIR/borhan-segmenter-$SEGMENTER_VERSION.tar.gz borhan-segmenter-$SEGMENTER_VERSION
echo "Packaged into $RPM_SOURCES_DIR/borhan-segmenter-$SEGMENTER_VERSION.tar.gz"
		
if [ -x "`which rpmbuild 2>/dev/null`" ];then
	rpmbuild -ba $RPM_SPECS_DIR/borhan-segmenter.spec
fi
