#!/bin/sh -e
set -e
wget -O - http://installrepo.borhan.org/repo/apt/debian/borhan-deb.gpg.key|apt-key add -
echo "deb [arch=amd64] http://installrepo.borhan.org/repo/apt/debian jupiter main" > /etc/apt/sources.list.d/borhan.list

# aptitude has a more advanced API then apt-get and is better at resolving deps. For some reason, it is not installed on all deb based system so lets see if we haveit.

if which aptitude;then
        APT_TOOL="aptitude -y"
else
        APT_TOOL="apt-get -y"
fi
$APT_TOOL update
$APT_TOOL install lsb-release 
# for Debian, the non-free repo must also be enabled
# Ubuntu: You must also make sure the multiverse repo is enabled in /etc/apt/sources.list
# Debian Jessie [8]: You must also make sure the following Wheezy repos are enabled in /etc/apt/sources.list
DISTRO=`lsb_release -s -i`
if [ "$DISTRO" = 'Ubuntu' ];then
	apt-add-repository multiverse
elif [ "$DISTRO" = 'Debian' ];then
	$APT_TOOL install software-properties-common
	apt-add-repository non-free
	CODENAME=`lsb_release  -s -c`
	if [ "$CODENAME" != 'wheezy' ];then
		apt-add-repository "deb http://ftp.debian.org/debian/ wheezy main"
		apt-add-repository "deb http://security.debian.org/ wheezy/updates main"
	fi
fi
$APT_TOOL install mysql-server
$APT_TOOL install borhan-postinst
$APT_TOOL install borhan-base
$APT_TOOL install borhan-widgets borhan-html5lib borhan-html5-studio
$APT_TOOL install borhan-front
$APT_TOOL install borhan-sphinx
$APT_TOOL install borhan-db
$APT_TOOL install borhan-batch
$APT_TOOL install borhan-dwh
$APT_TOOL install borhan-nginx
/etc/init.d/borhan-nginx start

