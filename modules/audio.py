import json
import os
import traceback
import pygame
from pydub import AudioSegment
from utils.debugger import error, dprint

class Audio:
    '''
    Class to handle audio operations.
    '''

    MUSIC = False

    def __init__(self):
        pygame.mixer.init()

    def play(self, audio_path):
        '''
        Method to play audio. Where:
            - audio_path: path to audio file.
        '''
        try:
            pygame.mixer.music.load(audio_path)
            pygame.mixer.music.play(loops=-1, fade_ms=1000)
            self.MUSIC = True
        except TypeError:
            pass
        except Exception:
            error("Error playing audio")

    def stop(self):
        '''
        Method to stop audio.
        '''
        try:
            pygame.mixer.music.stop()
            self.MUSIC = False
        except Exception:
            error("Error stopping audio")

    def stop_fading(self):
        '''
        Method to stop audio with fadeout.
        '''
        try:
            pygame.mixer.music.fadeout(1000)
            self.MUSIC = False
        except Exception:
            error("Error stopping audio")
    
    def quit_mixer(self):
        '''
        Method to quit mixer.
        '''
        try:
            pygame.mixer.music.unload()
            pygame.mixer.quit()
        except Exception:
            error("Error quitting mixer")

    def check(self, audio_path:SystemError):
        '''
        Method to check if audio is optimized, if not, optimize it. Where:
            - paths: list of paths to check.
            - save_path: path to save file.
        '''
        try:
            dprint("AUDIO", f"Checking audio...", "CYAN")

            extension = audio_path.split(".")[-1]
            if extension not in ["mp3"]:
                dprint("IMAGE",f"Unsupported file type: {audio_path}. Converting...", "CYAN")
                audio = AudioSegment.from_file(file=audio_path, format=extension)
                target_db = -25.0
                change_in_db = target_db - audio.dBFS
                normalized_audio = audio.apply_gain(change_in_db)
                new_path = f"{audio_path.split(f'.{extension}')[0]}.mp3"
                normalized_audio.export(new_path, format="mp3")
                os.remove(audio_path)
            else:
                new_path = audio_path
            
            return new_path
        except Exception:
            error("Error checking audio")