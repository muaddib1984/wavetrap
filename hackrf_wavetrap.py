#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: WAVETRAP PUSH-BUTTON RF RECORDER
# Author: Muad'Dib
# GNU Radio version: 3.10.2.0-rc1

from packaging.version import Version as StrictVersion

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

class hackrf_wavetrap(gr.top_block, Qt.QWidget):

    def __init__(self, rf_bw=20e6, rf_freq=1534e6, rf_gain=40.0, samp_rate=2e6):
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

        self.settings = Qt.QSettings("GNU Radio", "hackrf_wavetrap")

        try:
            if StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
                self.restoreGeometry(self.settings.value("geometry").toByteArray())
            else:
                self.restoreGeometry(self.settings.value("geometry"))
        except:
            pass

        ##################################################
        # Parameters
        ##################################################
        self.rf_bw = rf_bw
        self.rf_freq = rf_freq
        self.rf_gain = rf_gain
        self.samp_rate = samp_rate

        ##################################################
        # Variables
        ##################################################
        self.rootdir = rootdir = str(os.path.expanduser("~")+"/")
        self.record_file_path = record_file_path = "data/"
        self.note = note = 'RECORDING_NOTE'
        self.gui_samp_rate = gui_samp_rate = samp_rate
        self.gui_gain = gui_gain = 16
        self.freq = freq = rf_freq
        self.vga_gain = vga_gain = 16
        self.timestamp = timestamp = datetime.fromtimestamp(time.time()).strftime('%Y_%m_%d_%H:%M:%S')
        self.str_freq = str_freq = str(freq)
        self.rec_button = rec_button = 0
        self.gui_bandwidth = gui_bandwidth = rf_bw
        self.filename = filename = rootdir+record_file_path+note+"_"+str(int(freq))+"Hz_"+str(int(gui_samp_rate))+"sps_"+str(gui_gain)+"dB_"

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
        self._vga_gain_range = Range(0, 62, 2, 16, 200)
        self._vga_gain_win = RangeWidget(self._vga_gain_range, self.set_vga_gain, "RX VGA Gain", "counter_slider", int, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._vga_gain_win)
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
        self._gui_samp_rate_range = Range(200e3, 56e6, 1e6, samp_rate, 200)
        self._gui_samp_rate_win = RangeWidget(self._gui_samp_rate_range, self.set_gui_samp_rate, "sample_rate", "counter_slider", float, QtCore.Qt.Horizontal)
        self.tabs_grid_layout_0.addWidget(self._gui_samp_rate_win, 0, 1, 1, 1)
        for r in range(0, 1):
            self.tabs_grid_layout_0.setRowStretch(r, 1)
        for c in range(1, 2):
            self.tabs_grid_layout_0.setColumnStretch(c, 1)
        self._gui_gain_range = Range(0, 40, 1, 16, 200)
        self._gui_gain_win = RangeWidget(self._gui_gain_range, self.set_gui_gain, "RX Gain", "counter_slider", int, QtCore.Qt.Horizontal)
        self.tabs_grid_layout_0.addWidget(self._gui_gain_win, 0, 0, 1, 1)
        for r in range(0, 1):
            self.tabs_grid_layout_0.setRowStretch(r, 1)
        for c in range(0, 1):
            self.tabs_grid_layout_0.setColumnStretch(c, 1)
        self._gui_bandwidth_range = Range(200e3, 56e6, 1e6, rf_bw, 200)
        self._gui_bandwidth_win = RangeWidget(self._gui_bandwidth_range, self.set_gui_bandwidth, "Bandwidth", "counter_slider", float, QtCore.Qt.Horizontal)
        self.tabs_grid_layout_0.addWidget(self._gui_bandwidth_win, 0, 2, 1, 1)
        for r in range(0, 1):
            self.tabs_grid_layout_0.setRowStretch(r, 1)
        for c in range(2, 3):
            self.tabs_grid_layout_0.setColumnStretch(c, 1)
        self.soapy_hackrf_source_0 = None
        dev = 'driver=hackrf'
        stream_args = ''
        tune_args = ['']
        settings = ['']

        self.soapy_hackrf_source_0 = soapy.source(dev, "fc32", 1, '',
                                  stream_args, tune_args, settings)
        self.soapy_hackrf_source_0.set_sample_rate(0, gui_samp_rate)
        self.soapy_hackrf_source_0.set_bandwidth(0, gui_bandwidth)
        self.soapy_hackrf_source_0.set_frequency(0, freq)
        self.soapy_hackrf_source_0.set_gain(0, 'AMP', True)
        self.soapy_hackrf_source_0.set_gain(0, 'LNA', min(max(gui_gain, 0.0), 40.0))
        self.soapy_hackrf_source_0.set_gain(0, 'VGA', min(max(vga_gain, 0.0), 62.0))
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
            gui_samp_rate, #bw
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
        self.qtgui_edit_box_msg_0_0 = qtgui.edit_box_msg(qtgui.FLOAT, str_freq, 'Freq', True, True, 'freq', None)
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


        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.qtgui_edit_box_msg_0_0, 'msg'), (self.blocks_msgpair_to_var_0, 'inpair'))
        self.msg_connect((self.qtgui_edit_box_msg_0_0, 'msg'), (self.qtgui_freq_sink_x_0, 'freq'))
        self.msg_connect((self.qtgui_freq_sink_x_0, 'freq'), (self.qtgui_edit_box_msg_0_0, 'val'))
        self.connect((self.soapy_hackrf_source_0, 0), (self.blocks_file_sink_0, 0))
        self.connect((self.soapy_hackrf_source_0, 0), (self.qtgui_freq_sink_x_0, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "hackrf_wavetrap")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

    def get_rf_bw(self):
        return self.rf_bw

    def set_rf_bw(self, rf_bw):
        self.rf_bw = rf_bw
        self.set_gui_bandwidth(self.rf_bw)

    def get_rf_freq(self):
        return self.rf_freq

    def set_rf_freq(self, rf_freq):
        self.rf_freq = rf_freq
        self.set_freq(self.rf_freq)

    def get_rf_gain(self):
        return self.rf_gain

    def set_rf_gain(self, rf_gain):
        self.rf_gain = rf_gain

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.set_gui_samp_rate(self.samp_rate)

    def get_rootdir(self):
        return self.rootdir

    def set_rootdir(self, rootdir):
        self.rootdir = rootdir
        self.set_filename(self.rootdir+self.record_file_path+self.note+"_"+str(int(self.freq))+"Hz_"+str(int(self.gui_samp_rate))+"sps_"+str(self.gui_gain)+"dB_")

    def get_record_file_path(self):
        return self.record_file_path

    def set_record_file_path(self, record_file_path):
        self.record_file_path = record_file_path
        self.set_filename(self.rootdir+self.record_file_path+self.note+"_"+str(int(self.freq))+"Hz_"+str(int(self.gui_samp_rate))+"sps_"+str(self.gui_gain)+"dB_")

    def get_note(self):
        return self.note

    def set_note(self, note):
        self.note = note
        self.set_filename(self.rootdir+self.record_file_path+self.note+"_"+str(int(self.freq))+"Hz_"+str(int(self.gui_samp_rate))+"sps_"+str(self.gui_gain)+"dB_")
        Qt.QMetaObject.invokeMethod(self._note_line_edit, "setText", Qt.Q_ARG("QString", str(self.note)))

    def get_gui_samp_rate(self):
        return self.gui_samp_rate

    def set_gui_samp_rate(self, gui_samp_rate):
        self.gui_samp_rate = gui_samp_rate
        self.set_filename(self.rootdir+self.record_file_path+self.note+"_"+str(int(self.freq))+"Hz_"+str(int(self.gui_samp_rate))+"sps_"+str(self.gui_gain)+"dB_")
        self.qtgui_freq_sink_x_0.set_frequency_range(self.freq, self.gui_samp_rate)
        self.soapy_hackrf_source_0.set_sample_rate(0, self.gui_samp_rate)

    def get_gui_gain(self):
        return self.gui_gain

    def set_gui_gain(self, gui_gain):
        self.gui_gain = gui_gain
        self.set_filename(self.rootdir+self.record_file_path+self.note+"_"+str(int(self.freq))+"Hz_"+str(int(self.gui_samp_rate))+"sps_"+str(self.gui_gain)+"dB_")
        self.soapy_hackrf_source_0.set_gain(0, 'LNA', min(max(self.gui_gain, 0.0), 40.0))

    def get_freq(self):
        return self.freq

    def set_freq(self, freq):
        self.freq = freq
        self.set_filename(self.rootdir+self.record_file_path+self.note+"_"+str(int(self.freq))+"Hz_"+str(int(self.gui_samp_rate))+"sps_"+str(self.gui_gain)+"dB_")
        self.set_str_freq(str(self.freq))
        self.qtgui_freq_sink_x_0.set_frequency_range(self.freq, self.gui_samp_rate)
        self.soapy_hackrf_source_0.set_frequency(0, self.freq)

    def get_vga_gain(self):
        return self.vga_gain

    def set_vga_gain(self, vga_gain):
        self.vga_gain = vga_gain
        self.soapy_hackrf_source_0.set_gain(0, 'VGA', min(max(self.vga_gain, 0.0), 62.0))

    def get_timestamp(self):
        return self.timestamp

    def set_timestamp(self, timestamp):
        self.timestamp = timestamp

    def get_str_freq(self):
        return self.str_freq

    def set_str_freq(self, str_freq):
        self.str_freq = str_freq

    def get_rec_button(self):
        return self.rec_button

    def set_rec_button(self, rec_button):
        self.rec_button = rec_button
        self.blocks_file_sink_0.open(self.filename+str(datetime.fromtimestamp(time.time()).strftime('%Y_%m_%d_%H:%M:%S'))+".cfile" if self.rec_button == 1 else "/dev/null")
        self.qtgui_ledindicator_0.setState(True if self.rec_button == 1 else False)

    def get_gui_bandwidth(self):
        return self.gui_bandwidth

    def set_gui_bandwidth(self, gui_bandwidth):
        self.gui_bandwidth = gui_bandwidth
        self.soapy_hackrf_source_0.set_bandwidth(0, self.gui_bandwidth)

    def get_filename(self):
        return self.filename

    def set_filename(self, filename):
        self.filename = filename
        self.blocks_file_sink_0.open(self.filename+str(datetime.fromtimestamp(time.time()).strftime('%Y_%m_%d_%H:%M:%S'))+".cfile" if self.rec_button == 1 else "/dev/null")



def argument_parser():
    parser = ArgumentParser()
    parser.add_argument(
        "-b", "--rf-bw", dest="rf_bw", type=eng_float, default=eng_notation.num_to_str(float(20e6)),
        help="Set RF BANDWITDH [default=%(default)r]")
    parser.add_argument(
        "-f", "--rf-freq", dest="rf_freq", type=eng_float, default=eng_notation.num_to_str(float(1534e6)),
        help="Set RF FREQUENCY [default=%(default)r]")
    parser.add_argument(
        "-g", "--rf-gain", dest="rf_gain", type=eng_float, default=eng_notation.num_to_str(float(40.0)),
        help="Set RF GAIN [default=%(default)r]")
    parser.add_argument(
        "-s", "--samp-rate", dest="samp_rate", type=eng_float, default=eng_notation.num_to_str(float(2e6)),
        help="Set SAMPLE RATE [default=%(default)r]")
    return parser


def main(top_block_cls=hackrf_wavetrap, options=None):
    if options is None:
        options = argument_parser().parse_args()

    if StrictVersion("4.5.0") <= StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
        style = gr.prefs().get_string('qtgui', 'style', 'raster')
        Qt.QApplication.setGraphicsSystem(style)
    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls(rf_bw=options.rf_bw, rf_freq=options.rf_freq, rf_gain=options.rf_gain, samp_rate=options.samp_rate)

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
