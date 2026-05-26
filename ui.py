"""界面模块 — Tkinter 置顶窗口，显示问题记录和 AI 回答"""

import queue
import tkinter as tk
from datetime import datetime
from config import WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_X, WINDOW_Y


class MeetingUI:
    def __init__(self, answer_queue: queue.Queue):
        self.answer_queue = answer_queue
        self.root = tk.Tk()
        self.root.title("会议 AI 助手")
        self.root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}+{WINDOW_X}+{WINDOW_Y}")
        self.root.attributes("-topmost", True)
        self.root.configure(bg="#1e1e2e")

        self._build_widgets()
        self._poll_queue()

    def _build_widgets(self):
        style = {"bg": "#1e1e2e", "fg": "#cdd6f4", "font": ("Microsoft YaHei", 11)}
        title_style = {"bg": "#1e1e2e", "fg": "#89b4fa", "font": ("Microsoft YaHei", 13, "bold")}

        # --- 标题栏 ---
        header = tk.Frame(self.root, bg="#1e1e2e")
        header.pack(fill="x", padx=10, pady=(10, 0))

        tk.Label(header, text="📡 监听中...", **title_style).pack(side="left")
        self.status_label = tk.Label(header, text="", bg="#1e1e2e", fg="#a6adc8", font=("Microsoft YaHei", 10))
        self.status_label.pack(side="right")

        # --- 问题记录区 ---
        tk.Label(self.root, text="📝 老师问题记录", **title_style).pack(anchor="w", padx=10, pady=(10, 2))

        self.question_text = tk.Text(
            self.root, height=12, bg="#313244", fg="#cdd6f4",
            font=("Microsoft YaHei", 11), wrap="word", relief="flat", bd=0,
            insertbackground="#cdd6f4",
        )
        self.question_text.pack(fill="x", padx=10, pady=(0, 10))
        self.question_text.configure(state="disabled")

        # --- 分隔线 ---
        tk.Frame(self.root, bg="#45475a", height=2).pack(fill="x", padx=10, pady=5)

        # --- AI 回答区 ---
        tk.Label(self.root, text="🤖 AI 建议回答", **title_style).pack(anchor="w", padx=10, pady=(0, 2))

        self.answer_text = tk.Text(
            self.root, bg="#313244", fg="#a6e3a1",
            font=("Microsoft YaHei", 11), wrap="word", relief="flat", bd=0,
            insertbackground="#cdd6f4",
        )
        self.answer_text.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        self.answer_text.configure(state="disabled")

        # --- 底部按钮 ---
        btn_frame = tk.Frame(self.root, bg="#1e1e2e")
        btn_frame.pack(fill="x", padx=10, pady=(0, 10))

        tk.Button(
            btn_frame, text="清空回答", command=self._clear_answer,
            bg="#45475a", fg="#cdd6f4", font=("Microsoft YaHei", 10), relief="flat",
        ).pack(side="left", padx=(0, 5))

        tk.Button(
            btn_frame, text="复制回答", command=self._copy_answer,
            bg="#45475a", fg="#cdd6f4", font=("Microsoft YaHei", 10), relief="flat",
        ).pack(side="left")

    def _poll_queue(self):
        """轮询 answer_queue，更新 UI"""
        try:
            while True:
                question, answer = self.answer_queue.get_nowait()
                self._append_question(question)
                self._set_answer(f"Q: {question}\n\n{answer}")
                # 更新状态栏
                self.status_label.config(text=datetime.now().strftime("%H:%M:%S"))
        except queue.Empty:
            pass
        self.root.after(200, self._poll_queue)

    def _append_question(self, question: str):
        """追加问题到记录区"""
        time_str = datetime.now().strftime("%H:%M:%S")
        self.question_text.configure(state="normal")
        self.question_text.insert("end", f"[{time_str}] {question}\n")
        self.question_text.see("end")
        self.question_text.configure(state="disabled")

    def _set_answer(self, text: str):
        """设置 AI 回答区内容"""
        self.answer_text.configure(state="normal")
        self.answer_text.delete("1.0", "end")
        self.answer_text.insert("1.0", text)
        self.answer_text.configure(state="disabled")

    def _clear_answer(self):
        self.answer_text.configure(state="normal")
        self.answer_text.delete("1.0", "end")
        self.answer_text.configure(state="disabled")

    def _copy_answer(self):
        self.root.clipboard_clear()
        self.root.clipboard_append(self.answer_text.get("1.0", "end").strip())

    def run(self):
        print("[UI] 界面已启动")
        self.root.mainloop()
