#!/bin/bash - 
#===============================================================================
#          FILE: borhan-nfs-client-config.sh
#         USAGE: ./borhan-nfs-client-config.sh 
#   DESCRIPTION: NFS client side preps. 
#       OPTIONS: ---
# 	LICENSE: AGPLv3+
#  REQUIREMENTS: ---
#          BUGS: ---
#         NOTES: ---
#        AUTHOR: Jess Portnoy <jess.portnoy@borhan.com>
#  ORGANIZATION: Borhan, inc.
#       CREATED: 03/12/14 13:06:13 EDT
#      REVISION:  ---
#===============================================================================

#set -o nounset                              # Treat unset variables as an error
if [ $# -ne 4 ];then
        echo "Usage: $0 <NFS host> <domain> <nobody-user> <nobody-group>"
        exit 1
fi
NFS_HOST=$1
DOMAIN=$2
NOBODY_USER=$3
NOBODY_GROUP=$4
IDMAPD_CONFFILE=/etc/idmapd.conf
PREFIX=/opt/borhan
MOUNT_DIR=$PREFIX/web
mkdir -p $MOUNT_DIR
DISTRO=`lsb_release -i -s`
if [ "$DISTRO" = "Ubuntu" -o "$DISTRO" = "Debian" ];then
	apt-get install nfs-common -y
	SERVICES="rpcidmapd"
else
	yum install nfs-utils-lib nfs-utils -y
	getent group apache >/dev/null || groupadd -g 48 -r apache
	getent passwd apache >/dev/null || \
	  useradd -r -u 48 -g apache -s /sbin/nologin \
	    -d /var/www -c "Apache" apache
	SERVICES="rpcidmapd rpcbind"
fi
# create user/group, and update permissions
groupadd -r borhan -g7373 2>/dev/null || true
useradd -M -r -u7373 -d $PREFIX -s /bin/bash -c "Borhan server" -g borhan borhan 2>/dev/null || true
usermod -g borhan borhan 2>/dev/null || true

if grep -q "^Domain" $IDMAPD_CONFFILE;then
        sed -i "s@^Domain\s*=\s*.*@Domain = $DOMAIN@g" $IDMAPD_CONFFILE
else
        echo "Domain = $DOMAIN" >> $IDMAPD_CONFFILE
fi
if grep -q "^Nobody-User" $IDMAPD_CONFFILE;then
        sed -i "s@^Nobody-User\s*=\s*.*@Nobody-User = $NOBODY_USER@g" $IDMAPD_CONFFILE
        sed -i "s@^Nobody-Group\s*=\s*.*@Nobody-Group = $NOBODY_GROUP@g" $IDMAPD_CONFFILE
else
        echo "Nobody-User = $NOBODY_USER" >>$IDMAPD_CONFFILE
        echo "Nobody-User = $NOBODY_GROUP" >>$IDMAPD_CONFFILE
fi
echo "$NFS_HOST:$MOUNT_DIR $MOUNT_DIR nfs4 _netdev,auto 0 0" >> /etc/fstab
for DAEMON in $SERVICES ;do
	service $DAEMON restart
done
nfsidmap -c
cat /proc/mounts |grep -q "$NFS_HOST:$MOUNT_DIR.*$MOUNT_DIR"
if [ $? -ne 0 ];then
	mount $MOUNT_DIR || echo "Failed to mount" && exit 2
fi
su borhan -c "touch $MOUNT_DIR/"
if [ $? -eq 0 ];then
	echo "Mount is OK, writable to 'borhan' user"
else
	echo "Could not touch $MOUNT_DIR as 'borhan' user , you should fix it."
fi
