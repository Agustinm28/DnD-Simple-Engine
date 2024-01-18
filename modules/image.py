import json
import os
import traceback
from PIL import Image
from colorama import Fore as c

class ImageUtils:

    def __init__(self):
        pass

    def check(self, paths:list, save_path:str):
        try:

            print("Optimizing images...")

            with open(save_path, "r") as save_file:
                data = json.load(save_file)

            for path in paths:
                extension = path[1].split(".")[-1]
                if extension not in ["webp"]:
                    print(f"Unsupported file type: {path[1]}")
                    print("Converting...")
                    new_path = self.convert(path[1], extension, path[0], save_path)
                    data["scenes"][path[0]]["image_path"] = new_path
                    path[1] = new_path
                else:
                    pass
            
            with open(save_path, "w") as save_file:
                json.dump(data, save_file, indent=4)
            
            return paths
        except Exception:
            traceback.print_exc()
            return False
        
    def convert(self, image_path, scene_extension:str, name:str, save_path:str = None):

        image = Image.open(image_path)
        new_path = f"{image_path.split(f'.{scene_extension}')[0]}.webp"
        image.save(new_path, "webp")
        print(f"Converted {image_path} to {new_path}")
        os.remove(image_path)
        
        return new_path