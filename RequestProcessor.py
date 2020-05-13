import speech_recognition as sr
import sys
import os
from config import Config as c
from time import gmtime, strftime

class RequestProcessor():

    def __init__(self, mp, speaker):
        self.mp = mp
        self.speaker = speaker

    # Gets the time and prints it out
    def getTime(self):
        self.speaker.speak(("It is:" + strftime("%H %M", gmtime())))

    def say(self, phraseParts):
        phrase = " ".join(phraseParts)
        self.speaker.speak(phrase)

    def playMusic(self,requestParts):
        # Check if wanting to play a song or a folder of songs
        songList = []
        if("song" in requestParts):
            songList = self.getSong(requestParts[0:])
        elif("song" not in requestParts): # Assume that user probably wants song
            songList = self.getSong(requestParts[0:])
        elif(requestParts[0] == "album"):
            songList = self.getFolder(requestParts[0:])
        else:
            print(requestParts)
            self.speaker.speak("please say if you want a song or folder to play")

        # Play song or folder
        if(type(songList) is list and len(songList) > 0):
            self.speaker.speak("I can do this right now")
            # self.mp.listPlayer = vlc.Instance().media_list_player_new()
            # list_player.set_media_list(songList)
            # self.mp.play()
        elif(type(songList) is str):
            # Has found 1 song so will now play
            self.speaker.speak("I have found" + " ".join(requestParts) + ", playing now...", 2)
            # If song is playing, stop it
            if(self.mp.getPlayer() is not None):
               self.mp.stop()
            # FOR NOW: use python-vlc library
            self.mp.loadAndPlay(songList)
        else:
            self.speaker.speak(" ".join(requestParts) + " not found", 1)

    def findSongsInDir(self, directory, requestParts="*"): # Return all found sounds in a directory
        print("directory ", directory)
        print("requestParts ", requestParts)
        # Search music directory for song file that matches song name
        # r=>root, d=>directories, f=>files, https://www.techbeamers.com/python-list-all-files-directory/
        songsList = []
        for r, d, f in os.walk(directory):
            for item in f:
            # print("DEBUG: item ", item)
            # print("DEBUG: Mp3 check ", '.mp3' in item)
            # print("DEBUG: song name included check ", songName in item)
                addSong = True
                if((".mp3" in item) or (".wma" in item) or (".mp4" in item)):
                    if(requestParts == "*"): # Assume they want to play all songs in directory
                        foundMatchingSongs.append(os.path.join(r, item))
                        continue
                    for word in requestParts:
                        # Check that all the words in the request are somewhere in the item title
                        # print("word ", word, " item ", item)
                        if word.lower() not in item.lower():
                            addSong = False # If not don't add it to the list
                else:
                    # The file is probably not a song so don't bother adding it
                    addSong = False
                # If the song meets the criteria add it to the list
                if(addSong == True):
                    songsList.append(os.path.join(r, item))

        return songsList

    def getSong(self, requestParts):
        # Get song name from requestParts
        # print("DEBUG: SONG NAME", songName)
        foundMatchingSongs = self.findSongsInDir(c.getMusicFolder(), requestParts=requestParts)
        n = len(foundMatchingSongs)
        if(n >= 1):
            print("found", foundMatchingSongs)
            print("playing", foundMatchingSongs[0])
            return foundMatchingSongs[0]
        # TODO add selection option
        return foundMatchingSongs # TODO for now just have the first one found

    def getFolder(self, requestParts):
        folder = (" ".join(requestParts))[0:] # Reform song name and join with spaces
        return self.findSongsInDir(folder,"*")

    def stop(self):
        if(self.mp.getPlayer() is not None):
            self.speaker.speak("Stopping player")
            self.mp.stop()
        else:
            self.speaker.speak("Nothing is player")

    # Processes request read in from audio input
        # TODO implement a better way or recognising requests;
        # possibly some tree of analyse of the request to guess which request to execute
    def processRequest(self, requestParts, requestStr):
        if(("what" == requestParts[0]) or ("what's" == requestParts[0])): # Assume user is asking a question
            # List of requests related to what
            if("time" in requestParts): # Assume user is asking what the time is
                self.getTime()
            else:
                self.speaker.speak("Sorry I don't know what you are asking for...")

        elif("play" == requestParts[0].lower()): # Assume user wants a song to be played
            self.playMusic(requestParts[1:])

        elif("stop" == requestParts[0]):
            self.stop()
            self.speaker.speak("Stoping music...")

        elif("pause" == requestParts[0]):
             self.mp.pause()

        elif("unpause" == requestParts[0]):
             self.mp.unpause()

        elif("say" == requestParts[0]):
            self.say(requestParts[1:])

        elif("shut" == requestParts[0] and "down" == requestParts[1]):
            self.speaker.speak("Shutting down, goodbye...")
            sys.exit()
        elif("tell me a story" == requestStr):
            self.speaker.speak(c.getPlaguiesSpeech(), 10)
        else:
            self.speaker.speak("Sorry I don't understand", 2)
