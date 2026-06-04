#!/usr/bin/env python3
"""
AirPods Pro Head Tracking → Screen Pointer Visualizer
AirPods Pro ヘッドトラッキング → 画面ポインタ可視化
Launch orientation = center reference. Space to reset, Esc to quit.
起動時の向きがゼロ基準。Space でリセット、Esc で終了。
Window is resizable. / ウィンドウはリサイズ可能。
"""

import json, os, signal, subprocess, sys, threading
import tkinter as tk

DIR  = os.path.dirname(os.path.abspath(__file__))
APP  = os.path.join(DIR, "AirPodsGyroHelper.app")
FIFO = "/tmp/airpods_gyro.fifo"

def cleanup(*_):
    subprocess.run(["pkill", "-f", "airpods_gyro_bin"], capture_output=True)
    if os.path.exists(FIFO):
        os.unlink(FIFO)

# 起動時に前回の残骸を掃除 / Clean up leftovers from previous run
cleanup()

signal.signal(signal.SIGTERM, lambda s, f: (cleanup(), sys.exit(0)))
signal.signal(signal.SIGHUP,  lambda s, f: (cleanup(), sys.exit(0)))

YAW_RANGE   = 40.0  # ±40° で端まで
PITCH_RANGE = 25.0  # ±25° で端まで
DOT_RADIUS  = 14


class HeadPointer:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("AirPods Head Pointer")
        self.root.geometry("400x300+100+100")
        self.root.minsize(200, 150)
        self.root.resizable(True, True)
        self.root.configure(bg='black')
        self.root.attributes('-topmost', True)

        self.canvas = tk.Canvas(self.root, bg='#0a0a0a', highlightthickness=0)
        self.canvas.pack(fill='both', expand=True)

        # 背景要素（リサイズ時に再描画）
        self.line_h  = self.canvas.create_line(0, 0, 0, 0, fill='#2a2a2a')
        self.line_v  = self.canvas.create_line(0, 0, 0, 0, fill='#2a2a2a')
        self.oval_bg = self.canvas.create_oval(0, 0, 0, 0, outline='#1a3a2a')

        # ドット
        r = DOT_RADIUS
        self.dot = self.canvas.create_oval(-r, -r, r, r,
                                           fill='#00ff88', outline='#00cc66', width=2)

        # ラベル
        self.label = self.canvas.create_text(
            0, 0, anchor='center',
            text="Connecting... / 接続待機中...", fill='#666', font=('Helvetica', 12))

        self.yaw_ref   = None
        self.pitch_ref = None
        self.last_nx   = 0.0
        self.last_ny   = 0.0

        self.canvas.bind('<Configure>', self._on_resize)
        self.root.bind('<Escape>', lambda e: self.quit())
        self.root.bind('<space>',  lambda e: self.reset())

    def _on_resize(self, event):
        W, H = event.width, event.height
        cx, cy = W // 2, H // 2

        self.canvas.coords(self.line_h, 0, cy, W, cy)
        self.canvas.coords(self.line_v, cx, 0, cx, H)

        pad = 20
        self.canvas.coords(self.oval_bg,
                           pad, pad, W - pad, H - pad)

        self.canvas.coords(self.label, cx, H - 18)

        # ドットを現在位置に再配置
        self._place_dot(W, H, self.last_nx, self.last_ny)

    def _place_dot(self, W, H, nx, ny):
        cx, cy = W // 2, H // 2
        x = cx + nx * (W // 2 - 30)
        y = cy + ny * (H // 2 - 30)
        r = DOT_RADIUS
        self.canvas.coords(self.dot, x-r, y-r, x+r, y+r)

    def reset(self):
        self.yaw_ref   = None
        self.pitch_ref = None
        self.canvas.itemconfig(self.label, text="Reset / リセットしました", fill='#ffaa00')

    def quit(self):
        cleanup()
        self.root.quit()

    def update(self, yaw, pitch, roll):
        if self.yaw_ref is None:
            self.yaw_ref   = yaw
            self.pitch_ref = pitch
            self.canvas.itemconfig(self.label,
                text="Space: Reset / リセット    Esc: Quit / 終了", fill='#00ff88')

        dy =  yaw   - self.yaw_ref
        dp =  pitch - self.pitch_ref

        nx = -dy / YAW_RANGE
        ny = -dp / PITCH_RANGE
        self.last_nx = max(-1.0, min(1.0, nx))
        self.last_ny = max(-1.0, min(1.0, ny))

        W = self.canvas.winfo_width()
        H = self.canvas.winfo_height()
        self._place_dot(W, H, self.last_nx, self.last_ny)

    def run(self):
        self.root.mainloop()


def fifo_reader(pointer):
    if os.path.exists(FIFO):
        os.unlink(FIFO)
    os.mkfifo(FIFO)

    subprocess.Popen(["open", "-n", "-g", APP, "--args", FIFO])

    try:
        f = open(FIFO, 'r')
    except KeyboardInterrupt:
        return

    for line in f:
        line = line.strip()
        if not line:
            continue
        try:
            data = json.loads(line)
        except json.JSONDecodeError:
            continue
        if data.get("status") == "unavailable":
            pointer.root.after(0, pointer.canvas.itemconfig, pointer.label,
                               {'text': 'AirPods Pro not connected / 未接続', 'fill': '#ff4444'})
            break
        pointer.root.after(0, pointer.update,
                           data["yaw"], data["pitch"], data["roll"])

    f.close()
    cleanup()


pointer = HeadPointer()
t = threading.Thread(target=fifo_reader, args=(pointer,), daemon=True)
t.start()
pointer.run()
