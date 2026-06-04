# AirPods Head Tracker

> Control your screen with your head — using AirPods Pro as a motion sensor on macOS.

[English](#english) | [日本語](#japanese)

---

<a name="english"></a>
## English

### Overview

This project uses **AirPods Pro's built-in motion sensors** (`CMHeadphoneMotionManager`) to track head orientation in real time on macOS. It includes a terminal visualizer and a screen pointer demo where a dot follows your head movement.

### Requirements

- macOS 13 Ventura or later
- Xcode Command Line Tools
- Python 3.10 or later
- AirPods Pro (1st or 2nd gen) or AirPods (3rd gen)

### Setup

```bash
git clone https://github.com/tacosl4ver/airpods-head-tracker.git
cd airpods-head-tracker
chmod +x install.sh
./install.sh
```

On first launch, macOS will show a **"Motion & Fitness"** permission dialog. Accept it with your AirPods Pro in your ears.

### Usage

**Show gyro data in the terminal:**
```bash
python3 airpods_gyro_test.py
```
Displays Yaw / Pitch / Roll values in real time.

**Screen head pointer:**
```bash
python3 airpods_pointer_test.py
```
A dot on screen follows your head movement. Your facing direction at launch is the center.

| Key | Action |
|-----|--------|
| Space | Reset center reference |
| Esc | Quit |

Adjust sensitivity by changing `YAW_RANGE` / `PITCH_RANGE` in `airpods_pointer_test.py` (smaller = more sensitive).

### How It Works

A small Swift helper app (`AirPodsGyroHelper.app`) reads motion data via `CMHeadphoneMotionManager` and streams JSON over a named pipe (FIFO) to Python.

```
AirPods Pro → CMHeadphoneMotionManager → Swift helper → FIFO → Python
```

### File Structure

```
airpods_gyro_helper.swift     Swift source (CMHeadphoneMotionManager)
AirPodsGyroHelper.app/        App bundle (built by install.sh)
airpods_gyro_test.py          Terminal visualizer
airpods_pointer_test.py       Screen pointer demo
install.sh                    Build & setup script
```

---

<a name="japanese"></a>
## 日本語

### 概要

**AirPods Pro 内蔵のモーションセンサー**（`CMHeadphoneMotionManager`）を使い、頭の向きをリアルタイムで取得するmacOSサンプルです。ターミナルへの数値表示と、頭の動きに追従する画面ポインタのデモが含まれています。

### 動作環境

- macOS 13 Ventura 以降
- Xcode Command Line Tools
- Python 3.10 以降
- AirPods Pro（第1世代 / 第2世代）または AirPods（第3世代）

### セットアップ

```bash
git clone https://github.com/tacosl4ver/airpods-head-tracker.git
cd airpods-head-tracker
chmod +x install.sh
./install.sh
```

初回起動時に **「モーションデータへのアクセス」** の許可ダイアログが表示されます。AirPods Pro を耳に装着した状態で許可してください。

### 使い方

**ターミナルにジャイロ数値を表示:**
```bash
python3 airpods_gyro_test.py
```
Yaw（左右）/ Pitch（上下）/ Roll（傾き）がリアルタイムで確認できます。

**画面上でヘッドポインタを表示:**
```bash
python3 airpods_pointer_test.py
```
起動時の向きがゼロ基準となり、頭の動きに合わせてドットが移動します。

| キー | 動作 |
|------|------|
| Space | 基準をリセット |
| Esc | 終了 |

感度は `airpods_pointer_test.py` 内の `YAW_RANGE` / `PITCH_RANGE` で調整できます（数値を小さくすると敏感になります）。

### 仕組み

Swift で書かれたヘルパーアプリ（`AirPodsGyroHelper.app`）が `CMHeadphoneMotionManager` でモーションデータを取得し、FIFO（名前付きパイプ）経由で Python にJSON形式でストリーミングします。

```
AirPods Pro → CMHeadphoneMotionManager → Swift ヘルパー → FIFO → Python
```

### ファイル構成

```
airpods_gyro_helper.swift     Swift ソース（CMHeadphoneMotionManager）
AirPodsGyroHelper.app/        アプリバンドル（install.sh でビルド）
airpods_gyro_test.py          ターミナル可視化
airpods_pointer_test.py       画面ポインタ可視化
install.sh                    ビルド＆セットアップスクリプト
```
