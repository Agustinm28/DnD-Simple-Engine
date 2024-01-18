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

    def check(self, paths:list, save_path:str):
        '''
        Method to check if audio is optimized, if not, optimize it. Where:
            - paths: list of paths to check.
            - save_path: path to save file.
        '''
        try:
            dprint("AUDIO", f"Checking audio...", "CYAN")

            with open(save_path, "r") as save_file:
                data = json.load(save_file)

            for path in paths:
                extension = path[2].split(".")[-1]
                if extension not in ["mp3"]:
                    dprint("IMAGE",f"Unsupported file type: {path[2]}. Converting...", "CYAN")
                    audio = AudioSegment.from_file(file=path[2], format=extension)
                    target_db = -25.0
                    change_in_db = target_db - audio.dBFS
                    normalized_audio = audio.apply_gain(change_in_db)
                    new_path = f"{path[2].split(f'.{extension}')[0]}.mp3"
                    normalized_audio.export(new_path, format="mp3")
                    os.remove(path[2])
                    data["scenes"][path[0]]["audio_path"] = new_path
                    path[2] = new_path
                else:
                    pass
            
            with open(save_path, "w") as save_file:
                json.dump(data, save_file, indent=4)
            
            return paths
        except Exception:
            error("Error checking audio")