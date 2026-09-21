# CSE457 - Xử lý âm thanh và tiếng nói
## Lab 1: Phân tích và xử lý tín hiệu âm thanh số

* **Họ và tên:** Nguyễn Văn Minh
* **Mã số sinh viên (MSSV):** 2351260673
* **Cơ sở đào tạo:** Trường Đại học Thủy lợi

---

### Cấu trúc thư mục dự án

```text
Lab01_2351260673_NguyenVanMinh/
├── .venv/                              # Môi trường ảo Python
├── audio/                              # Thư mục dữ liệu âm thanh đầu vào
│   ├── piano_sample.mp3                # Tệp âm nhạc Piano thực nghiệm (Music)
│   ├── news_speech.mp3                 # Tệp tiếng nói Bản tin thời sự (Speech)
│   ├── filtered_*.wav                  # Tệp âm thanh sau lọc (Khối F)
│   └── quantized_*.wav                 # Tệp âm thanh sau lượng tử hóa (Khối G)
├── figures/                            # Thư mục đồ thị thực nghiệm
│   ├── waveform.png                    # Đồ thị dạng sóng chuẩn toàn bài + đoạn zoom (Khối B)
│   ├── fft.png                         # Đồ thị phổ FFT (Khối C)
│   ├── spectrogram.png                 # Đồ thị Spectrogram STFT (Khối D & E)
│   └── filter_response.png             # Đáp ứng tần số bộ lọc (Khối F)
├── reports/                            # Thư mục báo cáo thực hành
│   └── report_Lab01.md                 # Báo cáo kỹ thuật chi tiết
├── Lab01_2351260673.ipynb              # Notebook thực hành toàn bộ bài Lab
└── README.md                           # Giới thiệu và hướng dẫn dự án
```

---

### Hướng dẫn môi trường và thực thi

1. **Môi trường ảo Python:**
   * Sử dụng Python 3.12 với các thư viện: `numpy`, `scipy`, `matplotlib`, `pandas`, `pydub`, `soundfile`, `ipykernel`.

2. **Khởi chạy Notebook:**
   * Mở tệp [Lab01_2351260673.ipynb](Lab01_2351260673.ipynb) trong VS Code hoặc Jupyter Lab và chọn kernel Python từ `.venv` (hoặc `base (Python 3.12)`).

---

### Tiến độ các khối nội dung

- [x] **Khối A: Đọc, kiểm tra dữ liệu và trực quan hóa chuỗi âm thanh ban đầu** (Hoàn thành: Hỗ trợ cả 2 tệp Piano và Giọng nói, chuẩn hóa $[-1.0, 1.0]$, đo đạc Peak/RMS, bảng so sánh `pandas.DataFrame`, trực quan hóa sơ bộ dạng sóng ban đầu).
- [x] **Khối B: Phân tích miền thời gian** (Hoàn thành: Đo đạc Peak, RMS, Energy, phân tích 2 đoạn tương phản năng lượng cao vs. khoảng lặng chênh lệch 25.6 lần, xuất đồ thị chuẩn `figures/waveform.png`).
- [ ] **Khối C: Phân tích miền tần số bằng FFT** (Magnitude spectrum theo Hz và dB, xác định $\ge 3$ đỉnh phổ, khảo sát $N_{\text{FFT}}$ và $\Delta f$).
- [ ] **Khối D: STFT và Spectrogram** (Spectrogram 2D, khảo sát độ dài khung 10ms, 25ms, 50ms, phân tích trade-off thời gian - tần số).
- [ ] **Khối E: Thí nghiệm Cửa sổ (Windowing)** (So sánh Rectangular vs. Hamming, rò rỉ phổ và độ rộng búp sóng chính).
- [ ] **Khối F: Lọc số** (Thiết kế FIR Low-pass và High-pass/Band-pass, đáp ứng $|H(f)|$, group delay, xuất file `filtered_*.wav`).
- [ ] **Khối G: Lượng tử hóa, Resampling và Mã hóa** (Lượng tử hóa 4/8/16-bit, tính SNR thực nghiệm, Resampling 16kHz/8kHz, tính Compression ratio).
