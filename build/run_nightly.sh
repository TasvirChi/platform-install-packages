#!/bin/bash -e 
#===============================================================================
#          FILE: run.sh
#         USAGE: ./run.sh 
#   DESCRIPTION: 
#       OPTIONS: ---
#  REQUIREMENTS: ---
#          BUGS: ---
#         NOTES: ---
#        AUTHOR: Jess Portnoy (), <jess.portnoy@borhan.com>
#  ORGANIZATION: Borhan, inc.
#       CREATED: 12/01/14 10:17:05 EST
#      REVISION:  ---
#===============================================================================

#set -o nounset                              # Treat unset variables as an error
if [ ! -x `which wget 2>/dev/null` ];then
	echo "Need to install wget."
	exit 2
fi
if [ ! -x `which svn 2>/dev/null` ];then
	echo "Need to install svn."
	exit 2
fi
rm -f /tmp/nightly.log

mkdir -p tmp
RPMS_BASE_DIR=/home/jess/rpmbuild/RPMS
BORHAN_SERVER_VERSION=`curl https://api.github.com/repos/borhan/server -s |grep default_branch| sed 's/"default_branch":\s*"\(.*\)",/\1/' | sed 's@\s*@@g'`
BORHAN_SHORT_SERVER_VERSION=`echo $BORHAN_SERVER_VERSION|awk -F "-" '{print $2}'`

# set release [revision] to 1, if the new ver to push is the same as the one we currenly have on the nightly repo, however, then change to current revision + 1 instead.
BORHAN_SERVER_NEXT_REVISION=1
sudo yum clean all
BORHAN_SERVER_REMOTE_VERSION=`yum info borhan-base | grep Version|awk -F ": " '{print $2}'`
if [ "$BORHAN_SHORT_SERVER_VERSION" = "$BORHAN_SERVER_REMOTE_VERSION" ];then
	BORHAN_SERVER_REMOTE_REVISION=`yum info borhan-base | grep Release|awk -F ": " '{print $2}'`
	BORHAN_SERVER_NEXT_REVISION=`expr $BORHAN_SERVER_REMOTE_REVISION + 1`
fi
wget https://github.com/bordar/server/archive/$BORHAN_SERVER_VERSION.zip -O /home/jess/rpmbuild/SOURCES/$BORHAN_SERVER_VERSION.zip 
unzip -qo -j /home/jess/rpmbuild/SOURCES/$BORHAN_SERVER_VERSION.zip server-$BORHAN_SERVER_VERSION/configurations/base.ini -d "tmp/"
BMC_LOGIN_VERSION=`grep ^bmc_login_version tmp/base.ini |awk -F "=" '{print $2}'|sed 's@\s*@@g'`
BMC_VERSION=`grep ^bmc_version tmp/base.ini |awk -F "=" '{print $2}'|sed 's@\s*@@g'`
BMC_NEXT_REVISION=1
BMC_REMOTE_VERSION=`yum info borhan-bmc | grep Version|awk -F ": " '{print $2}'`
if [ "$BMC_VERSION" = "$BMC_REMOTE_VERSION" ];then
	BMC_REMOTE_REVISION=`yum info borhan-bmc | grep Release|awk -F ": " '{print $2}'`
	BMC_NEXT_REVISION=`expr $BMC_REMOTE_REVISION + 1`
fi

HTML5_APP_STUDIO_VERSION=`grep ^studio_version tmp/base.ini|awk -F "=" '{print $2}'|sed 's@\s*@@g'`
HTML5_APP_STUDIO_NEXT_REVISION=1
HTML5_APP_STUDIO_REMOTE_VERSION=`yum info borhan-html5-studio | grep Version|awk -F ": " '{print $2}'`
if [ "$HTML5_APP_STUDIO_VERSION" = "$HTML5_APP_STUDIO_REMOTE_VERSION" ];then
	HTML5_APP_STUDIO_REMOTE_REVISION=`yum info borhan-html5-studio | grep Release|awk -F ": " '{print $2}'`
	HTML5_APP_STUDIO_NEXT_REVISION=`expr $HTML5_APP_STUDIO_REMOTE_REVISION + 1`
fi
HTML5LIB_DEFAULT_BRANCH=`curl https://api.github.com/repos/borhan/mwembed -s |grep default_branch| sed 's/"default_branch":\s*"\(.*\)",/\1/' | sed 's@\s*@@g'`
wget --no-check-certificate https://github.com/bordar/mwEmbed/raw/$HTML5LIB_DEFAULT_BRANCH/includes/DefaultSettings.php -O tmp/DefaultSettings.php; 
dos2unix tmp/DefaultSettings.php
HTML5LIB_VERSION="v`grep wgMwEmbedVersion tmp/DefaultSettings.php |sed 's@^\s*$wgMwEmbedVersion\s*=\s*.\([0-9.]*\)..@\1@'`"
HTML5LIB_NEXT_REVISION=1
HTML5LIB_REMOTE_VERSION=`yum info borhan-html5lib | grep Version|awk -F ": " '{print $2}'`
if [ "$HTML5LIB_VERSION" = "$HTML5LIB_REMOTE_VERSION" ];then
	HTML5LIB_REMOTE_REVISION=`yum info borhan-html5lib | grep Release|awk -F ": " '{print $2}'`
	HTML5LIB_NEXT_REVISION=`expr $HTML5LIB_REMOTE_REVISION + 1`
fi
cp ~/rpmbuild/SOURCES/bmc_config.ini ~/rpmbuild/SOURCES/bmc_config.ini.stable
sed -i "s@\(.*html5_version.*\)\s*=.*@\1= $HTML5LIB_VERSION@g" ~/rpmbuild/SOURCES/bmc_config.ini
mv ~/.rpmmacros ~/.rpmmacros.stable
sed -e "s#@BMC_VERSION@#$BMC_VERSION#" -e "s#@BMC_LOGIN_VERSION@#$BMC_LOGIN_VERSION#" -e "s#@HTML5LIB_VERSION@#$HTML5LIB_VERSION#" `dirname $0`/.rpmmacros.tmplt > ~/.rpmmacros  

. `dirname $0`/sources.rc 
`dirname $0`/rpm-specific/bounce_rpm_ver.sh borhan-bmc.spec $BMC_VERSION $BMC_NEXT_REVISION "Borhan night build"
`dirname $0`/rpm-specific/bounce_rpm_ver.sh borhan-html5lib.spec $HTML5LIB_VERSION $HTML5LIB_NEXT_REVISION "Borhan night build"
`dirname $0`/rpm-specific/bounce_rpm_ver.sh borhan-html5-studio.spec $HTML5_APP_STUDIO_VERSION $HTML5_APP_STUDIO_NEXT_REVISION "Borhan night build"
`dirname $0`/rpm-specific/bounce_rpm_ver.sh borhan-base.spec $BORHAN_SHORT_SERVER_VERSION $BORHAN_SERVER_NEXT_REVISION "Borhan night build"

rpmbuild -ba $RPM_SPECS_DIR/borhan-base.spec
`dirname $0`/rpm-specific/push_rpm.sh $RPMS_BASE_DIR/noarch/borhan-base-$BORHAN_SHORT_SERVER_VERSION-$BORHAN_SERVER_NEXT_REVISION.noarch.rpm $BORHAN_SHORT_SERVER_VERSION 
echo "Pushed borhan-base-$BORHAN_SHORT_SERVER_VERSION-$BORHAN_SERVER_NEXT_REVISION.noarch.rpm to $BORHAN_SHORT_SERVER_VERSION" >> /tmp/nightly.log
`dirname $0`/package_borhan_bmc.sh
rpmbuild -ba $RPM_SPECS_DIR/$BMC_RPM_NAME.spec
`dirname $0`/rpm-specific/push_rpm.sh $RPMS_BASE_DIR/noarch/$BMC_RPM_NAME-$BMC_VERSION-$BMC_NEXT_REVISION.noarch.rpm $BORHAN_SHORT_SERVER_VERSION
echo "Pushed $RPMS_BASE_DIR/noarch/$BMC_RPM_NAME-$BMC_VERSION-$BMC_NEXT_REVISION.noarch.rpm to $BORHAN_SHORT_SERVER_VERSION" >> /tmp/nightly.log

mkdir -p $SOURCE_PACKAGING_DIR/$HTML5_APP_STUDIO_RPM_NAME-$HTML5_APP_STUDIO_VERSION
rm -rf $SOURCE_PACKAGING_DIR/$HTML5_APP_STUDIO_RPM_NAME-$HTML5_APP_STUDIO_VERSION/*
wget -q $HTML5_APP_STUDIO_URI -O$SOURCE_PACKAGING_DIR/$HTML5_APP_STUDIO_RPM_NAME-$HTML5_APP_STUDIO_VERSION/$HTML5_APP_STUDIO_NORMALIZED_ARCHIVE_NAME
cd $SOURCE_PACKAGING_DIR/$HTML5_APP_STUDIO_RPM_NAME-$HTML5_APP_STUDIO_VERSION
unzip -qq $HTML5_APP_STUDIO_NORMALIZED_ARCHIVE_NAME
rm $HTML5_APP_STUDIO_NORMALIZED_ARCHIVE_NAME
cd ../
tar jcf  $RPM_SOURCES_DIR/$HTML5_APP_STUDIO_RPM_NAME-$HTML5_APP_STUDIO_VERSION.tar.bz2 $HTML5_APP_STUDIO_RPM_NAME-$HTML5_APP_STUDIO_VERSION
echo "Packaged into $RPM_SOURCES_DIR/$HTML5_APP_STUDIO_RPM_NAME-$HTML5_APP_STUDIO_VERSION.tar.bz2"
rpmbuild -ba $RPM_SPECS_DIR/$HTML5_APP_STUDIO_RPM_NAME.spec
`dirname $0`/rpm-specific/push_rpm.sh $RPMS_BASE_DIR/noarch/$HTML5_APP_STUDIO_RPM_NAME-$HTML5_APP_STUDIO_VERSION-$HTML5_APP_STUDIO_NEXT_REVISION.noarch.rpm $BORHAN_SHORT_SERVER_VERSION
echo "Pushed $HTML5_APP_STUDIO_RPM_NAME-$HTML5_APP_STUDIO_VERSION-$HTML5_APP_STUDIO_NEXT_REVISION.noarch.rpm to $BORHAN_SHORT_SERVER_VERSION" >> /tmp/nightly.log

HTML5LIB_VERSIONS="$HTML5LIB_VERSIONS $HTML5LIB_VERSION"
#cd $SOURCE_PACKAGING_DIR
#for HTML5LIB_VERSION in $HTML5LIB_VERSIONS;do
#	if ! tar ztf  $HTML5LIB_RPM_NAME-$HTML5LIB_VERSION.tar.gz ;then
#		wget $HTML5LIB_BASE_URI/$HTML5LIB_VERSION -O $HTML5LIB_RPM_NAME-$HTML5LIB_VERSION.tar.gz
#		tar zxf $HTML5LIB_RPM_NAME-$HTML5LIB_VERSION.tar.gz 
#		rm -rf $HTML5LIB_RPM_NAME-$HTML5LIB_VERSION
#		mv `ls -rtd borhan-mwEmbed-* | tail -1` $HTML5LIB_RPM_NAME-$HTML5LIB_VERSION
#		tar zcf $RPM_SOURCES_DIR/$HTML5LIB_RPM_NAME-$HTML5LIB_VERSION.tar.gz $HTML5LIB_RPM_NAME-$HTML5LIB_VERSION
#		echo "Packaged into $RPM_SOURCES_DIR/$HTML5LIB_RPM_NAME-$HTML5LIB_VERSION.tar.gz"
#	fi
#done
#rpmbuild -ba $RPM_SPECS_DIR/$HTML5LIB_RPM_NAME.spec
#~/scripts/push_rpm.sh $RPMS_BASE_DIR/noarch/$HTML5LIB_RPM_NAME-$HTML5LIB_VERSION-$HTML5LIB_NEXT_REVISION.noarch.rpm nightly1

if [ "$1" = 'launch-ec2' ];then
	. ~/csi/csi-functions.rc
	INSTANCE_ID=`start_instances $NFS_IMG 1 $SECURITY_GROUP` 
	while ! get_instance_status $ID ;do 
		echo "Waiting for instance to init.."
		sleep 10 
	done

	IP=`get_instance_ip $INSTANCE_ID`
	while ! nc $IP 22 -w1 ;do 
		echo "Waiting for instance to init.."
		sleep 10 
	done
	ec2-create-tags $INSTANCE_ID --tag Name="Borhan-Sanity-`date`"
	scp $SSH_QUIET_OPTS -i ~/csi.pem ~/nightly/borhan-install.sh ec2-user@$IP:/tmp
	ssh $SSH_QUIET_OPTS -t -i ~/csi.pem ec2-user@$IP sudo bash /tmp/borhan-install.sh
	INSTANCE_HOSTNAME=`ssh $SSH_QUIET_OPTS -i ~/csi.pem ec2-user@$IP hostname 2>/dev/null`
	SQL_FILE=/tmp/$INSTANCE_HOSTNAME-reportme.`date +%d_%m_%Y`.sql
	scp $SSH_QUIET_OPTS -i ~/csi.pem ec2-user@$IP:$SQL_FILE /tmp
	#ec2-terminate-instances $INSTANCE_ID
	CSI_MACHINE=ce-csi.dev.borhan.com
	scp $SSH_QUIET_OPTS $SQL_FILE root@$CSI_MACHINE:/tmp 
	ssh $SSH_QUIET_OPTS root@$CSI_MACHINE /opt/vhosts/csi/update_csi_db.sh $SQL_FILE $BORHAN_SHORT_SERVER_VERSION
fi
ssh root@192.168.70.100 mail -s \'Nightly Core build ready\' jess.portnoy@borhan.com,Jonathan.Kanarek@borhan.com < /etc/issue 
