"""配置文件 — 修改这里的参数以适配你的环境"""

import os

# ============ Claude API ============
CLAUDE_API_KEY = os.environ.get("ANTHROPIC_API_KEY", "tp-c6374m1pvvb8mx181sqhjfoawnaylxndzf4mj6uovuc4q461")
CLAUDE_MODEL = "mimo-v2.5-pro"

# ============ Whisper 语音识别 ============
WHISPER_MODEL = "base"          # 先用 base 测试，稳定后可改回 medium
WHISPER_DEVICE = "cuda"         # 用 GPU 加速
WHISPER_COMPUTE_TYPE = "float16"  # GPU 用 float16
WHISPER_LANGUAGE = "zh"         # 中文

# ============ 音频采集 ============
SAMPLE_RATE = 16000             # 采样率
CHANNELS = 1                    # 单声道
BLOCK_SIZE = 4096               # 每次采集的帧数
# VB-Cable 设备号，运行 python -m sounddevice 查看后修改
# 一般 VB-Cable Output 的设备名包含 "CABLE" 字样
VB_CABLE_DEVICE = None          # None = 自动查找包含 "CABLE" 的设备

# ============ 问题检测 ============
QUESTION_KEYWORDS = [
    "吗", "呢", "怎么", "为什么", "什么", "哪个", "哪些",
    "多少", "几", "是否", "能否", "可以", "会不会",
    "什么意思", "如何", "怎样", "怎么样", "看法",
]
QUESTION_PUNCTUATION = ["？", "?"]

# ============ UI ============
WINDOW_WIDTH = 650
WINDOW_HEIGHT = 850
# 窗口位置：默认放在第二屏 (假设主屏在左，第二屏在右)
# 如果你的第二屏在左边，改成负数，如 -WINDOW_WIDTH - 100
WINDOW_X = 100
WINDOW_Y = 100

# ============ 材料目录 ============
MATERIALS_DIR = os.path.join(os.path.dirname(__file__), "materials")
