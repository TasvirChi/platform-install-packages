PATH=$PATH:/opt/borhan/bin
export PATH
alias allkaltlog='grep --color "ERR:\|PHP \|Stack trace:\|CRIT\|\[error\]" /opt/borhan/log/*.log /opt/borhan/log/batch/*.log'
alias kaltlog='tail -f /opt/borhan/log/*.log /opt/borhan/log/batch/*.log | grep -A 1 -B 1 --color "ERR:\|PHP\|trace\|CRIT\|\[error\]"'
if [ -r /etc/borhan.d/system.ini ];then
        . /etc/borhan.d/system.ini
fi
