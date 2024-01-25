import json
import pygame_gui
from utils.debugger import dprint
import pygame

class NewSaveMenu:

    def __init__(self, gameStateManager, engine, mouse):
        self.gameStateManager = gameStateManager
        self.engine = engine
        self.mouse = mouse
        self.handler = False

        self.scale_x = self.engine.resolution[0] / 1920
        self.scale_y = self.engine.resolution[1] / 1080
 
        self.widht = int(600 * self.scale_x)
        self.height = int(60 * self.scale_y)

        self.position_x = int(50 * self.scale_x)
        self.position_y = int(50 * self.scale_y)

        font_size = int(36 * min(self.scale_x, self.scale_y))
        self.font = pygame.font.Font("./assets/fonts/ancient.ttf", font_size)

        with open("./docs/theme.json", "r") as f:
            theme = json.load(f)
        
        theme["#name_input"]["font"][0]["size"] = str(font_size)
        theme["#desc_input"]["font"][0]["size"] = str(font_size)

        with open("./docs/theme.json", "w") as f:
            json.dump(theme, f, indent=4)
        
        # Name input box
        self.name_rect = pygame.Rect(self.position_x, self.position_y*2, self.widht, self.height)
        self.name_manager = pygame_gui.UIManager(self.engine.resolution, theme_path=self.engine.ENGINE_BUFFER["theme"])
        self.name_input = pygame_gui.elements.UITextEntryLine(relative_rect=self.name_rect, manager=self.name_manager, object_id="#name_input").set_text_length_limit(30)

        # Desc input box
        self.desc_rect = pygame.Rect(self.position_x, self.position_y*5, self.widht, self.height*10)
        self.desc_manager = pygame_gui.UIManager(self.engine.resolution, theme_path=self.engine.ENGINE_BUFFER["theme"])
        self.desc_input = pygame_gui.elements.UITextEntryBox(relative_rect=self.desc_rect, manager=self.desc_manager, object_id="#desc_input")

        #! VER EN pygame_gui, hay distintos modulos utiles para la seleccion de escenas, hay uno que te abre una ventana para seleccion de archivos, otro te muestra listas, etc.

    def run(self):

        self.engine.screen.blit(self.engine.ENGINE_BUFFER["main_menu"][0], (0,0))
        self.set_handler(True)

        # Name label
        name_label = self.font.render("Name", True, (0, 0, 0))
        self.engine.screen.blit(name_label, (self.position_x, self.position_y))

        # Desc label
        description_label = self.font.render("Description", True, (0, 0, 0))
        self.engine.screen.blit(description_label, (self.position_x, self.position_y*4))

        # Scenes label
        scenes_label = self.font.render("Scenes", True, (0, 0, 0))
        self.engine.screen.blit(scenes_label, (self.position_x*18, self.position_y))

        self.name_manager.update(pygame.time.Clock().tick(60) / 1000)
        self.desc_manager.update(pygame.time.Clock().tick(60) / 1000)
        self.name_manager.draw_ui(self.engine.screen)
        self.desc_manager.draw_ui(self.engine.screen)

    def get_handler(self):
        return self.handler

    def set_handler(self, handler):
        self.handler = handler

    def update_ui(self, res):
        
        dprint("NEW SAVE MENU", "Updating UI.", "BLUE")

        self.scale_x = res[0] / 1920
        self.scale_y = res[1] / 1080
 
        self.widht = int(600 * self.scale_x)
        self.height = int(60 * self.scale_y)

        self.position_x = int(50 * self.scale_x)
        self.position_y = int(50 * self.scale_y)

        font_size = int(36 * min(self.scale_x, self.scale_y))
        self.font = pygame.font.Font("./assets/fonts/ancient.ttf", font_size)

        # Open theme.json
        with open("./docs/theme.json", "r") as f:
            theme = json.load(f)
        
        theme["#name_input"]["font"][0]["size"] = str(font_size)
        theme["#desc_input"]["font"][0]["size"] = str(font_size)

        with open("./docs/theme.json", "w") as f:
            json.dump(theme, f, indent=4)

        self.name_rect = pygame.Rect(self.position_x, self.position_y*2, self.widht, self.height)
        name_label = self.font.render("Name", True, (0, 0, 0))
        self.engine.screen.blit(name_label, (self.position_x, self.position_y))

        self.desc_rect = pygame.Rect(self.position_x, self.position_y*5, self.widht, self.height*10)
        description_label = self.font.render("Description", True, (0, 0, 0))
        self.engine.screen.blit(description_label, (self.position_x, self.position_y*4))

        self.name_manager = pygame_gui.UIManager(res, theme_path=self.engine.ENGINE_BUFFER["theme"])
        self.name_input = pygame_gui.elements.UITextEntryLine(relative_rect=self.name_rect, manager=self.name_manager, object_id="#name_input").set_text_length_limit(30)

        self.desc_manager = pygame_gui.UIManager(res, theme_path=self.engine.ENGINE_BUFFER["theme"])
        self.desc_input = pygame_gui.elements.UITextEntryBox(relative_rect=self.desc_rect, manager=self.desc_manager, object_id="#desc_input")