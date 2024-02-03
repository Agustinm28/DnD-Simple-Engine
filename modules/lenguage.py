import os
from utils.debugger import info, error, dprint
import json

class Lenguage:

    def __init__(self, engine):
        self.engine = engine
        self.lenguages = []
        self.obtain_lenguages()

        self.lang_dict = {
            "English": "en",
            "Español": "es"
        }

    def get_lenguages(self):
        return self.lenguages

    def set_lenguages(self, lenguages):
        self.lenguages = lenguages
    
    def get_lang(self, language_short):
        for lang, short in self.lang_dict.items():
            if short == language_short:
                return lang

    def obtain_lenguages(self):
        '''
        Method to obtain the lenguages.
        '''
        try:
            langs = os.listdir('./docs/languages')
            for lang in langs:
                with open(f'./docs/languages/{lang}', 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    name = data['lenguage']
                    self.lenguages.append(name)
        except Exception:
            error("Error obtaining lenguages")

    def change_lenguage(self, lenguage):
        '''
        Method to change the lenguage.
        '''
        try:
            
            # Change in Json
            if lenguage in self.lang_dict:
                lenguage = self.lang_dict[lenguage]

            with open(f'./docs/engine.json', 'r', encoding='utf-8') as f:
                data = json.load(f)
                data["config"]["lang"] = lenguage

            with open(f'./docs/engine.json', 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4, ensure_ascii=False)

            # Change in Engine buffer
            self.engine.ENGINE_BUFFER['lang'] = lenguage

            # Restar buffer
            self.engine.restart_buffer(buffer='ENGINE')

        except Exception:
            error("Error changing lenguage")
