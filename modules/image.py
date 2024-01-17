import json
import os
from PIL import Image

class ImageUtils:

    def __init__(self):
        pass

    def check(self, folder_path:str):
        try:
            paths = os.listdir(folder_path)
            for path in paths:
                print(path)
                if path.split(".")[-1] not in ["webp"]:
                    print(f"Unsupported file type: {path}")
                    print("Converting...")
                    new_path = self.convert(path)
                    return new_path
                else:
                    pass
        except Exception:
            return False
        
    def convert(self, image_path, scene_extension:str, name:str, save_path:str = None):

        with open(save_path, "r") as save_file:
            data = json.load(save_file)

        image = Image.open(image_path)
        new_path = f"{image_path.split(f'.{scene_extension}')[0]}.webp"
        image.save(new_path, "webp")
        print(f"Converted {image_path} to {new_path}")
        os.remove(image_path)

        data["scenes"][name]["image_path"] = new_path

        with open(save_path, "w") as save_file:
            json.dump(data, save_file, indent=4)

        return new_path