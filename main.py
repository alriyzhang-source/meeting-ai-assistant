"""腾讯会议 AI 助手 — 主入口

使用方式：
1. 安装 VB-Audio Virtual Cable (https://vb-audio.com/Cable/)
2. 腾讯会议 → 设置 → 音频 → 扬声器选 "CABLE Input"
3. 将论文/资料转为 txt 放入 materials/ 文件夹
4. 运行: python main.py
"""

import sys
import queue
import signal

from audio_capture import start_audio_capture, list_audio_devices
from transcriber import start_transcriber
from ai_responder import start_ai_responder
from ui import MeetingUI


def main():
    # 列出音频设备（方便调试）
    if "--devices" in sys.argv:
        list_audio_devices()
        return

    print("=" * 50)
    print("  腾讯会议 AI 助手")
    print("=" * 50)
    print()
    print("前置准备：")
    print("  1. 已安装 VB-Audio Virtual Cable")
    print("  2. 腾讯会议扬声器设为 CABLE Input")
    print("  3. 材料已放入 materials/ 文件夹")
    print()
    print("提示：运行 python main.py --devices 可查看音频设备列表")
    print()

    # 创建线程间通信队列
    audio_queue = queue.Queue()    # 音频采集 → 识别
    text_queue = queue.Queue()     # 识别 → AI
    answer_queue = queue.Queue()   # AI → UI

    # 启动各模块
    stream = start_audio_capture(audio_queue)
    start_transcriber(audio_queue, text_queue)
    start_ai_responder(text_queue, answer_queue)

    # Ctrl+C 优雅退出
    def on_exit(sig, frame):
        print("\n[退出] 正在停止...")
        stream.stop()
        stream.close()
        sys.exit(0)

    signal.signal(signal.SIGINT, on_exit)

    # 启动 UI（主线程）
    ui = MeetingUI(answer_queue)
    ui.run()


if __name__ == "__main__":
    main()
