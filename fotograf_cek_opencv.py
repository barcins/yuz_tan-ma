import cv2 #kütüphane ekleme işlemi
from imutils import paths
import os, time
import numpy as np
from datetime import datetime


yuzprogramı = cv2.CascadeClassifier("kutuphane.xml") #kullanacağmız hazır yüz bulma programı
yuzprogramı = cv2.CascadeClassifier("classifier/haarcascade_frontalface_default.xml")


faceCascade = cv2.CascadeClassifier("classifier/haarcascade_frontalface_default.xml")
video_capture = cv2.VideoCapture(0)
kimler = os.getcwd() + "/dataset/_kimler/"

while True:
    # kare kare webcam den gelen görüntü yakalanıyor
    ret, frame = video_capture.read()

    griresim = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)#resmimizi griye donuştürme
    program = yuzprogramı.detectMultiScale(frame,1.3,3)#programı çalıştırma (taranacak resim,büyütme oranı,kontrol sayısı)
    program = yuzprogramı.detectMultiScale(frame, 1.1, 5, minSize=(100,100)) # Frame'deki yüzlerin yerlerini tespit etme

    
    for (a,b,c,d) in program : # (x,y,w,h)

        test = gray[a:a+c,b:b+d]
        test_img = np.array(test,'uint8')

        cv2.rectangle(frame,(a,b),(a+c,b+d),(255,0,0),2) #burada bulduğumuz insan yüzlerini kare içide alma işlemini yapıyoruz
        #(yüzlerin gösterileceği resim,(köşe ayarlama)(köşe ayarlama),(karenin rengi),karenin kalınlığı)
    

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) # Frame renklerini gri tonlara ayarlama
    faces = yuzprogramı.detectMultiScale(gray, 1.1, 5, minSize=(100,100)) # Frame'deki yüzlerin yerlerini tespit etme


    file_name = kimler + datetime.now().strftime('%Y-%m-%d_%H-%M-%S.jpg' ) 

    for (x,y,w,h) in faces: # Yüzleri işaretleme
        test = gray[x:x+w,y:y+h]
        test_img = np.array(test,'uint8')
        if(test_img.any()): # Frame içinde yüz varsa tahmin yapma
            cv2.rectangle(frame, (x,y), (x+w,y+h), (250, 150, 250) ,2)



            cv2.rectangle(frame, (x-100,y-100), ( (x+100) + (w) ,y+h+100), (0, 250, 250) ,5) # test kısmı sarı



            face = frame[  (y-100) : (y) + (h) + 100,     (x)-100 : (x) + (w)  + 100]  # (x,y,w,h) 

            #cv2.imwrite(file_name, face)
            cv2.waitKey(1)
            print("[INFO] Foto çekildi")





     


    # Sonuç ekranda gösteriliyor.
    cv2.imshow('Video', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# herşey tamamsa ekran yakalaması serbest bırakılıyor.
video_capture.release()
cv2.destroyAllWindows()



