import sys
import traceback
import pygame
import pygame.gfxdraw
from modules.audio import Audio
import json

class Engine:

    SCENES_BUFFER = {}
    ENGINE_BUFFER = {}
    AVAILABLE_RESOLUTIONS = []

    def __init__(self, resolution:tuple = None, mode = None, caption:str = "Simple DnD Engine"):
        self.resolution = resolution
        self.mode = mode
        self.caption = caption

        pygame.mixer.pre_init(44100, -16, 2, 4096)
        pygame.init() # Initialize pygame

        self.load_engine_assets(mode="CONFIG")

        self.screen = self.set_screen(self.resolution, self.mode, self.caption)
        self.audio = Audio() # Initialize audio module

        self.load_engine_assets(mode="ASSETS")

    def set_screen(self, resolution:tuple = None, mode = None, caption:str = "Simple DnD Engine"):

        # Setting resolution
        try:
            pygame.display.init()
            info = pygame.display.Info()
            native_resolution = (info.current_w, info.current_h)
            all_resolutions = pygame.display.list_modes()
            self.AVAILABLE_RESOLUTIONS = [res for res in all_resolutions if res[0] <= native_resolution[0] and res[1] <= native_resolution[1]]
            if resolution == None:
                resolution = (self.ENGINE_BUFFER["resolution"][0], self.ENGINE_BUFFER["resolution"][1])
            elif resolution != None and resolution in self.AVAILABLE_RESOLUTIONS:
                resolution = resolution
            else:
                resolution = self.AVAILABLE_RESOLUTIONS[-1] # Set resolution to the last available
        except Exception:
            print("Error getting available resolutions")
            traceback.print_exc()

        # Setting mode
        if mode == None:
            if self.ENGINE_BUFFER["fullscreen"]:
                mode = pygame.FULLSCREEN | pygame.DOUBLEBUF
            else:
                mode = pygame.RESIZABLE | pygame.DOUBLEBUF
        
        print("Resolution set to", resolution)
        
        screen = pygame.display.set_mode(resolution, mode, 16)
        pygame.display.set_caption(caption)

        self.resolution = resolution

        return screen
    
    def update_screen(self, resolution:tuple = None, mode = None, caption:str = "Simple DnD Engine"):
        pygame.display.quit()
        self.screen = self.set_screen(resolution, mode, caption)
        self.restart_buffer("ENGINE")
        self.ENGINE_BUFFER["resolution"] = [resolution[0], resolution[1]]

    def toggle_fullscreen(self, mode:bool = False):
        pygame.display.toggle_fullscreen()
        if mode == False:
            self.ENGINE_BUFFER["fullscreen"] = False
        else:
            self.ENGINE_BUFFER["fullscreen"] = True
        print(self.ENGINE_BUFFER)
    
    def add_to_buffer(self, buffer:str, name:str, scene_path:str, audio_path:str = None, value:str = None):
        SUPPORTED = ["jpg", "jpeg", "png", "webp", "mp3", "wav", "ogg"]

        if buffer == "SCENES":
            buffer = self.SCENES_BUFFER
        elif buffer == "ENGINE":
            buffer = self.ENGINE_BUFFER
        
        if name not in buffer:
            if value == "CONFIG":
                buffer[name] = scene_path
            elif value == "IMAGE":
                scene_extension = scene_path.split(".")[-1]
                if scene_extension in SUPPORTED:
                    memory_scene = pygame.image.load(scene_path).convert_alpha()
                    memory_scene = pygame.transform.scale(memory_scene, self.resolution)
                    if audio_path is not None and audio_path.split(".")[-1] in SUPPORTED:
                        memory_audio = audio_path
                    else:
                        memory_audio = None
                    buffer[name] = [memory_scene, memory_audio]
                else:
                    print("Unsupported file type")

    def add_to_engine_buffer(self, name:str, image_path:str = None, audio_path:str = None, value:str = None):
        if image_path is None or image_path == "":
            raise Exception("Asset value is required")
        self.add_to_buffer("ENGINE", name, image_path, audio_path, value=value)
        print(f"Element {name} added to engine buffer")

    def add_to_scenes_buffer(self, name:str, image_path:str, audio_path:str = None):
        if image_path is None or image_path == "":
            raise Exception("Scene path is required")
        self.add_to_buffer("SCENES", name, image_path, audio_path)
        print(f"Element {name} added to scene buffer")

    def restart_buffer(self, buffer:str):
        if buffer == "SCENES":
            self.SCENES_BUFFER = {}
            #! Esto despues
        elif buffer == "ENGINE":
            self.ENGINE_BUFFER = {}
            self.load_engine_assets(mode="CONFIG")
            self.load_engine_assets(mode="ASSETS")
        else:
            raise Exception("Buffer not found")
    
    def load_engine_assets(self, engine_config_path:str = "./docs/engine.json", mode:str = None):

        with open(engine_config_path, "r") as save_file:
            engine_data = json.load(save_file)

        if mode == "CONFIG":
            config = engine_data["config"]
            for name, value in config.items():
                self.add_to_engine_buffer(name, value, value="CONFIG")
        elif mode == "ASSETS":
            images = engine_data["assets"]["images"]
            for image_name, image_path in images.items():
                self.add_to_engine_buffer(image_name, image_path, value="IMAGE")

    def load_saved_game(self, save_path:str):
        #! Por el momento solo carga las escenas y sus audios
        #! Aca deberia mostrarse una pantalla de carga
        with open(save_path, "r") as save_file:
            save = json.load(save_file)

        scenes = save["scenes"]
        for scene_name, scene_data in scenes.items():
            self.add_to_scenes_buffer(scene_name, scene_data["image_path"], scene_data["audio_path"])

    def quit_engine(self):

        with open("./docs/engine.json", "r") as file:
            data = json.load(file)

        data["config"]["resolution"] = self.ENGINE_BUFFER["resolution"]
        data["config"]["fullscreen"] = self.ENGINE_BUFFER["fullscreen"]

        with open("./docs/engine.json", "w") as file:
            json.dump(data, file, indent=4)

        pygame.quit()
        sys.exit()
    