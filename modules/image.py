import json
import os
from PIL import Image
from utils.debugger import error, dprint
import pygame

class ImageUtils:

    def __init__(self):
        pass

    def check(self, image_path:str):
        '''
        Method to check if images are optimized, if not, optimize them. Where:
            - paths: list of paths to check.
            - save_path: path to save file.
        '''
        try:
            extension = image_path.split(".")[-1]
            if extension not in ["webp"]:
                dprint("IMAGE",f"Unsupported file type: {image_path}. Converting...", "CYAN")
                new_path = self.convert(image_path, extension)
            else:
                new_path = image_path
            return new_path
        except Exception:
            error("Error checking images")
            return False
        
    def convert(self, image_path, scene_extension:str):
        '''
        Method to convert images to webp (optimized format). Where:
            - image_path: path to image to convert.
            - scene_extension: extension of the scene.
        '''
        try:
            image = Image.open(image_path)
            new_path = f"{image_path.split(f'.{scene_extension}')[0]}.webp"
            image.save(new_path, "webp")
            dprint("IMAGE",f"Converted {image_path} to {new_path}", "GREEN") 
            os.remove(image_path)
            
            return new_path
        
        except Exception:
            error("Error converting image")
            return None
        
    def load_image(self, path):
        '''
        Method to load an image. Where:
            - path: path to image.
        '''
        try:
            image = pygame.image.load(path).convert_alpha()
            return image
        except Exception:
            error("Error loading image")
            return None