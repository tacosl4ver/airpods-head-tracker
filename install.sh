#!/bin/bash
set -e

echo "=== AirPods Head Tracker Setup / セットアップ ==="

# Xcode CLT チェック / Check for Xcode Command Line Tools
if ! xcode-select -p &>/dev/null; then
    echo "ERROR: Xcode Command Line Tools are required. / Xcode Command Line Tools が必要です。"
    echo "       Run: xcode-select --install"
    exit 1
fi

DIR="$(cd "$(dirname "$0")" && pwd)"
APP="$DIR/AirPodsGyroHelper.app"
BIN="$APP/Contents/MacOS/airpods_gyro_bin"

mkdir -p "$APP/Contents/MacOS"

echo ""
echo "1. Building Swift binary... / Swift バイナリをビルド中..."
swiftc "$DIR/airpods_gyro_helper.swift" \
    -framework CoreMotion \
    -framework Foundation \
    -o "$BIN"
echo "   OK: $BIN"

echo ""
echo "2. Code signing... / アドホック署名中..."
codesign --force --deep --sign - "$APP"
echo "   OK"

echo ""
echo "=== Setup complete! / セットアップ完了 ==="
echo ""
echo "Usage / 使い方:"
echo "  python3 airpods_gyro_test.py      # Show gyro values in terminal / ターミナルにジャイロ数値を表示"
echo "  python3 airpods_pointer_test.py   # Screen head pointer demo / 画面上でヘッドポインタを表示"
echo ""
echo "On first launch, grant 'Motion & Fitness' permission with your AirPods Pro in your ears."
echo "初回起動時に「モーションデータへのアクセス」許可ダイアログが出ます。AirPods Pro を耳に装着した状態で許可してください。"
