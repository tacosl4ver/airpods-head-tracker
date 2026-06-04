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
    print("AirPodsGyroHelper.app が見つかりません")
    sys.exit(1)

# FIFO を準備
if os.path.exists(FIFO):
    os.unlink(FIFO)
os.mkfifo(FIFO)

# open コマンドで LaunchServices 経由起動（TCC の responsible process が app 自身になる）
# -n: 常に新しいインスタンス  -g: フォアグラウンドに出さない
subprocess.Popen(["open", "-n", "-g", APP, "--args", FIFO])

print("AirPodsGyroHelper.app を起動中…")
print("初回は「モーションデータへのアクセス」許可ダイアログが出ます。")
print("（FIFO 接続待機中 — アプリ起動後に自動接続します）\n")

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
    if v < -30:  return "← 左    "
    if v >  30:  return "右 →    "
    return              "  正面  "

def pitch_label(v):
    if v >  15:  return "↑ 上向き"
    if v < -15:  return "↓ 下向き"
    return              "  水平  "

def roll_label(v):
    if v >  15:  return "/ 右傾き"
    if v < -15:  return "\\ 左傾き"
    return              "  まっすぐ"

def draw(y, p, r):
    print("\033[H\033[J", end='')
    print("╔══════════════════════════════════════════════════╗")
    print("║        AirPods Pro ヘッドトラッキング           ║")
    print("╠══════════════════════════════════════════════════╣")
    print(f"║  Yaw   (左右): {y:+7.1f}°  {yaw_label(y):<8}                ║")
    print(f"║  [{make_bar(y, -90, 90)}]  ║")
    print(f"║                                                  ║")
    print(f"║  Pitch (上下): {p:+7.1f}°  {pitch_label(p):<8}                ║")
    print(f"║  [{make_bar(p, -60, 60)}]  ║")
    print(f"║                                                  ║")
    print(f"║  Roll  (傾き): {r:+7.1f}°  {roll_label(r):<8}                ║")
    print(f"║  [{make_bar(r, -60, 60)}]  ║")
    print("╚══════════════════════════════════════════════════╝")
    print("\n  ※ 起動時の向きが基準 (0°)    Ctrl+C で終了")

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
            print("AirPods Pro が接続されていないか未対応です")
            break

        draw(data["yaw"], data["pitch"], data["roll"])

except KeyboardInterrupt:
    pass
finally:
    f.close()
    if os.path.exists(FIFO):
        os.unlink(FIFO)
    print("\n\n終了しました")
