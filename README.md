# AirPods Head Tracker

AirPods Pro のヘッドトラッキング（ジャイロ）データを macOS で取得し、画面ポインタとして可視化するサンプルです。

## 動作環境

- macOS 13 Ventura 以降
- Xcode Command Line Tools
- Python 3.10 以降
- AirPods Pro（第1世代 / 第2世代）または AirPods（第3世代）

## セットアップ

```bash
git clone https://github.com/YOUR_USERNAME/airpods-head-tracker.git
cd airpods-head-tracker
chmod +x install.sh
./install.sh
```

初回起動時に **「モーションデータへのアクセス」** の許可ダイアログが表示されます。  
AirPods Pro を耳に装着した状態で「OK」を押してください。

## 使い方

### ターミナルにジャイロ数値を表示

```bash
python3 airpods_gyro_test.py
```

Yaw（左右）/ Pitch（上下）/ Roll（傾き）がリアルタイムで表示されます。

### 画面上でヘッドポインタを表示

```bash
python3 airpods_pointer_test.py
```

起動時の向きがゼロ基準になり、頭の動きに合わせてドットが移動します。

| キー | 動作 |
|------|------|
| Space | 基準をリセット |
| Esc | 終了 |

感度は `airpods_pointer_test.py` 内の `YAW_RANGE` / `PITCH_RANGE` で調整できます（数値を小さくすると敏感になります）。

## 仕組み

`CMHeadphoneMotionManager`（CoreMotion）を使って AirPods Pro の姿勢データを取得します。  
Swift で書かれたヘルパーアプリ（`AirPodsGyroHelper.app`）が FIFO 経由で Python にデータを渡します。

## ファイル構成

```
airpods_gyro_helper.swift     Swift ソース（CMHeadphoneMotionManager）
AirPodsGyroHelper.app/        アプリバンドル（install.sh でビルド）
airpods_gyro_test.py          ターミナル可視化
airpods_pointer_test.py       画面ポインタ可視化
install.sh                    ビルド＆セットアップスクリプト
```
