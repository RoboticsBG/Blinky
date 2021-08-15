# Blinky UI v.0.0.3
## Simple Python Human Eyeblinks Counter

Uses a standard webcam to capture eye blinks. 
Added QT UI that allows to play media file via VLC.
This allows time syncronization of the measured blinks with the media playback.
Blink events are saved in standard CSV format for further processing.

Please feel free to use and modify this code for your own puroposes.

LICENSE: Simplified BSD License  

Source based on Neha Chaudhari / AlgoAsylum code. Read the original article here: https://medium.com/algoasylum/blink-detection-using-python-737a88893825

DLIB facial landmark file can be downloaded from here: http://dlib.net/files/shape_predictor_68_face_landmarks.dat.bz2


## 1. Install instructions (Mac)

Assumes that you have already installed Command Line Tool package and Pip.
 
- Open Terminal app.

- Go to the folder from where you will use Blinky: cd ~/Downloads/

- Clone the repo with: git clone https://github.com/RoboticsBG/Blinky

- Go the Blinky folder: cd Blinky

Issue the following commands:

    pyenv shell 3.9.1

    pip install PyQt5

    pip install python-vlc
 
    chmod +x Blinky.py

## 2. How to run

- Open Downloads/Blinky with Finder

- Click on the start.command - if all is installed OK, the program interface should appear.

- Click on "Choose Video" and choose media file to open - mp4, mov, avi, mkv, mp3, wav

The file will start playing and the EyeBlink detection will be simultaneously activated.

## 3. How to Exit
If you need to exit the program before the media is fully played use the Esc key. Important - the window with the camera image should be on focus in order to use Esc key to exit.

If you cannot exit gracefuly, please close the Terminal window. In this case the current mesurement data will not be saved.

If you finish the measurements with success you will find in the folder Downloads/Blinky a file named as follows:
blink-recording--DDMMYYYY-HHMMSS.csv 

You can open and edit this file with a Spreadsheet program like Numbers, Excel or Open office Calc