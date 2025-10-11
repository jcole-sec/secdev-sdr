# SDR FM Receiver

A professional FM radio receiver implementation using Ettus Research USRP B200 series hardware and GNU Radio.

## Features

- **Enhanced Audio Quality**: Advanced filtering chain minimizes static and noise
- **Real-time Controls**: Frequency tuning, gain control, volume, and squelch adjustment  
- **Audio Recording**: One-click recording to high-quality WAV files (48kHz, 16-bit)
- **Visual Feedback**: Real-time spectrum display for signal monitoring
- **Optimized Performance**: Efficient signal processing for stable operation

## Hardware Requirements

- **USRP B200** series SDR (70 MHz - 6 GHz)
- **USB 3.0** connection for optimal performance
- **FM Antenna** (recommended: telescopic or dipole antenna)

## Software Dependencies

### System Requirements

```bash
# Install UHD drivers
sudo add-apt-repository ppa:ettusresearch/uhd
sudo apt-get update
sudo apt-get install libuhd-dev uhd-host

# Download firmware images
sudo uhd_images_downloader

# Install GNU Radio
sudo apt-get install gnuradio
```

### USB Permissions Setup

```bash
# Copy udev rules for USRP access
sudo cp /usr/libexec/uhd/utils/uhd-usrp.rules /etc/udev/rules.d/
sudo udevadm control --reload-rules
sudo udevadm trigger
```

## Quick Start

1. **Connect Hardware**
   - Connect USRP B200 via USB 3.0
   - Attach FM antenna to RX2 port

2. **Verify Connection**
   ```bash
   ./setup_uhd_env.sh
   ```

3. **Launch FM Receiver**
   ```bash
   ./launch_fm_receiver.sh
   ```

## Usage

### GUI Controls

| Control | Range | Default | Description |
|---------|-------|---------|-------------|
| **Frequency** | 88.1 - 107.9 MHz | 88.5 MHz | FM station frequency |
| **RF Gain** | 20 - 76 dB | 40 dB | Receiver gain (adjust for signal strength) |
| **Volume** | 0 - 100% | 30% | Audio output level |
| **Squelch** | -80 to -20 dB | -50 dB | Noise threshold (higher = less noise) |

### Recording Audio

1. Tune to desired station and adjust audio quality
2. Click **🔴 Start Recording** (button turns red)
3. Monitor status display for filename and progress  
4. Click **⏹️ Stop Recording** when finished
5. Files saved as `fm_recording_[FREQ]MHz_[TIMESTAMP].wav`

### Signal Processing Chain

```
USRP B200 → Anti-Alias Filter → FM Demodulator → Power Squelch → 
Audio Filter → Volume Control → Audio Output + Recording
```

## Technical Specifications

- **RF Sample Rate**: 2.4 MHz (optimized for FM bandwidth)
- **Audio Sample Rate**: 48 kHz (CD quality)
- **RF Bandwidth**: 200 kHz (FM channel spacing)
- **Audio Bandwidth**: 300 Hz - 15 kHz (broadcast quality)
- **Recording Format**: WAV, 16-bit PCM, 48 kHz

## Files Description

| File | Purpose |
|------|---------|
| `fm_receiver.py` | Complete FM receiver with GUI and recording |
| `launch_fm_receiver.sh` | Convenient launcher with status info |
| `setup_uhd_env.sh` | UHD environment configuration |

## Troubleshooting

### No USRP Detected
- Verify USB 3.0 connection
- Check udev rules installation  
- Run `uhd_find_devices` manually

### Poor Audio Quality
- Adjust **RF Gain** (lower for strong signals, higher for weak)
- Fine-tune **Squelch** threshold
- Ensure good antenna connection and positioning

### Recording Issues
- Check disk space in project directory
- Verify write permissions
- Monitor GUI status messages for errors

### Performance Issues
- Ensure USB 3.0 operation (not USB 2.0)
- Close unnecessary applications
- Consider lowering GUI update rates

## Advanced Usage

### Custom Frequencies
Edit the frequency range in `fm_receiver.py` for non-broadcast applications (amateur radio, aviation, etc.)

### Signal Analysis
Use the real-time spectrum display to:
- Identify strong vs. weak signals
- Monitor RF interference
- Optimize antenna positioning
- Analyze signal quality

## GNU Radio Integration

- Edit `fm_receiver.grc` in GNU Radio Companion for customization
- Regenerate Python code with: `grcc fm_receiver.grc`
- Modify signal processing parameters for different applications

## License

This project is provided for educational and amateur radio use.

## References

- [Ettus Research USRP Documentation](https://www.ettus.com/support/documentation/)
- [GNU Radio Wiki](https://wiki.gnuradio.org/)
- [UHD Manual](https://files.ettus.com/manual/)