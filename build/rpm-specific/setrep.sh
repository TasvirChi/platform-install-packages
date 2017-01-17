#!/bin/bash - 
#===============================================================================
#          FILE: setrep.sh
#         USAGE: ./setrep.sh 
#   DESCRIPTION: copies over all RPMs from current stable to new ver and then removes the Core RPM packages so that 
# 		 new ones of the right version can be pushed to the new repo. 
#       OPTIONS: ---
#  REQUIREMENTS: ---
#          BUGS: ---
#         NOTES: ---
#        AUTHOR: Jess Portnoy (), <jess.portnoy@borhan.com>
#  ORGANIZATION: Borhan, inc.
#       CREATED: 12/01/14 08:27:56 EST
#      REVISION:  ---
#===============================================================================

#set -o nounset                              # Treat unset variables as an error
if [ $# -lt 1 ];then
        echo "$0 <repo_ver>"
        exit 1
fi
VERSION=$1

mkdir -p /opt/vhosts/repo/releases/$VERSION/RPMS/noarch
cp /opt/vhosts/repo/releases/latest/RPMS/noarch/*rpm /opt/vhosts/repo/releases/$VERSION/RPMS/noarch/
cd  /opt/vhosts/repo/releases/$VERSION/RPMS/noarch
rm  borhan-base-* borhan-batch-* borhan-front-* borhan-release-* borhan-server-* borhan-release-*
cp -r /opt/vhosts/repo/releases/latest/RPMS/x86_64 /opt/vhosts/repo/releases/$VERSION/RPMS/


