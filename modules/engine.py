import pygame
import pygame.gfxdraw
from modules.audio import Audio
import json

class Engine:

    SCENES_BUFFER = {}
    ENGINE_BUFFER = {}

    def __init__(self, resolution:tuple = (1920, 1080), mode = pygame.FULLSCREEN, caption:str = "Board"):
        self.resolution = resolution
        self.mode = mode
        self.caption = caption

        self.SCENES_BUFFER = {}
        self.ENGINE_BUFFER = {}
        
        pygame.init() # Initialize pygame
        self.screen = self.set_screen(self.resolution, self.mode, self.caption)
        self.audio = Audio() # Initialize audio module

        self.load_engine_assets()

    def set_screen(self, resolution:tuple = None, mode = pygame.FULLSCREEN, caption:str = "Board"):
        if resolution is None:
            screen_width, screen_height = pygame.display.get_surface().get_size()
            resolution = (screen_width, screen_height)
        screen = pygame.display.set_mode(resolution, mode)
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
                memory_scene = pygame.image.load(scene_path)
                if audio_path is not None and audio_path.split(".")[-1] in SUPPORTED:
                    memory_audio = pygame.mixer.Sound(audio_path)
                else:
                    memory_audio = None
                buffer[name] = [memory_scene, memory_audio]
            else:
                print("Unsupported file type")

    def add_to_engine_buffer(self, name:str, image_path:str, audio_path:str = None):
        if image_path is None or image_path is "":
            raise Exception("Scene path is required")
        self.add_to_buffer("ENGINE", name, image_path, audio_path)
        print(f"Element {name} added to engine buffer")

    def add_to_scenes_buffer(self, name:str, image_path:str, audio_path:str = None):
        if image_path is None or image_path is "":
            raise Exception("Scene path is required")
        self.add_to_buffer("SCENES", name, image_path, audio_path)
        print(f"Element {name} added to scene buffer")
        print(self.SCENES_BUFFER)

    def restart_buffer(self, buffer:str):
        if buffer == "SCENES":
            self.SCENES_BUFFER = {}
        elif buffer == "ENGINE":
            self.ENGINE_BUFFER = {}
        else:
            raise Exception("Buffer not found")
    
    def load_engine_assets(self):
        # Load main menu image
        self.add_to_engine_buffer("main_menu", "./images/generic/main/start.jpg")

        # Load loading image
        self.add_to_engine_buffer("loading", "./images/generic/main/loading.jpg")

        # Load main menu buttons images
        self.add_to_engine_buffer("start", "./images/assets/start.png")
        self.add_to_engine_buffer("options", "./images/assets/options.png")
        self.add_to_engine_buffer("exit", "./images/assets/exit.png")

        # Load scenes menu buttons image
        self.add_to_engine_buffer("scene", "./images/assets/scene.png")

    def load_saved_game(self, save_path:str):
        #! Por el momento solo carga las escenas y sus audios
        # Load json file

        #! Aca deberia mostrarse una pantalla de carga
        with open(save_path, "r") as save_file:
            save = json.load(save_file)

        scenes = save["scenes"]
        for scene_name, scene_data in scenes.items():
            self.add_to_scenes_buffer(scene_name, scene_data["image_path"], scene_data["audio_path"])
    