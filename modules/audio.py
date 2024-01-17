import pygame

class Audio:

    MUSIC = None

    def __init__(self):
        pygame.mixer.init()

    def play(self, audio_path):
        pygame.mixer.music.load(audio_path)
        pygame.mixer.music.play(-1)

    def stop(self):
        pygame.mixer.music.stop()

    def check(self):
        return self.MUSIC
    
    def quit_mixer(self):
        pygame.mixer.music.unload()
        pygame.mixer.quit()