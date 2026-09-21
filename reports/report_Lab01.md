# BÁO CÁO THỰC HÀNH LAB 1: PHÂN TÍCH VÀ XỬ LÝ TÍN HIỆU ÂM THANH SỐ

* **Học phần:** CSE457 – Xử lý âm thanh và tiếng nói
* **Họ và tên sinh viên:** Nguyễn Văn Minh
* **Mã số sinh viên (MSSV):** 2351260673
* **Môi trường thực thi:** Python 3.12 (NumPy, SciPy, Matplotlib, Pandas, Pydub)
* **Dữ liệu thực nghiệm:** 
  1. `audio/piano_sample.mp3` (Đoạn độc tấu Piano - Âm nhạc)
  2. `audio/news_speech.mp3` (Đoạn bản tin thời sự - Tiếng nói)

---

## KHỐI A: ĐỌC VÀ KIỂM TRA DỮ LIỆU ÂM THANH

### 1. Mục tiêu thực hiện
Theo đúng yêu cầu tại Mục 3 - Khối A của đề cương thực hành:
* Đọc đồng thời 2 tệp âm thanh thực nghiệm đại diện cho 2 dạng tín hiệu: Âm nhạc (`piano_sample.mp3`) và Tiếng nói (`news_speech.mp3`).
* Kiểm tra và trích xuất các thông số số hóa: Tần số lấy mẫu ($F_s$), số kênh ($C$), thời lượng ($T$), độ sâu mẫu ($B$), kích thước tệp và tốc độ bit ($Bitrate$).
* Chuyển đổi từ tín hiệu 2 kênh (Stereo) sang 1 kênh (Mono) và chuẩn hóa biên độ mẫu về miền số thực chuẩn $[-1.0, 1.0]$.
* Đo đạc các đại lượng đặc trưng (Peak, RMS) và kiểm tra nguy cơ xén biên (Clipping).
* Trực quan hóa chuỗi âm thanh ban đầu để quan sát sự khác biệt về đặc tính âm học.

---

### 2. Bảng tổng hợp số liệu đo đạc thực tế

Số liệu được đo đạc trực tiếp bằng mã nguồn Python sau khi nạp và chuẩn hóa tín hiệu về Mono $[-1.0, 1.0]$:

| Tệp dữ liệu | Sampling Rate ($F_s$) | Số kênh gốc | Thời lượng ($T$) | Dung lượng tệp | Bit rate MP3 | Peak (tuyệt đối) | Peak (dBFS) | RMS (hiệu dụng) | RMS (dBFS) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Piano (Âm nhạc)** | $48{,}000\text{ Hz}$ | 2 (Stereo) | $35.243\text{ s}$ | $834.8\text{ KB}$ | $194.0\text{ kbps}$ | $0.4420$ | $-7.09\text{ dBFS}$ | $0.0653$ | $-23.70\text{ dBFS}$ |
| **Speech (Bản tin)** | $48{,}000\text{ Hz}$ | 2 (Stereo) | $35.243\text{ s}$ | $834.6\text{ KB}$ | $194.0\text{ kbps}$ | $0.4571$ | $-6.80\text{ dBFS}$ | $0.0658$ | $-23.64\text{ dBFS}$ |

---

### 3. Nhận xét kỹ thuật Khối A

1. **Về tần số lấy mẫu và định lý Nyquist-Shannon:**
   * Cả 2 tệp âm thanh đều có tần số lấy mẫu $F_s = 48{,}000\text{ Hz}$. Theo định lý Nyquist ($F_s \ge 2 F_{\max}$), giới hạn tần số cao nhất được bảo toàn mà không bị chồng phổ (aliasing) là $F_N = \frac{F_s}{2} = 24{,}000\text{ Hz}$.
   * Tần số Nyquist $24\text{ kHz}$ bao quát trọn vẹn toàn bộ dải nghe của tai người ($20\text{ Hz} - 20{,}000\text{ Hz}$).

2. **So sánh đặc tính chuỗi âm thanh ban đầu giữa Âm nhạc và Tiếng nói:**
   * **Tín hiệu Piano (Âm nhạc):** Dạng sóng dao động liên tục theo nhịp điệu của các nốt nhạc, có độ ngân vang (sustain) kéo dài, biên độ suy hao dần theo hàm mũ của búa gõ dây đàn. Mức năng lượng hiệu dụng đạt $\text{RMS} = 0.0653$ ($-23.70\text{ dBFS}$).
   * **Tín hiệu Tiếng nói (Bản tin thời sự):** Dạng sóng thể hiện tính gián đoạn rõ rệt, gồm các cụm phát âm nguyên âm năng lượng lớn đan xen với các phụ âm năng lượng nhỏ và các khoảng lặng tự nhiên giữa các cụm từ ngữ. Mức năng lượng hiệu dụng tổng thể đạt $\text{RMS} = 0.0658$ ($-23.64\text{ dBFS}$).

3. **Kiểm tra hiện tượng xén biên (Clipping):**
   * Giá trị đỉnh cực đại của tệp Piano là $\text{Peak} = 0.4420$ ($-7.09\text{ dBFS}$) và tệp Tiếng nói là $\text{Peak} = 0.4571$ ($-6.80\text{ dBFS}$).
   * Cả hai giá trị đều thấp hơn đáng kể so với ngưỡng bão hòa $1.0$ ($0\text{ dBFS}$), khoảng headroom an toàn lần lượt là $7.09\text{ dBFS}$ và $6.80\text{ dBFS}$. Xác nhận cả 2 tệp đều hoàn toàn sạch, không bị méo hài phi tuyến do xén đỉnh (clipping).

4. **Bản chất định dạng nén MP3:**
   * Cả 2 tệp nguồn đều là tệp nén MP3 với tốc độ bit đo được $\approx 194.0\text{ kbps}$ (chuẩn nén tri giác lossy). Pydub/FFmpeg giải mã luồng bit này thành các mẫu số nguyên 16-bit trước khi đưa về mảng float64 trong Python.
   * Việc giải mã chỉ phục vụ cho việc biểu diễn và tính toán số, không thể khôi phục các thành phần tần số thính giác đã bị lược bỏ trong quá trình nén MP3 trước đó.

---

## KHỐI B: PHÂN TÍCH MIỀN THỜI GIAN (TIME-DOMAIN ANALYSIS)

### 1. Mục tiêu thực hiện
Theo đúng yêu cầu tại Mục 3 - Khối B của đề cương thực hành:
* Tính toán các chỉ số đặc trưng miền thời gian:
  * **Giá trị đỉnh (Peak):** $\text{Peak} = \max_n |x[n]|$
  * **Giá trị hiệu dụng (RMS):** $\text{RMS} = \sqrt{\frac{1}{N} \sum_{n=0}^{N-1} x^2[n]}$
  * **Năng lượng toàn phần (Energy):** $E = \sum_{n=0}^{N-1} x^2[n]$
* Chọn ít nhất 02 phân đoạn ngắn ($1.0\text{ s}$) có đặc tính đối lập rõ rệt để so sánh: Đoạn phát âm mạnh (năng lượng cao) và Đoạn khoảng lặng/ngắt nghỉ (năng lượng thấp).
* Vẽ đồ thị dạng sóng chuẩn gồm: Dạng sóng toàn bộ tệp ($35.243\text{ s}$) kết hợp với đồ thị phóng to chi tiết $1.0\text{ s}$ của 2 phân đoạn khảo sát, lưu vào tệp `figures/waveform.png`.
* Đánh giá hiện tượng xén biên (Clipping).

---

### 2. Bảng số liệu phân tích các phân đoạn miền thời gian

Các đại lượng được tính toán trên mảng tín hiệu đã chuẩn hóa về $[-1.0, 1.0]$ với $F_s = 48{,}000\text{ Hz}$ ($N = 48{,}000$ mẫu cho mỗi phân đoạn $1.0\text{ s}$):

| Phân đoạn tín hiệu | Khoảng thời gian | Số mẫu ($N$) | Peak (tuyệt đối) | Peak (dBFS) | RMS (hiệu dụng) | RMS (dBFS) | Năng lượng toàn phần ($E$) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Speech - Toàn bài** | $[0.0\text{s} - 35.2\text{s}]$ | $1{,}691{,}648$ | $0.4571$ | $-6.80\text{ dBFS}$ | $0.0658$ | $-23.64\text{ dBFS}$ | $7{,}317.54$ |
| **Speech - Đoạn 1 (Phát âm mạnh)** | $[13.0\text{s} - 14.0\text{s}]$ | $48{,}000$ | $0.4058$ | $-7.83\text{ dBFS}$ | $0.1424$ | $-16.93\text{ dBFS}$ | $973.58$ |
| **Speech - Đoạn 2 (Khoảng lặng/ngắt)** | $[11.0\text{s} - 12.0\text{s}]$ | $48{,}000$ | $0.1551$ | $-16.19\text{ dBFS}$ | $0.0282$ | $-31.01\text{ dBFS}$ | $38.04$ |
| **Piano - Toàn bài** | $[0.0\text{s} - 35.2\text{s}]$ | $1{,}691{,}648$ | $0.4420$ | $-7.09\text{ dBFS}$ | $0.0653$ | $-23.70\text{ dBFS}$ | $7{,}216.60$ |
| **Piano - Đoạn 1 (Hợp âm mạnh)** | $[11.0\text{s} - 12.0\text{s}]$ | $48{,}000$ | $0.3349$ | $-9.50\text{ dBFS}$ | $0.0830$ | $-21.62\text{ dBFS}$ | $330.65$ |
| **Piano - Đoạn 2 (Đoạn dạo nhỏ)** | $[0.0\text{s} - 1.0\text{s}]$ | $48{,}000$ | $0.1361$ | $-17.32\text{ dBFS}$ | $0.0330$ | $-29.63\text{ dBFS}$ | $52.25$ |

---

### 3. Đồ thị trực quan dạng sóng chuẩn (Waveform)

#### 3.1. Dạng sóng tệp Tiếng nói (Speech)
![Dạng sóng tệp Tiếng nói (Speech)](../figures/waveform_speech.png)

*Hình B.1: Dạng sóng miền thời gian của tệp Tiếng nói (Bản tin thời sự). Hàng 1: Toàn bộ tệp 35.2s với vùng highlight Đoạn 1 [13.0s - 14.0s] (đỏ: phát âm mạnh) và Đoạn 2 [11.0s - 12.0s] (xanh lá: khoảng lặng); Hàng 2: Phóng to chi tiết Đoạn 1 thể hiện các chu kỳ dao động thanh môn; Hàng 3: Phóng to chi tiết Đoạn 2 thể hiện mức nhiễu nền phẳng của khoảng lặng.*

#### 3.2. Dạng sóng tệp Âm nhạc (Piano)
![Dạng sóng tệp Âm nhạc (Piano)](../figures/waveform_piano.png)

*Hình B.2: Dạng sóng miền thời gian của tệp Âm nhạc (Độc tấu Piano). Hàng 1: Toàn bộ tệp 35.2s với vùng highlight Đoạn 1 [11.0s - 12.0s] (cam: hợp âm ngân vang) và Đoạn 2 [0.0s - 1.0s] (xanh ngọc: đoạn dạo đầu nhẹ); Hàng 2: Phóng to chi tiết Đoạn 1 thể hiện sự giao thoa phức hợp của nhiều dây đàn; Hàng 3: Phóng to chi tiết Đoạn 2 thể hiện các nốt đơn lẻ có năng lượng khiêm tốn.*

---

### 4. Nhận xét và giải thích kỹ thuật Khối B

1. **Sự tương phản năng lượng và RMS giữa 2 phân đoạn đối lập:**
   * **Đối với Tiếng nói (Speech):** Đoạn 1 ($13.0 - 14.0\text{s}$) có năng lượng đạt $E_1 = 973.58$ và $\text{RMS}_1 = 0.1424$ ($-16.93\text{ dBFS}$). Trong khi đó, Đoạn 2 ($11.0 - 12.0\text{s}$) là khoảng dừng nghỉ giữa hai mệnh đề nên năng lượng giảm chỉ còn $E_2 = 38.04$ và $\text{RMS}_2 = 0.0282$ ($-31.01\text{ dBFS}$). Tỷ lệ năng lượng chênh lệch tới $\frac{E_1}{E_2} \approx 25.6$ lần, tương ứng với mức chênh lệch biên độ hiệu dụng RMS lên tới $14.08\text{ dB}$.
   * **Đối với Âm nhạc (Piano):** Đoạn 1 ($11.0 - 12.0\text{s}$) là hợp âm ngân vang sau cú gõ phím mạnh có năng lượng đạt $E_1 = 330.65$ và $\text{RMS}_1 = 0.0830$ ($-21.62\text{ dBFS}$). Đoạn 2 ($0.0 - 1.0\text{s}$) là đoạn dạo đầu nhẹ nhàng với các nốt đơn lẻ, năng lượng chỉ đạt $E_2 = 52.25$ và $\text{RMS}_2 = 0.0330$ ($-29.63\text{ dBFS}$). Chênh lệch năng lượng gấp $6.33$ lần và chênh lệch RMS là $8.01\text{ dB}$.

2. **Phân tích hình dáng sóng qua đồ thị phóng to $1.0\text{ s}$:**
   * **Đặc tính Tiếng nói (Hình B.1):**
     * *Đoạn 1 (Phát âm hữu thanh - Voiced Speech):* Đồ thị phóng to hiển thị cấu trúc dao động chu kỳ cực kỳ rõ nét. Các đỉnh xung nhọn xuất hiện lặp lại tuần hoàn với chu kỳ khoảng $\approx 7 - 8\text{ ms}$, tương ứng với tần số rung của dây thanh quản (Pitch period / $F_0 \approx 125 - 140\text{ Hz}$). Biên độ dao động lớn, đạt đỉnh $\text{Peak} = 0.4058$.
     * *Đoạn 2 (Khoảng lặng - Pause/Silence):* Dạng sóng suy giảm nhanh về trạng thái gần như phẳng hoàn toàn ở khoảng giữa $11.3\text{s} - 11.8\text{s}$. Tín hiệu chỉ còn lại mức dao động ngẫu nhiên biên độ rất nhỏ ($\text{RMS} = 0.0282$, $-31.01\text{ dBFS}$) sinh ra từ tạp âm nền phòng thu và dư âm tắt dần của câu nói trước.
   * **Đặc tính Âm nhạc Piano (Hình B.2):**
     * *Đoạn 1 (Hợp âm ngân vang):* Dạng sóng thể hiện sự giao thoa phức hợp (complex interference) của nhiều dây đàn cùng rung đồng thời. Biên độ dao động dày đặc, bao gồm cả dao động cơ bản của nốt trầm và các họa âm tần số cao, suy giảm chậm và êm đềm theo thời gian ($\text{Peak} = 0.3349$).
     * *Đoạn 2 (Dạo đầu nhẹ):* Dạng sóng rời rạc hơn, biên độ nhỏ ($\text{Peak} = 0.1361$), thể hiện các nhịp gõ phím rải rác trước khi bước vào cao trào của bản nhạc.

3. **Kiểm tra hiện tượng xén biên (Clipping):**
   * Giá trị cực đại tuyệt đối đo được trên toàn bộ tín hiệu của Tiếng nói là $\text{Peak} = 0.4571 < 1.0$ ($-6.80\text{ dBFS}$) và của Piano là $\text{Peak} = 0.4420 < 1.0$ ($-7.09\text{ dBFS}$).
   * Mức khoảng cách an toàn (headroom) tới ngưỡng bão hòa $1.0$ luôn lớn hơn $6.8\text{ dBFS}$, bảo đảm cả hai nguồn tín hiệu đều hoàn toàn nguyên vẹn, không có hiện tượng clipping làm xuất hiện sóng hài bão hòa giả mạo trước khi chuyển sang phân tích phổ FFT ở Khối C.
