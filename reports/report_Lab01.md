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

### 2. Cơ sở lý thuyết và công thức toán học

1. **Chu kỳ lấy mẫu ($T_s$) và Tần số Nyquist ($F_N$):**
   $$T_s = \frac{1}{F_s}, \quad F_N = \frac{F_s}{2}$$
   Với $F_s = 48{,}000\text{ Hz}$, chu kỳ lấy mẫu là $T_s \approx 20.833\ \mu\text{s}$ và tần số giới hạn Nyquist là $F_N = 24{,}000\text{ Hz}$.

2. **Tốc độ bit dòng dữ liệu thô PCM tương đương ($R_{\text{PCM}}$):**
   $$R_{\text{PCM}} = F_s \times B \times C \quad [\text{bit/s}]$$
   Trong đó $B$ là số bit lượng tử hóa mỗi mẫu ($B = 16\text{ bit}$ sau giải mã) và $C$ là số kênh âm thanh ($C = 2$ cho Stereo, $C = 1$ cho Mono).

3. **Mức biên độ đỉnh (Peak) và hiệu dụng (RMS) theo thang logarit toàn thang (dBFS):**
   $$\text{Peak}_{\text{dBFS}} = 20 \log_{10}\left(\frac{\text{Peak}}{X_{\text{FS}}}\right) = 20 \log_{10}(\text{Peak}) \quad (\text{với } X_{\text{FS}} = 1.0)$$
   $$\text{RMS}_{\text{dBFS}} = 20 \log_{10}\left(\frac{\text{RMS}}{X_{\text{FS}}}\right) = 20 \log_{10}(\text{RMS})$$

4. **Khoảng cách an toàn chống xén biên (Headroom):**
   $$\text{Headroom} = 0\text{ dBFS} - \text{Peak}_{\text{dBFS}} = -\text{Peak}_{\text{dBFS}} \quad (\text{dB})$$

---

### 3. Bảng tổng hợp số liệu đo đạc thực tế

Số liệu được đo đạc trực tiếp bằng mã nguồn Python sau khi nạp và chuẩn hóa tín hiệu về Mono $[-1.0, 1.0]$:

| Tệp dữ liệu | Tần số lấy mẫu ($F_s$) | Số kênh gốc ($C$) | Độ sâu mẫu ($B$) | Thời lượng ($T$) | Dung lượng tệp | Bit rate MP3 gốc | Bit rate PCM tương đương ($R_{\text{PCM}}$) | Peak (tuyệt đối) | Peak (dBFS) | RMS (hiệu dụng) | RMS (dBFS) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Piano (Âm nhạc)** | $48{,}000\text{ Hz}$ | 2 (Stereo) | $16\text{ bit}$ | $35.243\text{ s}$ | $834.8\text{ KB}$ | $194.0\text{ kbps}$ | $1{,}536.0\text{ kbps}$ | $0.4420$ | $-7.09\text{ dBFS}$ | $0.0653$ | $-23.70\text{ dBFS}$ |
| **Speech (Bản tin)** | $48{,}000\text{ Hz}$ | 2 (Stereo) | $16\text{ bit}$ | $35.243\text{ s}$ | $834.6\text{ KB}$ | $194.0\text{ kbps}$ | $1{,}536.0\text{ kbps}$ | $0.4571$ | $-6.80\text{ dBFS}$ | $0.0658$ | $-23.64\text{ dBFS}$ |

---

### 4. Nhận xét kỹ thuật Khối A

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
* Tính toán các chỉ số đặc trưng miền thời gian: Giá trị đỉnh ($\text{Peak}$), Giá trị hiệu dụng ($\text{RMS}$), Năng lượng toàn phần ($E$).
* Chọn ít nhất 02 phân đoạn ngắn ($1.0\text{ s}$) có đặc tính đối lập rõ rệt để so sánh: Đoạn phát âm mạnh (năng lượng cao) và Đoạn khoảng lặng/ngắt nghỉ (năng lượng thấp).
* Vẽ đồ thị dạng sóng chuẩn gồm: Dạng sóng toàn bộ tệp ($35.243\text{ s}$) kết hợp với đồ thị phóng to chi tiết $1.0\text{ s}$ của 2 phân đoạn khảo sát, lưu vào tệp `figures/waveform.png`.
* Đánh giá hiện tượng xén biên (Clipping).

---

### 2. Cơ sở lý thuyết và công thức toán học

1. **Giá trị đỉnh tuyệt đối (Peak Amplitude):**
   $$\text{Peak} = \max_{0 \le n < N} |x[n]|$$
   Phản ánh biên độ tức thời lớn nhất của tín hiệu trong khoảng thời gian quan sát. Giá trị này giúp kiểm tra khoảng cách an toàn tới ngưỡng bão hòa $1.0$ ($0\text{ dBFS}$) để phát hiện nguy cơ xén biên (clipping).

2. **Giá trị hiệu dụng (Root Mean Square - RMS):**
   $$\text{RMS} = \sqrt{\frac{1}{N} \sum_{n=0}^{N-1} x^2[n]}$$
   Đại diện cho năng lượng công suất trung bình cảm nhận được của âm thanh, không bị ảnh hưởng cục bộ bởi một vài mẫu gai nhọn đột biến.

3. **Năng lượng toàn phần (Total Energy):**
   $$E = \sum_{n=0}^{N-1} x^2[n] = N \cdot \text{RMS}^2$$
   Tổng bình phương biên độ của tất cả các mẫu trong khoảng quan sát. Với hai phân đoạn có cùng độ dài $N$, năng lượng tỷ lệ thuận với bình phương giá trị RMS.

4. **Chuyển đổi sang thang decibel toàn thang (dBFS):**
   $$\text{Peak}_{\text{dBFS}} = 20 \log_{10}(\text{Peak}), \quad \text{RMS}_{\text{dBFS}} = 20 \log_{10}(\text{RMS})$$

5. **Tỷ số tương phản năng lượng và chênh lệch RMS giữa hai phân đoạn cùng chiều dài ($N_1 = N_2$):**
   $$\text{Ratio}_E = \frac{E_1}{E_2} \implies \Delta \text{RMS}_{\text{dB}} = \text{RMS}_{1,\text{dBFS}} - \text{RMS}_{2,\text{dBFS}} = 10 \log_{10}(\text{Ratio}_E) = 20 \log_{10}\left(\frac{\text{RMS}_1}{\text{RMS}_2}\right)$$

---

### 3. Bảng số liệu phân tích các phân đoạn miền thời gian

Các đại lượng được tính toán trên mảng tín hiệu đã chuẩn hóa về $[-1.0, 1.0]$ với $F_s = 48{,}000\text{ Hz}$ ($N = 48{,}000$ mẫu cho mỗi phân đoạn $1.0\text{ s}$):

| Tệp dữ liệu | Phân đoạn khảo sát | Khoảng thời gian | Số mẫu ($N$) | Peak (tuyệt đối) | Peak (dBFS) | RMS (hiệu dụng) | RMS (dBFS) | Năng lượng ($E$) | Đặc tính âm học nổi bật |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| **Speech** | Toàn bài | $[0.0\text{s} - 35.2\text{s}]$ | $1{,}691{,}648$ | $0.4571$ | $-6.80\text{ dBFS}$ | $0.0658$ | $-23.64\text{ dBFS}$ | $7{,}317.54$ | Tổng thể bài phát thanh thời sự |
| **Speech** | Đoạn 1 (Phát âm mạnh) | $[13.0\text{s} - 14.0\text{s}]$ | $48{,}000$ | $0.4058$ | $-7.83\text{ dBFS}$ | $0.1424$ | $-16.93\text{ dBFS}$ | $973.58$ | Nguyên âm hữu thanh, tuần hoàn rõ nét |
| **Speech** | Đoạn 2 (Khoảng lặng) | $[11.0\text{s} - 12.0\text{s}]$ | $48{,}000$ | $0.1551$ | $-16.19\text{ dBFS}$ | $0.0282$ | $-31.01\text{ dBFS}$ | $38.04$ | Khoảng nghỉ giữa hai câu, nhiễu nền phẳng |
| **Piano** | Toàn bài | $[0.0\text{s} - 35.2\text{s}]$ | $1{,}691{,}648$ | $0.4420$ | $-7.09\text{ dBFS}$ | $0.0653$ | $-23.70\text{ dBFS}$ | $7{,}216.60$ | Bản độc tấu dương cầm liên tục |
| **Piano** | Đoạn 1 (Hợp âm mạnh) | $[11.0\text{s} - 12.0\text{s}]$ | $48{,}000$ | $0.3349$ | $-9.50\text{ dBFS}$ | $0.0830$ | $-21.62\text{ dBFS}$ | $330.65$ | Hợp âm ngân vang, nhiều dây rung cộng hưởng |
| **Piano** | Đoạn 2 (Đoạn dạo nhỏ) | $[0.0\text{s} - 1.0\text{s}]$ | $48{,}000$ | $0.1361$ | $-17.32\text{ dBFS}$ | $0.0330$ | $-29.63\text{ dBFS}$ | $52.25$ | Nốt nhạc mở đầu đơn lẻ, năng lượng khiêm tốn |

---

### 4. Đồ thị trực quan dạng sóng chuẩn (Waveform)

#### 4.1. Dạng sóng tệp Tiếng nói (Speech)
![Dạng sóng tệp Tiếng nói (Speech)](../figures/waveform_speech.png)

*Hình B.1: Dạng sóng miền thời gian của tệp Tiếng nói (Bản tin thời sự). Hàng 1: Toàn bộ tệp 35.2s với vùng highlight Đoạn 1 [13.0s - 14.0s] (đỏ: phát âm mạnh) và Đoạn 2 [11.0s - 12.0s] (xanh lá: khoảng lặng); Hàng 2: Phóng to chi tiết Đoạn 1 thể hiện các chu kỳ dao động thanh môn; Hàng 3: Phóng to chi tiết Đoạn 2 thể hiện mức nhiễu nền phẳng của khoảng lặng.*

#### 4.2. Dạng sóng tệp Âm nhạc (Piano)
![Dạng sóng tệp Âm nhạc (Piano)](../figures/waveform_piano.png)

*Hình B.2: Dạng sóng miền thời gian của tệp Âm nhạc (Độc tấu Piano). Hàng 1: Toàn bộ tệp 35.2s với vùng highlight Đoạn 1 [11.0s - 12.0s] (cam: hợp âm ngân vang) và Đoạn 2 [0.0s - 1.0s] (xanh ngọc: đoạn dạo đầu nhẹ); Hàng 2: Phóng to chi tiết Đoạn 1 thể hiện sự giao thoa phức hợp của nhiều dây đàn; Hàng 3: Phóng to chi tiết Đoạn 2 thể hiện các nốt đơn lẻ có năng lượng khiêm tốn.*

---

### 5. Nhận xét và giải thích kỹ thuật Khối B

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

---

## KHỐI C: PHÂN TÍCH MIỀN TẦN SỐ BẰNG FFT (FREQUENCY-DOMAIN ANALYSIS)

### 1. Mục tiêu thực hiện
* Áp dụng cửa sổ Hamming $w[n]$ ($L = 48{,}000$ mẫu) lên phân đoạn ổn định $1.0\text{ s}$ của cả 2 tệp âm thanh (Piano $[11.0\text{s} - 12.0\text{s}]$ và Speech $[13.0\text{s} - 14.0\text{s}]$).
* Tính phổ biến đổi Fourier nhanh thực (`rfft`), xác định và định vị các đỉnh phổ chính (spectral peaks).
* Khảo sát ảnh hưởng của $N_{\text{FFT}}$, phân biệt rạch ròi giữa khoảng cách bin tần số ($\Delta f$) và độ phân giải vật lý thực sự ($\Delta f_{\text{phys}}$).

### 2. Cơ sở lý thuyết và công thức toán học

1. **Cửa sổ làm mịn Hamming độ dài $L$ mẫu:**
   $$w[n] = 0.54 - 0.46 \cos\left(\frac{2\pi n}{L-1}\right), \quad 0 \le n \le L-1$$
   Nhân cửa sổ Hamming đưa biên độ hai đầu biên của khung về $0$ một cách êm ái, triệt tiêu sự gián đoạn chu kỳ giả mạo khi tính DFT tuần hoàn, nén búp sóng phụ (side-lobes) xuống mức $-42\text{ dB}$ và giảm thiểu hiện tượng rò rỉ phổ (spectral leakage).

2. **Tín hiệu sau đóng khung nhân cửa sổ (Windowing):**
   $$x_w[n] = x[n] \cdot w[n], \quad 0 \le n \le L-1$$

3. **Biến đổi Fourier rời rạc (DFT) kích thước $N_{\text{FFT}}$:**
   $$X[k] = \sum_{n=0}^{N_{\text{FFT}}-1} x_w[n] \, e^{-j \frac{2\pi k n}{N_{\text{FFT}}}} = \sum_{n=0}^{L-1} x_w[n] \, e^{-j \frac{2\pi k n}{N_{\text{FFT}}}}, \quad k = 0, 1, \dots, N_{\text{FFT}}-1$$
   *(với $x_w[n] = 0$ khi $n \ge L$ trong trường hợp đệm số không Zero-padding $N_{\text{FFT}} > L$)*.

4. **Trục tần số rời rạc và khoảng cách bin tần số (Frequency-bin spacing):**
   $$f_k = k \cdot \Delta f = k \cdot \frac{F_s}{N_{\text{FFT}}}, \quad k = 0, 1, \dots, \frac{N_{\text{FFT}}}{2}$$
   $$\Delta f = \frac{F_s}{N_{\text{FFT}}} \quad [\text{Hz}]$$

5. **Số điểm phổ thực tế (One-sided RFFT points):**
   $$K = \frac{N_{\text{FFT}}}{2} + 1$$

6. **Độ phân giải tần số vật lý thực sự (Physical Frequency Resolution):**
   $$\Delta f_{\text{phys}} \approx \frac{F_s}{L} = \frac{1}{T_w} \quad [\text{Hz}]$$
   *(với $T_w = \frac{L}{F_s}$ là thời lượng quan sát thời gian của khung tín hiệu)*.

7. **Phổ biên độ tuyến tính và phổ biên độ logarit (dB):**
   $$|X[k]| = \sqrt{\text{Re}^2\{X[k]\} + \text{Im}^2\{X[k]\}}$$
   $$|X[k]|_{\text{dB}} = 20 \log_{10}\big(\max(|X[k]|, \, 10^{-12})\big) \quad [\text{dB}]$$

---

### 3. Bảng số liệu đo đạc thực tế

#### 3.1. Tọa độ các đỉnh phổ nổi bật ($N_{\text{FFT}} = 65536$, phân đoạn $1.0\text{ s}$)

* **Bảng 3.1a: Các đỉnh phổ đặc trưng của Âm nhạc (Piano - Phân đoạn $[11.0\text{s} - 12.0\text{s}]$, $L = 48{,}000$, $\Delta f = 0.7324\text{ Hz}$)**

| Thứ tự đỉnh | Chỉ số Bin ($k$) | Tần số đo ($f_k$) | Biên độ tuyến tính ($|X|$) | Biên độ logarit ($20\log_{10}|X|$) | Nốt nhạc tham chiếu | Tần số lý thuyết ($f_{\text{ref}}$) | Sai số $\Delta f$ | Đặc trưng âm học |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| **Đỉnh 1** | $118$ | $86.43\text{ Hz}$ | $387.98$ | $51.78\text{ dB}$ | Nốt F2 | $87.31\text{ Hz}$ | $0.88\text{ Hz}$ | Họa âm cơ bản nốt F2 |
| **Đỉnh 2** | $177$ | $129.64\text{ Hz}$ | $427.04$ | $52.61\text{ dB}$ | Nốt C3 | $130.81\text{ Hz}$ | $1.17\text{ Hz}$ | Họa âm nốt C3 (quãng năm F2) |
| **Đỉnh 3** | $238$ | $174.32\text{ Hz}$ | $257.21$ | $48.21\text{ dB}$ | Nốt F3 | $174.61\text{ Hz}$ | $0.29\text{ Hz}$ | Họa âm nốt F3 (quãng tám F2) |
| **Đỉnh 4** | $853$ | $624.76\text{ Hz}$ | $303.52$ | $49.64\text{ dB}$ | Nốt D#5 / Eb5 | $622.25\text{ Hz}$ | $2.51\text{ Hz}$ | Họa âm bậc cao ngân vang |
| **Đỉnh 5** | $1016$ | $744.14\text{ Hz}$ | $321.23$ | $50.14\text{ dB}$ | Nốt F#5 / Gb5 | $739.99\text{ Hz}$ | $4.15\text{ Hz}$ | Họa âm bậc cao nốt F#5 |

* **Bảng 3.1b: Các đỉnh phổ đặc trưng của Tiếng nói (Speech - Phân đoạn $[13.0\text{s} - 14.0\text{s}]$, $L = 48{,}000$, $\Delta f = 0.7324\text{ Hz}$)**

| Thứ tự đỉnh | Chỉ số Bin ($k$) | Tần số đo ($f_k$) | Biên độ tuyến tính ($|X|$) | Biên độ logarit ($20\log_{10}|X|$) | Thành phần âm ngữ tương ứng | Phân tích cơ chế phát âm |
| :---: | :---: | :---: | :---: | :---: | :--- | :--- |
| **Đỉnh 1** | $75$ | $54.93\text{ Hz}$ | $1{,}824.75$ | $65.22\text{ dB}$ | Dải siêu trầm (Sub-bass) | Năng lượng cộng hưởng buồng họng và rung lồng ngực |
| **Đỉnh 2** | $149$ | $109.13\text{ Hz}$ | $638.64$ | $56.11\text{ dB}$ | Tần số cơ bản thanh môn $F_0$ (Pitch) | Tần số rung cơ bản của dây thanh quản (nam giới $100-120\text{ Hz}$) |
| **Đỉnh 3** | $226$ | $165.53\text{ Hz}$ | $374.87$ | $51.48\text{ dB}$ | Họa âm bậc cao thanh môn ($1.5 \sim 2 F_0$) | Dao động bậc hài của chuỗi xung khí thanh môn |
| **Đỉnh 4** | $356$ | $260.74\text{ Hz}$ | $453.99$ | $53.14\text{ dB}$ | Dải chuyển tiếp formant trầm | Chuyển tiếp âm sắc giữa thanh quản và khoang miệng |
| **Đỉnh 5** | $400$ | $292.97\text{ Hz}$ | $495.19$ | $53.90\text{ dB}$ | Formant thứ nhất $F_1$ của nguyên âm | Đỉnh cộng hưởng âm học của khoang miệng khi phát âm nguyên âm |

---

#### 3.2. So sánh định lượng và kiểm chứng công thức 2 cấu hình $N_{\text{FFT}}$

| Tham số khảo sát | Công thức lý thuyết | Khung ngắn gốc ($L=2048$, $N_{\text{FFT}}=2048$) | Khung ngắn Zero-padding ($L=2048$, $N_{\text{FFT}}=65536$) | Phân đoạn chuẩn ($L=48000$, $N_{\text{FFT}}=65536$) | Ý nghĩa kỹ thuật & Bản chất vật lý |
| :--- | :---: | :---: | :---: | :---: | :--- |
| **Độ dài khung tín hiệu ($L$)** | $L = T_w \times F_s$ | $2{,}048$ mẫu ($42.67\text{ ms}$) | $2{,}048$ mẫu ($42.67\text{ ms}$) | $48{,}000$ mẫu ($1.000\text{ s}$) | Chiều dài cửa sổ thời gian quan sát tín hiệu |
| **Kích thước biến đổi FFT ($N_{\text{FFT}}$)** | Lũy thừa của 2 ($2^M$) | $2{,}048$ | $65{,}536$ | $65{,}536$ | Số điểm tính toán của thuật toán FFT |
| **Số mẫu đệm số 0 (Zero-padding)** | $N_{\text{FFT}} - L$ | $0$ mẫu | $63{,}488$ mẫu | $17{,}536$ mẫu | Thêm các mẫu 0 vào cuối mảng để tăng mật độ tính toán |
| **Khoảng cách bin tần số ($\Delta f$)** | $\Delta f = \frac{F_s}{N_{\text{FFT}}}$ | $\frac{48000}{2048} = 23.4375\text{ Hz}$ | $\frac{48000}{65536} \approx 0.7324\text{ Hz}$ | $\frac{48000}{65536} \approx 0.7324\text{ Hz}$ | Lưới lấy mẫu phổ; Zero-padding làm dày lưới gấp 32 lần |
| **Số điểm phổ thực tế (RFFT)** | $K = \frac{N_{\text{FFT}}}{2} + 1$ | $1{,}025$ điểm | $32{,}769$ điểm | $32{,}769$ điểm | Số bin tần số trong dải tần Nyquist $[0, 24000\text{ Hz}]$ |
| **Độ phân giải vật lý thực ($\Delta f_{\text{phys}}$)** | $\Delta f_{\text{phys}} \approx \frac{F_s}{L} = \frac{1}{T_w}$ | $23.4375\text{ Hz}$ | **$23.4375\text{ Hz}$ (Không đổi!)** | **$1.0000\text{ Hz}$ (Tăng $23.4$ lần)** | Khả năng phân tách 2 tần số gần nhau phụ thuộc hoàn toàn vào $L$ ($T_w$) |
| **Đặc trưng dạng phổ quan sát** | Trực quan trên đồ thị | Lưới tần số thưa, đỉnh phổ nhọn gấp khúc thô | Đường phổ trơn mượt, các điểm $N_{\text{FFT}}=2048$ nằm trên đường nội suy | Đường phổ vừa trơn mượt, vừa tách biệt các vạch họa âm sát nhau |

---

### 4. Đồ thị trực quan phổ tần số FFT

#### 4.1. Phổ FFT tệp Âm nhạc (Piano)
![Phổ FFT Piano](../figures/fft_piano.png)

*Hình C.1: Phân tích phổ FFT đoạn Piano [11.0s - 12.0s]. Hàng 1: Phổ tuyến tính; Hàng 2: Phổ logarit dB đánh dấu 5 đỉnh phổ chính; Hàng 3: So sánh chi tiết dải hẹp 50 - 600 Hz giữa N_FFT = 2048 (điểm rời rạc) và N_FFT = 65536 (nội suy mượt).*

#### 4.2. Phổ FFT tệp Tiếng nói (Speech)
![Phổ FFT Speech](../figures/fft_speech.png)

*Hình C.2: Phân tích phổ FFT đoạn Tiếng nói [13.0s - 14.0s]. Hàng 1: Phổ tuyến tính; Hàng 2: Phổ logarit dB đánh dấu 5 đỉnh phổ chính; Hàng 3: So sánh chi tiết dải hẹp 50 - 600 Hz giữa N_FFT = 2048 và N_FFT = 65536.*

---

### 5. Nhận xét kỹ thuật Khối C

1. **Đặc trưng cấu trúc phổ:**
   * **Piano:** Xuất hiện các đỉnh nhọn rời rạc rất rõ nét với các tần số tương ứng với các nốt nhạc cụ thể trong hợp âm (F2: $86.4\text{ Hz}$, C3: $129.6\text{ Hz}$, F3: $174.3\text{ Hz}$...). Dây đàn buông rung tự do tạo nên phổ hài rõ ràng với độ suy giảm có trật tự.
   * **Tiếng nói:** Tập trung năng lượng chủ yếu ở dải tần thấp dưới $500\text{ Hz}$ với đỉnh thanh môn $F_0 \approx 109\text{ Hz}$ và các formant thấp của nguyên âm hữu thanh.
2. **Vai trò của cửa sổ Hamming:** Cửa sổ Hamming đưa biên độ 2 đầu biên tín hiệu về 0 êm đềm, triệt tiêu sự gián đoạn chu kỳ giả mạo khi tính DFT, làm giảm búp sóng phụ xuống dưới $-40\text{ dB}$ và hạn chế tối đa hiện tượng rò rỉ phổ (spectral leakage).
3. **Bản chất Zero-padding và độ phân giải phổ:**
   * Tăng $N_{\text{FFT}}$ từ $2048$ lên $65536$ chỉ thu hẹp khoảng cách bin tần số $\Delta f = F_s / N_{\text{FFT}}$ từ $23.44\text{ Hz}$ xuống $0.73\text{ Hz}$, đóng vai trò như phép nội suy sinc trong miền tần số để vẽ đường cong phổ mượt mà hơn (các điểm $N_{\text{FFT}}=2048$ nằm chính xác trên đường cong $N_{\text{FFT}}=65536$).
   * Zero-padding **không làm tăng độ phân giải vật lý thực sự**. Khả năng phân tách 2 tần số vật lý sát nhau phụ thuộc hoàn toàn vào chiều dài cửa sổ thời gian ($\Delta f_{\text{phys}} \approx 1/L$).
