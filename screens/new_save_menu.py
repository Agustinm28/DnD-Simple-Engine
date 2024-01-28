import json
import pygame_gui
from utils.debugger import dprint
import pygame
from classes.campaign import Campaign

class NewSaveMenu:

    def __init__(self, gameStateManager, engine, mouse, repository, imageutils, save):
        self.gameStateManager = gameStateManager
        self.engine = engine
        self.mouse = mouse
        self.repository = repository
        self.imageutils = imageutils
        self.save = save
        self.campaign = Campaign()
        self.new_update = False

        self.scenes = []
        self.preloaded_data = {
            "save_id": "",
            "name": "",
            "description": "",
            "scenes": [] # [(image, audio), (image, audio)]
        }

        self.update_ui()

    def run(self):

        if self.gameStateManager.get_last_state() != 'save_menu':
            self.gameStateManager.set_last_state('save_menu')

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
        self.engine.screen.blit(add_label, (self.position_x*21.5, self.position_y*12))

        # Image label
        image_label = self.font.render("Image", True, (255, 255, 255))
        self.engine.screen.blit(image_label, (self.position_x*18, self.position_y*13))

        # Audio label
        audio_label = self.font.render("Associated audio", True, (255, 255, 255))
        self.engine.screen.blit(audio_label, (self.position_x*25, self.position_y*13))

        self.update_managers(self.optimice_manager, update=True, draw=True)
        self.update_managers(self.manager_list, update=False, draw=True)

        mouse_pos = pygame.mouse.get_pos()
        self.check_mouse_input(mouse_pos)

    def get_handler(self):
        return self.handler

    def set_handler(self, handler):
        self.handler = handler
    
    def get_new_update(self):
        return self.new_update
    
    def set_new_update(self, new_update):
        self.new_update = new_update

    def get_preloaded_data(self):
        return self.preloaded_data
    
    def set_preloaded_data(self, file_id:str, name:str, desc:str, scenes:list):
        self.preloaded_data["save_id"] = file_id
        self.preloaded_data["name"] = name
        self.preloaded_data["description"] = desc
        self.preloaded_data["scenes"] = scenes

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

    def update_ui(self, skip = False, complete = False):
        
        self.handler = False
        self.image = None
        self.audio = None
        self.selection = False
        self.images, self.audios = self.repository.load_repository()
        self.images.append("Select image")
        self.audios.append("None")
        self.loaded = False
        self.actual_image = "Select image"
        self.actual_audio = "None"
        if complete:
            self.scenes = []

        self.scale_x = self.engine.resolution[0] / 1920
        self.scale_y = self.engine.resolution[1] / 1080
 
        self.widht = int(600 * self.scale_x)
        self.height = int(60 * self.scale_y)

        self.position_x = int(50 * self.scale_x)
        self.position_y = int(50 * self.scale_y)

        font_size = int(36 * min(self.scale_x, self.scale_y))
        button_font_size = int(28 * min(self.scale_x, self.scale_y))
        self.font = pygame.font.Font("./assets/fonts/ancient.ttf", font_size)

        with open("./docs/theme.json", "r") as f:
            theme = json.load(f)
        
        theme["#ui_input"]["font"][0]["size"] = str(font_size)
        theme["#ui_label"]["font"][0]["size"] = str(font_size)
        theme["#ui_selector"]["font"][0]["size"] = str(font_size)
        theme["#ui_button"]["font"][0]["size"] = str(button_font_size)
        theme["#ui_dialog"]["font"][0]["size"] = str(button_font_size)

        with open("./docs/theme.json", "w") as f:
            json.dump(theme, f, indent=4)
        
        # Name input box
        if skip == False:
            self.name_rect = pygame.Rect(self.position_x, self.position_y*2, self.widht, self.height)
            self.name_manager = pygame_gui.UIManager(self.engine.resolution, theme_path=self.engine.ENGINE_BUFFER["theme"])
            self.name_input = pygame_gui.elements.UITextEntryLine(relative_rect=self.name_rect, manager=self.name_manager, object_id="#ui_input")
            self.name_input.set_text_length_limit(30)

            # Desc input box
            self.desc_rect = pygame.Rect(self.position_x, self.position_y*5, self.widht, self.height*10)
            self.desc_manager = pygame_gui.UIManager(self.engine.resolution, theme_path=self.engine.ENGINE_BUFFER["theme"])
            self.desc_input = pygame_gui.elements.UITextEntryBox(relative_rect=self.desc_rect, manager=self.desc_manager, object_id="#ui_input")

        # Scenes selector
        self.scenes_rect = pygame.Rect(self.position_x*15, self.position_y*2, self.widht*1.7, self.height*8)
        self.scenes_manager = pygame_gui.UIManager(self.engine.resolution, theme_path=self.engine.ENGINE_BUFFER["theme"])
        self.scenes_selector = pygame_gui.elements.UISelectionList(relative_rect=self.scenes_rect, manager=self.scenes_manager, object_id="#ui_selector", item_list=self.scenes)

        # Confirmation dialog
        self.confirmation_rect = pygame.Rect(self.position_x*5, self.position_y*6, self.widht*1.5, self.height*5)
        self.confirmation_manager = pygame_gui.UIManager(self.engine.resolution, theme_path=self.engine.ENGINE_BUFFER["theme"])
        self.confirmation_dialog = pygame_gui.windows.UIConfirmationDialog(
            rect=self.confirmation_rect,
            manager=self.confirmation_manager,
            window_title="Delete",
            action_long_desc="Do you want to delete this scene from the list?",
            action_short_name="Delete from list",
            blocking=True,
            object_id="#ui_dialog"
        )
        self.confirmation_dialog.hide()

        self.show_image_rect = pygame.Rect(self.position_x*15, self.position_y*15.5, self.widht/1.5, self.height*4) 
        self.show_image_manager = pygame_gui.UIManager(self.engine.resolution, theme_path=self.engine.ENGINE_BUFFER["theme"])
        self.show_image = pygame_gui.elements.UIImage(
            relative_rect=self.show_image_rect,
            manager=self.show_image_manager,
            image_surface=self.imageutils.load_image("./assets/images/generic/main/blank.webp"),
            object_id="#show_image"
        )

        # Image dropdown selector
        self.image_dropdown_rect = pygame.Rect(self.position_x*15, self.position_y*14, self.widht/1.5, self.height)
        self.image_dropdown_manager = pygame_gui.UIManager(self.engine.resolution, theme_path=self.engine.ENGINE_BUFFER["theme"])
        self.image_dropdown = pygame_gui.elements.UIDropDownMenu(
            options_list=self.images,
            relative_rect=self.image_dropdown_rect,
            manager=self.image_dropdown_manager,
            starting_option="Select image",
            object_id="#ui_dropdown"
        )

        # Audio dropdown selector
        self.audio_dropdown_rect = pygame.Rect(self.position_x*23.5, self.position_y*14, self.widht/1.5, self.height)
        self.audio_dropdown_manager = pygame_gui.UIManager(self.engine.resolution, theme_path=self.engine.ENGINE_BUFFER["theme"])
        self.audio_dropdown = pygame_gui.elements.UIDropDownMenu(
            options_list=self.audios,
            relative_rect=self.audio_dropdown_rect,
            manager=self.audio_dropdown_manager,
            starting_option="None",
            object_id="#ui_dropdown"
        )

        # Add button
        self.add_button_rect = pygame.Rect(self.position_x*33, self.position_y*16, self.widht/3, self.height)
        self.add_button_manager = pygame_gui.UIManager(self.engine.resolution, theme_path=self.engine.ENGINE_BUFFER["theme"])
        self.add_button = pygame_gui.elements.UIButton(
            relative_rect=self.add_button_rect,
            manager=self.add_button_manager,
            text="Add",
            object_id="#ui_button"
        )

        # Create campaign button
        self.create_button_rect = pygame.Rect(self.position_x*32.5, self.position_y*18, self.widht/2.3, self.height)
        self.create_button_manager = pygame_gui.UIManager(self.engine.resolution, theme_path=self.engine.ENGINE_BUFFER["theme"])
        self.create_button = pygame_gui.elements.UIButton(
            relative_rect=self.create_button_rect,
            manager=self.create_button_manager,
            text="Create campaign",
            object_id="#ui_button"
        )

        # Edit campaign button
        self.edit_button_rect = pygame.Rect(self.position_x*32.5, self.position_y*19, self.widht/2.3, self.height)
        self.edit_button_manager = pygame_gui.UIManager(self.engine.resolution, theme_path=self.engine.ENGINE_BUFFER["theme"])
        self.edit_button = pygame_gui.elements.UIButton(
            relative_rect=self.edit_button_rect,
            manager=self.edit_button_manager,
            text="Edit campaign",
            object_id="#ui_button"
        )
        self.edit_button.hide() 

        if self.preloaded_data["save_id"] != "":
            self.create_button.hide()
            self.create_button.disable()
            self.edit_button.show()
            self.edit_button.enable()
            self.campaign.set_id(self.preloaded_data["save_id"])

        if self.preloaded_data["name"] != "":
            self.name_input.set_text(self.preloaded_data["name"])
        if self.preloaded_data["description"] != "":
            self.desc_input.set_text(self.preloaded_data["description"])
        if self.preloaded_data["scenes"] != []:
            self.scenes = self.preloaded_data["scenes"]
            self.scenes_selector.set_item_list(self.scenes)

        self.manager_list = [
            self.name_manager,
            self.desc_manager,
            self.scenes_manager,
            self.show_image_manager,
            self.add_button_manager,
            self.create_button_manager,
            self.edit_button_manager,
            self.image_dropdown_manager,
            self.audio_dropdown_manager,
            self.confirmation_manager
        ]
        self.optimice_manager = []

        self.update_managers(self.manager_list, update=True, draw=True)

    def check_scene(self):
        if self.actual_image == "Select image":
            return False
        else:
            return True
        
    def check_campaign(self):
        if self.name_input.get_text() == "" or self.desc_input.get_text() == "" or self.scenes == []:
            return False
        else:
            return True
        
    def get_path_scenes(self, scenes):
        complete_scenes = []
        for scene in scenes: 
            if scene[1] == "None" or scene[1] == None:
                # Name, image_path, audio_path
                complete_scenes.append([scene[0], self.repository.get_path_from_repository(scene[0], "image"), ""])
            else:
                complete_scenes.append([scene[0], self.repository.get_path_from_repository(scene[0], "image"), [scene[1], self.repository.get_path_from_repository(scene[1], "audio")]])

        return complete_scenes

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
            for scene in self.scenes:
                if scene[0] == self.scene:
                    self.scenes.remove(scene)
            self.set_optimice_manager_list([self.scenes_manager, self.confirmation_manager])
            self.update_ui(skip=True)
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
        elif self.image_dropdown.selected_option != self.actual_image and self.loaded == False:
            self.loaded = True
            self.image = self.image_dropdown.selected_option
            if "Select image" in self.images:
                self.images.remove("Select image")
            self.set_optimice_manager_list([self.image_dropdown_manager, self.show_image_manager])
            self.show_image.set_image(self.imageutils.load_image(self.repository.get_path_from_repository(self.image, "image")))
            self.actual_image = self.image
            self.loaded = False
        elif self.audio_dropdown_rect.collidepoint(mouse_pos):
            self.set_optimice_manager_list([self.audio_dropdown_manager])
        elif self.audio_dropdown.selected_option != self.actual_audio and self.loaded == False:
            self.loaded = True
            self.audio = self.audio_dropdown.selected_option
            self.set_optimice_manager_list([self.audio_dropdown_manager])
            self.actual_audio = self.audio
            self.loaded = False
        elif self.add_button_rect.collidepoint(mouse_pos):
            self.set_optimice_manager_list([self.add_button_manager])
            if self.add_button.check_pressed():
                self.add_button.pressed = False
                if self.check_scene():
                    self.scenes.append((self.image, self.audio))
                    self.set_optimice_manager_list([self.add_button_manager, self.scenes_manager])
                    self.update_ui(skip=True)
                    dprint("NEW SAVE", "Add button clicked.", "BLUE")
                else:
                    dprint("NEW SAVE", "No image selected.", "RED")
        elif self.create_button_rect.collidepoint(mouse_pos) and self.selection == False:
            self.set_optimice_manager_list([self.create_button_manager])
            if self.create_button.check_pressed():
                self.create_button.pressed = False
                if self.check_campaign():
                    self.campaign.set_name(self.name_input.get_text())
                    self.campaign.set_description(self.desc_input.get_text())
                    complete_scenes = self.get_path_scenes(self.scenes)
                    self.campaign.set_scenes(complete_scenes)
                    self.save.save_campaign(self.campaign)
                    dprint("NEW SAVE", "Campaign created", "BLUE")
                    self.set_new_update(True)
                    self.gameStateManager.set_state('save_menu')
                else:
                    dprint("NEW SAVE", "No name, description or scenes selected.", "RED")
        elif self.edit_button_rect.collidepoint(mouse_pos):
            self.set_optimice_manager_list([self.edit_button_manager])
            if self.edit_button.check_pressed():
                self.edit_button.pressed = False
                if self.check_campaign():
                    self.campaign.set_name(self.name_input.get_text())
                    self.campaign.set_description(self.desc_input.get_text())
                    complete_scenes = self.get_path_scenes(self.scenes)
                    self.campaign.set_scenes(complete_scenes)
                    self.save.edit_campaign(self.campaign)
                    dprint("NEW SAVE", "Campaign edited", "BLUE")
                    self.set_new_update(True)
                    self.gameStateManager.set_state('save_menu')
                else:
                    dprint("NEW SAVE", "No name, description or scenes selected.", "RED")
        