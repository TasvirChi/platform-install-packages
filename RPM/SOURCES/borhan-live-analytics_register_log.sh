#!/bin/sh -

LOGSDIR=/opt/borhan/log/nginx
LOGFILE=live_access_log.gz.1
CASSANDRA_NODE_NAME=$1

PREFIX=`hostname`-`date +%Y%m%d%H%M%S`
UNIQLOGNAME=${PREFIX}.gz
MAX_NUM_OF_LINES=5000

cd $LOGSDIR
if [ ! -s $LOGFILE ];then
        exit 0
fi
mv $LOGFILE $UNIQLOGNAME
zcat $UNIQLOGNAME  | split - -l${MAX_NUM_OF_LINES} -d ${PREFIX}
gzip ${PREFIX}*

rm -f ${UNIQLOGNAME}

for splitted_file in ${PREFIX}*; do
    java -Dlog4j.configuration=file:/opt/borhan/lib/log4j.properties -cp /opt/borhan/lib/*:/opt/borhan/lib/register-file.jar com.borhan.live.RegisterFile $CASSANDRA_NODE_NAME $LOGSDIR $splitted_file 2>&1 | gzip >> /opt/borhan/log/register-file.`date +%F`.log.gz
done
