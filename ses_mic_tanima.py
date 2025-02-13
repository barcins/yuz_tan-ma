# Python program to translate
# speech to text and text to speech


import speech_recognition as sr
import pyttsx3 


r = sr.Recognizer()
r.energy_threshold=4000


# Initialize the recognizer 

# Function to convert text to
# speech
def SpeakText(command):
    
    # Initialize the engine
    engine = pyttsx3.init()
    engine.say(command) 
    engine.runAndWait()
    
    
# Loop infinitely for user to
# speak

while True:    
    
    # Exception handling to handle
    # exceptions at the runtime
    try:
        
        # use the microphone as source for input.
        with sr.Microphone() as source2:
            # wait for a second to let the recognizer
            # adjust the energy threshold based on
            # the surrounding noise level 
            r.adjust_for_ambient_noise(source2)
            #listens for the user's input 
            audio2 = r.listen(source2)

            
            # Using google to recognize audio
            MyText = r.recognize_google(audio2, language='tr-tr')
            MyText = MyText.lower()
            if len(MyText) > 0:
                print("Did you say &quot;",MyText)
                SpeakText(MyText)

                
            
    except sr.RequestError as e:
        print("RequestError:", e)
        
    except sr.UnknownValueError as e:
        print("UnknownValueError", e)
ß