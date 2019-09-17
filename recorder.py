from threading import Thread
import cv2
import numpy as np
from PyQt5 import QtCore
from PIL import Image
from PyQt5 import QtGui
from cv2 import *

class VideoRecorder(Thread):
    def __init__(self,ui):
        super().__init__()
        self.ui = ui
        self.cap = cv2.VideoCapture(0)
        self.live_image = [[]]
        self.running = True
        self.status = True
        self.deleteOldFiles()

    
    def deleteOldFiles(self):
        folder = './pics/'
        for the_file in os.listdir(folder):
            file_path = os.path.join(folder, the_file)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
                #elif os.path.isdir(file_path): shutil.rmtree(file_path)
            except Exception as e:
                print(e)

  

    def run(self):
        while self.status:            
            #time.sleep(1)
            if self.running:
                ret, image_np = self.cap.read()
                #image_np = cv2.flip( image_np, 1 )
                gray_image = cv2.cvtColor(image_np, cv2.COLOR_BGR2GRAY)
                haar_cascade_face = cv2.CascadeClassifier('./data/haarcascades/haarcascade_frontalface_alt.xml')
                faces_rects = haar_cascade_face.detectMultiScale(gray_image, scaleFactor = 1.2, minNeighbors = 5)
                
                imgs = [] 
                for (x,y,w,h) in faces_rects:
                    cv2.rectangle(image_np, (x, y), (x+w, y+h), (0, 255, 0), 2)
                    imgs.append(image_np[y:y + h, x:x + w])
                    # print("[INFO] Object found. Saving locally.")
                    # cv2.imwrite(str(w) + str(h) + '_faces.jpg', roi_color)
                self.live_image[0] = imgs                

                # height, width, channel = image_np.shape
                # bytesPerLine = 3 * width
                # qImg = QtGui.QImage(image_np.data, width, height, bytesPerLine,QtGui.QImage.Format_RGB888)
                # pixmap = QtGui.QPixmap(qImg)
                #self.ui.videoLabel.setPixmap(pixmap)

                height, width, channel = image_np.shape
                img = QtGui.QImage(image_np.data, width, height ,QtGui.QImage.Format_RGB888)
                convertToQtFormat = QtGui.QPixmap.fromImage(img)
                pixmap = QtGui.QPixmap(convertToQtFormat)
                resizeImage = pixmap.scaled(640, 480, QtCore.Qt.KeepAspectRatio)               
                self.ui.videoLabel.setPixmap(resizeImage)
        self.ui.processingGIF()
        print("Record Thread End")        