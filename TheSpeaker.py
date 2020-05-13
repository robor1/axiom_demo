import pyttsx3
from time import sleep

class TheSpeaker():
    def __init__(self):
        # Set up speaking engine
        self.engine = pyttsx3.init()
        # Lower the rate at which the AI speaks
        rate = self.engine.getProperty('rate')
        self.engine.setProperty('rate', rate-75)
        # Make tts at full volume
        self.engine.setProperty('volume', 1)

        self.engine.setProperty('voice', 'en 4')

        self.timeToSpeak = 4 # Seconds

    def speak(self, whatToSay, tts=-1): # TODO change this to self.timeToSpeak
        if(tts == -1):
            tts = self.timeToSpeak
        # TEST: put recognizer energy threashold really high while
        self.engine.say(whatToSay)
        self.engine.runAndWait()
        sleep(tts) # Hacky wait to stop python from listening while it is speaking?
