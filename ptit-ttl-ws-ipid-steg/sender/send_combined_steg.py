from scapy.all import IP, TCP, send
import random

def send_stego_packet(dst_ip, ttl, ip_id, win, is_noise=False):
    pkt = IP(dst=dst_ip, ttl=ttl, id=ip_id)/TCP(dport=12345, sport=54321, window=win)
    send(pkt, verbose=0)
    if is_noise:
        print(f"Sent packets...")
    else:
        print(f"Sending...")

def encode_bit_to_field(bit, values):
    return values[0] if bit == 0 else values[1]

def main():
    import sys
    if len(sys.argv) != 2:
        print("Usage: sudo python3 send_combined_steg.py <message>")
        return

    dst_ip = "192.168.50.10"
    message = sys.argv[1]
    bits = ''.join(format(ord(c), '08b') for c in message)
    chunks = [bits[i:i+3] for i in range(0, len(bits), 3)]

    for chunk in chunks:
        b1 = int(chunk[0]) if len(chunk) > 0 else 0
        b2 = int(chunk[1]) if len(chunk) > 1 else 0
        b3 = int(chunk[2]) if len(chunk) > 2 else 0

        ttl = encode_bit_to_field(b1, [100, 101])
        ip_id = encode_bit_to_field(b2, [20000, 20001])
        win = encode_bit_to_field(b3, [2048, 2049])

        send_stego_packet(dst_ip, ttl, ip_id, win)

        for _ in range(random.randint(1, 2)):
            ttl_noise = random.choice([64, 128, 255])
            ip_id_noise = random.randint(100, 300)
            win_noise = random.choice([8192, 16384])
            send_stego_packet(dst_ip, ttl_noise, ip_id_noise, win_noise, is_noise=True)

    print(f"[+] Done sending message: '{message}'")

if __name__ == "__main__":
    main()

