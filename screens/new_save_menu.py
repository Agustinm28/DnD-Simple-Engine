import json
import pygame_gui
from utils.debugger import dprint
import pygame

class NewSaveMenu:

    def __init__(self, gameStateManager, engine, mouse, repository):
        self.gameStateManager = gameStateManager
        self.engine = engine
        self.mouse = mouse
        self.repository = repository

        self.update_ui()

    def run(self):

        self.engine.screen.blit(self.engine.ENGINE_BUFFER["main_menu"][0], (0,0))
        self.set_handler(True)

        # Name label
        name_label = self.font.render("Name", True, (255, 255, 255))
        self.engine.screen.blit(name_label, (self.position_x*1.5, self.position_y))

        # Desc label
        description_label = self.font.render("Description", True, (255, 255, 255))
        self.engine.screen.blit(description_label, (self.position_x*1.5, self.position_y*4))

        # Scenes label
        scenes_label = self.font.render("Scenes", True, (255, 255, 255))
        self.engine.screen.blit(scenes_label, (self.position_x*15.5, self.position_y))

        # Add label
        add_label = self.font.render("Add an scene", True, (255, 255, 255))
        self.engine.screen.blit(add_label, (self.position_x*23.5, self.position_y*12))

        # Image label
        image_label = self.font.render("Image", True, (255, 255, 255))
        self.engine.screen.blit(image_label, (self.position_x*19.5, self.position_y*13))

        # Audio label
        audio_label = self.font.render("Associated audio", True, (255, 255, 255))
        self.engine.screen.blit(audio_label, (self.position_x*28, self.position_y*13))

        self.update_managers(self.optimice_manager, update=True, draw=True)
        self.update_managers(self.manager_list, update=False, draw=True)

        mouse_pos = pygame.mouse.get_pos()
        self.check_mouse_input(mouse_pos)

    def get_handler(self):
        return self.handler

    def set_handler(self, handler):
        self.handler = handler

    def set_optimice_manager_list(self, manager_list):
        self.optimice_manager = manager_list

    def get_manager_list(self):
        return self.manager_list
    
    def handle_events(self, event):
        for manager in self.optimice_manager:
            manager.process_events(event)

    def update_managers(self, manager_list, update=False, draw=False):
        for manager in manager_list:
            if update:
                manager.update(pygame.time.Clock().tick(60) / 1000)
            if draw:
                manager.draw_ui(self.engine.screen)

    def update_ui(self):
        
        self.handler = False
        self.image = None
        self.selection = False
        self.scenes = []
        self.images, self.audios = self.repository.load_repository()
        self.images.append("Select image")
        self.audios.append("None")

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
        self.name_input = pygame_gui.elements.UITextEntryLine(relative_rect=self.name_rect, manager=self.name_manager, object_id="#name_input")
        self.name_input.set_text_length_limit(30)

        # Desc input box
        self.desc_rect = pygame.Rect(self.position_x, self.position_y*5, self.widht, self.height*10)
        self.desc_manager = pygame_gui.UIManager(self.engine.resolution, theme_path=self.engine.ENGINE_BUFFER["theme"])
        self.desc_input = pygame_gui.elements.UITextEntryBox(relative_rect=self.desc_rect, manager=self.desc_manager, object_id="#desc_input")

        # Scenes selector
        self.scenes_rect = pygame.Rect(self.position_x*15, self.position_y*2, self.widht*1.7, self.height*8)
        self.scenes_manager = pygame_gui.UIManager(self.engine.resolution, theme_path=self.engine.ENGINE_BUFFER["theme"])
        self.scenes_selector = pygame_gui.elements.UISelectionList(relative_rect=self.scenes_rect, manager=self.scenes_manager, object_id="#scene_selector", item_list=self.scenes)

        # Confirmation dialog
        self.confirmation_rect = pygame.Rect(self.position_x*5, self.position_y*6, self.widht*2, self.height*5)
        self.confirmation_manager = pygame_gui.UIManager(self.engine.resolution, theme_path=self.engine.ENGINE_BUFFER["theme"])
        self.confirmation_dialog = pygame_gui.windows.UIConfirmationDialog(
            rect=self.confirmation_rect,
            manager=self.confirmation_manager,
            window_title="Delete",
            action_long_desc="Do you want to delete this scene from the list?",
            action_short_name="Delete from list",
            blocking=True,
            object_id="#confirmation_dialog"
        )
        self.confirmation_dialog.hide()

        # Image dropdown selector
        self.image_dropdown_rect = pygame.Rect(self.position_x*16, self.position_y*14, self.widht/1.4, self.height)
        self.image_dropdown_manager = pygame_gui.UIManager(self.engine.resolution, theme_path=self.engine.ENGINE_BUFFER["theme"])
        self.image_dropdown = pygame_gui.elements.UIDropDownMenu(
            options_list=self.images,
            relative_rect=self.image_dropdown_rect,
            manager=self.image_dropdown_manager,
            starting_option="Select image",
            object_id="#image_dropdown"
        )

        # Audio dropdown selector
        self.audio_dropdown_rect = pygame.Rect(self.position_x*26, self.position_y*14, self.widht/1.4, self.height)
        self.audio_dropdown_manager = pygame_gui.UIManager(self.engine.resolution, theme_path=self.engine.ENGINE_BUFFER["theme"])
        self.audio_dropdown = pygame_gui.elements.UIDropDownMenu(
            options_list=self.audios,
            relative_rect=self.audio_dropdown_rect,
            manager=self.audio_dropdown_manager,
            starting_option="None",
            object_id="#audio_dropdown"
        )

        self.manager_list = [
            self.name_manager,
            self.desc_manager,
            self.scenes_manager,
            self.confirmation_manager,
            self.image_dropdown_manager,
            self.audio_dropdown_manager
        ]
        self.optimice_manager = []

        self.update_managers(self.manager_list, update=True, draw=True)

    def check_mouse_input(self, mouse_pos):
        if self.name_rect.collidepoint(mouse_pos):
            self.set_optimice_manager_list([self.name_manager])
        elif self.desc_rect.collidepoint(mouse_pos):
            self.set_optimice_manager_list([self.desc_manager])
        elif self.scenes_rect.collidepoint(mouse_pos) and self.selection == False:
            self.scenes_selector.pressed = False
            self.scenes_selector.enable()
            self.set_optimice_manager_list([self.scenes_manager])
            self.scene = self.scenes_selector.get_single_selection()
            if self.scene != None:
                self.set_optimice_manager_list([self.scenes_manager, self.confirmation_manager])
                self.confirmation_dialog.show()
                self.confirmation_dialog.rebuild()
        elif self.confirmation_dialog.confirm_button.check_pressed():
            self.confirmation_dialog.confirm_button.pressed = False
            self.confirmation_dialog.hide()
            self.scenes_selector.disable()
            self.set_optimice_manager_list([self.scenes_manager, self.confirmation_manager])
            self.scenes.pop(self.scenes.index(self.scene))
            self.update_ui()
            dprint("NEW SAVE", "Scene deleted.", "GREEN")
        elif self.confirmation_dialog.cancel_button.check_pressed():
            self.confirmation_dialog.cancel_button.pressed = False
            self.confirmation_dialog.hide()
            self.scenes_selector.disable()
            self.set_optimice_manager_list([self.scenes_manager, self.confirmation_manager])
            dprint("NEW SAVE", "Scene deletion canceled.", "GREEN")
        elif self.confirmation_dialog.close_window_button.check_pressed():
            self.confirmation_dialog.close_window_button.pressed = False
            self.confirmation_dialog.hide()
            self.scenes_selector.disable()
            self.set_optimice_manager_list([self.scenes_manager, self.confirmation_manager])
            dprint("NEW SAVE", "Scene deletion canceled.", "GREEN")
        elif self.image_dropdown_rect.collidepoint(mouse_pos):
            self.set_optimice_manager_list([self.image_dropdown_manager])
            if self.image_dropdown.selected_option != "Select image":
                self.image = self.image_dropdown.selected_option
                if "Select image" in self.images:
                    self.images.remove("Select image")
                self.set_optimice_manager_list([self.image_dropdown_manager])
        elif self.audio_dropdown_rect.collidepoint(mouse_pos):
            self.set_optimice_manager_list([self.audio_dropdown_manager])
            if self.audio_dropdown.selected_option != "None":
                self.audio = self.audio_dropdown.selected_option
                self.set_optimice_manager_list([self.audio_dropdown_manager])