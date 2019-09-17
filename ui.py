from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import cv2
from threading import Thread
from PIL import Image
from show import ShowImages 
from classification import Classification
from recorder import VideoRecorder
import pandas as pd
import numpy as np
class Ui_MainWindow(object):
    def __init__(self):
        super().__init__()        
        self.defaultmap = QtGui.QPixmap("default.png")
        self.processmap = QtGui.QMovie("procession.gif")
        self.images = []
        self.emotions = []
        self.labelfont = QtGui.QFont('Times',12)   
        self.analysis = Classification()
        self.mainWindow = None

        # for storing data
        self.capturePixels = None

    def closeEvent(self,event):
        buttonReply = QMessageBox.question(self.mainWindow, 'Closing Message', "Are You Sure To Exit ?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if buttonReply == QMessageBox.Yes:            
            print('Yes clicked.')
            self.video.status = False
            self.app.exit()
            event.accept()
        else:
            print('No clicked.')
            event.ignore()




    def setupVideoFrame(self):
        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setGeometry(QtCore.QRect(5, 10, 650, 400))
        self.frame.setFrameShape(QtWidgets.QFrame.Box)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setMidLineWidth(2)
        self.frame.setObjectName("frame")
        self.videoLabel = QtWidgets.QLabel(self.frame)  
        #self.videoLabel.setFixedWidth(300)
        self.videoLabel.setGeometry(4, 5, 650, 400);  
        self.pushButton = QtWidgets.QPushButton(self.frame)
        self.pushButton.setGeometry(QtCore.QRect(50, 50, 150, 30))
        self.pushButton.setObjectName("pushButton")
    
    
    def setupFrame3(self):                 
        self.changelbl = QtWidgets.QLabel(self.centralwidget)
        self.changelbl.setText('Change Emotions (Learn / Update Datasets ) :  ')
        self.changelbl.setFont(self.labelfont)
        self.changelbl.setGeometry(QtCore.QRect(670, 1, 600, 100))

        self.frame_3 = QtWidgets.QFrame(self.centralwidget)
        self.frame_3.setGeometry(QtCore.QRect(660, 100, 650, 100))
        self.frame_3.setFrameShape(QtWidgets.QFrame.Box)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_3.setMidLineWidth(1)
        self.frame_3.setObjectName("frame_3")        
        self.grid3 = QGridLayout(self.frame_3)
        self.frame_3.setLayout(self.grid3)

        self.setupComboBox()
        self.setupButton()


    def setupFrame2(self):         
        self.emotlbl = QtWidgets.QLabel(self.centralwidget)
        self.emotlbl.setText('Your Capture Faces ')
        self.emotlbl.setFont(self.labelfont)
        self.emotlbl.setGeometry(QtCore.QRect(10, 380, 600, 100))

        self.frame_2 = QtWidgets.QFrame(self.centralwidget)
        self.frame_2.setGeometry(QtCore.QRect(5, 450, 1200, 200))
        self.frame_2.setFrameShape(QtWidgets.QFrame.Box)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setMidLineWidth(1)
        self.frame_2.setObjectName("frame_2")
        
        self.grid = QGridLayout(self.frame_2)
        self.frame_2.setLayout(self.grid)

        # self.lbl2 = QtWidgets.QLabel()
        # self.lbl2.setFont(self.labelfont)
        # self.lbl2.setText("Faces")
        # self.grid.addWidget(self.lbl2,0,0)

        self.img1 = QtWidgets.QLabel()
        self.grid.addWidget(self.img1,0,0)
        self.img1.setPixmap(self.defaultmap)  

        self.img2 = QtWidgets.QLabel()
        self.grid.addWidget(self.img2,0,1)
        self.img2.setPixmap(self.defaultmap)  

        self.img3 = QtWidgets.QLabel()
        self.grid.addWidget(self.img3,0,2)
        self.img3.setPixmap(self.defaultmap)  

        self.img4 = QtWidgets.QLabel()
        self.grid.addWidget(self.img4,0,3)
        self.img4.setPixmap(self.defaultmap)  

        self.img5 = QtWidgets.QLabel()
        self.grid.addWidget(self.img5,0,4)
        self.img5.setPixmap(self.defaultmap)  

        self.em1 = QtWidgets.QLabel()
        self.em1.setFont(self.labelfont)
        self.grid.addWidget(self.em1,1,0)
        self.em2 = QtWidgets.QLabel()
        self.em2.setFont(self.labelfont)
        self.grid.addWidget(self.em2,1,1)
        self.em3 = QtWidgets.QLabel()
        self.em3.setFont(self.labelfont)
        self.grid.addWidget(self.em3,1,2)
        self.em4 = QtWidgets.QLabel()
        self.em4.setFont(self.labelfont)
        self.grid.addWidget(self.em4,1,3)
        self.em5 = QtWidgets.QLabel()
        self.em5.setFont(self.labelfont)
        self.grid.addWidget(self.em5,1,4)
        
        
        self.emotions.append(self.em1)
        self.emotions.append(self.em2)
        self.emotions.append(self.em3)
        self.emotions.append(self.em4)
        self.emotions.append(self.em5)

        self.images.append(self.img1)
        self.images.append(self.img2)
        self.images.append(self.img3)
        self.images.append(self.img4)
        self.images.append(self.img5)  

    def setupButton(self):
        self.bt1 = QtWidgets.QPushButton("OK")
        self.bt2 = QtWidgets.QPushButton("OK")
        self.bt3 = QtWidgets.QPushButton("OK")
        self.bt4 = QtWidgets.QPushButton("OK")
        self.bt5 = QtWidgets.QPushButton("OK")
        self.updateBT = QtWidgets.QPushButton("Update Emotions")

        self.bt1.clicked.connect(self.changeEmotion1)
        self.bt2.clicked.connect(self.changeEmotion2)
        self.bt3.clicked.connect(self.changeEmotion3)
        self.bt4.clicked.connect(self.changeEmotion4)
        self.bt5.clicked.connect(self.changeEmotion5)

        self.updateBT.clicked.connect(self.updateEmotionsIntoCSV)

        self.grid3.addWidget(self.bt1,1,0)
        self.grid3.addWidget(self.bt2,1,1)
        self.grid3.addWidget(self.bt3,1,2)
        self.grid3.addWidget(self.bt4,1,3)
        self.grid3.addWidget(self.bt5,1,4)

        self.grid3.addWidget(self.updateBT,2,0)

    def setupComboBox(self):
        self.box1 = QtWidgets.QComboBox()        
        self.box1.addItem("Angry",0)
        self.box1.addItem("Disgust",1)
        self.box1.addItem("Fear",2)
        self.box1.addItem("Happy",3)
        self.box1.addItem("Sad",4)
        self.box1.addItem("Surprise",5)
        self.box1.addItem("Normal",6)

        self.box2 = QtWidgets.QComboBox()        
        self.box2.addItem("Angry",0)
        self.box2.addItem("Disgust",1)
        self.box2.addItem("Fear",2)
        self.box2.addItem("Happy",3)
        self.box2.addItem("Sad",4)
        self.box2.addItem("Surprise",5)
        self.box2.addItem("Normal",6)

        self.box3 = QtWidgets.QComboBox()        
        self.box3.addItem("Angry",0)
        self.box3.addItem("Disgust",1)
        self.box3.addItem("Fear",2)
        self.box3.addItem("Happy",3)
        self.box3.addItem("Sad",4)
        self.box3.addItem("Surprise",5)
        self.box3.addItem("Normal",6)

        self.box4 = QtWidgets.QComboBox()        
        self.box4.addItem("Angry",0)
        self.box4.addItem("Disgust",1)
        self.box4.addItem("Fear",2)
        self.box4.addItem("Happy",3)
        self.box4.addItem("Sad",4)
        self.box4.addItem("Surprise",5)
        self.box4.addItem("Normal",6)

        self.box5 = QtWidgets.QComboBox()        
        self.box5.addItem("Angry",0)
        self.box5.addItem("Disgust",1)
        self.box5.addItem("Fear",2)
        self.box5.addItem("Happy",3)
        self.box5.addItem("Sad",4)
        self.box5.addItem("Surprise",5)
        self.box5.addItem("Normal",6)

        
        self.grid3.addWidget(self.box1,0,0)
        self.grid3.addWidget(self.box2,0,1)
        self.grid3.addWidget(self.box3,0,2)
        self.grid3.addWidget(self.box4,0,3)
        self.grid3.addWidget(self.box5,0,4)
        


    def setupUi(self, MainWindow):
        self.mainWindow = MainWindow
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(900, 700)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.setupVideoFrame()
        self.setupFrame2()
        self.setupFrame3()
        
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.pushButton.clicked.connect(self.startCapturing)
        self.pushButton.setFont(self.labelfont)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        MainWindow.closeEvent  = self.closeEvent
        video = VideoRecorder(self)
        self.video = video 
        video.start()

    def startCapturing(self):
        capture  = self.CaptureEmotions(self)
        capture.start()

    def changeEmotion1(self):
        txt = self.box1.currentIndex()
        print(txt)
        self.capturePixels.iloc[0,2304] = txt
    def changeEmotion2(self):
        txt = self.box2.currentIndex()
        print(txt)     
        self.capturePixels.iloc[1,2304] = txt
    def changeEmotion3(self):
        txt = self.box3.currentIndex()
        print(txt)     
        self.capturePixels.iloc[2,2304] = txt
    def changeEmotion4(self):
        txt = self.box4.currentIndex()
        print(txt)     
        self.capturePixels.iloc[3,2304] = txt
    def changeEmotion5(self):
        txt = self.box5.currentIndex()
        print(txt)               
        self.capturePixels.iloc[4,2304] = txt

    def updateEmotionsIntoCSV(self):
        #self.capturePixels.to_csv('./dataset/emotions_prepare.csv') 
        for i in self.capturePixels.index:
            row = self.capturePixels.iloc[i,:]
            with open('./dataset/emotions_prepare.csv','a') as fd:
                #vals = [','.join(str(ele)) for ele in row]                
                rw = ""
                for r in row:
                    rw += str(r) + "," 
                vals = rw + "\n"                
                fd.write(vals)    
        self.capturePixels = None             
        
    def processingGIF(self):
        print("set GIF")
        self.videoLabel.setMovie(self.processmap)    

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButton.setText(_translate("MainWindow", "Start Capture"))

    class CaptureEmotions(Thread):    
        def __init__(self,uiobj):
            super().__init__()
            self.uiobj = uiobj
        def run(self):
            imgarray = self.uiobj.video.live_image[0]
           
            print(len(imgarray))
            
            self.uiobj.video.status = False
           
            flat_np_array = []
            a=1
            for i in imgarray:
                if a==6:
                    break
                image = i
                
                gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                gray_image = cv2.resize(gray_image, (48, 48))
                flat_np = gray_image.flatten()
                                       
                
                emotion,emotionNumber = self.uiobj.analysis.svm(flat_np)

                # Store Flat array into list
                flat_np =  np.append(flat_np,emotionNumber)
                flat_np_array.append(flat_np)
                
                filename = emotion + '_faces_' + str(a) + ".jpg"
            
                cv2.imwrite("./pics/"+ filename, i)
                
                showThread = ShowImages(self.uiobj,filename,a-1)
                showThread.start()
                a+=1

            # Make DataFrame for new pixels
            self.uiobj.capturePixels = pd.DataFrame(flat_np_array)
            #print(self.uiobj.capturePixels)
            #self.uiobj.capturePixels.to_csv('./dataset/emotions_prepare.csv')
            
            #with open('document.csv','a') as fd:
            #    fd.write(myCsvRow)
            video = VideoRecorder(self.uiobj)
            self.uiobj.video = video 
            video.start()
        

