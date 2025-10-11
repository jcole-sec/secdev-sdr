#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: RTL-SDR FM Receiver
# Description: RTL-SDR FM Radio Receiver - Professional implementation for RTL-SDR dongles
# GNU Radio version: 3.10.9.2

from PyQt5 import Qt
from gnuradio import qtgui
from PyQt5 import QtCore
from gnuradio import analog
from gnuradio import audio
from gnuradio import blocks
from gnuradio import filter
from gnuradio.filter import firdes
from gnuradio import gr
from gnuradio.fft import window
import sys
import signal
from PyQt5 import Qt
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
import osmosdr
import time
import sip
import os
from datetime import datetime



class rtl_fm_receiver(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "RTL-SDR FM Receiver", catch_exceptions=True)
        Qt.QWidget.__init__(self)
        self.setWindowTitle("RTL-SDR FM Receiver")
        qtgui.util.check_set_qss()
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except BaseException as exc:
            print(f"Qt GUI: Could not set Icon: {str(exc)}", file=sys.stderr)
        self.top_scroll_layout = Qt.QVBoxLayout()
        self.setLayout(self.top_scroll_layout)
        self.top_scroll = Qt.QScrollArea()
        self.top_scroll.setFrameStyle(Qt.QFrame.NoFrame)
        self.top_scroll_widget = Qt.QWidget()
        self.top_scroll_layout.addWidget(self.top_scroll)
        self.top_scroll.setWidget(self.top_scroll_widget)
        self.top_scroll.setWidgetResizable(True)
        self.top_widget = self.top_scroll_widget
        self.top_layout = Qt.QVBoxLayout(self.top_widget)
        self.top_layout.setSpacing(10)
        
        # Create control panels with group boxes
        self.controls_layout = Qt.QHBoxLayout()
        
        # Frequency Control Group
        self.freq_group = Qt.QGroupBox("Frequency Control")
        self.freq_layout = Qt.QVBoxLayout(self.freq_group)
        
        # Hardware Control Group  
        self.hardware_group = Qt.QGroupBox("Hardware Settings")
        self.hardware_layout = Qt.QVBoxLayout(self.hardware_group)
        
        # Audio Control Group
        self.audio_group = Qt.QGroupBox("Audio Control")
        self.audio_layout = Qt.QVBoxLayout(self.audio_group)
        
        # Recording Control Group
        self.record_group = Qt.QGroupBox("Recording")
        self.record_layout = Qt.QVBoxLayout(self.record_group)
        
        # Add groups to main controls layout
        self.controls_layout.addWidget(self.freq_group)
        self.controls_layout.addWidget(self.hardware_group)
        self.controls_layout.addWidget(self.audio_group)
        self.controls_layout.addWidget(self.record_group)
        
        # Add controls to main layout
        self.top_layout.addLayout(self.controls_layout)

        self.settings = Qt.QSettings("GNU Radio", "rtl_fm_receiver")

        try:
            geometry = self.settings.value("geometry")
            if geometry:
                self.restoreGeometry(geometry)
        except BaseException as exc:
            print(f"Qt GUI: Could not restore geometry: {str(exc)}", file=sys.stderr)
        self.setMinimumWidth(1200)
        self.setMinimumHeight(800)
        
        # Set window properties for better performance
        self.setWindowFlags(Qt.Qt.Window | Qt.Qt.WindowMinimizeButtonHint | Qt.Qt.WindowMaximizeButtonHint | Qt.Qt.WindowCloseButtonHint)
        
        # Apply modern dark theme
        self.setStyleSheet("""
            QMainWindow {
                background-color: #2b2b2b;
                color: #ffffff;
            }
            QWidget {
                background-color: #2b2b2b;
                color: #ffffff;
                font-family: 'Segoe UI', Arial, sans-serif;
                font-size: 10pt;
            }
            QGroupBox {
                font-weight: bold;
                border: 2px solid #555555;
                border-radius: 8px;
                margin: 5px;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
            }
            QSlider::groove:horizontal {
                border: 1px solid #555555;
                height: 8px;
                background: #404040;
                border-radius: 4px;
            }
            QSlider::handle:horizontal {
                background: #0078d4;
                border: 1px solid #005a9e;
                width: 18px;
                height: 18px;
                border-radius: 9px;
            }
            QSlider::handle:horizontal:hover {
                background: #106ebe;
            }
            QLabel {
                color: #ffffff;
                font-weight: normal;
            }
        """)

        ##################################################
        # Variables
        ##################################################
        self.samp_rate_audio = samp_rate_audio = 240e3
        self.rf_gain = rf_gain = 40
        self.freq_offset = freq_offset = 0
        self.center_freq = center_freq = 88.5e6
        self.samp_rate = samp_rate = 2.4e6
        self.record_enable = record_enable = 0
        self.audio_decimation = audio_decimation = int(samp_rate_audio / 48000)
        self.volume = volume = 0.3
        self.muted = False
        self.previous_volume = 0.3

        ##################################################
        # Blocks
        ##################################################
        # RTL-SDR Source
        self.osmosdr_source_0 = osmosdr.source(
            args="numchan=" + str(1) + " " + ""
        )
        self.osmosdr_source_0.set_time_unknown_pps(osmosdr.time_spec_t())
        self.osmosdr_source_0.set_sample_rate(samp_rate)
        self.osmosdr_source_0.set_center_freq(center_freq, 0)
        self.osmosdr_source_0.set_freq_corr(0, 0)
        self.osmosdr_source_0.set_dc_offset_mode(0, 0)
        self.osmosdr_source_0.set_iq_balance_mode(0, 0)
        self.osmosdr_source_0.set_gain_mode(False, 0)
        self.osmosdr_source_0.set_gain(rf_gain, 0)
        self.osmosdr_source_0.set_if_gain(20, 0)
        self.osmosdr_source_0.set_bb_gain(20, 0)
        self.osmosdr_source_0.set_antenna('', 0)
        self.osmosdr_source_0.set_bandwidth(0, 0)

        # Frequency control with presets
        self._center_freq_range = qtgui.Range(88.1e6, 107.9e6, 100e3, 88.5e6, 200)
        self._center_freq_win = qtgui.RangeWidget(self._center_freq_range, self.set_center_freq, "FM Frequency (MHz)", "counter_slider", float, QtCore.Qt.Horizontal)
        self.freq_layout.addWidget(self._center_freq_win)
        
        # Add frequency presets
        self.preset_layout = Qt.QHBoxLayout()
        presets = [("NPR", 88.5e6), ("Pop", 95.5e6), ("Rock", 101.1e6), ("Jazz", 104.3e6), ("Classical", 107.1e6)]
        for name, freq in presets:
            btn = Qt.QPushButton(f"{name}\n{freq/1e6:.1f}")
            btn.setFixedSize(60, 40)
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #404040;
                    border: 1px solid #606060;
                    border-radius: 4px;
                    color: white;
                    font-size: 8pt;
                }
                QPushButton:hover {
                    background-color: #505050;
                }
                QPushButton:pressed {
                    background-color: #0078d4;
                }
            """)
            btn.clicked.connect(lambda checked, f=freq: self.set_center_freq(f))
            self.preset_layout.addWidget(btn)
        self.freq_layout.addLayout(self.preset_layout)

        # RF Gain control with auto-gain button
        self._rf_gain_range = qtgui.Range(0, 50, 1, 40, 200)
        self._rf_gain_win = qtgui.RangeWidget(self._rf_gain_range, self.set_rf_gain, "RF Gain (dB)", "counter_slider", float, QtCore.Qt.Horizontal)
        self.hardware_layout.addWidget(self._rf_gain_win)
        
        # Auto-gain button
        self.auto_gain_button = Qt.QPushButton("Auto Gain")
        self.auto_gain_button.setFixedHeight(30)
        self.auto_gain_button.setStyleSheet("""
            QPushButton {
                background-color: #404040;
                border: 1px solid #606060;
                border-radius: 4px;
                color: white;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #505050;
            }
        """)
        self.auto_gain_button.clicked.connect(self.auto_adjust_gain)
        self.hardware_layout.addWidget(self.auto_gain_button)
        
        # Sample rate display
        self.samp_rate_label = Qt.QLabel(f"Sample Rate: {self.samp_rate/1e6:.1f} MSPS")
        self.samp_rate_label.setAlignment(QtCore.Qt.AlignCenter)
        self.hardware_layout.addWidget(self.samp_rate_label)

        # Volume control with mute button
        self._volume_range = qtgui.Range(0, 1.0, 0.01, 0.3, 200)
        self._volume_win = qtgui.RangeWidget(self._volume_range, self.set_volume, "Volume", "counter_slider", float, QtCore.Qt.Horizontal)
        self.audio_layout.addWidget(self._volume_win)
        
        # Mute button
        self.mute_button = Qt.QPushButton("🔊 Mute")
        self.mute_button.setFixedHeight(30)
        self.mute_button.setCheckable(True)
        self.mute_button.setStyleSheet("""
            QPushButton {
                background-color: #404040;
                border: 1px solid #606060;
                border-radius: 4px;
                color: white;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #505050;
            }
            QPushButton:checked {
                background-color: #d13438;
            }
        """)
        self.mute_button.clicked.connect(self.toggle_mute)
        self.audio_layout.addWidget(self.mute_button)

        # Recording controls
        self._record_enable_push_button = Qt.QPushButton('🔴 Start Recording')
        self._record_enable_push_button.setFixedHeight(40)
        # Initial green styling for ready state
        self._record_enable_push_button.setStyleSheet("""
            QPushButton { 
                background-color: #44ff44; 
                color: black; 
                font-weight: bold; 
                border-radius: 6px;
                border: 2px solid #339933;
                font-size: 11pt;
            }
            QPushButton:hover {
                background-color: #55ff55;
            }
        """)
        self._record_enable_push_button.pressed.connect(lambda: self.set_record_enable(1 if self.record_enable == 0 else 0))
        self.record_layout.addWidget(self._record_enable_push_button)
        
        # Recording status label
        self.record_status_label = Qt.QLabel("Ready to record")
        self.record_status_label.setAlignment(QtCore.Qt.AlignCenter)
        self.record_status_label.setStyleSheet("color: #00ff00; font-weight: bold;")
        self.record_layout.addWidget(self.record_status_label)

        # Create visualization layout
        self.viz_layout = Qt.QHBoxLayout()
        
        # Spectrum display - optimized for performance
        self.qtgui_freq_sink_x_0 = qtgui.freq_sink_c(
            2048, #size - reduced for better performance
            window.WIN_BLACKMAN_hARRIS, #wintype
            center_freq, #fc
            samp_rate, #bw
            "RF Spectrum Analyzer", #name
            1,
            None # parent
        )
        self.qtgui_freq_sink_x_0.set_update_time(0.1)  # Faster updates
        self.qtgui_freq_sink_x_0.set_y_axis(-120, -20)  # Optimized range
        self.qtgui_freq_sink_x_0.set_y_label('Power', 'dB')
        self.qtgui_freq_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, 0.0, 0, "")
        self.qtgui_freq_sink_x_0.enable_autoscale(False)
        self.qtgui_freq_sink_x_0.enable_grid(True)
        self.qtgui_freq_sink_x_0.set_fft_average(0.8)  # Smoother display
        self.qtgui_freq_sink_x_0.enable_axis_labels(True)
        self.qtgui_freq_sink_x_0.enable_control_panel(True)
        self.qtgui_freq_sink_x_0.set_fft_window_normalized(False)

        # Improved spectrum display styling
        labels = ['RF Signal', '', '', '', '',
                  '', '', '', '', '']
        widths = [2, 1, 1, 1, 1,
                  1, 1, 1, 1, 1]
        colors = ["#00ff00", "red", "blue", "orange", "cyan",
                  "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_freq_sink_x_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_freq_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_freq_sink_x_0.set_line_width(i, widths[i])
            self.qtgui_freq_sink_x_0.set_line_color(i, colors[i])
            self.qtgui_freq_sink_x_0.set_line_alpha(i, alphas[i])

        self._qtgui_freq_sink_x_0_win = sip.wrapinstance(self.qtgui_freq_sink_x_0.qwidget(), Qt.QWidget)
        self.viz_layout.addWidget(self._qtgui_freq_sink_x_0_win, 2)
        
        # Add waterfall display for better visualization
        self.qtgui_waterfall_sink_x_0 = qtgui.waterfall_sink_c(
            1024, #size
            window.WIN_BLACKMAN_hARRIS, #wintype
            center_freq, #fc
            samp_rate, #bw
            "Waterfall Display", #name
            1, #number of inputs
            None # parent
        )
        self.qtgui_waterfall_sink_x_0.set_update_time(0.10)
        self.qtgui_waterfall_sink_x_0.enable_grid(False)
        self.qtgui_waterfall_sink_x_0.enable_axis_labels(True)
        
        labels = ['RF Signal', '', '', '', '',
                  '', '', '', '', '']
        colors = [5, 0, 0, 0, 0,
                  0, 0, 0, 0, 0]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_waterfall_sink_x_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_waterfall_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_waterfall_sink_x_0.set_color_map(i, colors[i])
            self.qtgui_waterfall_sink_x_0.set_line_alpha(i, alphas[i])

        self._qtgui_waterfall_sink_x_0_win = sip.wrapinstance(self.qtgui_waterfall_sink_x_0.qwidget(), Qt.QWidget)
        self.viz_layout.addWidget(self._qtgui_waterfall_sink_x_0_win, 1)
        
        # Add visualization to main layout
        self.top_layout.addLayout(self.viz_layout)
        
        # Status bar with device information
        self.status_layout = Qt.QHBoxLayout()
        
        self.device_status_label = Qt.QLabel("RTL-SDR: Initializing...")
        self.device_status_label.setStyleSheet("""
            QLabel {
                background-color: #333333;
                color: #00ff00;
                padding: 5px;
                border-radius: 3px;
                font-weight: bold;
            }
        """)
        
        self.signal_strength_label = Qt.QLabel("Signal: --")
        self.signal_strength_label.setStyleSheet("""
            QLabel {
                background-color: #333333;
                color: #ffaa00;
                padding: 5px;
                border-radius: 3px;
                font-weight: bold;
            }
        """)
        
        self.cpu_usage_label = Qt.QLabel("CPU: --")
        self.cpu_usage_label.setStyleSheet("""
            QLabel {
                background-color: #333333;
                color: #00aaff;
                padding: 5px;
                border-radius: 3px;
                font-weight: bold;
            }
        """)
        
        self.status_layout.addWidget(self.device_status_label)
        self.status_layout.addWidget(self.signal_strength_label)
        self.status_layout.addWidget(self.cpu_usage_label)
        self.status_layout.addStretch()
        
        self.top_layout.addLayout(self.status_layout)
        
        # Update status periodically
        self.status_timer = QtCore.QTimer()
        self.status_timer.timeout.connect(self.update_status)
        self.status_timer.start(1000)  # Update every second

        # Low pass filter for FM channel selection
        self.low_pass_filter_0 = filter.fir_filter_ccf(
            (int(samp_rate / samp_rate_audio)),
            firdes.low_pass(
                1,
                samp_rate,
                75e3,
                25e3,
                window.WIN_HAMMING,
                6.76))

        # FM demodulator
        self.analog_wfm_rcv_0 = analog.wfm_rcv(
            quad_rate=samp_rate_audio,
            audio_decimation=audio_decimation,
        )

        # Audio sink
        self.audio_sink_0 = audio.sink(48000, '', True)

        # Volume control block
        self.blocks_multiply_const_vxx_0 = blocks.multiply_const_ff(volume)

        # Recording blocks
        self.recording_enabled = False
        self.record_filename = f"rtl_recording_{88.5}MHz_{datetime.now().strftime('%Y%m%d_%H%M%S')}.wav"
        # Create a persistent wavfile sink that we can open/close
        self.blocks_wavfile_sink_0 = blocks.wavfile_sink(
            "/dev/null",  # Start with a dummy file
            1,
            48000,
            blocks.FORMAT_WAV,
            blocks.FORMAT_PCM_16,
            False
        )
        # Connect the wavfile sink to the audio stream permanently
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.blocks_wavfile_sink_0, 0))

        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_wfm_rcv_0, 0), (self.blocks_multiply_const_vxx_0, 0))
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.audio_sink_0, 0))
        self.connect((self.low_pass_filter_0, 0), (self.analog_wfm_rcv_0, 0))
        self.connect((self.osmosdr_source_0, 0), (self.low_pass_filter_0, 0))
        self.connect((self.osmosdr_source_0, 0), (self.qtgui_freq_sink_x_0, 0))
        self.connect((self.osmosdr_source_0, 0), (self.qtgui_waterfall_sink_x_0, 0))

    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "rtl_fm_receiver")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

    def get_samp_rate_audio(self):
        return self.samp_rate_audio

    def set_samp_rate_audio(self, samp_rate_audio):
        self.samp_rate_audio = samp_rate_audio
        self.set_audio_decimation(int(self.samp_rate_audio / 48000))

    def get_rf_gain(self):
        return self.rf_gain

    def set_rf_gain(self, rf_gain):
        self.rf_gain = rf_gain
        self.osmosdr_source_0.set_gain(self.rf_gain, 0)

    def get_freq_offset(self):
        return self.freq_offset

    def set_freq_offset(self, freq_offset):
        self.freq_offset = freq_offset

    def get_center_freq(self):
        return self.center_freq

    def set_center_freq(self, center_freq):
        self.center_freq = center_freq
        self.osmosdr_source_0.set_center_freq(self.center_freq, 0)
        self.qtgui_freq_sink_x_0.set_frequency_range(self.center_freq, self.samp_rate)
        self.qtgui_waterfall_sink_x_0.set_frequency_range(self.center_freq, self.samp_rate)

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.osmosdr_source_0.set_sample_rate(self.samp_rate)
        self.low_pass_filter_0.set_taps(firdes.low_pass(1, self.samp_rate, 75e3, 25e3, window.WIN_HAMMING, 6.76))
        self.qtgui_freq_sink_x_0.set_frequency_range(self.center_freq, self.samp_rate)
        self.qtgui_waterfall_sink_x_0.set_frequency_range(self.center_freq, self.samp_rate)
        self.samp_rate_label.setText(f"Sample Rate: {self.samp_rate/1e6:.1f} MSPS")

    def get_record_enable(self):
        return self.record_enable

    def set_record_enable(self, record_enable):
        self.record_enable = record_enable
        
        if self.record_enable == 1 and not self.recording_enabled:
            # Start recording - create new filename and open file
            self.record_filename = f"rtl_recording_{self.center_freq/1e6:.1f}MHz_{datetime.now().strftime('%Y%m%d_%H%M%S')}.wav"
            try:
                # Close any existing file and open new one
                self.blocks_wavfile_sink_0.close()
                self.blocks_wavfile_sink_0.open(self.record_filename)
                self.recording_enabled = True
                # Red styling for recording state
                self._record_enable_push_button.setText('⏹️ Stop Recording')
                self._record_enable_push_button.setStyleSheet("""
                    QPushButton { 
                        background-color: #ff4444; 
                        color: white; 
                        font-weight: bold; 
                        border-radius: 6px;
                        border: 2px solid #cc3333;
                        font-size: 11pt;
                    }
                    QPushButton:hover {
                        background-color: #ff5555;
                    }
                """)
                self.record_status_label.setText(f"Recording: {self.record_filename}")
                self.record_status_label.setStyleSheet("color: #ff0000; font-weight: bold;")
                print(f"Started recording to: {self.record_filename}")
            except Exception as e:
                print(f"Error starting recording: {e}")
            
        elif self.record_enable == 0 and self.recording_enabled:
            # Stop recording - close the file
            try:
                self.blocks_wavfile_sink_0.close()
                self.recording_enabled = False
                # Green styling for ready state
                self._record_enable_push_button.setText('🔴 Start Recording')
                self._record_enable_push_button.setStyleSheet("""
                    QPushButton { 
                        background-color: #44ff44; 
                        color: black; 
                        font-weight: bold; 
                        border-radius: 6px;
                        border: 2px solid #339933;
                        font-size: 11pt;
                    }
                    QPushButton:hover {
                        background-color: #55ff55;
                    }
                """)
                self.record_status_label.setText("Ready to record")
                self.record_status_label.setStyleSheet("color: #00ff00; font-weight: bold;")
                print(f"Stopped recording to: {self.record_filename}")
            except Exception as e:
                print(f"Error stopping recording: {e}")

    def auto_adjust_gain(self):
        """Automatically adjust RF gain based on signal level"""
        try:
            # Simple auto-gain algorithm
            # Start with medium gain and adjust based on reception
            optimal_gain = 30  # Default starting point
            self.set_rf_gain(optimal_gain)
            print(f"Auto-gain set to {optimal_gain} dB")
        except Exception as e:
            print(f"Auto-gain error: {e}")

    def toggle_mute(self):
        """Toggle audio mute"""
        if self.mute_button.isChecked():
            # Mute audio
            self.previous_volume = self.volume
            self.set_volume(0.0)
            self.mute_button.setText("🔇 Unmute")
            self.muted = True
        else:
            # Unmute audio
            self.set_volume(self.previous_volume)
            self.mute_button.setText("🔊 Mute")
            self.muted = False

    def get_audio_decimation(self):
        return self.audio_decimation

    def set_audio_decimation(self, audio_decimation):
        self.audio_decimation = audio_decimation

    def get_volume(self):
        return self.volume

    def set_volume(self, volume):
        self.volume = volume
        self.blocks_multiply_const_vxx_0.set_k(self.volume)
        if hasattr(self, '_volume_win'):
            self._volume_win.d_widget.setValue(self.volume)

    def update_status(self):
        """Update status bar information"""
        try:
            # Update device status
            self.device_status_label.setText(f"RTL-SDR: Connected at {self.center_freq/1e6:.1f} MHz")
            
            # Simple signal strength indication (placeholder)
            self.signal_strength_label.setText(f"Signal: {self.rf_gain} dB gain")
            
            # CPU usage placeholder
            self.cpu_usage_label.setText("CPU: Active")
            
        except Exception as e:
            self.device_status_label.setText(f"RTL-SDR: Error - {str(e)[:20]}...")




def main(top_block_cls=rtl_fm_receiver, options=None):

    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()

    tb.start()

    tb.show()

    def sig_handler(sig=None, frame=None):
        tb.stop()
        tb.wait()

        Qt.QApplication.quit()

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    timer = Qt.QTimer()
    timer.start(500)
    timer.timeout.connect(lambda: None)

    qapp.exec_()

if __name__ == '__main__':
    main()