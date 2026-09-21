# CSE457 - Xử lý âm thanh và tiếng nói
## Lab 1: Phân tích và xử lý tín hiệu âm thanh số

* **Sinh viên:** Nguyễn Văn Minh
* **Mã số sinh viên (MSSV):** 2351260673
* **Cơ sở đào tạo:** Trường Đại học Thủy lợi

---

### Cấu trúc dự án

```text
Lab01_2351260673_NguyenVanMinh/
├── .venv/                              # Môi trường ảo Python
├── audio/                              # Thư mục chứa dữ liệu âm thanh
│   ├── piano_sample.mp3                # Dữ liệu âm nhạc Piano thực nghiệm (Khối A)
│   ├── filtered_*.wav                  # Âm thanh sau lọc (Khối F - Đang cập nhật)
│   └── quantized_*.wav                 # Âm thanh sau lượng tử hóa (Khối G - Đang cập nhật)
├── figures/                            # Thư mục lưu đồ thị trích xuất
│   └── partA_stereo_vs_mono.png        # Đồ thị so sánh dạng sóng Stereo vs Mono
├── Lab01_2351260673.ipynb              # Jupyter Notebook thực hành toàn bộ bài Lab
├── report_2351260673.md                # Báo cáo kỹ thuật chi tiết
├── Lab_01_CSE457_Xu_Ly_Am_Thanh_Va_Tieng_Noi.md # Đề cương & hướng dẫn Lab
└── README.md                           # Hướng dẫn dự án
```

---

### Hướng dẫn cài đặt và chạy môi trường

1. **Kích hoạt môi trường ảo:**
   ```powershell
   .\.venv\Scripts\Activate.ps1
   ```

2. **Các thư viện chính đã cài đặt:**
   * `numpy` (Tính toán số học ma trận)
   * `scipy` (Xử lý tín hiệu, lọc số, biến đổi Fourier)
   * `matplotlib` (Vẽ đồ thị và trực quan hóa)
   * `pydub` (Đọc và giải mã đa định dạng âm thanh)
   * `soundfile` (Đọc, ghi tệp âm thanh WAV PCM)
   * `ipykernel` (Kernel thực thi cho Jupyter Notebook)

3. **Chạy Jupyter Notebook:**
   * Mở file [Lab01_2351260673.ipynb](Lab01_2351260673.ipynb) trong VS Code hoặc khởi chạy Jupyter Server:
   ```powershell
   jupyter notebook Lab01_2351260673.ipynb
   ```

---

### Tiến độ thực hiện các khối nhiệm vụ

- [x] **Khối A: Đọc và kiểm tra dữ liệu âm thanh** (Hoàn thành: Trích xuất metadata, Stereo sang Mono, chuẩn hóa $[-1.0, 1.0]$, đo Peak/RMS, lưu đồ thị sóng).
- [ ] **Khối B: Phân tích miền thời gian** (Waveform zoom ngắn, Energy, so sánh 2 đoạn đặc trưng).
- [ ] **Khối C: Phân tích miền tần số bằng FFT** (Magnitude spectrum, spectral peaks, phân tích $N_{\text{FFT}}$ và $\Delta f$).
- [ ] **Khối D: STFT và Spectrogram** (Trade-off thời gian - tần số, khảo sát 10ms, 25ms, 50ms).
- [ ] **Khối E: Thí nghiệm Cửa sổ (Windowing)** (Rectangular vs. Hamming, rò rỉ phổ).
- [ ] **Khối F: Thiết kế và Lọc số FIR** (Low-pass, High-pass/Band-pass, đáp ứng tần số $|H(f)|$, group delay).
- [ ] **Khối G: Lượng tử hóa, Resampling và Mã hóa** (SNR thực nghiệm 4/8/16-bit, Resample 16kHz/8kHz, Compression ratio).
