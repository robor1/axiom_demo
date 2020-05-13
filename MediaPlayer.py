import vlc

class MediaPlayer():
    def __init__(self):
        self.player = None

    # https://linuxconfig.org/how-to-play-audio-with-vlc-in-python
    # Plays a file using vlc player
    def loadAndPlay(self, fileLoc):
        self.player = vlc.MediaPlayer(fileLoc)
        self.player.audio_set_volume(100)
        self.player.play()

    # play without loading new file
    def play(self):
        self.player.play()

    def load(self, fileLoc):
        self.player = vlc.MediaPlayer(fileLoc)

    def pause(self):
        self.player.pause()

    def unpause(self):
        self.player.pause()

    def stop(self):
        self.player.stop()

    def getPlayer(self):
        return self.player

    def quietForListening(self):
        # Reduce it to 20 volume
        self.player.audio_set_volume(50)

    def setVolume(self, volume):
        self.player.audio_set_volume(volume)
