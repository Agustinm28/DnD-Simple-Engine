import traceback
import pygame
import pygame.gfxdraw
from modules.audio import Audio
import json

class Engine:

    SCENES_BUFFER = {}
    ENGINE_BUFFER = {}
    AVAILABLE_RESOLUTIONS = []

    def __init__(self, resolution:tuple = None, mode = None, caption:str = "Board"):
        self.resolution = resolution
        self.mode = mode
        self.caption = caption

        pygame.mixer.pre_init(44100, -16, 2, 4096)
        pygame.init() # Initialize pygame

        self.screen = self.set_screen(self.resolution, self.mode, self.caption)
        self.audio = Audio() # Initialize audio module

        self.load_engine_assets()

    def set_screen(self, resolution:tuple = None, mode = None, caption:str = "Board"):

        # Setting resolution
        try:
            info = pygame.display.Info()
            native_resolution = (info.current_w, info.current_h)
            all_resolutions = pygame.display.list_modes()
            self.AVAILABLE_RESOLUTIONS = [res for res in all_resolutions if res[0] <= native_resolution[0] and res[1] <= native_resolution[1]]
            if resolution == None:
                resolution = native_resolution
            elif resolution != None and resolution in self.AVAILABLE_RESOLUTIONS:
                pass
            else:
                resolution = self.AVAILABLE_RESOLUTIONS[-1] # Set resolution to the last available
        except Exception:
            print("Error getting available resolutions")
            traceback.print_exc()

        # Setting mode
        if mode == None:
            mode = pygame.FULLSCREEN | pygame.DOUBLEBUF

        screen = pygame.display.set_mode(resolution, mode, 16)
        pygame.display.set_caption(caption)

        return screen
    
    def add_to_buffer(self, buffer:str, name:str, scene_path:str, audio_path:str = None):
        SUPPORTED = ["jpg", "jpeg", "png", "mp3", "wav", "ogg"]

        if buffer == "SCENES":
            buffer = self.SCENES_BUFFER
        elif buffer == "ENGINE":
            buffer = self.ENGINE_BUFFER
        
        if name not in buffer:
            scene_extension = scene_path.split(".")[-1]
            if scene_extension in SUPPORTED:
                memory_scene = pygame.image.load(scene_path).convert_alpha()
                memory_scene = pygame.transform.scale(memory_scene, self.resolution)
                if audio_path is not None and audio_path.split(".")[-1] in SUPPORTED:
                    memory_audio = pygame.mixer.Sound(audio_path)
                else:
                    memory_audio = None
                buffer[name] = [memory_scene, memory_audio]
            else:
                print("Unsupported file type")

    def add_to_engine_buffer(self, name:str, image_path:str, audio_path:str = None):
        if image_path is None or image_path == "":
            raise Exception("Scene path is required")
        self.add_to_buffer("ENGINE", name, image_path, audio_path)
        print(f"Element {name} added to engine buffer")

    def add_to_scenes_buffer(self, name:str, image_path:str, audio_path:str = None):
        if image_path is None or image_path == "":
            raise Exception("Scene path is required")
        self.add_to_buffer("SCENES", name, image_path, audio_path)
        print(f"Element {name} added to scene buffer")

    def restart_buffer(self, buffer:str):
        if buffer == "SCENES":
            self.SCENES_BUFFER = {}
        elif buffer == "ENGINE":
            self.ENGINE_BUFFER = {}
        else:
            raise Exception("Buffer not found")
    
    def load_engine_assets(self, engine_config_path:str = "./docs/engine.json"):

        with open(engine_config_path, "r") as save_file:
            engine_data = json.load(save_file)

        images = engine_data["assets"]["images"]

        for image_name, image_path in images.items():
            self.add_to_engine_buffer(image_name, image_path)

    def load_saved_game(self, save_path:str):
        #! Por el momento solo carga las escenas y sus audios
        # Load json file

        #! Aca deberia mostrarse una pantalla de carga
        with open(save_path, "r") as save_file:
            save = json.load(save_file)

        scenes = save["scenes"]
        for scene_name, scene_data in scenes.items():
            self.add_to_scenes_buffer(scene_name, scene_data["image_path"], scene_data["audio_path"])
    