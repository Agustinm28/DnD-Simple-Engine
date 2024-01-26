import json
import os
import pygame_gui
from utils.debugger import dprint, error
import pygame
import time
import shutil

class Repository:

    def __init__(self, gameStateManager, engine, mouse, image_optimizer):
        self.gameStateManager = gameStateManager
        self.engine = engine
        self.mouse = mouse
        self.image_optimizer = image_optimizer

        self.handler = False
        self.images, self.audios = self.load_repository()
        self.image_path = ""
        self.audio_path = ""
        self.image = None
        self.selection = False

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

        ### IMAGES UI ###
        self.update_ui("images")
        self.update_ui("audios")

    def run(self):
        try:
            self.engine.screen.blit(self.engine.ENGINE_BUFFER["main_menu"][0], (0,0))
            self.set_handler(True)

            self.update_managers(self.optimice_manager, update=True, draw=True)
            self.update_managers(self.manager_list, update=False, draw=True)
            mouse_pos = pygame.mouse.get_pos()

            self.check_mouse_input(mouse_pos)

        except Exception:
            error("Error while displaying repository menu")

    def get_handler(self):
        return self.handler
    
    def set_handler(self, handler):
        self.handler = handler

    def load_repository(self):
        with open("./docs/repository.json", "r") as f:
            repository = json.load(f)

        images_list = list(repository["images"].keys())
        audios_list = list(repository["audios"].keys())

        return images_list, audios_list
    
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

    def copy_and_optimize(self, path, file_type):
        if file_type == "image":
            new_path = f"./assets/images/repository/{path.split('\\')[-1]}"
            shutil.copy(path, new_path)
            new_path = self.image_optimizer.check(new_path)
        elif file_type == "audio":
            new_path = f"./assets/audio/repository/{path.split('\\')[-1]}"
            shutil.copy(path, new_path)
            new_path = self.engine.audio.check(new_path)
        return new_path
    
    def save_in_repository(self, name, path, media_type):
        with open("./docs/repository.json", "r") as f:
            repository = json.load(f)
        
        if media_type == "audio":
            repository["audios"][name] = path
        elif media_type == "image":
            repository["images"][name] = path

        with open("./docs/repository.json", "w") as f:
            json.dump(repository, f, indent=4)

    def delete_in_repository(self, name, media_type):
        with open("./docs/repository.json", "r") as f:
            repository = json.load(f)
        
        if media_type == "audio":
            path = repository["audios"][name]
            del repository["audios"][name]
            os.remove(path)
        elif media_type == "image":
            path = repository["images"][name]
            del repository["images"][name]
            os.remove(path)

        with open("./docs/repository.json", "w") as f:
            json.dump(repository, f, indent=4)

    def update_managers(self, manager_list, update=False, draw=False):
        for manager in manager_list:
            if update:
                manager.update(pygame.time.Clock().tick(60) / 1000)
            if draw:
                manager.draw_ui(self.engine.screen)

    def handle_events(self, event):
        for manager in self.optimice_manager:
            manager.process_events(event)

    def set_optimice_manager_list(self, manager_list):
        self.optimice_manager = manager_list

    def get_manager_list(self):
        return self.manager_list

    def update_ui(self, ui:str):

        self.handler = False
        self.images, self.audios = self.load_repository()
        self.image_path = ""
        self.audio_path = ""
        self.image = None
        self.selection = False

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

        if ui == "images":
            self.update_images_ui()
        elif ui == "audios":
            self.update_audios_ui()

    def update_images_ui(self):
        ### IMAGES UI ###
        # Images label
        self.images_rect = pygame.Rect(self.position_x, self.position_y, self.widht*2, self.height)
        self.images_manager = pygame_gui.UIManager(self.engine.resolution, theme_path=self.engine.ENGINE_BUFFER["theme"])
        self.images_label = pygame_gui.elements.UILabel(relative_rect=self.images_rect, manager=self.images_manager, object_id="#images_label", text="Images")

        self.image_rect = pygame.Rect(self.position_x, self.position_y*2, self.widht*2, self.height*10)
        self.image_manager = pygame_gui.UIManager(self.engine.resolution, theme_path=self.engine.ENGINE_BUFFER["theme"])
        self.image_selector = pygame_gui.elements.UISelectionList(relative_rect=self.image_rect, manager=self.image_manager, object_id="#image_selector", item_list=self.images)
        
        # Name label
        self.name_label_rect = pygame.Rect(self.position_x, self.position_y*15, self.widht/2, self.height)
        self.name_label_manager = pygame_gui.UIManager(self.engine.resolution, theme_path=self.engine.ENGINE_BUFFER["theme"])
        self.name_label = pygame_gui.elements.UILabel(relative_rect=self.name_label_rect, manager=self.name_label_manager, object_id="#name_label", text="Name")

        # Name input box
        self.name_rect = pygame.Rect(self.position_x*4, self.position_y*15, self.widht*1.5, self.height)
        self.name_manager = pygame_gui.UIManager(self.engine.resolution, theme_path=self.engine.ENGINE_BUFFER["theme"])
        self.name_input = pygame_gui.elements.UITextEntryLine(relative_rect=self.name_rect, manager=self.name_manager, object_id="#name_input")
        self.name_input.set_text_length_limit(30)

        # Selection button
        self.select_rect = pygame.Rect(self.position_x, self.position_y*17, self.widht/1.5, self.height)
        self.select_manager = pygame_gui.UIManager(self.engine.resolution, theme_path=self.engine.ENGINE_BUFFER["theme"])
        self.select_button = pygame_gui.elements.UIButton(relative_rect=self.select_rect, manager=self.select_manager, object_id="#select_button", text="Select Image")

        # Selection label
        self.select_label_rect = pygame.Rect(self.position_x*5, self.position_y*17, self.widht, self.height)
        self.select_label_manager = pygame_gui.UIManager(self.engine.resolution, theme_path=self.engine.ENGINE_BUFFER["theme"])
        self.select_label = pygame_gui.elements.UILabel(relative_rect=self.select_label_rect, manager=self.select_label_manager, object_id="#select_label", text="No image selected")

        # File selection manager
        self.file_rect = pygame.Rect(self.position_x, self.position_y*5, self.widht*2, self.height*10)
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

        # Confirmation dialog
        self.confirmation_rect = pygame.Rect(self.position_x*10, self.position_y*6, self.widht*2, self.height*5)
        self.confirmation_manager = pygame_gui.UIManager(self.engine.resolution, theme_path=self.engine.ENGINE_BUFFER["theme"])
        self.confirmation_dialog = pygame_gui.windows.UIConfirmationDialog(
            rect=self.confirmation_rect,
            manager=self.confirmation_manager,
            window_title="Delete",
            action_long_desc="Do you want to delete this image?",
            action_short_name="Delete",
            blocking=True,
            object_id="#confirmation_dialog"
        )
        self.confirmation_dialog.hide()

        # Save button
        self.save_rect = pygame.Rect(self.position_x, self.position_y*19, self.widht/1.5, self.height)
        self.save_manager = pygame_gui.UIManager(self.engine.resolution, theme_path=self.engine.ENGINE_BUFFER["theme"])
        self.save_button = pygame_gui.elements.UIButton(relative_rect=self.save_rect, manager=self.save_manager, object_id="#save_button", text="Save")

        # Alert label
        self.alert_rect = pygame.Rect(self.position_x*5, self.position_y*19, self.widht, self.height)
        self.alert_manager = pygame_gui.UIManager(self.engine.resolution, theme_path=self.engine.ENGINE_BUFFER["theme"])
        self.alert_label = pygame_gui.elements.UILabel(relative_rect=self.alert_rect, manager=self.alert_manager, object_id="#alert_label", text="")

        self.manager_list = [
            self.image_manager, 
            self.name_manager, 
            self.select_manager, 
            self.select_label_manager, 
            self.file_manager, 
            self.save_manager, 
            self.alert_manager, 
            self.confirmation_manager, 
            self.images_manager, 
            self.name_label_manager
            ]
        self.optimice_manager = []

        self.update_managers(self.manager_list, update=True, draw=True)

    def update_audios_ui(self):
        ### AUDIOS UI ###
        x_distance = 15
        # Audios label
        self.audios_rect = pygame.Rect(self.position_x*x_distance, self.position_y, self.widht*2, self.height)
        self.audios_manager = pygame_gui.UIManager(self.engine.resolution, theme_path=self.engine.ENGINE_BUFFER["theme"])
        self.audios_label = pygame_gui.elements.UILabel(relative_rect=self.audios_rect, manager=self.audios_manager, object_id="#audios_label", text="Audios")

        # Audio selector
        self.audio_rect = pygame.Rect(self.position_x*x_distance, self.position_y*2, self.widht*2, self.height*10)
        self.audio_manager = pygame_gui.UIManager(self.engine.resolution, theme_path=self.engine.ENGINE_BUFFER["theme"])
        self.audio_selector = pygame_gui.elements.UISelectionList(relative_rect=self.audio_rect, manager=self.audio_manager, object_id="#audio_selector", item_list=self.audios)
        
        # Name label
        self.audio_name_label_rect = pygame.Rect(self.position_x*x_distance, self.position_y*15, self.widht/2, self.height)
        self.audio_name_label_manager = pygame_gui.UIManager(self.engine.resolution, theme_path=self.engine.ENGINE_BUFFER["theme"])
        self.audio_name_label = pygame_gui.elements.UILabel(relative_rect=self.audio_name_label_rect, manager=self.audio_name_label_manager, object_id="#audio_name_label", text="Name")

        # Name input box
        self.audio_name_rect = pygame.Rect(self.position_x*(x_distance+3), self.position_y*15, self.widht*1.5, self.height)
        self.audio_name_manager = pygame_gui.UIManager(self.engine.resolution, theme_path=self.engine.ENGINE_BUFFER["theme"])
        self.audio_name_input = pygame_gui.elements.UITextEntryLine(relative_rect=self.audio_name_rect, manager=self.audio_name_manager, object_id="#name_input")
        self.audio_name_input.set_text_length_limit(30)

        # Selection button
        self.audio_select_rect = pygame.Rect(self.position_x*x_distance, self.position_y*17, self.widht/1.5, self.height)
        self.audio_select_manager = pygame_gui.UIManager(self.engine.resolution, theme_path=self.engine.ENGINE_BUFFER["theme"])
        self.audio_select_button = pygame_gui.elements.UIButton(relative_rect=self.audio_select_rect, manager=self.audio_select_manager, object_id="#audio_select_button", text="Select Audio")

        # Selection label
        self.audio_select_label_rect = pygame.Rect(self.position_x*(4+x_distance), self.position_y*17, self.widht, self.height)
        self.audio_select_label_manager = pygame_gui.UIManager(self.engine.resolution, theme_path=self.engine.ENGINE_BUFFER["theme"])
        self.audio_select_label = pygame_gui.elements.UILabel(relative_rect=self.audio_select_label_rect, manager=self.audio_select_label_manager, object_id="#audio_select_label", text="No audio selected")

        # File selection manager
        self.audio_file_rect = pygame.Rect(self.position_x*x_distance, self.position_y*5, self.widht*2, self.height*10)
        self.audio_file_manager = pygame_gui.UIManager(self.engine.resolution, theme_path=self.engine.ENGINE_BUFFER["theme"])
        self.audio_file_dialog = pygame_gui.windows.UIFileDialog(
                    rect=self.audio_file_rect,
                    manager=self.audio_file_manager,
                    window_title="Select Audio",
                    initial_file_path="./assets/audio/personalized", #! Despues cambiar por c:/
                    allow_existing_files_only=True,
                    allow_picking_directories=False,
                    allowed_suffixes={".mp3", ".wav", ".ogg", ".flac"}
                )
        self.audio_file_dialog.hide()

        # Confirmation dialog
        self.audio_confirmation_rect = pygame.Rect(self.position_x*(9+x_distance), self.position_y*6, self.widht*2, self.height*5)
        self.audio_confirmation_manager = pygame_gui.UIManager(self.engine.resolution, theme_path=self.engine.ENGINE_BUFFER["theme"])
        self.audio_confirmation_dialog = pygame_gui.windows.UIConfirmationDialog(
            rect=self.audio_confirmation_rect,
            manager=self.audio_confirmation_manager,
            window_title="Delete",
            action_long_desc="Do you want to delete this audio?",
            action_short_name="Delete",
            blocking=True,
            object_id="#audio_confirmation_dialog"
        )
        self.audio_confirmation_dialog.hide()

        # Save button
        self.audio_save_rect = pygame.Rect(self.position_x*x_distance, self.position_y*19, self.widht/1.5, self.height)
        self.audio_save_manager = pygame_gui.UIManager(self.engine.resolution, theme_path=self.engine.ENGINE_BUFFER["theme"])
        self.audio_save_button = pygame_gui.elements.UIButton(relative_rect=self.audio_save_rect, manager=self.audio_save_manager, object_id="#audio_save_button", text="Save")

        # Alert label
        self.audio_alert_rect = pygame.Rect(self.position_x*(4+x_distance), self.position_y*19, self.widht, self.height)
        self.audio_alert_manager = pygame_gui.UIManager(self.engine.resolution, theme_path=self.engine.ENGINE_BUFFER["theme"])
        self.audio_alert_label = pygame_gui.elements.UILabel(relative_rect=self.audio_alert_rect, manager=self.audio_alert_manager, object_id="#audio_alert_label", text="")

        self.manager_list = [
            self.image_manager, 
            self.name_manager, 
            self.select_manager, 
            self.select_label_manager, 
            self.file_manager, 
            self.save_manager, 
            self.alert_manager, 
            self.confirmation_manager, 
            self.images_manager, 
            self.name_label_manager,
            self.audios_manager,
            self.audio_manager,
            self.audio_name_manager,
            self.audio_select_manager,
            self.audio_select_label_manager,
            self.audio_file_manager,
            self.audio_save_manager,
            self.audio_alert_manager,
            self.audio_confirmation_manager,
            self.audio_name_label_manager
            ]
        self.optimice_manager = []

        self.update_managers(self.manager_list, update=True, draw=True)

    def check_mouse_input(self, mouse_pos):
         # Hover Select path rect
            if self.select_rect.collidepoint(mouse_pos):
                self.set_optimice_manager_list([self.select_manager])
                if self.select_button.check_pressed():
                    self.selection = True
                    self.select_button.pressed = False
                    self.set_optimice_manager_list([self.file_manager, self.select_label_manager])
                    self.file_dialog.show()
            # Hover Images rect
            elif self.image_rect.collidepoint(mouse_pos) and self.selection == False:
                self.image_selector.pressed = False
                self.image_selector.enable()
                self.set_optimice_manager_list([self.image_manager])
                self.image = self.image_selector.get_single_selection()
                if self.image != None:
                    self.set_optimice_manager_list([self.confirmation_manager, self.image_manager])
                    self.confirmation_dialog.show()
                    self.confirmation_dialog.rebuild()

            # Press Confirm delete rect
            elif self.confirmation_dialog.confirm_button.check_pressed():
                self.confirmation_dialog.confirm_button.pressed = False
                self.confirmation_dialog.hide()
                self.image_selector.disable()
                self.set_optimice_manager_list([self.confirmation_manager, self.image_manager])
                self.delete_in_repository(self.image, "image")
                self.update_ui("images")
                self.update_ui("audios")
                dprint("REPOSITORY", "Image deleted.", "GREEN")
            # Press Cancel delete rect
            elif self.confirmation_dialog.cancel_button.check_pressed():
                self.confirmation_dialog.cancel_button.pressed = False
                self.confirmation_dialog.hide()
                self.image_selector.disable()
                self.set_optimice_manager_list([self.confirmation_manager, self.image_manager])
                dprint("REPOSITORY", "Image not deleted.", "GREEN")
            # Press Close delete rect
            elif self.confirmation_dialog.close_window_button.check_pressed():
                self.confirmation_dialog.close_window_button.pressed = False
                self.confirmation_dialog.hide()
                self.image_selector.disable()
                self.set_optimice_manager_list([self.confirmation_manager, self.image_manager])
                dprint("REPOSITORY", "Image not deleted.", "GREEN")

            # Press Confirm path rect
            elif self.file_dialog.ok_button.check_pressed():
                self.selection = False
                self.file_dialog.ok_button.pressed = False
                self.file_dialog.hide()
                self.set_optimice_manager_list([self.select_manager, self.select_label_manager, self.file_manager])
                self.image_path = self.file_dialog.current_file_path
                self.select_label.set_text(str(self.image_path).split("\\")[-1])
            # Press Cancel path rect
            elif self.file_dialog.cancel_button.check_pressed():
                self.selection = False
                self.file_dialog.cancel_button.pressed = False
                self.file_dialog.hide()
                self.set_optimice_manager_list([self.select_manager, self.select_label_manager, self.file_manager])
            # Press Close path rect
            elif self.file_dialog.close_window_button.check_pressed():
                self.selection = False
                self.file_dialog.close_window_button.pressed = False
                self.file_dialog.hide()
                self.set_optimice_manager_list([self.select_manager, self.select_label_manager, self.file_manager])
            
            # Hover Path selector rect
            elif self.file_rect.collidepoint(mouse_pos) and self.selection:
                self.set_optimice_manager_list([self.file_manager, self.select_label_manager])
            # Hover Name input rect
            elif self.name_rect.collidepoint(mouse_pos):
                self.set_optimice_manager_list([self.name_manager])
            # Hover Save rect
            elif self.save_rect.collidepoint(mouse_pos):
                self.set_optimice_manager_list([self.save_manager, self.alert_manager, self.image_manager])
                if self.save_button.check_pressed():
                    name = self.name_input.get_text()
                    status = self.check_data(name, self.image_path)
                    if status:
                        self.image = [name, str(self.image_path)]
                        new_path = self.copy_and_optimize(str(self.image_path), "image")
                        self.save_in_repository(name, str(new_path), "image")
                        dprint("REPOSITORY", "Image saved.", "GREEN")
                        self.update_ui("images")
                        self.update_ui("audios")

            ### AUDIOS INPUT ###
                        
            # Hover Select audio path rect
            if self.audio_select_rect.collidepoint(mouse_pos):
                self.set_optimice_manager_list([self.audio_select_manager])
                if self.audio_select_button.check_pressed():
                    self.selection = True
                    self.audio_select_button.pressed = False
                    self.set_optimice_manager_list([self.audio_file_manager, self.audio_select_label_manager])
                    self.audio_file_dialog.show()
            # Hover Audios rect
            elif self.audio_rect.collidepoint(mouse_pos) and self.selection == False:
                self.audio_selector.pressed = False
                self.audio_selector.enable()
                self.set_optimice_manager_list([self.audio_manager])
                self.audio = self.audio_selector.get_single_selection()
                if self.audio != None:
                    self.set_optimice_manager_list([self.audio_confirmation_manager, self.audio_manager])
                    self.audio_confirmation_dialog.show()
                    self.audio_confirmation_dialog.rebuild()

            # Press Confirm delete rect
            elif self.audio_confirmation_dialog.confirm_button.check_pressed():
                self.audio_confirmation_dialog.confirm_button.pressed = False
                self.audio_confirmation_dialog.hide()
                self.audio_selector.disable()
                self.set_optimice_manager_list([self.audio_confirmation_manager, self.audio_manager])
                self.delete_in_repository(self.audio, "audio")
                self.update_ui("images")
                self.update_ui("audios")
                dprint("REPOSITORY", "Audio deleted.", "GREEN")
            # Press Cancel delete rect
            elif self.audio_confirmation_dialog.cancel_button.check_pressed():
                self.audio_confirmation_dialog.cancel_button.pressed = False
                self.audio_confirmation_dialog.hide()
                self.audio_selector.disable()
                self.set_optimice_manager_list([self.audio_confirmation_manager, self.audio_manager])
                dprint("REPOSITORY", "Audio not deleted.", "GREEN")
            # Press Close delete rect
            elif self.audio_confirmation_dialog.close_window_button.check_pressed():
                self.audio_confirmation_dialog.close_window_button.pressed = False
                self.audio_confirmation_dialog.hide()
                self.audio_selector.disable()
                self.set_optimice_manager_list([self.audio_confirmation_manager, self.audio_manager])
                dprint("REPOSITORY", "Audio not deleted.", "GREEN")

            # Press Confirm path rect
            elif self.audio_file_dialog.ok_button.check_pressed():
                self.selection = False
                self.audio_file_dialog.ok_button.pressed = False
                self.audio_file_dialog.hide()
                self.set_optimice_manager_list([self.audio_select_manager, self.audio_select_label_manager, self.audio_file_manager])
                self.audio_path = self.audio_file_dialog.current_file_path
                self.audio_select_label.set_text(str(self.audio_path).split("\\")[-1])
            # Press Cancel path rect
            elif self.audio_file_dialog.cancel_button.check_pressed():
                self.selection = False
                self.audio_file_dialog.cancel_button.pressed = False
                self.audio_file_dialog.hide()
                self.set_optimice_manager_list([self.audio_select_manager, self.audio_select_label_manager, self.audio_file_manager])
            # Press Close path rect
            elif self.audio_file_dialog.close_window_button.check_pressed():
                self.selection = False
                self.audio_file_dialog.close_window_button.pressed = False
                self.audio_file_dialog.hide()
                self.set_optimice_manager_list([self.audio_select_manager, self.audio_select_label_manager, self.audio_file_manager])
            
            # Hover Path selector rect
            elif self.audio_file_rect.collidepoint(mouse_pos) and self.selection:
                self.set_optimice_manager_list([self.audio_file_manager, self.audio_select_label_manager])
            # Hover Name input rect
            elif self.audio_name_rect.collidepoint(mouse_pos):
                self.set_optimice_manager_list([self.audio_name_manager])
            # Hover Save rect
            elif self.audio_save_rect.collidepoint(mouse_pos):
                self.set_optimice_manager_list([self.audio_save_manager, self.audio_alert_manager, self.audio_manager])
                if self.audio_save_button.check_pressed():
                    name = self.audio_name_input.get_text()
                    status = self.check_data(name, self.audio_path)
                    if status:
                        self.audio = [name, str(self.audio_path)]
                        new_path = self.copy_and_optimize(str(self.audio_path), "audio")
                        self.save_in_repository(name, str(new_path), "audio")
                        dprint("REPOSITORY", "Audio saved.", "GREEN")
                        self.update_ui("images")
                        self.update_ui("audios")