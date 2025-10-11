#!/usr/bin/env python3
"""
RTL-SDR Test Script
Simple test to verify RTL-SDR functionality without GUI
"""

import osmosdr
import time
from gnuradio import gr, blocks, analog, filter
from gnuradio.filter import firdes
from gnuradio.fft import window

class rtl_test(gr.top_block):
    def __init__(self):
        gr.top_block.__init__(self, "RTL-SDR Test")
        
        # Variables
        self.samp_rate = 2.4e6
        self.center_freq = 88.5e6
        self.rf_gain = 40
        
        # RTL-SDR Source
        self.osmosdr_source_0 = osmosdr.source(args="numchan=1")
        self.osmosdr_source_0.set_sample_rate(self.samp_rate)
        self.osmosdr_source_0.set_center_freq(self.center_freq, 0)
        self.osmosdr_source_0.set_freq_corr(0, 0)
        self.osmosdr_source_0.set_dc_offset_mode(0, 0)
        self.osmosdr_source_0.set_iq_balance_mode(0, 0)
        self.osmosdr_source_0.set_gain_mode(False, 0)
        self.osmosdr_source_0.set_gain(self.rf_gain, 0)
        
        # Simple power measurement
        self.blocks_complex_to_mag_squared_0 = blocks.complex_to_mag_squared(1)
        self.blocks_moving_average_xx_0 = blocks.moving_average_ff(int(self.samp_rate/10), 1.0/int(self.samp_rate/10), 4000, 1)
        self.blocks_probe_signal_x_0 = blocks.probe_signal_f()
        
        # Connections  
        self.connect((self.osmosdr_source_0, 0), (self.blocks_complex_to_mag_squared_0, 0))
        self.connect((self.blocks_complex_to_mag_squared_0, 0), (self.blocks_moving_average_xx_0, 0))
        self.connect((self.blocks_moving_average_xx_0, 0), (self.blocks_probe_signal_x_0, 0))

def main():
    print("RTL-SDR Functionality Test")
    print("=" * 30)
    
    try:
        # Test device detection
        print("1. Testing device detection...")
        tb = rtl_test()
        print("   ✓ RTL-SDR source created successfully")
        
        # Test signal reception
        print("2. Testing signal reception...")
        tb.start()
        
        # Monitor signal for a few seconds
        for i in range(5):
            time.sleep(1)
            power = tb.blocks_probe_signal_x_0.level()
            print(f"   Signal power at 88.5 MHz: {power:.2e}")
        
        tb.stop()
        tb.wait()
        print("   ✓ Signal reception test completed")
        
        print("\n✓ RTL-SDR test completed successfully!")
        print("\nYour RTL-SDR is working properly and ready for the FM receiver.")
        
    except Exception as e:
        print(f"❌ RTL-SDR test failed: {e}")
        print("\nTroubleshooting:")
        print("- Check RTL-SDR dongle is connected")  
        print("- Ensure drivers are installed: sudo apt install rtl-sdr gr-osmosdr")
        print("- Try: rtl_test -t")
        return 1
        
    return 0

if __name__ == '__main__':
    exit(main())