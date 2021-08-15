import sys

import vlc
from PyQt5.QtCore import QDir, Qt, QUrl
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel, QPushButton, QFileDialog
import cv2
import dlib
import math
from datetime import datetime
import time
from threading import Thread

BLINK_RATIO_THRESHOLD = 5.7
RunBlink=True
measurements="";
pname="Unknown";
vlFile="";


def midpoint(point1 ,point2):
    return (point1.x + point2.x)/2,(point1.y + point2.y)/2

def euclidean_distance(point1 , point2):
    return math.sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)

def get_blink_ratio(eye_points, facial_landmarks): 
         corner_left  = (facial_landmarks.part(eye_points[0]).x, 
                         facial_landmarks.part(eye_points[0]).y)
         corner_right = (facial_landmarks.part(eye_points[3]).x, 
                         facial_landmarks.part(eye_points[3]).y)
    
         center_top    = midpoint(facial_landmarks.part(eye_points[1]), 
                         facial_landmarks.part(eye_points[2]))
         center_bottom = midpoint(facial_landmarks.part(eye_points[5]), 
                             facial_landmarks.part(eye_points[4]))
         horizontal_length = euclidean_distance(corner_left,corner_right)
         vertical_length = euclidean_distance(center_top,center_bottom)
         ratio = horizontal_length / vertical_length
         return ratio	

class SimplePlayer(QMainWindow):

    def __init__(self, master=None):
        QMainWindow.__init__(self, master)

        # Define file variables
        self.playlist = ['']

        # Define the QT-specific variables we're going to use
        self.vertical_box_layout = QVBoxLayout()
        self.central_widget = QWidget(self)
        self.video_frame = QLabel()
        self.openButton = QPushButton("Choose video")
        #self.quitButton = QPushButton("Save and Exit")
        # Define the VLC-specific variables we're going to use
        self.vlc_instance = vlc.Instance('--quiet')
        self.vlc_player = self.vlc_instance.media_list_player_new()
        self.media_list = self.vlc_instance.media_list_new(self.playlist)
       
        
        # Create the user interface, set up the player, and play the 2 videos
        self.create_user_interface()

    def video_player_setup(self):
        """Sets media list for the VLC player and then sets VLC's output to the video frame"""
        self.vlc_player.set_media_list(self.media_list)
        self.vlc_player.get_media_player().set_nsobject(int(self.video_frame.winId()))

    def create_user_interface(self):
        """Create a 1280x720 UI consisting of a vertical layout, central widget, and QLabel"""
        self.setCentralWidget(self.central_widget)
        self.vertical_box_layout.addWidget(self.video_frame)
       
        self.vertical_box_layout.addWidget(self.openButton)
        #self.vertical_box_layout.addWidget(self.quitButton)

        self.openButton.clicked.connect(self.openFile)
        #self.quitButton.clicked.connect(self.graceQuit) 
        self.central_widget.setLayout(self.vertical_box_layout)

        #self.resize(1280, 720)
        self.showMaximized()
    def openFile(self):
        fileName, _ = QFileDialog.getOpenFileName(self, "Open Movie",
                QDir.homePath()+"/Downloads/")
        global measurements
        global vlFile
         
        if fileName != '':
        	#self.playButton.setEnabled(True)
        	vlFile=QUrl.fromLocalFile(fileName).toLocalFile()
        	measurements+="VideoFile: "+fileName+"\n"
        	self.video_player_setup()
        	self.playlist = vlFile
        	self.vlc_player.play()
        	#vlc_player.set_fullscreen(self)
        	RunBlink=True
        	w = Blink()

        	t1 = Thread(target=w.show())
        	t1.start()
        	t1.join()
        	#w.show()
        	self.graceQuit()
    def graceQuit(self):
    	  #Clean Exit
    	  global RunBlink
    	  global measurements
    	  RunBlink=False
    	  w=None
    	  measurements+=datetime.now().strftime('%H:%M:%S.%f')[:-3]+";End\n"  
    	  print(measurements)
    	  rectime=datetime.now().strftime('-%d%m%Y-%H%M%S')
    	  text_file = open("blink-recording-"+rectime+".csv", "w")
    	  text_file.write(measurements)
    	  text_file.close()
    	  self.close() 

class Blink(QWidget):
   def __init__(self):
     super().__init__()
     layout = QVBoxLayout()
     global measurements
     global RunBlink
     self.label = QLabel("Another Window")
     layout.addWidget(self.label)
     self.setLayout(layout)
	   #livestream from the webcam 
     cap = cv2.VideoCapture(0)
     #name of the display window in openCV
     cv2.namedWindow('BlinkDetector',cv2.WINDOW_NORMAL)
     #cv2.resizeWindow('BlinkDetector', 150,100)

     #-----Step 3: Face detection with dlib-----
     detector = dlib.get_frontal_face_detector()

     #-----Step 4: Detecting Eyes using landmarks in dlib-----
     predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")
     #these landmarks are based on the image above 
     left_eye_landmarks  = [36, 37, 38, 39, 40, 41]
     right_eye_landmarks = [42, 43, 44, 45, 46, 47]
     measurements+="Tested Person: "+pname+"\n"
     measurements+="Start Date: "+datetime.now().strftime('%d.%m.%Y')+"\n"
     measurements+="Start Time: "+datetime.now().strftime('%H:%M:%S.%f')[:-3]+"\n"
     measurements+="Software: IR Blink Detector v.1.2\n"
     measurements+=datetime.now().strftime('%H:%M:%S.%f')[:-3]+";Start\n"
     bb=0  
     while RunBlink:
           #True:
           #capturing frame
           retval, frame = cap.read()
           #exit the application if frame not found
           if not retval:
                 print("Can't receive frame (stream end?). Exiting ...")
                 break 

           frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
           faces,_,_ = detector.run(image = frame, upsample_num_times = 0, adjust_threshold = 0.0)

           for face in faces:
                landmarks = predictor(frame, face)
                left_eye_ratio  = get_blink_ratio(left_eye_landmarks, landmarks)
                right_eye_ratio = get_blink_ratio(right_eye_landmarks, landmarks)
                blink_ratio     = (left_eye_ratio + right_eye_ratio) / 2
                if blink_ratio > BLINK_RATIO_THRESHOLD:
                          #Blink detected! Do Something! 
                          cv2.putText(frame,"BLINKING",(10,50), cv2.FONT_HERSHEY_SIMPLEX,2,(255,255,255),2,cv2.LINE_AA)
                          cv2.putText(frame,"BLINKING",(10,70), cv2.FONT_HERSHEY_SIMPLEX,2,(0,0,0),2,cv2.LINE_AA)
                          
                          #print(datetime.now().strftime('%H:%M:%S.%f')[:-3])
                          if (bb==0): 
                              measurements+=datetime.now().strftime('%H:%M:%S.%f')[:-3]+";Blink\n"
                              bb=1
                          else: bb=0
  
           img = cv2.resize(frame, (150, 100))
           cv2.imshow('BlinkDetector', img)
           key = cv2.waitKey(1)
           if key == 27:
               print("===");
               print("End Time: "+datetime.now().strftime('%H:%M:%S.%f')[:-3])
               break

     #releasing the VideoCapture object
     cap.release()
     cv2.destroyAllWindows()


if __name__ == '__main__':
    app = QApplication([])
    player = SimplePlayer()
    player.show()
    sys.exit(app.exec_())

