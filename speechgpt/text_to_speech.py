import pyttsx3


class tts:
    def __init__(self):
        self.engine = pyttsx3.init()
        voices = self.engine.getProperty('voices')
        self.engine.setProperty('voice', voices[0].id)

    def say(self, message):
        self.engine.say(message)
        self.engine.runAndWait()