from sklearn.svm import SVC
import pandas as pd
import numpy as np

class Classification:
    def __init__(self):
        self.loadEmotionDataset()

    def loadEmotionDataset(self):
        print("Read Emotion CSV")
        self.emotionsDF = pd.read_csv('./dataset/emotion.csv')
        self.emotionsDF = self.emotionsDF.drop(['Unnamed: 0'], axis=1)
        self.data = self.emotionsDF.iloc[:, 0:2304].values
        self.emot = self.emotionsDF['emotion'].values
        print("Reading END")    

    def svm(self,flat_np):
        clf = SVC(kernel='linear')
        clf = clf.fit(self.data, self.emot)
        y_pred = clf.predict(flat_np.reshape(1,-1))
        Y = y_pred[0]
        emotion = ""
        if Y==0:
            emotion = "angry"
        elif Y==1:
            emotion = "disgust"
        elif Y==2:
            emotion = "fear"
        elif Y==3:
            emotion = "happy"
        elif Y==4:
           emotion = "sad"
        elif Y==5:
            emotion = "surprise"
        elif Y==6:
            emotion = "normal"
        return emotion.capitalize(),Y
