import json
import os
import traceback
import pygame
from pydub import AudioSegment
from pydub.playback import play

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

    def check(self, paths:list, save_path:str):
        try:

            print("Optimizing audio...")

            with open(save_path, "r") as save_file:
                data = json.load(save_file)

            for path in paths:
                extension = path[2].split(".")[-1]
                if extension not in ["mp3"]:
                    print(f"Unsupported file type: {path[2]}")
                    print("Converting...")
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
            traceback.print_exc()