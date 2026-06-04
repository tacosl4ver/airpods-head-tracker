#!/bin/bash
set -e

echo "=== AirPods Head Tracker セットアップ ==="

# Xcode CLT チェック
if ! xcode-select -p &>/dev/null; then
    echo "ERROR: Xcode Command Line Tools が必要です。"
    echo "       xcode-select --install を実行してください。"
    exit 1
fi

DIR="$(cd "$(dirname "$0")" && pwd)"
APP="$DIR/AirPodsGyroHelper.app"
BIN="$APP/Contents/MacOS/airpods_gyro_bin"

echo ""
echo "1. Swift バイナリをビルド中..."
swiftc "$DIR/airpods_gyro_helper.swift" \
    -framework CoreMotion \
    -framework Foundation \
    -o "$BIN"
echo "   OK: $BIN"

echo ""
echo "2. アドホック署名..."
codesign --force --deep --sign - "$APP"
echo "   OK"

echo ""
echo "=== セットアップ完了 ==="
echo ""
echo "使い方:"
echo "  python3 airpods_gyro_test.py      # ターミナルにジャイロ数値を表示"
echo "  python3 airpods_pointer_test.py   # 画面上でヘッドポインタを表示"
echo ""
echo "初回起動時に「モーションデータへのアクセス」許可ダイアログが出ます。"
echo "AirPods Pro を耳に装着した状態で許可してください。"
