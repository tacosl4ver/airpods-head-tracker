#!/usr/bin/env python3
"""AirPods Pro ジャイロ可視化テスト（LaunchServices + FIFO 版）"""

import json
import os
import subprocess
import sys
import time

DIR    = os.path.dirname(os.path.abspath(__file__))
APP    = os.path.join(DIR, "AirPodsGyroHelper.app")
FIFO   = "/tmp/airpods_gyro.fifo"

if not os.path.isdir(APP):
    print("AirPodsGyroHelper.app not found. Run install.sh first.")
    print("AirPodsGyroHelper.app が見つかりません。先に install.sh を実行してください。")
    sys.exit(1)

# FIFO を準備
if os.path.exists(FIFO):
    os.unlink(FIFO)
os.mkfifo(FIFO)

# open コマンドで LaunchServices 経由起動（TCC の responsible process が app 自身になる）
# -n: 常に新しいインスタンス  -g: フォアグラウンドに出さない
subprocess.Popen(["open", "-n", "-g", APP, "--args", FIFO])

print("Launching AirPodsGyroHelper.app... / AirPodsGyroHelper.app を起動中…")
print("On first launch, grant 'Motion & Fitness' permission. / 初回は「モーションデータへのアクセス」を許可してください。")
print("(Waiting for FIFO connection... / FIFO 接続待機中…)\n")

# FIFO を読み込み用に開く（Swift 側が書き込み用に開くまでここでブロック）
try:
    f = open(FIFO, 'r')
except KeyboardInterrupt:
    os.unlink(FIFO)
    sys.exit(0)

BAR_W = 43

def make_bar(value, lo, hi):
    norm = (value - lo) / (hi - lo)
    pos  = max(0, min(BAR_W - 1, int(norm * BAR_W)))
    mid  = BAR_W // 2
    bar  = ['-'] * BAR_W
    bar[mid] = '+'
    bar[pos] = '◉'
    return ''.join(bar)

def yaw_label(v):
    if v < -30:  return "← Left  "
    if v >  30:  return "Right → "
    return              " Center "

def pitch_label(v):
    if v >  15:  return "↑ Up    "
    if v < -15:  return "↓ Down  "
    return              " Level  "

def roll_label(v):
    if v >  15:  return "/ Tilt R"
    if v < -15:  return "\\ Tilt L"
    return              " Straight"

def draw(y, p, r):
    print("\033[H\033[J", end='')
    print("╔══════════════════════════════════════════════════╗")
    print("║     AirPods Pro Head Tracking / ヘッドトラッキング ║")
    print("╠══════════════════════════════════════════════════╣")
    print(f"║  Yaw   (L/R 左右): {y:+7.1f}°  {yaw_label(y):<9}           ║")
    print(f"║  [{make_bar(y, -90, 90)}]  ║")
    print(f"║                                                  ║")
    print(f"║  Pitch (U/D 上下): {p:+7.1f}°  {pitch_label(p):<9}           ║")
    print(f"║  [{make_bar(p, -60, 60)}]  ║")
    print(f"║                                                  ║")
    print(f"║  Roll  (Tilt 傾き): {r:+7.1f}°  {roll_label(r):<9}          ║")
    print(f"║  [{make_bar(r, -60, 60)}]  ║")
    print("╚══════════════════════════════════════════════════╝")
    print("\n  Reference = launch orientation (0°)  /  起動時の向きが基準 (0°)    Ctrl+C to quit / 終了")

try:
    for line in f:
        line = line.strip()
        if not line:
            continue
        try:
            data = json.loads(line)
        except json.JSONDecodeError:
            continue

        if data.get("status") == "unavailable":
            print("AirPods Pro not connected or unsupported. / AirPods Pro が接続されていないか未対応です。")
            break

        draw(data["yaw"], data["pitch"], data["roll"])

except KeyboardInterrupt:
    pass
finally:
    f.close()
    if os.path.exists(FIFO):
        os.unlink(FIFO)
    print("\n\nExited. / 終了しました。")
