#!/bin/bash

# SDR FM Radio Receiver Launcher
# High-quality FM receiver with recording capability

echo "=========================================="
echo "    SDR FM Radio Receiver v2.0"
echo "    Enhanced filtering and recording"
echo "=========================================="

# Get script directory for relative paths
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Set up UHD environment
source "${SCRIPT_DIR}/setup_uhd_env.sh"

# Check if USRP is connected
echo "Checking USRP B200 connectivity..."
if ! uhd_find_devices | grep -q "B200"; then
    echo "ERROR: USRP B200 not detected!"
    echo "Please check USB connection and ensure device is powered."
    exit 1
fi

echo "✓ USRP B200 detected successfully"
echo ""

echo "Features:"
echo "• Enhanced filtering for minimal static"
echo "• Power squelch to eliminate noise"  
echo "• Audio band-pass filtering (300Hz-15kHz)"
echo "• Real-time spectrum display"
echo "• One-click audio recording to WAV files"
echo ""

echo "Controls:"
echo "• FM Frequency: 88.1 - 107.9 MHz (default: 88.5 MHz)"
echo "• RF Gain: 20-76 dB (adjust for signal strength)"
echo "• Volume: 0-100% (start at 30%)"
echo "• Squelch: -80 to -20 dB (eliminates weak signals)"
echo "• Recording: Click button to start/stop recording"
echo ""

echo "Starting FM receiver..."
echo "Close the GUI window to stop."
echo ""

# Run the receiver
python3 "${SCRIPT_DIR}/fm_receiver.py"

echo ""
echo "FM receiver stopped."