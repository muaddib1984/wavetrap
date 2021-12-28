#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: WAVETRAP PUSH-BUTTON RF RECORDER
# Author: Muad'Dib
# GNU Radio version: 3.9.4.0

from distutils.version import StrictVersion

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print("Warning: failed to XInitThreads()")

from PyQt5 import Qt
from gnuradio import eng_notation
from gnuradio import qtgui
from gnuradio.filter import firdes
import sip
from datetime import datetime
from gnuradio import blocks
from gnuradio import gr
from gnuradio.fft import window
import sys
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import soapy
from gnuradio.qtgui import Range, RangeWidget
from PyQt5 import QtCore
import os
import time



from gnuradio import qtgui

class lime_wavetrap(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "WAVETRAP PUSH-BUTTON RF RECORDER", catch_exceptions=True)
        Qt.QWidget.__init__(self)
        self.setWindowTitle("WAVETRAP PUSH-BUTTON RF RECORDER")
        qtgui.util.check_set_qss()
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except:
            pass
        self.top_scroll_layout = Qt.QVBoxLayout()
        self.setLayout(self.top_scroll_layout)
        self.top_scroll = Qt.QScrollArea()
        self.top_scroll.setFrameStyle(Qt.QFrame.NoFrame)
        self.top_scroll_layout.addWidget(self.top_scroll)
        self.top_scroll.setWidgetResizable(True)
        self.top_widget = Qt.QWidget()
        self.top_scroll.setWidget(self.top_widget)
        self.top_layout = Qt.QVBoxLayout(self.top_widget)
        self.top_grid_layout = Qt.QGridLayout()
        self.top_layout.addLayout(self.top_grid_layout)

        self.settings = Qt.QSettings("GNU Radio", "lime_wavetrap")

        try:
            if StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
                self.restoreGeometry(self.settings.value("geometry").toByteArray())
            else:
                self.restoreGeometry(self.settings.value("geometry"))
        except:
            pass

        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = 20e6
        self.rootdir = rootdir = str(os.path.expanduser("~")+"/")
        self.record_file_path = record_file_path = "data/"
        self.note = note = 'RECORDING_NOTE'
        self.gain = gain = 50.0
        self.freq = freq = 852e6
        self.timestamp = timestamp = datetime.fromtimestamp(time.time()).strftime('%Y_%m_%d_%H:%M:%S')
        self.rec_button = rec_button = 0
        self.filename = filename = rootdir+record_file_path+note+"_"+str(int(freq))+"Hz_"+str(int(samp_rate))+"sps_"+str(gain)+"dB_"
        self.bandwidth = bandwidth = samp_rate*.8

        ##################################################
        # Blocks
        ##################################################
        self.tabs = Qt.QTabWidget()
        self.tabs_widget_0 = Qt.QWidget()
        self.tabs_layout_0 = Qt.QBoxLayout(Qt.QBoxLayout.TopToBottom, self.tabs_widget_0)
        self.tabs_grid_layout_0 = Qt.QGridLayout()
        self.tabs_layout_0.addLayout(self.tabs_grid_layout_0)
        self.tabs.addTab(self.tabs_widget_0, 'Tab 0')
        self.top_grid_layout.addWidget(self.tabs, 0, 0, 7, 4)
        for r in range(0, 7):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 4):
            self.top_grid_layout.setColumnStretch(c, 1)
        self._samp_rate_range = Range(200e3, 56e6, 1e6, 20e6, 200)
        self._samp_rate_win = RangeWidget(self._samp_rate_range, self.set_samp_rate, "sample_rate", "counter_slider", float, QtCore.Qt.Horizontal)
        self.tabs_grid_layout_0.addWidget(self._samp_rate_win, 0, 1, 1, 1)
        for r in range(0, 1):
            self.tabs_grid_layout_0.setRowStretch(r, 1)
        for c in range(1, 2):
            self.tabs_grid_layout_0.setColumnStretch(c, 1)
        _rec_button_push_button = Qt.QPushButton('RECORD')
        _rec_button_push_button = Qt.QPushButton('RECORD')
        self._rec_button_choices = {'Pressed': 1, 'Released': 0}
        _rec_button_push_button.pressed.connect(lambda: self.set_rec_button(self._rec_button_choices['Pressed']))
        _rec_button_push_button.released.connect(lambda: self.set_rec_button(self._rec_button_choices['Released']))
        self.tabs_grid_layout_0.addWidget(_rec_button_push_button, 1, 3, 1, 1)
        for r in range(1, 2):
            self.tabs_grid_layout_0.setRowStretch(r, 1)
        for c in range(3, 4):
            self.tabs_grid_layout_0.setColumnStretch(c, 1)
        self._gain_range = Range(0, 89.0, 1, 50.0, 200)
        self._gain_win = RangeWidget(self._gain_range, self.set_gain, "RX Gain", "counter_slider", float, QtCore.Qt.Horizontal)
        self.tabs_grid_layout_0.addWidget(self._gain_win, 0, 0, 1, 1)
        for r in range(0, 1):
            self.tabs_grid_layout_0.setRowStretch(r, 1)
        for c in range(0, 1):
            self.tabs_grid_layout_0.setColumnStretch(c, 1)
        self.soapy_limesdr_source_0 = None
        dev = 'driver=lime'
        stream_args = ''
        tune_args = ['']
        settings = ['']

        self.soapy_limesdr_source_0 = soapy.source(dev, "fc32", 1, '',
                                  stream_args, tune_args, settings)
        self.soapy_limesdr_source_0.set_sample_rate(0, samp_rate)
        self.soapy_limesdr_source_0.set_bandwidth(0, 0.0)
        self.soapy_limesdr_source_0.set_frequency(0, freq)
        self.soapy_limesdr_source_0.set_frequency_correction(0, 0)
        self.soapy_limesdr_source_0.set_gain(0, min(max(gain, -12.0), 61.0))
        self.qtgui_ledindicator_0 = self._qtgui_ledindicator_0_win = qtgui.GrLEDIndicator("RED=RECORDING", "red", "green", True if rec_button == 1 else False, 40, 2, 1, 1, self)
        self.qtgui_ledindicator_0 = self._qtgui_ledindicator_0_win
        self.tabs_grid_layout_0.addWidget(self._qtgui_ledindicator_0_win, 0, 3, 1, 1)
        for r in range(0, 1):
            self.tabs_grid_layout_0.setRowStretch(r, 1)
        for c in range(3, 4):
            self.tabs_grid_layout_0.setColumnStretch(c, 1)
        self.qtgui_freq_sink_x_0 = qtgui.freq_sink_c(
            8192, #size
            window.WIN_BLACKMAN_hARRIS, #wintype
            freq, #fc
            samp_rate, #bw
            "", #name
            1,
            None # parent
        )
        self.qtgui_freq_sink_x_0.set_update_time(0.05)
        self.qtgui_freq_sink_x_0.set_y_axis(-140, 10)
        self.qtgui_freq_sink_x_0.set_y_label('Relative Gain', 'dB')
        self.qtgui_freq_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, 0.0, 0, "")
        self.qtgui_freq_sink_x_0.enable_autoscale(False)
        self.qtgui_freq_sink_x_0.enable_grid(False)
        self.qtgui_freq_sink_x_0.set_fft_average(1.0)
        self.qtgui_freq_sink_x_0.enable_axis_labels(True)
        self.qtgui_freq_sink_x_0.enable_control_panel(False)
        self.qtgui_freq_sink_x_0.set_fft_window_normalized(False)



        labels = ['', '', '', '', '',
            '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
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
        self.tabs_grid_layout_0.addWidget(self._qtgui_freq_sink_x_0_win, 2, 0, 5, 4)
        for r in range(2, 7):
            self.tabs_grid_layout_0.setRowStretch(r, 1)
        for c in range(0, 4):
            self.tabs_grid_layout_0.setColumnStretch(c, 1)
        self.qtgui_edit_box_msg_0_0 = qtgui.edit_box_msg(qtgui.FLOAT, '852e6', 'Msg-based input', True, True, 'freq', None)
        self._qtgui_edit_box_msg_0_0_win = sip.wrapinstance(self.qtgui_edit_box_msg_0_0.qwidget(), Qt.QWidget)
        self.tabs_grid_layout_0.addWidget(self._qtgui_edit_box_msg_0_0_win, 1, 0, 1, 1)
        for r in range(1, 2):
            self.tabs_grid_layout_0.setRowStretch(r, 1)
        for c in range(0, 1):
            self.tabs_grid_layout_0.setColumnStretch(c, 1)
        self._note_tool_bar = Qt.QToolBar(self)
        self._note_tool_bar.addWidget(Qt.QLabel("RECORDING NOTE (press enter to update)" + ": "))
        self._note_line_edit = Qt.QLineEdit(str(self.note))
        self._note_tool_bar.addWidget(self._note_line_edit)
        self._note_line_edit.returnPressed.connect(
            lambda: self.set_note(str(str(self._note_line_edit.text()))))
        self.tabs_grid_layout_0.addWidget(self._note_tool_bar, 1, 1, 1, 2)
        for r in range(1, 2):
            self.tabs_grid_layout_0.setRowStretch(r, 1)
        for c in range(1, 3):
            self.tabs_grid_layout_0.setColumnStretch(c, 1)
        self.blocks_msgpair_to_var_0 = blocks.msg_pair_to_var(self.set_freq)
        self.blocks_file_sink_0 = blocks.file_sink(gr.sizeof_gr_complex*1, filename+str(datetime.fromtimestamp(time.time()).strftime('%Y_%m_%d_%H:%M:%S'))+".cfile" if rec_button == 1 else "/dev/null", False)
        self.blocks_file_sink_0.set_unbuffered(False)
        self._bandwidth_range = Range(200e3, 56e6, 1e6, samp_rate*.8, 200)
        self._bandwidth_win = RangeWidget(self._bandwidth_range, self.set_bandwidth, "Bandwidth", "counter_slider", float, QtCore.Qt.Horizontal)
        self.tabs_grid_layout_0.addWidget(self._bandwidth_win, 0, 2, 1, 1)
        for r in range(0, 1):
            self.tabs_grid_layout_0.setRowStretch(r, 1)
        for c in range(2, 3):
            self.tabs_grid_layout_0.setColumnStretch(c, 1)



        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.qtgui_edit_box_msg_0_0, 'msg'), (self.blocks_msgpair_to_var_0, 'inpair'))
        self.msg_connect((self.qtgui_freq_sink_x_0, 'freq'), (self.qtgui_edit_box_msg_0_0, 'val'))
        self.connect((self.soapy_limesdr_source_0, 0), (self.blocks_file_sink_0, 0))
        self.connect((self.soapy_limesdr_source_0, 0), (self.qtgui_freq_sink_x_0, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "lime_wavetrap")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.set_bandwidth(self.samp_rate*.8)
        self.set_filename(self.rootdir+self.record_file_path+self.note+"_"+str(int(self.freq))+"Hz_"+str(int(self.samp_rate))+"sps_"+str(self.gain)+"dB_")
        self.qtgui_freq_sink_x_0.set_frequency_range(self.freq, self.samp_rate)
        self.soapy_limesdr_source_0.set_sample_rate(0, self.samp_rate)

    def get_rootdir(self):
        return self.rootdir

    def set_rootdir(self, rootdir):
        self.rootdir = rootdir
        self.set_filename(self.rootdir+self.record_file_path+self.note+"_"+str(int(self.freq))+"Hz_"+str(int(self.samp_rate))+"sps_"+str(self.gain)+"dB_")

    def get_record_file_path(self):
        return self.record_file_path

    def set_record_file_path(self, record_file_path):
        self.record_file_path = record_file_path
        self.set_filename(self.rootdir+self.record_file_path+self.note+"_"+str(int(self.freq))+"Hz_"+str(int(self.samp_rate))+"sps_"+str(self.gain)+"dB_")

    def get_note(self):
        return self.note

    def set_note(self, note):
        self.note = note
        self.set_filename(self.rootdir+self.record_file_path+self.note+"_"+str(int(self.freq))+"Hz_"+str(int(self.samp_rate))+"sps_"+str(self.gain)+"dB_")
        Qt.QMetaObject.invokeMethod(self._note_line_edit, "setText", Qt.Q_ARG("QString", str(self.note)))

    def get_gain(self):
        return self.gain

    def set_gain(self, gain):
        self.gain = gain
        self.set_filename(self.rootdir+self.record_file_path+self.note+"_"+str(int(self.freq))+"Hz_"+str(int(self.samp_rate))+"sps_"+str(self.gain)+"dB_")
        self.soapy_limesdr_source_0.set_gain(0, min(max(self.gain, -12.0), 61.0))

    def get_freq(self):
        return self.freq

    def set_freq(self, freq):
        self.freq = freq
        self.set_filename(self.rootdir+self.record_file_path+self.note+"_"+str(int(self.freq))+"Hz_"+str(int(self.samp_rate))+"sps_"+str(self.gain)+"dB_")
        self.qtgui_freq_sink_x_0.set_frequency_range(self.freq, self.samp_rate)
        self.soapy_limesdr_source_0.set_frequency(0, self.freq)

    def get_timestamp(self):
        return self.timestamp

    def set_timestamp(self, timestamp):
        self.timestamp = timestamp

    def get_rec_button(self):
        return self.rec_button

    def set_rec_button(self, rec_button):
        self.rec_button = rec_button
        self.blocks_file_sink_0.open(self.filename+str(datetime.fromtimestamp(time.time()).strftime('%Y_%m_%d_%H:%M:%S'))+".cfile" if self.rec_button == 1 else "/dev/null")
        self.qtgui_ledindicator_0.setState(True if self.rec_button == 1 else False)

    def get_filename(self):
        return self.filename

    def set_filename(self, filename):
        self.filename = filename
        self.blocks_file_sink_0.open(self.filename+str(datetime.fromtimestamp(time.time()).strftime('%Y_%m_%d_%H:%M:%S'))+".cfile" if self.rec_button == 1 else "/dev/null")

    def get_bandwidth(self):
        return self.bandwidth

    def set_bandwidth(self, bandwidth):
        self.bandwidth = bandwidth




def main(top_block_cls=lime_wavetrap, options=None):

    if StrictVersion("4.5.0") <= StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
        style = gr.prefs().get_string('qtgui', 'style', 'raster')
        Qt.QApplication.setGraphicsSystem(style)
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
