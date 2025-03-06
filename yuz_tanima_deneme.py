import cv2, sys, os, re
import numpy as np
from math import ceil


def zoom(img, zoom_factor=2):
    return cv2.resize(img, None, fx=zoom_factor, fy=zoom_factor)    


# Haar cascade classifier yükleme
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

frame = 0

print("sys:", sys.argv)

if(len(sys.argv)>1):
   if(sys.argv[1]=='foto'): # Video
      frame = cv2.imread('foto.jpg') # Fotoğraf dosyası okuma
   elif(sys.argv[1]=='video'): # Video
      video_capture = cv2.VideoCapture('video.mp4') # Video dosyası okuma
   elif(sys.argv[1]=='kamera'): # Kamera
      video_capture = cv2.VideoCapture(0)  # Birden fazla kamera bulunan bilgisayarlarda 0 değeri değişebilir.
   else:
      video_capture = cv2.VideoCapture('video.mp4')         
else:
   video_capture = cv2.VideoCapture('video.mp4')        
   
recognizer = cv2.face.LBPHFaceRecognizer_create() 
min_confidence = 10

# Yüz verilerini okuma
def get_face_data():
    images = [] # Fotoğraf listesi oluşturma
    image_label = [] # Fotoğraf isim listesi oluşturma
    names = [] # Dizin adı listesi oluşturma
    cd = os.getcwd() # Programın çalıştığı dizini elde etme
    dir_faces = os.path.join(cd, 'dataset') # Çalışma dizinine faces dizinini ekleme
    folders = os.listdir(dir_faces) # faces dizini içindeki dizinlerin listesini alma
	
    # Faces dizini altındaki her bir dizin için işlem yapma
    for id1 in range(len(folders)):
        names.append(folders[id1]) # Faces dizini altındaki dizin adını names listesine ekleme 
        dir_per = os.path.join(dir_faces, folders[id1]) # Her bir kişiye ait dizin yol tanımlaması 

        if not re.search(".DS_Store", dir_per) :
            folder_imgs = os.listdir(dir_per) # Her bir kişiye ait dizin içindeki fotoğraf dosyalarını alma
            # Her bir kişiye ait dizin içindeki her bir fotoğrafa işlem yapma
            for id2 in folder_imgs:
                im = cv2.imread(os.path.join(dir_per, id2), 0) # Her bir kişiye ait dizinde bulunan fotğraf dosyası yol tanımlaması 
                faces = face_cascade.detectMultiScale(im, 1.1, 5, minSize=(50,50)) # Fotoğraf dosyaları içindeki yüzleri alma
                # Her bir yüze işlem yapma			
                for (x,y,w,h) in faces:
                    img_array = np.array(im[x:x+w,y:y+h],'uint8')
                    images.append(img_array) # Yüz bilgilerini images listesine ekleme
                    image_label.append(id1) # Kişi adını image_label listesine ekleme

    cv2.destroyAllWindows()
	
    return images, image_label, names

# Training işlemi
image_data, labels, names = get_face_data()
recognizer.train(image_data, np.array(labels))

video_capture = cv2.VideoCapture(0)
while True:    


    ret, frame = video_capture.read()
    print(sys.argv)


    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) # Frame renklerini gri tonlara ayarlama
    faces = face_cascade.detectMultiScale(gray, 1.1, 5, minSize=(100,100)) # Frame'deki yüzlerin yerlerini tespit etme
    for (x,y,w,h) in faces: # Yüzleri işaretleme
        cv2.rectangle(frame, (x,y), (x+w,y+h), (250, 150, 250) ,2)
        test = gray[x:x+w,y:y+h]
        test_img = np.array(test,'uint8')
        if(test_img.any()): # Frame içinde yüz varsa tahmin yapma
            index, confidence = recognizer.predict(test_img)
        if(confidence>=min_confidence): # Tahmin değerini ekrana yazma
           cv2.putText(frame,names[index],(x,y+h+20),cv2.FONT_HERSHEY_DUPLEX,.5,(0,255,0)) # Kişi adını yazma
           cv2.putText(frame,str(ceil(confidence))+"%",(x,y-20),cv2.FONT_HERSHEY_DUPLEX,.5,(0,255,0)) # Güvenilirlik derecesini yazma

    cv2.imshow('dataset', frame) # Yüzlerin işaretlendiği datasetğrafı ekranda gösterme
    cv2.waitKey(0) # Herhangi bir tuşa basıldığında program sona erer.
        
    cv2.imshow('Video', frame) # Frame'i ekranda gösterme
    k = cv2.waitKey(1) & 0xFF
    if k == 27: # Esc tuşu ile çıkış
       break

if(sys.argv[1]!='dataset'):
   video_capture.release()
cv2.destroyAllWindows()
