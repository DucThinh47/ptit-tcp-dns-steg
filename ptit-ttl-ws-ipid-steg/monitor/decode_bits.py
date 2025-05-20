def bits_to_text(bits):
    chars = []
    for i in range(0, len(bits), 8):
        byte = bits[i:i+8]
        if len(byte) < 8:
            print(f"[!] Bỏ qua byte không đủ 8 bit: {byte}")
            continue
        byte_str = ''.join(str(b) for b in byte)
        char = chr(int(byte_str, 2))
        chars.append(char)
    return ''.join(chars)

def main():
    bit_string = input("Nhập chuỗi bit (không có dấu cách):\n> ")

    bits = [int(b) for b in bit_string.strip()]
    
    message = bits_to_text(bits)
    print(f"\nThông điệp giải mã được là: {message}")

if __name__ == "__main__":
    main()

