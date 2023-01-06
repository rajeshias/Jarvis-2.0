import sys, os
import pyautogui
import speech_recognition
import webbrowser
import time
import pyperclip
import geocoder
import requests
import urllib.request

from askgpt import askGPT
from text_to_speech import tts
from datetime import datetime
from bs4 import BeautifulSoup

g = geocoder.ip('me')


def gpt(audio_text):
    answer = ""
    try:
        answer = askGPT(message=audio_text)
    except:
        return "Sorry, Please check Internet connection"
    answer = answer.replace('\n', ' ')
    return answer

def blockPrint():
    sys.stdout = open(os.devnull, 'w')

def enablePrint():
    sys.stdout = sys.__stdout__

def readselected():
    pyautogui.hotkey('ctrl', 'c')
    time.sleep(.01)
    return pyperclip.paste()



class Jarvis:
    def __init__(self, session_token="", wake_word = None, voice_on = True):
        self.session_token = session_token
        self.wake_word = wake_word
        self.voice_on = voice_on
        self.recognizer = speech_recognition.Recognizer()
        self.voice = tts()
        self.gptSwitched = False
        
    def switchGPT(self, default = False):
        self.gptSwitched = not self.gptSwitched
        if default:
            self.gptSwitched = True
    
    def wishMe(self):
        api_url = "https://fcc-weather-api.glitch.me/api/current?lat=" + str(g.latlng[0]) + "&lon=" + str(g.latlng[1])

        data = requests.get(api_url)
        data_json = data.json()
        if data_json['cod'] == 200:
            main = data_json['main']
            wind = data_json['wind']
            weather_desc = data_json['weather'][0]
            self.voice.say(str(data_json['coord']['lat']) + 'latitude' + str(data_json['coord']['lon']) + 'longitude')
            self.voice.say('Internet location is served from' + data_json['name'] + data_json['sys']['country'] + 'dia')
            self.voice.say('weather type ' + weather_desc['main'])
            self.voice.say('Wind speed is ' + str(wind['speed']) + ' metre per second')
            self.voice.say('Temperature: ' + str(main['temp']) + 'degree celcius')
            self.voice.say('Humidity is ' + str(main['humidity']))
        hour = int(datetime.now().hour)
        if 0 <= hour < 12:
            self.voice.say(gpt("Wish me good morning"))
        elif 12 <= hour < 18:
            self.voice.say(gpt("wish me Good Afternoon"))
        else:
            self.voice.say(gpt('wish me Good Evening'))

    def listen(self, awake=False):
        if awake or self.wake_word is None:
            print('Listening...\n')
            
            with speech_recognition.Microphone() as mic:
                        blockPrint()
                        # self.recognizer.adjust_for_ambient_noise(mic, duration=0.3)
                        audio = self.recognizer.listen(mic, phrase_time_limit=3)
                        try:
                            audio_text = self.recognizer.recognize_google(audio, language = 'en-IN').lower()
                        except speech_recognition.UnknownValueError:
                            return
                        enablePrint()
            
            print(audio_text)
            if audio_text.startswith('open news') or audio_text.startswith('play news') or 'latest news' in audio_text or 'local news' in audio_text or 'tamil news' in audio_text:
                wion = urllib.request.urlopen("https://www.youtube.com/channel/UC_gUM8rL-Lrg6O3adPW9K1g/videos")
                wionsoup = str(BeautifulSoup(wion.read().decode(), 'lxml'))
                latestnews = wionsoup.find("ytimg.com/vi/") + 13
                newurl = ''

                if 'tamil' in audio_text or 'local' in audio_text:
                    sun = urllib.request.urlopen("https://www.youtube.com/@Sunnewstamil/videos")
                    sunsoup = str(BeautifulSoup(sun.read().decode(), 'lxml'))
                    localnews = sunsoup.find("ytimg.com/vi/") + 13
                    while sunsoup[localnews] != '/':
                        newurl += sunsoup[localnews]
                        localnews += 1
                    webbrowser.open("https://www.youtube.com/watch?v=" + newurl)
                    return

                while wionsoup[latestnews] != '/':
                    newurl += wionsoup[latestnews]
                    latestnews += 1
                webbrowser.open("https://www.youtube.com/watch?v=" + newurl)
                return

            elif 'what is the time' in audio_text or 'what time is it' in audio_text:
                strTime = datetime.now().strftime("%H:%M:%S")
                self.voice.say(f'the time is {strTime}')
                return

            elif 'read this' in audio_text:
                self.voice.say(readselected())   
                return

            elif 'what is this' in audio_text:
                self.voice.say(gpt(readselected()))
                return

            elif 'close this' in audio_text:
                pyautogui.hotkey('ctrl', 'w')
                return

            elif 'open youtube' in audio_text:
                webbrowser.open('https://youtube.com')
                return

            elif 'open google' in audio_text:
                webbrowser.open('https://google.com')
                return

            elif 'open gmail' in audio_text:
                webbrowser.open('www.gmail.com')
                return

            elif audio_text.startswith('play'):
                msg=audio_text[5:]
                song = urllib.parse.urlencode({"search_query": msg})
                result = urllib.request.urlopen("http://www.youtube.com/results?search_query=" + song)
                soup=BeautifulSoup(result.read().decode(),'lxml')
                index=str(soup).find("/watch?v=")
                url="http://www.youtube.com"+str(soup)[index:index+20]
                webbrowser.open(url)
                return

            elif audio_text.startswith('search'):
                audio_text=audio_text[7:]
                url = 'https://google.com/search?q=' + audio_text
                webbrowser.open(url)
                return

            elif 'open cmd' in audio_text:
                os.startfile("C:\\WINDOWS\\system32\\cmd.exe")
                return

            elif 'enhance' in audio_text or 'magnify' in audio_text:
                os.startfile("C:\\WINDOWS\\system32\\magnify.exe")
                return

            elif 'open notepad' in audio_text:
                os.startfile("C:\\WINDOWS\\system32\\notepad.exe")
                return
                
            elif 'open android studio' in audio_text:
                os.startfile("C:\\Program Files\\Android\\Android Studio\\bin\\studio64.exe")
                return

            elif 'open task manager' in audio_text:
                os.startfile("C:\\WINDOWS\\system32\\Taskmgr.exe")
                return

            elif 'open calculator' in audio_text:
                os.startfile("C:\\WINDOWS\\system32\\calc.exe")
                return

            elif 'gpt shutdown' in audio_text:
                os.system('shutdown /p /f')
                return

            elif 'take screenshot' in audio_text:
                os.system('cmd /c start ms-screenclip:')
                return

            elif 'open network' in audio_text:
                os.system('cmd /c start ms-availablenetworks:')
                return

            elif 'open github' in audio_text:
                webbrowser.open('https://github.com/rajeshias')
                return

            elif "gpt sleep" in audio_text or "gpt go to sleep" in audio_text:
                self.voice.say("going to sleep")
                sys.exit()
            
            if "gpt" in audio_text or self.gptSwitched:
                print(f"Asking ChatGPT: {audio_text}")
                answer = gpt(audio_text)
                print(f"ChatGPT: {answer}")
                self.voice.say(answer)
                self.switchGPT()
                if answer.endswith("?"):
                    self.switchGPT(True)
                return answer
            
                        
        else:
            while True:
                try:
                    with speech_recognition.Microphone() as mic:
                        blockPrint()
                        self.recognizer.adjust_for_ambient_noise(mic, duration=0.2)
                        audio = self.recognizer.listen(mic)
                        audio_text = self.recognizer.recognize_google(audio).lower()
                        enablePrint()
                    
                    
                    if audio_text == 'quit':
                        return    
                                
                    if audio_text == str(self.wake_word).lower():
                        print("Waking up...")
                        self.listen(awake=True)
                        return
                    
                        
                except speech_recognition.UnknownValueError:
                    self.recognizer = speech_recognition.Recognizer()
                    continue
            
        