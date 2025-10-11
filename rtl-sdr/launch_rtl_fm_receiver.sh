#!/bin/bash

# RTL-SDR FM Radio Receiver Launcher
# Configures RTL-SDR environment and launches the receiver

echo "=========================================="
echo "    RTL-SDR FM Radio Receiver v1.0"
echo "    Enhanced filtering and recording"
echo "=========================================="

# Check if RTL-SDR devices are available
echo "Checking for RTL-SDR devices..."
if ! rtl_test -t > /dev/null 2>&1; then
    echo "❌ No RTL-SDR devices found!"
    echo ""
    echo "Make sure your RTL-SDR dongle is:"
    echo "• Plugged into a USB port"
    echo "• Not being used by another application"
    echo "• Properly detected by the system"
    echo ""
    echo "Try running 'rtl_test' to verify device detection"
    exit 1
fi

echo "✓ RTL-SDR device detected successfully"
echo ""

# Display device information
echo "RTL-SDR Device Information:"
rtl_test -t 2>&1 | head -5

echo ""
echo "Features:"
echo "• Enhanced filtering for minimal static"
echo "• Real-time spectrum display"
echo "• Audio recording to WAV files"
echo "• RTL-SDR dongle support (0.5 MHz - 1.75 GHz)"
echo ""
echo "Controls:"
echo "• FM Frequency: 88.1 - 107.9 MHz (default: 88.5 MHz)"
echo "• RF Gain: 0-50 dB (adjust for signal strength)"
echo "• Volume: 0-100% (start at 30%)"
echo "• Recording: Click button to start/stop recording"
echo ""
echo "Starting RTL-SDR FM receiver..."
echo "Close the GUI window to stop."
echo ""

# Launch the receiver
cd "$(dirname "$0")"
python3 rtl_fm_receiver.py

echo ""
echo "RTL-SDR FM receiver stopped."