import speech_recognition as sr
from config import Config as c
from RequestProcessor import RequestProcessor
from TheSpeaker import TheSpeaker
from MediaPlayer import MediaPlayer
import simpleaudio as sa
import sys

# Listen for user to prompt interaction with program
def listenForInteraction(activationPhrase, source, r): # TODO find a better way to listen for a phrase
    while(True):
        print("~~listening in background for '" + activationPhrase + "'~~")
        try:
            audio = r.listen(source, timeout=None, phrase_time_limit=2.5)
            text = r.recognize_google(audio_data=audio, language="en-GB")
            print(text)
            if(activationPhrase in text):
                break
        except sr.UnknownValueError:
            # Ignore this an continue listening
            continue
        except sr.WaitTimeoutError:
            # Ignore time out and keep listening
            continue

def ping(wave_obj):
    play_obj = wave_obj.play()


if __name__ == "__main__":
    activationPhrase = c.getActivationPhrase()
    if(len(sys.argv) == 2):
        activationPhrase = sys.argv[1]
    # Initailse needed classes
    mp = MediaPlayer()
    r = sr.Recognizer()

    #r.energy_threshold = 5000
    speaker = TheSpeaker()
    rp = RequestProcessor(mp, speaker)
    # print(sr.Microphone.list_microphone_names())
    # micNum = int(input("Choose mic number"))

    # Set up ping sound
    wave_obj = sa.WaveObject.from_wave_file(c.getPingLocation())

    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source, duration=0.5)
        # r.pause_threshold = 0.5
    # TODO figure out how to change microphones
        while(True):
            if(mp.getPlayer() is not None):
                mp.setVolume(100) # Put volume back up after listening
            listenForInteraction(activationPhrase, source, r)
            if(mp.getPlayer() is not None):
                    mp.quietForListening()
	    # Ping user to notify them you are ready to be listened TODO improve this
            ping(wave_obj)
            try:
                audio = r.listen(source=source, timeout=5, phrase_time_limit=5) # Listen to the source
                text = r.recognize_google(audio_data=audio, language="en-GB")
                print("I heard -> " + text)
                requestParts = text.split(' ') # Split request up by spaces
                rp.processRequest(requestParts, text)
            except sr.UnknownValueError:
                print("Sorry I couldn't understand you...")
                continue
            except sr.WaitTimeoutError:
                print("Guess you had nothing to say...")
                continue
