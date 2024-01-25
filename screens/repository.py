import json
import pygame_gui
from utils.debugger import dprint, error
import pygame

class Repository:

    def __init__(self, gameStateManager, engine, mouse):
        self.gameStateManager = gameStateManager
        self.engine = engine
        self.mouse = mouse
        self.handler = False
        self.images, self.audios = self.load_repository()
        self.image_path = ""
        self.audio_path = ""
        self.image = None

        self.scale_x = self.engine.resolution[0] / 1920
        self.scale_y = self.engine.resolution[1] / 1080
 
        self.widht = int(300 * self.scale_x)
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

        self.image_rect = pygame.Rect(self.position_x, self.position_y, self.widht*2, self.height*10)
        self.image_manager = pygame_gui.UIManager(self.engine.resolution, theme_path=self.engine.ENGINE_BUFFER["theme"])
        self.image_selector = pygame_gui.elements.UISelectionList(relative_rect=self.image_rect, manager=self.image_manager, object_id="#image_selector", item_list=self.images)
        self.image_selector.disable()

        # Name input box
        self.name_rect = pygame.Rect(self.position_x, self.position_y*14, self.widht*2, self.height)
        self.name_manager = pygame_gui.UIManager(self.engine.resolution, theme_path=self.engine.ENGINE_BUFFER["theme"])
        self.name_input = pygame_gui.elements.UITextEntryLine(relative_rect=self.name_rect, manager=self.name_manager, object_id="#name_input")
        self.name_input.set_text_length_limit(30)

        # Selection button
        self.select_rect = pygame.Rect(self.position_x, self.position_y*16, self.widht/1.5, self.height)
        self.select_manager = pygame_gui.UIManager(self.engine.resolution, theme_path=self.engine.ENGINE_BUFFER["theme"])
        self.select_button = pygame_gui.elements.UIButton(relative_rect=self.select_rect, manager=self.select_manager, object_id="#select_button", text="Select Image")

        # Selection label
        self.select_label_rect = pygame.Rect(self.position_x*5, self.position_y*16, self.widht, self.height)
        self.select_label_manager = pygame_gui.UIManager(self.engine.resolution, theme_path=self.engine.ENGINE_BUFFER["theme"])
        self.select_label = pygame_gui.elements.UILabel(relative_rect=self.select_label_rect, manager=self.select_label_manager, object_id="#select_label", text="No image selected")

        # File selection manager
        self.file_rect = pygame.Rect(self.position_x, self.position_y*4, self.widht*2, self.height*10)
        self.file_manager = pygame_gui.UIManager(self.engine.resolution, theme_path=self.engine.ENGINE_BUFFER["theme"])
        self.file_dialog = pygame_gui.windows.UIFileDialog(
                    rect=self.file_rect,
                    manager=self.file_manager,
                    window_title="Select Image",
                    initial_file_path="./assets/personalized", #! Despues cambiar por c:/
                    allow_existing_files_only=True,
                    allow_picking_directories=False,
                    allowed_suffixes={".png", ".jpg", ".jpeg", ".webp", ".gif"}
                )
        self.file_dialog.hide()

        # Save button
        self.save_rect = pygame.Rect(self.position_x, self.position_y*18, self.widht/1.5, self.height)
        self.save_manager = pygame_gui.UIManager(self.engine.resolution, theme_path=self.engine.ENGINE_BUFFER["theme"])
        self.save_button = pygame_gui.elements.UIButton(relative_rect=self.save_rect, manager=self.save_manager, object_id="#save_button", text="Save")

        # Alert label
        self.alert_rect = pygame.Rect(self.position_x*5, self.position_y*18, self.widht, self.height)
        self.alert_manager = pygame_gui.UIManager(self.engine.resolution, theme_path=self.engine.ENGINE_BUFFER["theme"])
        self.alert_label = pygame_gui.elements.UILabel(relative_rect=self.alert_rect, manager=self.alert_manager, object_id="#alert_label", text="")

    def run(self):
        try:
            self.engine.screen.blit(self.engine.ENGINE_BUFFER["main_menu"][0], (0,0))
            self.set_handler(True)

            self.image_manager.update(pygame.time.Clock().tick(60) / 1000)
            self.image_manager.draw_ui(self.engine.screen)
            self.name_manager.update(pygame.time.Clock().tick(60) / 1000) #! Optimizar input de name, anda lento
            self.name_manager.draw_ui(self.engine.screen)
            self.select_manager.update(pygame.time.Clock().tick(60) / 1000)
            self.select_manager.draw_ui(self.engine.screen)
            self.select_label_manager.update(pygame.time.Clock().tick(60) / 1000)
            self.select_label_manager.draw_ui(self.engine.screen)
            self.file_manager.update(pygame.time.Clock().tick(60) / 1000)
            self.file_manager.draw_ui(self.engine.screen)
            self.save_manager.update(pygame.time.Clock().tick(60) / 1000)
            self.save_manager.draw_ui(self.engine.screen)
            self.alert_manager.update(pygame.time.Clock().tick(60) / 1000)
            self.alert_manager.draw_ui(self.engine.screen)

            if self.select_button.check_pressed():
                dprint("REPOSITORY", "Select button clicked.", "BLUE")
                self.file_dialog.show()
            elif self.file_dialog.ok_button.check_pressed():
                self.file_dialog.ok_button.pressed = False
                dprint("REPOSITORY", "Ok button clicked.", "BLUE")
                self.image_path = self.file_dialog.current_file_path
                self.select_label.set_text(str(self.image_path).split("\\")[-1])
            elif self.file_dialog.cancel_button.check_pressed():
                self.file_dialog.cancel_button.pressed = False
                dprint("REPOSITORY", "Cancel button clicked.", "BLUE")
            elif self.save_button.check_pressed():
                dprint("REPOSITORY", "Save button clicked.", "BLUE")
                name = self.name_input.get_text()
                status = self.check_data(name, self.image_path)
                if status:
                    self.image = [name, str(self.image_path)]
                    dprint("REPOSITORY", "Image saved.", "GREEN")
                    #! Implementar logica para que la imagen se copie en la carpeta de imagenes del juego y se optimice, luego que se actualice la lista de arriba

        except Exception:
            error("Error while displaying repository menu")

    def get_handler(self):
        return self.handler
    
    def set_handler(self, handler):
        self.handler = handler

    def load_repository(self):
        with open("./docs/repository.json", "r") as f:
            repository = json.load(f)
        
        images = repository["images"]
        audios = repository["audios"]

        return images, audios
    
    def check_data(self, name, path):
        if name == "":
            self.alert_label.set_text("Name can't be empty")
            return False
        elif path == "":
            self.alert_label.set_text("Select an image")
            return False
        else:
            self.alert_label.set_text("")
            return True

    def update_ui(self, res):
        
        dprint("REPOSITORY", "Updating UI.", "BLUE")

        self.scale_x = res[0] / 1920
        self.scale_y = res[1] / 1080
 
        self.widht = int(600 * self.scale_x)
        self.height = int(600 * self.scale_y)

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

        self.image_rect = pygame.Rect(self.position_x, self.position_y, self.widht, self.height)

        self.image_manager = pygame_gui.UIManager(res, theme_path=self.engine.ENGINE_BUFFER["theme"])
        self.image_selector = pygame_gui.elements.UISelectionList(relative_rect=self.image_rect, manager=self.image_manager, object_id="#image_selector", item_list=self.item_list)
        self.image_selector.disable()
