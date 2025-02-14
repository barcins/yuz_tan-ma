
import pyaudio, os, threading
import wave
from datetime import datetime
import cv2, time

ses_kaydi = os.getcwd() + "/audio/"

print(pyaudio.PyAudio().get_default_input_device_info())
for i in range(pyaudio.PyAudio().get_device_count()):
    dev = pyaudio.PyAudio().get_device_info_by_index(i)
    print((i,dev['name'],dev['maxInputChannels']))



p = pyaudio.PyAudio()
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
RECORD_SECONDS = 10

KAYITTUMA_SN = 120


def kaydi_kaydet(frames):
    WAVE_OUTPUT_FILENAME = ses_kaydi + "ses_kaydi" + datetime.now().strftime('%Y-%m-%d_%H-%M-%S.wav' ) 
    wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()

def ses_kaydi_al():

    
    print("* ses recording")
    os.chdir("audio") 
    while True:
        silincek_ses_dosyalari = len( os.listdir()) - 20 # ses dosyalarının bulund
        files = sorted(filter(os.path.isfile, os.listdir('.')), key=os.path.getmtime) # ses dosyaları listele kayıt tarihine göre sırala
        if silincek_ses_dosyalari > 0:
            for file in range(silincek_ses_dosyalari ):
                os.remove(files[file]) # önceki kayıtları sil
                #print("kontrol # önceki kayıtları sil", files[file])


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

        start = time.perf_counter()
        t3 = threading.Thread(target=kaydi_kaydet, args=[frames])
        t3.start()
        finish = time.perf_counter()
        #print(f'Finished in {round(finish-start, 2)} second(s) ')





#ses_kaydi_al()