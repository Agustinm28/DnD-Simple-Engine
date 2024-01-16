import pygame

class Audio:

    MUSIC = None

    def __init__(self):
        pygame.mixer.init()

    def play(self, audio_path:str):

        self.MUSIC = pygame.mixer.Sound(audio_path)
        self.MUSIC.play()

    def stop(self):
        self.MUSIC.stop()

    def check(self):
        return self.MUSIC