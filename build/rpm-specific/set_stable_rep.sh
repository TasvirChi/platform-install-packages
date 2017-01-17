#!/bin/bash - 
#===============================================================================
#          FILE: set_stable_rep.sh
#         USAGE: ./set_stable_rep.sh 
#   DESCRIPTION: to be run on the repo server when a new version becomes stable. 
#       OPTIONS: ---
#  REQUIREMENTS: ---
#          BUGS: ---
#         NOTES: ---
#        AUTHOR: Jess Portnoy (), <jess.portnoy@borhan.com>
#  ORGANIZATION: Borhan, inc.
#       CREATED: 12/01/14 08:26:57 EST
#      REVISION:  ---
#===============================================================================

#set -o nounset                              # Treat unset variables as an error
if [ $# -lt 1 ]; then
        echo "$0 <new stable version>"
        exit 1
fi
VERSION=$1
BASE_DIR_RELEASES=/opt/vhosts/repo/releases
if [ -d $BASE_DIR_RELEASES/$VERSION ];then
        rm $BASE_DIR_RELEASES/nightly $BASE_DIR_RELEASES/latest $BASE_DIR_RELEASES/stable
        ln -s  $BASE_DIR_RELEASES/$VERSION $BASE_DIR_RELEASES/nightly
        ln -s  $BASE_DIR_RELEASES/$VERSION $BASE_DIR_RELEASES/latest
        ln -s  $BASE_DIR_RELEASES/$VERSION $BASE_DIR_RELEASES/stable
        rm -f $BASE_DIR_RELEASES/borhan-release.noarch.rpm
        ln -s  $BASE_DIR_RELEASES/$VERSION/RPMS/noarch/borhan-release-$VERSION-1.noarch.rpm $BASE_DIR_RELEASES/borhan-release.noarch.rpm
else
        echo "$BASE_DIR_RELEASES/$VERSION no present:("
        exit 2
fi


