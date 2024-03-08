import os
import sys
import time
import pygame
import pygame.gfxdraw
from modules.audio import Audio
from modules.image import ImageUtils
from utils.debugger import dprint, error, set_break, info
import json
import locale

class Engine:
    '''
    Class to handle engine operations.
    '''

    SCENES_BUFFER = {}
    ENGINE_BUFFER = {}
    AVAILABLE_RESOLUTIONS = []

    def __init__(self, resolution:tuple = None, mode = None, caption:str = "Simple DnD Engine"):
        self.resolution = resolution
        self.mode = mode
        self.caption = caption

        pygame.mixer.pre_init(44100, -16, 2, 4096)
        pygame.init() # Initialize pygame

        num_displays = pygame.display.get_num_displays() # Get number of displays

        self.load_engine_assets(mode="CONFIG")

        self.screen = self.set_screen(self.resolution, self.mode, self.caption)
        self.audio = Audio() # Initialize audio module
        self.image = ImageUtils()

        self.load_engine_assets(mode="ASSETS")

        pygame.display.set_icon(self.ENGINE_BUFFER["icon"][0])

    def set_screen(self, resolution:tuple = None, mode = None, caption:str = "Simple DnD Engine"):
        '''
        Method to set screen. Where:
            - resolution: resolution of the screen. -> (x, y)
            - mode: mode of the screen. -> [Fullscreen, resizable]
            - caption: caption of the screen.
        '''

        # Setting resolution
        try:
            # Display init and info
            pygame.display.init()
            info = pygame.display.Info()

            # Get available resolutions
            native_resolution = (info.current_w, info.current_h)
            all_resolutions = pygame.display.list_modes()
            self.AVAILABLE_RESOLUTIONS = [res for res in all_resolutions if res[0] <= native_resolution[0] and res[1] <= native_resolution[1]]

            if resolution == None:
                # If resolution is not set, set it to the native resolution
                x = self.ENGINE_BUFFER["resolution"][0]
                y = self.ENGINE_BUFFER["resolution"][1]
                if (x, y) == (None, None):
                    resolution = native_resolution
                    self.ENGINE_BUFFER["resolution"] = [resolution[0], resolution[1]]
                else:
                    # If resolution is set, check if it is available
                    resolution = (x, y)
            elif resolution != None and resolution in self.AVAILABLE_RESOLUTIONS:
                resolution = resolution
            else:
                # If resolution is not available, set it to the last available
                resolution = self.AVAILABLE_RESOLUTIONS[-1]

            if mode == None:
                if self.ENGINE_BUFFER["fullscreen"]:
                    mode = pygame.FULLSCREEN | pygame.DOUBLEBUF
                else:
                    mode = pygame.RESIZABLE | pygame.DOUBLEBUF
            
            dprint("ENGINE", f"Resolution set to {resolution}", "BLUE")
            
            screen = pygame.display.set_mode(resolution, mode, 16)
            pygame.display.set_caption(caption)

            self.resolution = resolution
            
            return screen
        
        except Exception:
            error("Error while setting resolution and mode")

    
    def update_screen(self, resolution:tuple = None, mode = None, caption:str = "Simple DnD Engine"):
        '''
        Method to update screen. Where:
            - resolution: resolution of the screen. -> (x, y)
            - mode: mode of the screen. -> [Fullscreen, resizable]
            - caption: caption of the screen.
        '''
        try:
            pygame.display.quit()
            self.screen = self.set_screen(resolution, mode, caption)
            self.restart_buffer("ENGINE")
            self.ENGINE_BUFFER["resolution"] = [resolution[0], resolution[1]]
        except Exception:
            error("Error while updating screen")

    def toggle_fullscreen(self, mode:bool = False):
        '''
        Method to toggle fullscreen. Where:
            - mode: mode of the screen. -> [True (Fullscreen), False (Resizable)]
        '''
        try:
            pygame.display.toggle_fullscreen()
            if mode == False:
                self.ENGINE_BUFFER["fullscreen"] = False
                self.mode = pygame.RESIZABLE | pygame.DOUBLEBUF
            else:
                self.ENGINE_BUFFER["fullscreen"] = True
                self.mode = pygame.FULLSCREEN | pygame.DOUBLEBUF
        except Exception:
            error("Error while toggling fullscreen")
    
    def add_to_buffer(self, buffer:str, name:str, scene_path:str, audio_path:str = None, value:str = None, save_path:str = None):
        '''
        Method to add an element to a buffer. Where:
            - buffer: buffer to add the element. -> [SCENES, ENGINE]
            - name: name of the element.
            - scene_path: path to the image.
            - audio_path: path to the audio.
            - value: value of the element. -> [CONFIG, IMAGE]
        '''
        try:
            SUPPORTED = ["webp", "png", "mp3"]

            if buffer == "SCENES":
                buffer = self.SCENES_BUFFER
            elif buffer == "ENGINE":
                buffer = self.ENGINE_BUFFER
            
            if name not in buffer:
                if value == "CONFIG":
                    buffer[name] = scene_path
                elif value == "IMAGE":
                    scene_extension = scene_path.split(".")[-1]
                    if scene_extension not in SUPPORTED:
                        raise Exception("Unsupported file type")
                    try:
                        memory_scene = pygame.image.load(scene_path).convert_alpha()
                        memory_scene = pygame.transform.scale(memory_scene, self.resolution)
                    except FileNotFoundError:
                        # Delete the element from the save_path file
                        with open(save_path, "r") as save_file:
                            save = json.load(save_file)

                        scenes = save["scenes"]
                        scenes.pop(name)

                        with open(save_path, "w") as save_file:
                            json.dump(save, save_file, indent=4)

                    if audio_path is not None and audio_path.split(".")[-1] in SUPPORTED:
                        memory_audio = audio_path
                    else:
                        memory_audio = None
                    buffer[name] = [memory_scene, memory_audio]
                elif value == "AUDIO":
                    buffer[name] = audio_path
        except Exception:
            error("Error while adding element to buffer")

    def add_to_engine_buffer(self, name:str, image_path:str = None, audio_path:str = None, value:str = None):
        '''
        Method to add an element to the engine buffer. Where:
            - name: name of the element.
            - image_path: path to the image.
            - audio_path: path to the audio.
            - value: value of the element. -> [CONFIG, IMAGE]
        '''
        try:
            self.add_to_buffer("ENGINE", name, image_path, audio_path, value=value)
            dprint("ENGINE", f"Element {name} added to engine buffer", "GREEN")
        except Exception:
            error("Error while adding element to engine buffer")

    def add_to_scenes_buffer(self, name:str, image_path:str, audio_path:str = None, save_path:str = None):
        '''
        Method to add an element to the scenes buffer. Where:
            - name: name of the element.
            - image_path: path to the image.
            - audio_path: path to the audio.
        '''
        try:
            if image_path is None or image_path == "":
                raise Exception("Scene path is required")
            self.add_to_buffer("SCENES", name, image_path, audio_path, value="IMAGE", save_path=save_path)
            dprint("ENGINE", f"Element {name} added to scene buffer", "GREEN")
        except Exception:
            error("Error while adding element to scene buffer")

    def restart_buffer(self, buffer:str):
        '''
        Method to restart a buffer. Where:
            - buffer: buffer to restart. -> [SCENES, ENGINE]
        '''
        try:
            if buffer == "SCENES":
                if len(self.SCENES_BUFFER) > 0:
                    self.SCENES_BUFFER = {}
            elif buffer == "ENGINE":
                self.ENGINE_BUFFER = {}
                self.load_engine_assets(mode="CONFIG")
                self.load_engine_assets(mode="ASSETS")
            else:
                raise Exception("Buffer not found")
        except Exception:
            error("Error while restarting buffer")
    
    def load_engine_assets(self, engine_config_path:str = "./docs/engine.json", mode:str = None):
        '''
        Method to load engine assets. Where:
            - engine_config_path: path to engine config file.
            - mode: mode to load. -> [CONFIG, ASSETS]
        '''
        try:
            with open(engine_config_path, "r") as save_file:
                engine_data = json.load(save_file)

            if mode == "CONFIG":
                config = engine_data["config"]
                theme = engine_data["theme"]
                language = config["lang"]
                if language == None:
                    local_lang = locale.getdefaultlocale()[0].split("_")[0]
                    self.set_initial_lang(local_lang)
                    config["lang"] = local_lang
                    language = local_lang
                if language == "en":
                    language = self.load_language('./docs/languages/en.json')
                if language == "es":
                    language = self.load_language('./docs/languages/es.json')
                for name, value in config.items():
                    self.add_to_engine_buffer(name, value, value="CONFIG")
                self.add_to_engine_buffer("theme", theme, value="CONFIG")
                self.add_to_engine_buffer("language", language, value="CONFIG")
            elif mode == "ASSETS":
                images = engine_data["assets"]["images"]
                audios = engine_data["assets"]["audios"]
                for image_name, image_path in images.items():
                    self.add_to_engine_buffer(image_name, image_path, value="IMAGE")
                for audio_name, audio_path in audios.items():
                    self.add_to_engine_buffer(audio_name, audio_path=audio_path, value="AUDIO")
        except Exception:
            error("Error while loading engine assets")

    def load_language(self, language_path:str = "./docs/languages/en.json"):
        '''
        Method to load language. Where:
            - language_path: path to language file.
        '''
        try:
            with open(language_path, "r", encoding='utf-8') as file:
                language = json.load(file)
            return language
        except Exception:
            error("Error while loading language")
    
    def set_initial_lang(self, language:str):
        with open(f'./docs/engine.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
            data["config"]["lang"] = language

        with open(f'./docs/engine.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

    def load_saved_game(self, save_path:str):
        '''
        Method to load a saved game. Where:
            - save_path: path to saved game.
        '''
        try:
            start = time.time()
            dprint("ENGINE", f"Loading saved game from {save_path}", "CYAN")
            
            # If path does not exist
            if not os.path.exists(save_path):
                raise Exception("Save path does not exist")

            with open(save_path, "r") as save_file:
                save = json.load(save_file)

            try:
                id_num = save["id"]
                c_name = save["name"]
                description = save["description"]
                characters = save["characters"]
                scenes = save["scenes"]
            except Exception:
                raise Exception("Save file is not complete")
            
            scenes_data = []

            for scene_name, scene_data in scenes.items():
                scenes_data.append([scene_name, scene_data["image_path"], scene_data["audio_path"][1]])

            for value in scenes_data:
                self.add_to_scenes_buffer(value[0], value[1], value[2], save_path=save_path)

            end = time.time()
            info(f"Time to load: {end - start}") 

        except Exception:
            error("Error while loading saved game")

    def quit_engine(self):
        '''
        Method to quit engine.
        '''

        try:
            with open("./docs/engine.json", "r") as file:
                data = json.load(file)

            data["config"]["resolution"] = self.ENGINE_BUFFER["resolution"]
            data["config"]["fullscreen"] = self.ENGINE_BUFFER["fullscreen"]

            with open("./docs/engine.json", "w") as file:
                json.dump(data, file, indent=4)

            pygame.quit()
            sys.exit()
        except Exception:
            error("Error while quitting engine")