#!/bin/bash
echo "$(date)"
./gradlew  -q --console=plain &
sleep 2
LOG_ROS="ros.log"
LOG_JAS="jason.log"
PIDS_ROS=$(ps aux --sort=-%cpu | grep ros | awk 'NR<21{print $2}' | tr '\n' ',' | sed 's/.$//')
top -b -d 0.01 -p $PIDS_ROS | awk \
    -v cpuLog="$LOG_ROS" '
    BEGIN{sCPU=0.0; sMEM=0.0; count=1; tCPU=0.0; tMEM=0.0} 
    $1+0>0 {sCPU+=$9; sMEM+=$10;}
    /^$/ {if (sCPU>0) {tCPU+=sCPU; tMEM+=sMEM; printf "AvgCPU: %3d - AvgMEM: %3.1f \n", int(tCPU/count), tMEM/count > cpuLog; fflush(cpuLog); sCPU=0.0; sMEM=0.0; count++;}}' &
top_ros=$!

PID_JAS=$(jps | grep JaCaMoLauncher | awk 'NR==1{print $1}')
top -b -d 0.01 -p $PID_JAS | awk \
    -v cpuLog="$LOG_JAS" '
    BEGIN{sCPU=0.0; sMEM=0.0; count=1; tCPU=0.0; tMEM=0.0} 
    $1+0>0 {sCPU+=$9; sMEM+=$10;}
    /^$/ {if (sCPU>0) {tCPU+=sCPU; tMEM+=sMEM; printf "%d, CPU: %3d - MEM: %4.1f - AvgMEM: %3.1f \n", count, sCPU, sMEM, tMEM/count > cpuLog; fflush(cpuLog); sCPU=0.0; sMEM=0.0; count++;}}' &
top_jason=$!

end=$((SECONDS+120))
while [ $SECONDS -lt $end ]; do
    ps -p $PID_JAS -o %cpu
    ps -p $PIDS_ROS -o %cpu | awk \
    'BEGIN{sCPU=0;} 
    $1+0>0 {sCPU+=$1; printf "\b\b\b\b%4d", sCPU;}'
    echo " "
    sleep 2
done
echo "$(date)"
kill -9 $top_ros
kill -9 $top_jason
touch .stop___MAS
exit 0

# Command line test (adjust the PID):
#top -b -d 2 -p 3843697 ...

# Change lines 12 and 13 for those bellow to print all values
#    $1+0>0 {sCPU+=$9; printf "%d, ", $9  > cpuLog}
#    /^$/ {if (sCPU>0) {tCPU+=sCPU; printf "\b\b - Sum: %d, Avg: %f \n", sCPU, tCPU/count > cpuLog; fflush(cpuLog); sCPU=0; count++;}}' &
