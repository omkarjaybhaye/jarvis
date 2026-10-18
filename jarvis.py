import pyttsx3
import datetime
import speech_recognition as sr
import wikipedia 
import smtplib
import webbrowser as wb
import os
import pyautogui
import psutil
import pyjokes
import sounddevice as sd
import scipy.io.wavfile as wav
import io

engine = pyttsx3.init()

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def time():
    speak("the current time is")
    Time = datetime.datetime.now().strftime("%H:%M:%S")
    speak(Time)

def date():
    year = int(datetime.datetime.now().year)
    month = int(datetime.datetime.now().month)
    date = int(datetime.datetime.now().day)
    speak("the current date is")
    speak(str(date))
    speak(str(month))
    speak(str(year))

def wishme():
    speak("Welcome back sir")
    time() 
    date()
    hour = datetime.datetime.now().hour
    if hour>= 6 and hour<12:
        speak("Good morning sir!")
    elif hour>=12 and hour<18:
        speak("Good Afternoon sir!")
    elif hour >=18 and hour<24:
        speak("Good Evening sir")
    else :
        speak("good Night sir!")
    speak("Jarvis at your service Please tell me how can i help u!")

# Swapped out PyAudio for sounddevice and memory streams
def takeCommand():
    r = sr.Recognizer()
    
    fs = 44100      # Sample rate
    duration = 4    # Duration of recording in seconds (adjust if you need more time)
    
    print("Listening.......")
    
    try:
        # Record audio data using sounddevice instead of sr.Microphone()
        recording = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='int16')
        sd.wait()   # Wait until the recording finishes
        
        # Write audio data to an in-memory byte buffer
        byte_io = io.BytesIO()
        wav.write(byte_io, fs, recording)
        byte_io.seek(0)
        
        # Load audio buffer into speech_recognition framework
        with sr.AudioFile(byte_io) as source:
            audio = r.record(source)

        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(query)

    except Exception as e:
        print(e)
        speak("Say that again please...")
        return "None"

    return query    

def sendemail(to , content):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login('abc@gmail.com', '123')
    server.sendmail('abzc@gmail.com', to, content)
    server.close()

def screenshot():
    img = pyautogui.screenshot()
    img.save("C:/Users/onsha/OneDrive/Desktop/AI Assist/ss.png")

def cpu():
    usage = str(psutil.cpu_percent())
    speak('cpu is at ' + usage + ' percent')
    battery = psutil.sensors_battery()
    if battery:
        speak(f"Battery is at {battery.percent} percent")
    else:
        speak("Could not detect battery status")

def jokes():
    speak(pyjokes.get_joke())


if  __name__ == "__main__":
    wishme()
    while True:
        query = takeCommand().lower()

        if 'time' in query:
            time()

        elif 'date' in query:
            date()
        
        elif 'wikipedia' in query:
            speak("Searching.....")
            query = query.replace("wikipedia","")
            result = wikipedia.summary(query, sentences=2)
            print(result)
            speak(result)

        elif 'send email' in query:
            try:
                speak("What should i say?")
                content = takeCommand()
                to = 'xyz@gmail.com'
                #sendemail(to,content)
                speak(content)
            except Exception as e:
                print(e)
                speak("Unable to send the email")

        elif 'search in chrome' in query:
            speak("What should i search?")
            chromepath = "C:/Program Files/Google/Chrome/Application/chrome.exe"
            search = takeCommand().lower()
            wb.get(chromepath).open_new_tab(search)

        elif 'logout' in query:
            os.system("Shutdown -l")

        elif 'shutdown' in query:
            os.system("Shutdown /s /t 1")

        elif 'restart' in query:
            os.system("Shutdown /r /t 1")

        elif 'play songs' in query:
            songs_dir = 'C:/Users/Omkar Jaybhaye/Music'
            songs = os.listdir(songs_dir)
            os.startfile(os.path.join(songs_dir, songs[-1]))

        elif 'remember that' in query:
            speak("What should i remember?")
            data = takeCommand()
            speak("you said me to remember that,"+data)
            remember = open('data.txt', 'w')
            remember.write(data)
            remember.close()

        elif 'do you know anything' in query:
            remember = open('data.txt','r')
            speak("you said me to remember that"+remember.read())

        elif 'screenshot' in query:
            screenshot()
            speak("Taken screenshot")

        elif 'cpu' in query:
            cpu()

        elif 'joke' in query:
            jokes()

        elif 'offline' in query:
            speak("Going offline see u later.")
            quit()
