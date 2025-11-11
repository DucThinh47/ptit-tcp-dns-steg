# Lab: Giấu tin trong mạng sử dụng TCP và DNS
## Lý thuyết
**Phần 1: Giấu tin qua TCP Destination Port (Kỹ thuật tcp_covert.sh)**

***1. Lý thuyết "Kênh ẩn" qua Port (Port-based Covert Channel)***
- `Kênh hợp lệ`: Giao thức TCP thông thường.
- `Kênh ẩn`: Tạo ra bằng cách cố ý gửi các gói tin (TCP) đến các Destination Port (Cổng đích) cụ thể. Trình tự (sequence) của các cổng đích này sẽ tạo nên thông điệp.


***2. Kỹ thuật Mã hóa ASCII-Offset (ASCII-Offset Encoding)***
- `Quy tắc`: Cổng_đích_ẩn = Giá_trị_Offset + Mã_ASCII_của_ký_tự
- Suy ra từ bài lab:
    - `Offset` (Giá trị nền) là 8000.
    - Dải ký tự là ASCII từ 32 đến 126 (các ký tự in được).
    - Do đó, cổng đích nằm trong dải:
        - `8000 + 32` (ký tự 'space') = `8032`
        - `8000 + 126` (ký tự '~') = `8126`
- Ví dụ: Để gửi chữ "A" (mã ASCII là 65), script sẽ gửi một gói tin TCP đến cổng đích `8000 + 65 = 8065`.

***3. Nguyên tắc "Thêm nhiễu" (Chaffing)***

Bài lab mô tả rõ cách thức lẩn tránh:
- `Tín hiệu (Signal)`: Các gói tin có cổng đích trong dải [8032, 8126] là các gói mang tin ẩn.
- `Nhiễu (Noise)`: Script `tcp_covert.sh` cũng tạo ra "các port nhiễu" (các gói tin nhiễu) có cổng đích nằm ngoài dải này để che giấu luồng tin thật. Bên nhận (`decode_port.py`) phải biết quy tắc này để lọc bỏ nhiễu.

***4. Kỹ thuật "Truyền tin Tuần tự" (Sequential Transmission)***

Thông điệp được gửi đi bằng một chuỗi các gói tin, với mỗi gói tin đại diện cho một ký tự. Bên nhận phải bắt và sắp xếp các gói tin này theo đúng thứ tự để khôi phục lại thông điệp.

**Phần 2: Giấu tin qua DNS Query (Kỹ thuật dns_covert.sh)**
Kỹ thuật này sử dụng Tầng Ứng dụng, cụ thể là các truy vấn DNS (Domain Name System), để truyền dữ liệu.

***5. Lý thuyết "Đường hầm DNS" (DNS Tunneling)***

Đây là tên gọi tiêu chuẩn cho kỹ thuật này.
- `Kênh hợp lệ`: Các truy vấn DNS (thường qua cổng 53) là một loại lưu lượng mạng rất phổ biến và hầu như luôn được tường lửa cho phép đi qua.
- `Kênh ẩn`: Dữ liệu bí mật được "gói" (encapsulate) bên trong trường Query Name (Tên miền Truy vấn) của một gói tin DNS.

***6. Kỹ thuật Mã hóa Dữ liệu trong Tên miền con (Subdomain Encoding)***
Đây là cách thức dữ liệu được "gói" vào.
- `Quy tắc`: Bên gửi (sender) lấy một mẩu thông điệp (ví dụ: "ATT") và đặt nó làm tên miền con (subdomain) của một tên miền "mẹ" (carrier domain) mà nó kiểm soát.
- Ví dụ:
    - `Thông điệp`: "SECRET"
    - `Tên miền mẹ`: ptit.vn
    - Bên gửi sẽ tạo ra một truy vấn DNS (DNS Query) cho tên miền: `S.E.C.R.E.T.ptit.vn` (Hoặc `SECRET.ptit.vn`, tùy cách mã hóa).
- `Bên nhận`: Bên nhận (có thể là một máy chủ DNS độc hại của kẻ tấn công) sẽ nhận được truy vấn này, trích xuất phần tên miền con ("SECRET") và ghép chúng lại để lấy thông điệp.

***7. Nguyên tắc Phát hiện dựa trên Dấu hiệu (Signature-based Detection)***

Bài lab cũng chỉ ra cách để phát hiện kỹ thuật này, đây là các "dấu hiệu" (signatures) bất thường:
- `Tên miền mẹ Cố định`: Rất nhiều truy vấn DNS đi đến các tên miền con khác nhau nhưng đều thuộc cùng một tên miền mẹ (ví dụ: *.secret.ptit).
- `Độ dài Cố định`: Các tên miền con mang tin thường có độ dài cố định (ví dụ: 3-5 ký tự), không giống với các tên miền con bình thường.
- `Hành vi Bất thường`: "Không có truy vấn ngược (PTR record)" hoặc các truy vấn không nhận được phản hồi hợp lệ. Đây là dấu hiệu của việc "bắn và quên" (fire-and-forget) chỉ để gửi dữ liệu đi (data exfiltration).
## Thực hành
Thực hiện kiểm tra ping từ `sender` đến `receiver` và quan sát trên wireshark xem có bắt được gói tin không:

![img](0)

Mở Wireshark trên máy `monitor`:

![img](1)

Trên máy `sender`, cấp quyền thực thi cho script `tcp_covert.sh`:

    chmod +x tcp_covert.sh

![img](2)

Tiến hành thực thi script `tcp_covert.sh`:

    sudo  ./tcp_covert.sh

![img](3)

Với kỹ thuật giấu tin này, Port đích thường nằm trong khoảng `8000-8126` (tương ứng ASCII 32-126 + 8000). Các port nhiễu thường nằm ngoài khoảng này hoặc không theo quy tắc.

Trên máy `monitor`, quan sát Wireshark, tìm ra các gói tin có thông điệp ẩn giấu:

![img](4)

Sau khi tìm ra danh sách các gói tin, ghi nhớ số lượng gói tin, liệt kê giá trị Destination port field tương ứng của từng gói tin vào trong nội dung file `decode_port`:

![img](5)

Sau đó thực thi file để tìm ra thông điệp gốc:

    python3 decode_port.py

Sau đó, ghi danh sách ports, thông điệp tìm được và số gói tin vào file `answer.txt` trên máy receiver (đối với số gói tin, ghi vào bên cạnh thông điệp tìm được, ví dụ (thong_diep 10)):

    nano answer.txt

Trên máy `sender`, cấp quyền thực thi cho script `dns_covert.sh`:

    chmod +x dns_covert.sh

![img](6)

Tiến hành thực thi script `dns_covert.sh`:

    sudo ./dns_covert.sh

![img](7)

Đối với kỹ thuật giấu tin này, tên miền chứa subdomain đặc biệt (ví dụ: *.secret.ptit). Độ dài subdomain cố định (thường 3-5 ký tự). Không có truy vấn ngược (PTR record) đi kèm.

Trên Wireshark, quan sát, lọc ra các gói có chứa thông điệp ẩn:

![img](8)

Ghi nhớ số lượng gói tin có chứa thông điệp ẩn, tìm ra thông điệp ẩn và ghi kết quả vào file `answer.txt` trên máy receiver (chú ý, đối với số gói tin, ghi vào bên cạnh thông điệp tìm được, ví dụ (`thong_diep 10`)).





