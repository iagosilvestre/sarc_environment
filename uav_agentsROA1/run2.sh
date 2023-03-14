#!/bin/bash
echo "Starting the Monitored Agent "

./gradlew &
#J_PID=$!
#ps aux|grep java
sleep 3
J_PID=$(jps | grep JaCaMoLauncher | awk 'NR==1{print $1}')
#echo $J_PID
top -b -d 1 -p $J_PID >> top_cpu.txt &
TOP_PID=$!
ros2 topic pub /ariac/start_human std_msgs/msg/Bool '{data: true}' --once 

# Loop to get the CPU usage of the processes until a key is pressed
while true; do
# Wait for user input
  read -n1 -t 1 -r -p "Press 'q' to quit... " key
  echo ""
  if [[ "$key" == "q" ]]; then
    break
  fi
done

kill $TOP_PID
touch .stop___MAS
echo "Agent ended "
exit 0
