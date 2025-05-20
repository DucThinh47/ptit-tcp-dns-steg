from scapy.all import rdpcap, IP, TCP

def decode_fields(pkt):
    ttl_bit = pkt[IP].ttl & 1
    ipid_bit = pkt[IP].id % 2
    win_bit = pkt[TCP].window & 1
    return ttl_bit, ipid_bit, win_bit

def is_valid_stego(pkt):
    return (pkt[IP].ttl in [100, 101]) and \
           (pkt[IP].id in [20000, 20001]) and \
           (pkt[TCP].window in [2048, 2049])

def bits_to_text(bits):
    chars = []
    for i in range(0, len(bits), 8):
        byte = bits[i:i+8]
        if len(byte) == 8:
            chars.append(chr(int(''.join(map(str, byte)), 2)))
    return ''.join(chars)

def main():
    import sys
    if len(sys.argv) != 2:
        print("Usage: python3 detect_combined_steg.py <pcap_file>")
        return

    pkts = rdpcap(sys.argv[1])
    bits = []

    for i, pkt in enumerate(pkts):
        if IP in pkt and TCP in pkt:
            if is_valid_stego(pkt):
                ttl_bit, ipid_bit, win_bit = decode_fields(pkt)
                print(f"Packet #{i}: TTL={pkt[IP].ttl}, IPID={pkt[IP].id}, WIN={pkt[TCP].window}")
                bits.extend([ttl_bit, ipid_bit, win_bit])
            else:
                print(f"Packet #{i}: TTL={pkt[IP].ttl}, IPID={pkt[IP].id}, WIN={pkt[TCP].window}")

    print("\n[+] Decoded Message:")
    print(bits_to_text(bits))

if __name__ == "__main__":
    main()

