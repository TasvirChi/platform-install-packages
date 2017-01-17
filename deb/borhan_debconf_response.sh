echo borhan-base    borhan-base/admin_console_email        string  @ADMIN_CONSOLE_ADMIN_MAIL@ | debconf-set-selections
echo borhan-base    borhan-base/admin_console_passwd_again password        @ADMIN_CONSOLE_PASSWORD@ | debconf-set-selections
echo borhan-base    borhan-base/admin_console_passwd_dont_match    note | debconf-set-selections
echo borhan-base    borhan-base/admin_console_passwd_invalid_char  note | debconf-set-selections
echo borhan-base    borhan-base/admin_console_passwd       password        @ADMIN_CONSOLE_PASSWORD@ | debconf-set-selections
echo borhan-base    borhan-base/apache_hostname    string  @BORHAN_VIRTUAL_HOST_NAME@ | debconf-set-selections
echo borhan-base    borhan-base/bad_time_zone      note | debconf-set-selections
echo borhan-base    borhan-base/cdn_hostname       string  @CDN_HOST@ | debconf-set-selections
echo borhan-base    borhan-base/contact_phone      string  +1 800 871 5224 | debconf-set-selections
echo borhan-base    borhan-base/contact_url        string  http://corp.borhan.com/company/contact-us | debconf-set-selections
echo borhan-base    borhan-base/db_hostname        string  @DB1_HOST@ | debconf-set-selections
echo borhan-base    borhan-base/db_port    string  @DB1_PORT@ | debconf-set-selections
echo borhan-base    borhan-base/dwh_db_hostname    string  @DB1_HOST@ | debconf-set-selections
echo borhan-base    borhan-base/dwh_db_port        string  @DB1_PORT@ | debconf-set-selections
echo borhan-base    borhan-base/env_name   string  Borhan Video Platform | debconf-set-selections
echo borhan-base    borhan-base/install_analytics_consent  boolean false | debconf-set-selections
echo borhan-base    borhan-base/install_analytics_email    string @YOUR_EMAIL@ | debconf-set-selections
echo borhan-base    borhan-base/ip_range   string  @IP_RANGE@ | debconf-set-selections
echo borhan-base    borhan-base/media_server_hostname      string | debconf-set-selections
echo borhan-base    borhan-base/mysql_super_passwd password        @MYSQL_ROOT_PASSWD@ | debconf-set-selections
echo borhan-base    borhan-base/mysql_super_user   string  root | debconf-set-selections
echo borhan-base    borhan-base/borhan_mysql_passwd       password        @DB1_PASS@ | deconf-set-selections
echo borhan-base    borhan-base/borhan_mysql_passwd_again password        @DB1_PASS@ | deconf-set-selections
echo borhan-base    borhan-base/auto_generate_borhan_mysql_passwd boolean false | debconf-set-selections
echo borhan-base    borhan-base/second_sphinx_hostname     string  @SPHINX_SERVER1@ | debconf-set-selections
echo borhan-base    borhan-base/service_url        string  @SERVICE_URL@ | debconf-set-selections
echo borhan-base    borhan-base/sphinx_hostname    string  @SPHINX_SERVER2@ | debconf-set-selections
echo borhan-base    borhan-base/time_zone  string @TIME_ZONE@| debconf-set-selections
echo borhan-base    borhan-base/vhost_port string  @BORHAN_VIRTUAL_HOST_PORT@ | debconf-set-selections
echo borhan-base    borhan-base/vod_packager_hostname      string  @VOD_PACKAGER_HOST@ | debconf-set-selections
echo borhan-base    borhan-base/vod_packager_port  string  @VOD_PACKAGER_PORT@ | debconf-set-selections

echo borhan-db      borhan-db/db_already_installed boolean false | debconf-set-selections
echo borhan-db      borhan-db/db_hostname  string  @DB1_HOST@ | debconf-set-selections
echo borhan-db      borhan-db/db_port      string  3306 | debconf-set-selections
echo borhan-db      borhan-db/fix_mysql_settings   boolean true | debconf-set-selections
echo borhan-db      borhan-db/mysql_super_passwd   password        @MYSQL_ROOT_PASSWD@ | debconf-set-selections
echo borhan-db      borhan-db/mysql_super_user     string  root | debconf-set-selections
echo borhan-db      borhan-db/remove_db    boolean false | debconf-set-selections


echo borhan-front   borhan-front/apache_ssl_cert   string  /etc/ssl/certs/ssl-cert-snakeoil.pem | debconf-set-selections
echo borhan-front   borhan-front/apache_ssl_chain  string | debconf-set-selections
echo borhan-front   borhan-front/apache_ssl_key    string  /etc/ssl/private/ssl-cert-snakeoil.key | debconf-set-selections
echo borhan-front   borhan-front/is_apache_ssl     boolean false | debconf-set-selections
echo borhan-front   borhan-front/self_signed_cert  note | debconf-set-selections
echo borhan-front   borhan-front/service_url       string  @SERVICE_URL@ | debconf-set-selections
echo borhan-front   borhan-front/vhost_port        string  @BORHAN_VIRTUAL_HOST_PORT@ | debconf-set-selections
echo borhan-front   borhan-front/web_interfaces    multiselect | debconf-set-selections

echo borhan-nginx   borhan-nginx/borhan_service_url       string  @SERVICE_URL@ | debconf-set-selections
echo borhan-nginx   borhan-nginx/nginx_hostname    string  @VOD_PACKAGER_HOST@ | debconf-set-selections
echo borhan-nginx   borhan-nginx/nginx_port        string  @VOD_PACKAGER_PORT@ | debconf-set-selections
echo borhan-nginx   borhan-nginx/ssl_cert	     string  @SSL_CERT@  | debconf-set-selections
echo borhan-nginx   borhan-nginx/ssl_key	     string  @SSL_KEY@  | debconf-set-selections
echo borhan-nginx   borhan-nginx/is_ssl	     boolean false | debconf-set-selections

echo mysql-server-5.5        mysql-server/root_password_again        password @MYSQL_ROOT_PASSWD@ | debconf-set-selections
echo mysql-server-5.5        mysql-server/root_password      password @MYSQL_ROOT_PASSWD@ | debconf-set-selections
