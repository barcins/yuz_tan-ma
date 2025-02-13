#!usr/bin/env python  
#coding=utf-8  
import speech_recognition as sr
import pyttsx3 , threading
import os
import glob
from pathlib import Path
import pyaudio  
import wave  
from playsound import playsound


def ses_to_yazi():
    r = sr.Recognizer()
    r.energy_threshold=4000 # ses eşik değeri

    def SpeakText(command):
        # yazıyı sesli olarak oku
        engine = pyttsx3.init()
        engine.say(command) 
        engine.runAndWait()

    


    def ses_to_yazi(file):
        try:
            hellow=sr.AudioFile(file) # kayıtdaki sesi alma
            with hellow as source: 
                audio = r.record(source)

            MyText = r.recognize_google(audio, language='tr-tr')
            MyText = MyText.lower()
            if len(MyText) > 0:
                print("Konusma;",MyText) #SpeakText(MyText)
        except sr.UnknownValueError:
            pass
        except sr.RequestError as e:
        # print("Could not request results from Google Speech Recognition service; {0}".format(e))
            pass


    okunanlar = []
    while  True:
        os.chdir("audio") # ses dosyalarının bulunduğu klasöre git
        files = sorted(filter(os.path.isfile, os.listdir('.')), key=os.path.getmtime) # ses dosyaları listele kayıt tarihine göre sırala
        for arr in okunanlar:
            if arr not in files:
                files.remove(arr)
        for file in files:
            if file not in okunanlar:   
                playsound(file) # kayıtlı ses dosyasını çal
                try:
                    # kayıtdaki sesi yazıya çevirme.
                    t3 = threading. Thread(target=ses_to_yazi, args=[file])
                    t3.start()
                except sr.RequestError as e:
                    print("RequestError:", e)
                except sr.UnknownValueError as e:
                    pass

                okunanlar.append(file)
                print(okunanlar)



#ses_to_yazi()
