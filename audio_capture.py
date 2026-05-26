"""音频采集模块 — 从 VB-Cable 虚拟声卡捕获腾讯会议音频"""

import queue
import numpy as np
import sounddevice as sd
from config import SAMPLE_RATE, CHANNELS, BLOCK_SIZE, VB_CABLE_DEVICE


def find_vb_cable_device() -> int:
    """自动查找 VB-Cable 设备号"""
    devices = sd.query_devices()
    for i, dev in enumerate(devices):
        name = dev["name"].lower()
        if "cable" in name and dev["max_input_channels"] > 0:
            print(f"[音频] 找到 VB-Cable 设备: [{i}] {dev['name']}")
            return i
    # 如果找不到，列出所有输入设备供用户选择
    print("[音频] 未自动找到 VB-Cable 设备，以下是所有输入设备：")
    for i, dev in enumerate(devices):
        if dev["max_input_channels"] > 0:
            print(f"  [{i}] {dev['name']}")
    raise RuntimeError("请在 config.py 中手动设置 VB_CABLE_DEVICE 为正确的设备号")


def start_audio_capture(audio_queue: queue.Queue) -> sd.InputStream:
    """启动音频采集，数据放入 audio_queue"""
    device = VB_CABLE_DEVICE if VB_CABLE_DEVICE is not None else find_vb_cable_device()

    def callback(indata, frames, time_info, status):
        if status:
            print(f"[音频] 状态: {status}")
        # indata shape: (frames, channels), 转为 float32 一维数组
        audio = indata[:, 0].copy()
        audio_queue.put(audio)

    stream = sd.InputStream(
        device=device,
        channels=CHANNELS,
        samplerate=SAMPLE_RATE,
        blocksize=BLOCK_SIZE,
        dtype="float32",
        callback=callback,
    )
    stream.start()
    print(f"[音频] 开始采集 (设备: {device}, 采样率: {SAMPLE_RATE})")
    return stream


def list_audio_devices():
    """列出所有音频设备，用于调试"""
    print("\n===== 音频设备列表 =====")
    devices = sd.query_devices()
    for i, dev in enumerate(devices):
        kind = "输入" if dev["max_input_channels"] > 0 else "输出"
        if dev["max_input_channels"] > 0 or dev["max_output_channels"] > 0:
            print(f"  [{i}] {kind} | {dev['name']}")
    print()
