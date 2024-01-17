import pygame

class Audio:

    MUSIC = False

    def __init__(self):
        pygame.mixer.init()

    def play(self, audio_path):
        pygame.mixer.music.load(audio_path)
        pygame.mixer.music.play(loops=-1, fade_ms=1000)
        self.MUSIC = True

    def stop(self):
        pygame.mixer.music.stop()
        self.MUSIC = False

    def stop_fading(self):
        pygame.mixer.music.fadeout(1500)
        self.MUSIC = False
    
    def quit_mixer(self):
        pygame.mixer.music.unload()
        pygame.mixer.quit()