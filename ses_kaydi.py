
import pyaudio, os, threading
import wave
from datetime import datetime
import cv2, time, glob

ses_kaydi = os.getcwd() + "/audio/"

print(pyaudio.PyAudio().get_default_input_device_info())
for i in range(pyaudio.PyAudio().get_device_count()):
    dev = pyaudio.PyAudio().get_device_info_by_index(i)
    #print((i,dev['name'],dev['maxInputChannels']))



p = pyaudio.PyAudio()
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
RECORD_SECONDS = 10
KAYITSAYISI = 4


def ses_dosyalarini_sil():
    old_path =  os.getcwd()
    audio_path = os.getcwd() + "/audio/"
    for file in glob.glob(audio_path+"*.wav"):
        os.remove(file) # okunmuş eski dosyaları siliyoruz 

def kaydi_kaydet(frames, ses_dosya_sayac):
    WAVE_OUTPUT_FILENAME = ses_kaydi  + "ses_kaydi_" + str(ses_dosya_sayac) + "_" + datetime.now().strftime('%Y-%m-%d_%H-%M-%S.wav') 
    WAVE_OUTPUT_FILENAME = ses_kaydi  + "ses_kaydi_" + str(ses_dosya_sayac) + "_.wav" 
    wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()

def ses_kaydi_al():
    print("[START] * ses recording")
    #os.chdir("audio") 
    ses_dosya_sayac = 0
    

    while True:
        ses_dosya_sayac += 1
        if ses_dosya_sayac > KAYITSAYISI:
            ses_dosya_sayac = 1
        p = pyaudio.PyAudio()
        stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)
        
        frames = []
        for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
            data = stream.read(CHUNK, exception_on_overflow=False)
            frames.append(data)

        stream.stop_stream()
        stream.close()
        p.terminate()

        t3 = threading.Thread(target=kaydi_kaydet, args=[frames, ses_dosya_sayac])
        t3.start()





#ses_kaydi_al()