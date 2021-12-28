# WAVETRAP
WAVETRAP is a Push-Button IQ Recorder intended to make capturing RF Data in the field fast and simple.
This collection of GNURadio Flowgraphs is made with only built in blocks from GNURadio 3.9 (gr-fosphor is an Out-of-Tree block, but is optional)
Wavetrap works with
Ettus B2xx Radios, RTL-SDR Dongles and the LimeSDR-mini but can easily be modified to include other SDR's.
![GUI screenshot](https://github.com/muaddib1984/wavetrap/blob/main/flowgraph_images/wavetrap_fosphor_gui.png)


## DEPENDENCIES:
[GNURadio 3.9+](https://github.com/gnuradio/gnuradio)

[gr-fosphor (optional)](https://github.com/osmocom/gr-fosphor)

## SETUP/FEATURES:
Features include:
-Momentary Push-Button Recording 
-GREEN/RED Recording Indicator
-Double Click Re-Tune in the Spectrum Window
-Automated Dynamic File naming which includes the following metadata about the recording in the filename:
    -Date/Time
    -Center Frequency
    -Bandwidth
    -Sample Rate
    -Gain 
    -Recording Note (user's comment on the current recording)

These parameters will automatically update between recordings, so if you take a recording, re-tune and take another, the filenames will reflect the correct frequency each time you make a recording.

-File Management
    -puts recordings in 'home/user/data' by default
    -change one path variable to adjust the subdirectory under /home/userpath

SETUP:
Pretty simple.
1) Create a directory called 'data' in your /home/<username> path
2) Open the flowgraph that corresponds to your SDR hardware
    -UHD
    -Lime
    -RTL
(you can change the 'data' directory to whatever you want by modifying the 'record_file_path' variable in the flowgraph)

### USAGE:

1) Run the flowgraph
2) Tune to the frequency you are interested in recording using the Message Edit Box. You can tune the frequency by simply double clicking on the spectrum window or entering the frequency in the Message Edit Box.
3) Enter a description of the recording in the 'RECORDING_NOTE' box and press enter to update the field. This will be included in the filename for easy identification later.
4) When you are ready to record, click and hold the 'RECORD'. The LED Indicator Widget will change from GREEN to RED.
5) Once you release the recording button, open the 'data' directory or the one you made to confirm the file is there.

![GUI screenshot](https://github.com/muaddib1984/wavetrap/blob/main/flowgraph_images/wavetrap_fosphor_recording.png)

###FLOWGRAPHS

**WAVETRAP UHD:**
![GUI screenshot](https://github.com/muaddib1984/wavetrap/blob/main/flowgraph_images/uhd_wavetrap.png)

**WAVETRAP RTL:**
![GUI screenshot](https://github.com/muaddib1984/wavetrap/blob/main/flowgraph_images/rtl_wavetrap.png)

**WAVETRAP LIME:**
![GUI screenshot](https://github.com/muaddib1984/wavetrap/blob/main/flowgraph_images/lime_wavetrap.png)

