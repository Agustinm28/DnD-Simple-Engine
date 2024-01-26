class Campaign:

    def __init__(self, id:str = "", name:str = "", description:str = "", characters:list[dict] = [], scenes:list[list] = []):
        self.id = id
        self.name = name
        self.description = description
        self.characters = characters
        self.scenes = scenes

    def get_id(self):
        return self.id
    
    def set_id(self, id:str):
        self.id = id

    def get_name(self):
        return self.name
    
    def set_name(self, name:str):
        self.name = name

    def get_description(self):
        return self.description
    
    def set_description(self, description:str):
        self.description = description

    def get_characters(self):
        return self.characters
    
    def set_characters(self, characters:list[dict]):
        self.characters = characters

    def get_scenes(self):
        return self.scenes
    
    def set_scenes(self, scenes:list):
        self.scenes = scenes

    def toJson(self):

        scenes_dict = {}
        for scene in self.scenes:
            scenes_dict[scene[0]] = {
                "image_path": scene[1],
                "audio_path": scene[2]
            }

        characters_dict = {
            "None": {
                "player": "",
                "race": "",
                "subrace": "",
                "background": "",
                "class": "",
                "level": "",
                "description": ""
            }
        }

        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "characters": characters_dict,
            "scenes": scenes_dict
        }

    def __str__(self):
        return f'{self.name} - {self.description}'