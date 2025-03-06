#!usr/bin/env python  
#coding=utf-8  
import speech_recognition as sr
import pyttsx3 , threading
import os
import glob
from pathlib import Path
import pyaudio  
import wave ,time
from playsound import playsound
from datetime import datetime

old_path =  os.getcwd()
audio_path = os.getcwd() + "/audio/"

time.sleep(5)

r = sr.Recognizer()
r.energy_threshold=4000 # ses eşik değeri


def ses_to_yazi_fonk():
    def ses_to_yazi(file):
        def SpeakText(command):
            # yazıyı sesli olarak oku
            engine = pyttsx3.init()
            engine.say(command) 
            engine.runAndWait()

        try:
            hellow=sr.AudioFile(file) # kayıtdaki sesi alma
            with hellow as source: 
                audio = r.record(source)

            MyText = r.recognize_google(audio, language='tr-tr')
            MyText = MyText.lower()
            if len(MyText) > 0:
                f = open("log_audio.txt", "a")
                #print("Konusma;",MyText) #SpeakText(MyText)
                f.write("{0} -- {1}\n".format(datetime.now().strftime("%Y-%m-%d %H:%M"), MyText))
                f.close()
        except sr.UnknownValueError:
            pass
        except sr.RequestError as e:
        # print("Could not request results from Google Speech Recognition service; {0}".format(e))
            pass


    okunanlar = []
    while  True:
        files = glob.glob(audio_path+"*.wav")
        if files:
            files_sort = sorted(files, key=os.path.getmtime)
            files_time = [os.path.getmtime(file) for file in files_sort]
            for file in files_sort:
                if os.path.getmtime(file) not in okunanlar:   
                    
                    try:
                        #print(file, os.path.getmtime(file))
                        playsound(file) # kayıtlı ses dosyasını çal
                        # kayıtdaki sesi yazıya çevirme.
                        t3 = threading. Thread(target=ses_to_yazi, args=[file])
                        t3.start()
                    except Exception as err:
                        print("ses_to_yazi_fonk Err:", err, file, os.path.getmtime(file))

                    okunanlar.append(os.path.getmtime(file))
                    if not okunanlar:
                        for arr in okunanlar:
                            if arr not in files_time:
                                okunanlar.remove(arr)
                                print("kontrol files.remove(arr)", arr)

            time.sleep(5)


#ses_to_yazi_fonk()
