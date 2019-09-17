import time
from PyQt5 import QtGui
from threading import Thread

class ShowImages(Thread):
    def __init__(self,ui,filename,index):
        super().__init__()
        self.ui = ui
        self.filename = filename
        self.index = index
    
    def run(self):
        map = QtGui.QPixmap("./pics/" + str(self.filename))
        self.ui.images[self.index].setPixmap(map)  
        emot = self.filename.split('_')[0]
        self.ui.emotions[self.index].setText(emot)        
        print("Show Thread End")            