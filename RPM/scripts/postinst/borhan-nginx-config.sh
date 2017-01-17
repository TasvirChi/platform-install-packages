#!/bin/bash - 
#===============================================================================
#          FILE: borhan-nginx-config.sh
#         USAGE: ./borhan-nginx-config.sh 
#   DESCRIPTION: configure server as an Nginx  node.
#       OPTIONS: ---
# 	LICENSE: AGPLv3+
#  REQUIREMENTS: ---
#          BUGS: ---
#         NOTES: ---
#        AUTHOR: Jess Portnoy <jess.portnoy@borhan.com>
#  ORGANIZATION: Borhan, inc.
#       CREATED: 01/02/14 09:23:34 EST
#      REVISION:  ---
#===============================================================================

#set -o nounset                              # Treat unset variables as an error
verify_user_input()
{
        ANSFILE=$1
        . $ANSFILE
        RC=0
        for VAL in WWW_HOST VOD_PACKAGER_HOST VOD_PACKAGER_PORT IS_NGINX_SSL ; do
                if [ -z "${!VAL}" ];then
                        VALS="$VALS\n$VAL"
                        RC=1
                fi
        done
        if [ $RC -eq 1 ];then
                OUT="ERROR: Missing the following params in $ANSFILE
                $VALS
                "
                echo -en "${BRIGHT_RED}$OUT${NORMAL}\n"
                send_install_becon borhan-nginx $ZONE "install_fail"  "$OUT"
                exit $RC 
        fi
}


BORHAN_FUNCTIONS_RC=`dirname $0`/borhan-functions.rc
if [ ! -r "$BORHAN_FUNCTIONS_RC" ];then
	OUT="ERROR: Could not find $BORHAN_FUNCTIONS_RC so, exiting.."
	echo -e $OUT
	exit 3
fi
. $BORHAN_FUNCTIONS_RC
if ! rpm -q borhan-nginx;then
	echo -e "${BRIGHT_BLUE}Skipping as borhan-nginx is not installed.${NORMAL}"
	exit 0 
fi

if [ -n "$1" -a -r "$1" ];then
        ANSFILE=$1
        verify_user_input $ANSFILE
        . $ANSFILE
	if [ -z "$RTMP_PORT" ];then
                RTMP_PORT=1935
        fi
        export ANSFILE
else
	echo -e "${CYAN}Borhan API host [${YELLOW}`hostname`${CYAN}]:${NORMAL} "
	read -e WWW_HOST
	if [ -z "$WWW_HOST" ];then
		WWW_HOST=`hostname`
	fi

	echo -e "${CYAN}Nginx server name [${YELLOW}`hostname`${CYAN}]:${NORMAL} "
	read -e VOD_PACKAGER_HOST
	if [ -z "$VOD_PACKAGER_HOST" ];then
		VOD_PACKAGER_HOST=`hostname`
	fi

	echo -en "${CYAN}Nginx port to listen on [${YELLOW}88${CYAN}]:${NORMAL} "
	read -e VOD_PACKAGER_PORT
	if [ -z "$VOD_PACKAGER_PORT" ];then
		VOD_PACKAGER_PORT=88
	fi
	echo -en "${CYAN}RTMP port to listen on [${YELLOW}1935${CYAN}]:${NORMAL} "
	read -e RTMP_PORT
	if [ -z "$RTMP_PORT" ];then
		RTMP_PORT=1935
	fi
	echo -en "Would you like to configure Nginx with SSL?[Y/n]"
	read IS_NGINX_SSL
	if [ -z "$IS_NGINX_SSL" ];then
        	IS_NGINX_SSL='Y'
        fi  
	if [ "$IS_NGINX_SSL" = 'Y' -o "$IS_NGINX_SSL" = 'y' ];then
		echo -en "${CYAN}Nginx SSL port to listen on [${YELLOW}8443${CYAN}]:${NORMAL} "
		read -e VOD_PACKAGER_SSL_PORT
		if [ -z "$VOD_PACKAGER_SSL_PORT" ];then
			VOD_PACKAGER_SSL_PORT=8443
		fi
		echo -en "${CYAN}Nginx SSL cert: ${NORMAL} "
		read -e SSL_CERT 
		echo -en "${CYAN}Nginx SSL key: ${NORMAL} "
		read -e SSL_KEY
	fi
fi
if [ -f /etc/nginx/nginx.conf ];then
	mv /etc/nginx/nginx.conf /etc/nginx/nginx.conf.old
fi
sed -e 's#@STATIC_FILES_PATH@#/etc/nginx/static#g' -e "s#@VOD_PACKAGER_HOST@#$VOD_PACKAGER_HOST#g" -e "s#@VOD_PACKAGER_PORT@#$VOD_PACKAGER_PORT#g" -e "s#@RTMP_PORT@#$RTMP_PORT#g" -e "s#@LOG_DIR@#$LOG_DIR#" -e "s#@WWW_HOST@#$WWW_HOST#g" /etc/nginx/conf.d/nginx.conf.template > /etc/nginx/nginx.conf
sed -e 's#@STATIC_FILES_PATH@#/etc/nginx/static#g' /etc/nginx/conf.d/borhan.conf.template > /etc/nginx/conf.d/borhan.conf
sed -i "s#@LOG_DIR@#$LOG_DIR#" /etc/logrotate.d/nginx

if [ "$IS_NGINX_SSL" = 'Y' -o "$IS_NGINX_SSL" = 'y' ];then
	sed -e "s#@VOD_PACKAGER_HOST@#$VOD_PACKAGER_HOST#g" -e "s#@VOD_PACKAGER_SSL_PORT@#$VOD_PACKAGER_SSL_PORT#g" -e "s#@SSL_CERT@#$SSL_CERT#g" -e "s#@SSL_KEY@#$SSL_KEY#g" /etc/nginx/conf.d/ssl.conf.template > /etc/nginx/conf.d/ssl.conf
else
	touch /etc/nginx/conf.d/ssl.conf
fi
chkconfig borhan-nginx on
if service borhan-nginx status >/dev/null 2>&1;then
	service borhan-nginx reload
else
	service borhan-nginx start
fi

