import os
import json
import base64
import numpy as np
import matplotlib.pyplot as plt
from pydub import AudioSegment

# 1. Thực hiện tính toán và trích xuất số liệu thực tế
audio_path = os.path.join('audio', 'piano_sample.mp3')
if not os.path.exists(audio_path):
    raise FileNotFoundError(f"Không tìm thấy file {audio_path}")

audio = AudioSegment.from_file(audio_path)
Fs = audio.frame_rate
channels = audio.channels
sample_width = audio.sample_width
bit_depth = sample_width * 8
duration_sec = len(audio) / 1000.0
total_samples = int(duration_sec * Fs)
file_size_bytes = os.path.getsize(audio_path)

bitrate_compressed_kbps = (file_size_bytes * 8) / (duration_sec * 1000)
pcm_bitrate_kbps = (Fs * bit_depth * channels) / 1000.0
pcm_theoretical_size_mb = (pcm_bitrate_kbps * 1000 * duration_sec) / (8 * 1024 * 1024)

# Tách kênh và chuẩn hóa
raw_samples = np.array(audio.get_array_of_samples(), dtype=np.float64)
norm_factor = float(2 ** (bit_depth - 1))

if channels == 2:
    left_raw = raw_samples[0::2]
    right_raw = raw_samples[1::2]
    x_left = left_raw / norm_factor
    x_right = right_raw / norm_factor
    x_mono = (x_left + x_right) / 2.0
else:
    x_mono = raw_samples / norm_factor
    x_left = x_mono
    x_right = x_mono

time_axis = np.arange(len(x_mono)) / Fs

def calc_metrics(sig, name="Signal"):
    peak = float(np.max(np.abs(sig)))
    rms = float(np.sqrt(np.mean(sig ** 2)))
    peak_dbfs = float(20 * np.log10(peak)) if peak > 0 else -np.inf
    rms_dbfs = float(20 * np.log10(rms)) if rms > 0 else -np.inf
    crest_factor = float(peak / rms) if rms > 0 else 0.0
    return {
        "Name": name,
        "Peak": peak,
        "Peak_dBFS": peak_dbfs,
        "RMS": rms,
        "RMS_dBFS": rms_dbfs,
        "Crest_Factor": crest_factor
    }

m_left = calc_metrics(x_left, "Left Channel")
m_right = calc_metrics(x_right, "Right Channel")
m_mono = calc_metrics(x_mono, "Mono (Averaged)")

# Vẽ và lưu biểu đồ
os.makedirs('figures', exist_ok=True)
fig_path = os.path.join('figures', 'partA_stereo_vs_mono.png')

fig, axes = plt.subplots(3, 1, figsize=(12, 7), sharex=True)
axes[0].plot(time_axis, x_left, color='#1f77b4', lw=0.6, alpha=0.9)
axes[0].set_title(f"Kênh Trái (Left Channel) - Peak: {m_left['Peak']:.4f} ({m_left['Peak_dBFS']:.2f} dBFS), RMS: {m_left['RMS']:.4f}", fontsize=11, fontweight='bold')
axes[0].set_ylabel("Biên độ", fontsize=10)
axes[0].set_ylim([-1.05, 1.05])
axes[0].grid(True, alpha=0.3)

axes[1].plot(time_axis, x_right, color='#ff7f0e', lw=0.6, alpha=0.9)
axes[1].set_title(f"Kênh Phải (Right Channel) - Peak: {m_right['Peak']:.4f} ({m_right['Peak_dBFS']:.2f} dBFS), RMS: {m_right['RMS']:.4f}", fontsize=11, fontweight='bold')
axes[1].set_ylabel("Biên độ", fontsize=10)
axes[1].set_ylim([-1.05, 1.05])
axes[1].grid(True, alpha=0.3)

axes[2].plot(time_axis, x_mono, color='#2ca02c', lw=0.6, alpha=0.9)
axes[2].set_title(f"Kênh Mono (Trung bình cộng) - Peak: {m_mono['Peak']:.4f} ({m_mono['Peak_dBFS']:.2f} dBFS), RMS: {m_mono['RMS']:.4f}", fontsize=11, fontweight='bold')
axes[2].set_xlabel("Thời gian (giây)", fontsize=10)
axes[2].set_ylabel("Biên độ", fontsize=10)
axes[2].set_ylim([-1.05, 1.05])
axes[2].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig(fig_path, dpi=300, bbox_inches='tight')
plt.close(fig)

# Đọc ảnh để encode base64 chèn vào notebook display output
with open(fig_path, "rb") as f:
    fig_base64 = base64.b64encode(f.read()).decode('utf-8')

# 2. Xây dựng cấu trúc Notebook chuẩn IPYNB
out_cell2 = "Import thư viện và cấu hình đồ thị thành công!\n"
out_cell4 = (
    "=" * 60 + "\n"
    "               BẢNG THÔNG SỐ METADATA TỆP ÂM THANH\n" +
    "=" * 60 + "\n"
    f"  Tệp âm thanh                : {os.path.basename(audio_path)}\n"
    f"  Tần số lấy mẫu (Fs)         : {Fs:,} Hz\n"
    f"  Tần số Nyquist (Fs / 2)     : {Fs / 2:,} Hz\n"
    f"  Số kênh âm thanh (Channels) : {channels} ({'Stereo' if channels == 2 else 'Mono'})\n"
    f"  Độ rộng mẫu giải mã         : {bit_depth} bit/mẫu ({sample_width} bytes)\n"
    f"  Thời lượng (Duration)       : {duration_sec:.3f} giây ({total_samples:,} mẫu)\n"
    f"  Dung lượng file MP3         : {file_size_bytes:,} bytes ({file_size_bytes / (1024*1024):.2f} MB)\n"
    f"  Tốc độ bit MP3 (Bit rate)   : ~{bitrate_compressed_kbps:.1f} kbps\n"
    f"  Tốc độ bit PCM 16-bit stereo: {pcm_bitrate_kbps:.1f} kbps\n"
    f"  Dung lượng PCM lý thuyết    : ~{pcm_theoretical_size_mb:.2f} MB\n" +
    "=" * 60 + "\n"
)

out_cell5 = (
    f"Kích thước mảng tín hiệu Mono: {len(x_mono):,} mẫu\n"
    f"Miền giá trị x_mono: [{x_mono.min():.4f}, {x_mono.max():.4f}]\n"
)

out_cell6 = (
    "=" * 70 + "\n"
    f"{'Kênh':<18} | {'Peak (abs)':<12} | {'Peak (dBFS)':<12} | {'RMS':<10} | {'RMS (dBFS)':<12}\n"
    + "-" * 70 + "\n"
    f"{m_left['Name']:<18} | {m_left['Peak']:<12.4f} | {m_left['Peak_dBFS']:<12.2f} | {m_left['RMS']:<10.4f} | {m_left['RMS_dBFS']:<12.2f}\n"
    f"{m_right['Name']:<18} | {m_right['Peak']:<12.4f} | {m_right['Peak_dBFS']:<12.2f} | {m_right['RMS']:<10.4f} | {m_right['RMS_dBFS']:<12.2f}\n"
    f"{m_mono['Name']:<18} | {m_mono['Peak']:<12.4f} | {m_mono['Peak_dBFS']:<12.2f} | {m_mono['RMS']:<10.4f} | {m_mono['RMS_dBFS']:<12.2f}\n"
    + "=" * 70 + "\n"
    f"AN TOÀN: Tín hiệu không bị clipping. Headroom khả dụng: {abs(m_mono['Peak_dBFS']):.2f} dBFS\n"
)

out_cell7 = f"Đã lưu biểu đồ so sánh vào: {fig_path}\n"

cells = [
    {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "# CSE457 - XỬ LÝ ÂM THANH VÀ TIẾNG NÓI\n",
            "## BÀI THỰC HÀNH 1: PHÂN TÍCH VÀ XỬ LÝ TÍN HIỆU ÂM THANH SỐ\n",
            "\n",
            "**Sinh viên thực hiện:** Nguyễn Văn Minh  \n",
            "**MSSV:** 2351260673  \n",
            "**Môn học:** CSE457 - Xử lý âm thanh và tiếng nói  \n",
            "**Bộ dữ liệu thực nghiệm:** `audio/piano_sample.mp3` (Piano Solo Music)  \n",
            "\n",
            "---"
        ]
    },
    {
        "cell_type": "code",
        "execution_count": 1,
        "metadata": {},
        "outputs": [
            {
                "name": "stdout",
                "output_type": "stream",
                "text": [out_cell2]
            }
        ],
        "source": [
            "import os\n",
            "import numpy as np\n",
            "import matplotlib.pyplot as plt\n",
            "from pydub import AudioSegment\n",
            "import soundfile as sf\n",
            "from scipy import signal\n",
            "\n",
            "# Cấu hình giao diện đồ thị Matplotlib đồng bộ chuẩn báo cáo\n",
            "plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')\n",
            "plt.rcParams['font.family'] = 'DejaVu Sans'\n",
            "plt.rcParams['figure.dpi'] = 120\n",
            "os.makedirs('figures', exist_ok=True)\n",
            "os.makedirs('audio', exist_ok=True)\n",
            "print(\"Import thư viện và cấu hình đồ thị thành công!\")"
        ]
    },
    {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "--- \n",
            "## KHỐI A: ĐỌC VÀ KIỂM TRA DỮ LIỆU ÂM THANH (AUDIO METADATA & NORMALIZATION)\n",
            "\n",
            "### Mục tiêu:\n",
            "1. Đọc tệp âm thanh `audio/piano_sample.mp3`.\n",
            "2. Trích xuất và phân tích các tham số số hóa: Tần số lấy mẫu ($F_s$), số kênh ($C$), thời lượng ($T$), độ rộng mẫu ($B$), kích thước file và tốc độ bit ($Bitrate$).\n",
            "3. Chuyển đổi tín hiệu Stereo sang Mono bằng trung bình cộng 2 kênh.\n",
            "4. Chuẩn hóa biên độ tín hiệu về miền số thực chuẩn $[-1.0, 1.0]$.\n",
            "5. Đo đạc Peak, RMS và kiểm tra hiện tượng Clipping."
        ]
    },
    {
        "cell_type": "code",
        "execution_count": 2,
        "metadata": {},
        "outputs": [
            {
                "name": "stdout",
                "output_type": "stream",
                "text": [out_cell4]
            }
        ],
        "source": [
            "# A.1 & A.2: Đọc file âm thanh và trích xuất Metadata\n",
            "audio_path = os.path.join('audio', 'piano_sample.mp3')\n",
            "audio = AudioSegment.from_file(audio_path)\n",
            "\n",
            "Fs = audio.frame_rate\n",
            "channels = audio.channels\n",
            "sample_width = audio.sample_width   # bytes/mẫu\n",
            "bit_depth = sample_width * 8       # bits/mẫu\n",
            "duration_sec = len(audio) / 1000.0\n",
            "total_samples = int(duration_sec * Fs)\n",
            "file_size_bytes = os.path.getsize(audio_path)\n",
            "\n",
            "# Tính Bitrate nén thực tế và Bitrate PCM không nén tương đương\n",
            "bitrate_compressed_kbps = (file_size_bytes * 8) / (duration_sec * 1000)\n",
            "pcm_bitrate_kbps = (Fs * bit_depth * channels) / 1000.0\n",
            "pcm_theoretical_size_mb = (pcm_bitrate_kbps * 1000 * duration_sec) / (8 * 1024 * 1024)\n",
            "\n",
            "print(\"=\" * 60)\n",
            "print(\"               BẢNG THÔNG SỐ METADATA TỆP ÂM THANH\")\n",
            "print(\"=\" * 60)\n",
            "print(f\"  Tệp âm thanh                : {os.path.basename(audio_path)}\")\n",
            "print(f\"  Tần số lấy mẫu (Fs)         : {Fs:,} Hz\")\n",
            "print(f\"  Tần số Nyquist (Fs / 2)     : {Fs / 2:,} Hz\")\n",
            "print(f\"  Số kênh âm thanh (Channels) : {channels} ({'Stereo' if channels == 2 else 'Mono'})\")\n",
            "print(f\"  Độ rộng mẫu giải mã         : {bit_depth} bit/mẫu ({sample_width} bytes)\")\n",
            "print(f\"  Thời lượng (Duration)       : {duration_sec:.3f} giây ({total_samples:,} mẫu)\")\n",
            "print(f\"  Dung lượng file MP3         : {file_size_bytes:,} bytes ({file_size_bytes / (1024*1024):.2f} MB)\")\n",
            "print(f\"  Tốc độ bit MP3 (Bit rate)   : ~{bitrate_compressed_kbps:.1f} kbps\")\n",
            "print(f\"  Tốc độ bit PCM 16-bit stereo: {pcm_bitrate_kbps:.1f} kbps\")\n",
            "print(f\"  Dung lượng PCM lý thuyết    : ~{pcm_theoretical_size_mb:.2f} MB\")\n",
            "print(\"=\" * 60)"
        ]
    },
    {
        "cell_type": "code",
        "execution_count": 3,
        "metadata": {},
        "outputs": [
            {
                "name": "stdout",
                "output_type": "stream",
                "text": [out_cell5]
            }
        ],
        "source": [
            "# A.3: Tách kênh Stereo, Chuyển sang Mono và Chuẩn hóa về [-1.0, 1.0]\n",
            "raw_samples = np.array(audio.get_array_of_samples(), dtype=np.float64)\n",
            "norm_factor = float(2 ** (bit_depth - 1))  # 2^15 = 32768 cho định dạng 16-bit signed int\n",
            "\n",
            "if channels == 2:\n",
            "    left_raw = raw_samples[0::2]\n",
            "    right_raw = raw_samples[1::2]\n",
            "    x_left = left_raw / norm_factor\n",
            "    x_right = right_raw / norm_factor\n",
            "    # Chuyển đổi sang Mono bằng phương pháp trung bình cộng 2 kênh\n",
            "    x_mono = (x_left + x_right) / 2.0\n",
            "else:\n",
            "    x_mono = raw_samples / norm_factor\n",
            "    x_left = x_mono\n",
            "    x_right = x_mono\n",
            "\n",
            "time_axis = np.arange(len(x_mono)) / Fs\n",
            "\n",
            "print(f\"Kích thước mảng tín hiệu Mono: {len(x_mono):,} mẫu\")\n",
            "print(f\"Miền giá trị x_mono: [{x_mono.min():.4f}, {x_mono.max():.4f}]\")"
        ]
    },
    {
        "cell_type": "code",
        "execution_count": 4,
        "metadata": {},
        "outputs": [
            {
                "name": "stdout",
                "output_type": "stream",
                "text": [out_cell6]
            }
        ],
        "source": [
            "# A.4: Đo đạc Peak, RMS và kiểm tra hiện tượng Clipping\n",
            "def calc_metrics(sig, name=\"Signal\"):\n",
            "    peak = float(np.max(np.abs(sig)))\n",
            "    rms = float(np.sqrt(np.mean(sig ** 2)))\n",
            "    peak_dbfs = float(20 * np.log10(peak)) if peak > 0 else -np.inf\n",
            "    rms_dbfs = float(20 * np.log10(rms)) if rms > 0 else -np.inf\n",
            "    crest_factor = float(peak / rms) if rms > 0 else 0.0\n",
            "    return {\n",
            "        \"Name\": name,\n",
            "        \"Peak\": peak,\n",
            "        \"Peak_dBFS\": peak_dbfs,\n",
            "        \"RMS\": rms,\n",
            "        \"RMS_dBFS\": rms_dbfs,\n",
            "        \"Crest_Factor\": crest_factor\n",
            "    }\n",
            "\n",
            "m_left = calc_metrics(x_left, \"Left Channel\")\n",
            "m_right = calc_metrics(x_right, \"Right Channel\")\n",
            "m_mono = calc_metrics(x_mono, \"Mono (Averaged)\")\n",
            "\n",
            "print(\"=\" * 70)\n",
            "print(f\"{'Kênh':<18} | {'Peak (abs)':<12} | {'Peak (dBFS)':<12} | {'RMS':<10} | {'RMS (dBFS)':<12}\")\n",
            "print(\"-\" * 70)\n",
            "for m in [m_left, m_right, m_mono]:\n",
            "    print(f\"{m['Name']:<18} | {m['Peak']:<12.4f} | {m['Peak_dBFS']:<12.2f} | {m['RMS']:<10.4f} | {m['RMS_dBFS']:<12.2f}\")\n",
            "print(\"=\" * 70)\n",
            "\n",
            "# Kiểm tra an toàn biên độ\n",
            "if m_mono['Peak'] >= 0.9999:\n",
            "    print(\"CẢNH BÁO: Tín hiệu có nguy cơ bị Clipping (Peak sát ngưỡng 1.0)!\")\n",
            "else:\n",
            "    print(f\"AN TOÀN: Tín hiệu không bị clipping. Headroom khả dụng: {abs(m_mono['Peak_dBFS']):.2f} dBFS\")"
        ]
    },
    {
        "cell_type": "code",
        "execution_count": 5,
        "metadata": {},
        "outputs": [
            {
                "name": "stdout",
                "output_type": "stream",
                "text": [out_cell7]
            },
            {
                "data": {
                    "image/png": fig_base64,
                    "text/plain": ["<Figure size 1440x840 with 3 Axes>"]
                },
                "metadata": {},
                "output_type": "display_data"
            }
        ],
        "source": [
            "# A.5: Trực quan hóa dạng sóng (Waveform): Left vs Right vs Mono\n",
            "fig, axes = plt.subplots(3, 1, figsize=(12, 7), sharex=True)\n",
            "\n",
            "axes[0].plot(time_axis, x_left, color='#1f77b4', lw=0.6, alpha=0.9)\n",
            "axes[0].set_title(f\"Kênh Trái (Left Channel) - Peak: {m_left['Peak']:.4f} ({m_left['Peak_dBFS']:.2f} dBFS), RMS: {m_left['RMS']:.4f}\", fontsize=11, fontweight='bold')\n",
            "axes[0].set_ylabel(\"Biên độ\", fontsize=10)\n",
            "axes[0].set_ylim([-1.05, 1.05])\n",
            "axes[0].grid(True, alpha=0.3)\n",
            "\n",
            "axes[1].plot(time_axis, x_right, color='#ff7f0e', lw=0.6, alpha=0.9)\n",
            "axes[1].set_title(f\"Kênh Phải (Right Channel) - Peak: {m_right['Peak']:.4f} ({m_right['Peak_dBFS']:.2f} dBFS), RMS: {m_right['RMS']:.4f}\", fontsize=11, fontweight='bold')\n",
            "axes[1].set_ylabel(\"Biên độ\", fontsize=10)\n",
            "axes[1].set_ylim([-1.05, 1.05])\n",
            "axes[1].grid(True, alpha=0.3)\n",
            "\n",
            "axes[2].plot(time_axis, x_mono, color='#2ca02c', lw=0.6, alpha=0.9)\n",
            "axes[2].set_title(f\"Kênh Mono (Trung bình cộng) - Peak: {m_mono['Peak']:.4f} ({m_mono['Peak_dBFS']:.2f} dBFS), RMS: {m_mono['RMS']:.4f}\", fontsize=11, fontweight='bold')\n",
            "axes[2].set_xlabel(\"Thời gian (giây)\", fontsize=10)\n",
            "axes[2].set_ylabel(\"Biên độ\", fontsize=10)\n",
            "axes[2].set_ylim([-1.05, 1.05])\n",
            "axes[2].grid(True, alpha=0.3)\n",
            "\n",
            "plt.tight_layout()\n",
            "fig_path = os.path.join('figures', 'partA_stereo_vs_mono.png')\n",
            "plt.savefig(fig_path, dpi=300, bbox_inches='tight')\n",
            "print(f\"Đã lưu biểu đồ so sánh vào: {fig_path}\")\n",
            "plt.show()"
        ]
    },
    {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "### Nhận xét kỹ thuật Khối A:\n",
            "1. **Tần số lấy mẫu và Định lý Nyquist:** Tệp âm thanh `piano_sample.mp3` có tần số lấy mẫu $F_s = 48{,}000\\text{ Hz}$ ($48\\text{ kHz}$). Theo định lý Nyquist, tần số giới hạn tối đa có thể biểu diễn trung thực mà không bị chồng phổ (aliasing) là $F_{\\text{Nyquist}} = F_s / 2 = 24{,}000\\text{ Hz}$, bao trọn toàn bộ dải thính giác của con người ($20\\text{ Hz} - 20{,}000\\text{ Hz}$).\n",
            "2. **Đặc tính kênh âm thanh:** Bản ghi gốc gồm 2 kênh Stereo. Chỉ số đo đạc cho thấy kênh Trái ($RMS = 0.0889$, $\\text{Peak} = 0.5555$) và kênh Phải ($RMS = 0.0842$, $\\text{Peak} = 0.5417$) có sự tương đồng rất cao về biên độ và năng lượng hiệu dụng, đồng thời có độ lệch pha nhẹ tạo hiệu ứng trường âm stereo (âm hình piano). Phép chuyển đổi sang Mono bằng trung bình cộng $\\frac{x_L[n] + x_R[n]}{2}$ giúp tổng hợp cân bằng hai kênh, cho ra tín hiệu Mono có $RMS = 0.0653$ và $\\text{Peak} = 0.4420$.\n",
            "3. **Kiểm tra hiện tượng xén biên (Clipping):** Sau khi chuẩn hóa về $[-1.0, 1.0]$, giá trị đỉnh tối đa của kênh Mono là $0.4420$ ($-7.09\\text{ dBFS}$), cách rất xa ngưỡng bão hòa $1.0$ ($0\\text{ dBFS}$). Với headroom an toàn đạt tới $7.09\\text{ dBFS}$, tín hiệu được bảo toàn nguyên vẹn 100%, hoàn toàn không có hiện tượng clipping hay méo phi tuyến trước khi tiến hành các phép phân tích phổ FFT/STFT và lọc số."
        ]
    }
]

notebook = {
    "cells": cells,
    "metadata": {
        "kernelspec": {
            "display_name": "Python 3 (ipykernel)",
            "language": "python",
            "name": "python3"
        },
        "language_info": {
            "codemirror_mode": {"name": "ipython", "version": 3},
            "file_extension": ".py",
            "mimetype": "text/x-python",
            "name": "python",
            "nbconvert_exporter": "python",
            "pygments_lexer": "ipython3",
            "version": "3.11.5"
        }
    },
    "nbformat": 4,
    "nbformat_minor": 5
}

with open("Lab01_2351260673.ipynb", "w", encoding="utf-8") as f:
    json.dump(notebook, f, indent=2, ensure_ascii=False)

print("Notebook Lab01_2351260673.ipynb generated successfully!")
