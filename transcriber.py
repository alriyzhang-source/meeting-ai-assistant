"""语音识别模块 — vosk 实时转录（不依赖 PyTorch）"""

import queue
import threading
import json
import numpy as np
import vosk
from config import SAMPLE_RATE

MODEL_PATH = "vosk-model-cn"


def load_vosk_model() -> vosk.Model:
    """加载 vosk 中文模型"""
    print(f"[识别] 加载 vosk 模型: {MODEL_PATH}")
    model = vosk.Model(MODEL_PATH)
    print("[识别] 模型加载完成")
    return model


def start_transcriber(audio_queue: queue.Queue, text_queue: queue.Queue) -> threading.Thread:
    """启动语音识别线程"""
    model = load_vosk_model()
    rec = vosk.KaldiRecognizer(model, SAMPLE_RATE)
    rec.SetWords(True)

    def _transcribe_loop():
        last_text = ""
        while True:
            try:
                chunk = audio_queue.get(timeout=1.0)
            except queue.Empty:
                continue

            # vosk 需要 int16 格式的 bytes
            audio_int16 = (chunk * 32768).astype(np.int16)
            data = audio_int16.tobytes()

            if rec.AcceptWaveform(data):
                result = json.loads(rec.Result())
                text = result.get("text", "").strip()
                if text and text != last_text:
                    # vosk 中文模型可能带空格，去掉
                    text = text.replace(" ", "")
                    text_queue.put(text)
                    last_text = text
                    print(f"[识别] {text}")

    thread = threading.Thread(target=_transcribe_loop, daemon=True, name="Transcriber")
    thread.start()
    print("[识别] 识别线程已启动")
    return thread
