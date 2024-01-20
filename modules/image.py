import json
import os
from PIL import Image
from utils.debugger import error, dprint

class ImageUtils:
    '''
    Class to handle image operations.
    '''

    def __init__(self):
        pass

    def check(self, paths:list, save_path:str):
        '''
        Method to check if images are optimized, if not, optimize them. Where:
            - paths: list of paths to check.
            - save_path: path to save file.
        '''
        try:
            dprint("IMAGE",f"Checking images...", "CYAN")
            with open(save_path, "r") as save_file:
                data = json.load(save_file)

            for path in paths:
                extension = path[1].split(".")[-1]
                if extension not in ["webp"]:
                    dprint("IMAGE",f"Unsupported file type: {path[1]}. Converting...", "CYAN")
                    new_path = self.convert(path[1], extension)
                    data["scenes"][path[0]]["image_path"] = new_path
                    path[1] = new_path
                else:
                    pass
            
            with open(save_path, "w") as save_file:
                json.dump(data, save_file, indent=4)
            
            return paths
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