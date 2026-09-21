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

### 3. Nhận xét kỹ thuật dựa trên số liệu thực nghiệm

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
