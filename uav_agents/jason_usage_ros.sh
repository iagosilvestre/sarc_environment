#!/bin/bash
echo "Starting the Monitored Agent "

./gradlew &
sleep 3
J_PID=$(jps | grep JaCaMoLauncher | awk 'NR==1{print $1}')

PNAME="JaCaMoLauncher"
LOG_FILE="top_cpu.txt"
#PID=$(ps a|grep ros | awk 'NR<21{print $1}' | tr '\n' ',' | sed 's/.$//')

top -b -d 2 -p $J_PID | awk \
    -v cpuLog="$LOG_FILE" -v pid="$J_PID" -v pname="$PNAME" '
    /^top -/{time = $3}
    $1+0>0 {printf "%s %s :: %s[%s] CPU Usage: %d%%\n", \
            strftime("%Y-%m-%d"), time, pname, pid, $9 > cpuLog
            fflush(cpuLog)}'
            
