import json
import os
import pygame
from utils.debugger import dprint, error
import time
import pygame_gui

class SaveMenu:

    def __init__(self, gameStateManager, engine, mouse, loading, new_save, save_utils, repository):
        self.gameStateManager = gameStateManager
        self.engine = engine
        self.mouse = mouse
        self.loading = loading
        self.new_save = new_save
        self.save_utils = save_utils
        self.repository = repository

        self.update_ui()
     
    def run(self):
        try:

            if self.repository.get_in_repository():
                self.repository.set_in_repository(False)

            if self.gameStateManager.get_last_state() != 'main_menu':
                self.gameStateManager.set_last_state('main_menu')

            if self.new_save.get_new_update():
                self.update_ui()
                self.update_managers(self.manager_list, update=True, draw=True)
                self.new_save.set_new_update(False)

            self.engine.screen.blit(self.engine.ENGINE_BUFFER["main_menu"][0], (0,0))
            self.set_handler(True)
            
            self.update_managers(self.optimice_manager, update=True, draw=True)
            self.update_managers(self.manager_list, update=False, draw=True)

            mouse_pos = pygame.mouse.get_pos()
            self.check_mouse_input(mouse_pos)

        except Exception:
            error("Error showing saves menu")

    def get_handler(self):
        return self.handler

    def set_handler(self, handler):
        self.handler = handler

    def set_optimice_manager_list(self, manager_list):
        self.optimice_manager = manager_list

    def get_manager_list(self):
        return self.manager_list
    
    def get_path(self, campaign):
        for save in self.saves:
            if save[0] == campaign:
                return save[1]
            
    def get_campaign_data(self, campaign):
        path = self.get_path(campaign)

        with open(path, "r") as save_file:
            data = json.load(save_file)
        
        file_id = path.split("/")[-1].split(".")[0]

        scenes = []

        for scene in data["scenes"]:
            scenes.append((scene, data["scenes"][scene]["audio_path"][0]))

        return {
            "id": file_id,
            "name": data["name"],
            "description": data["description"],
            "characters": data["characters"],
            "scenes": scenes
        }
    
    def handle_events(self, event):
        for manager in self.optimice_manager:
            manager.process_events(event)

            if event.type == pygame_gui.UI_SELECTION_LIST_DOUBLE_CLICKED_SELECTION and self.repository.get_in_repository() == False:
                self.selection = True
                self.set_optimice_manager_list([self.saves_manager])
                self.campaign = self.saves_selector.get_single_selection()
                if self.campaign != None:
                    self.save = self.get_path(self.campaign)
                self.engine.screen.blit(self.engine.ENGINE_BUFFER["loading"][0], (0,0))
                self.loading.set_save_path(self.save)
                self.gameStateManager.set_state('loading')
            elif event.type == pygame_gui.UI_SELECTION_LIST_NEW_SELECTION and self.repository.get_in_repository() == False:
                self.set_optimice_manager_list([self.saves_manager])
                self.campaign = self.saves_selector.get_single_selection()
                if self.campaign != None:
                    self.save = self.get_path(self.campaign)
                self.edit_button.show()
                self.delete_button.show()
                self.update_managers(self.manager_list, update=True, draw=True)
            elif event.type == pygame_gui.UI_SELECTION_LIST_DROPPED_SELECTION and self.repository.get_in_repository() == False:
                self.set_optimice_manager_list([self.saves_manager])
                self.edit_button.hide()
                self.delete_button.hide()
                self.update_managers(self.manager_list, update=True, draw=True)

    def update_managers(self, manager_list, update=False, draw=False):
        for manager in manager_list:
            if update:
                manager.update(pygame.time.Clock().tick(60) / 1000)
            if draw:
                manager.draw_ui(self.engine.screen)

    def update_ui(self):

        self.handler = False
        self.selection = False
        self.campaign = None
        self.save = ""

        self.paths = ['./docs/save_data/' + save for save in os.listdir('./docs/save_data')]
        self.saves = []

        # Read every save file and get the name, then append it to saves list in the format (name, path)
        for path in self.paths:
            with open(path, "r") as save_file:
                data = json.load(save_file)
                self.saves.append((data["name"], path))

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

        # Saves selector
        self.saves_rect = pygame.Rect(self.position_x*10, self.position_y, self.widht*1.5, self.height*12)
        self.saves_manager = pygame_gui.UIManager(self.engine.resolution, theme_path=self.engine.ENGINE_BUFFER["theme"])
        self.saves_selector = pygame_gui.elements.UISelectionList(relative_rect=self.saves_rect, manager=self.saves_manager, object_id="#ui_selector", item_list=self.saves, allow_double_clicks=True)

        # New campaign button
        self.new_button_rect = pygame.Rect(self.position_x*16, self.position_y*16, self.widht/2, self.height)
        self.new_button_manager = pygame_gui.UIManager(self.engine.resolution, theme_path=self.engine.ENGINE_BUFFER["theme"])
        self.new_button = pygame_gui.elements.UIButton(
            relative_rect=self.new_button_rect,
            manager=self.new_button_manager,
            text="+ New campaign",
            object_id="#ui_button"
        )

        # Edit campaign button
        self.edit_button_rect = pygame.Rect(self.position_x*29, self.position_y*7, self.widht/2.5, self.height)
        self.edit_button_manager = pygame_gui.UIManager(self.engine.resolution, theme_path=self.engine.ENGINE_BUFFER["theme"])
        self.edit_button = pygame_gui.elements.UIButton(
            relative_rect=self.edit_button_rect,
            manager=self.edit_button_manager,
            text="Edit",
            object_id="#ui_button"
        )
        self.edit_button.hide()
        
        # Delete campaign button
        self.delete_button_rect = pygame.Rect(self.position_x*29, self.position_y*9, self.widht/2.5, self.height)
        self.delete_button_manager = pygame_gui.UIManager(self.engine.resolution, theme_path=self.engine.ENGINE_BUFFER["theme"])
        self.delete_button = pygame_gui.elements.UIButton(
            relative_rect=self.delete_button_rect,
            manager=self.delete_button_manager,
            text="Delete",
            object_id="#ui_button"
        )
        self.delete_button.hide()

        # Confirmation dialog
        self.confirmation_rect = pygame.Rect(self.position_x*5, self.position_y*6, self.widht, self.height*3)
        self.confirmation_manager = pygame_gui.UIManager(self.engine.resolution, theme_path=self.engine.ENGINE_BUFFER["theme"])
        self.confirmation_dialog = pygame_gui.windows.UIConfirmationDialog(
            rect=self.confirmation_rect,
            manager=self.confirmation_manager,
            window_title="Delete",
            action_long_desc=f"Do you want to delete this campaign?",
            action_short_name="Delete campaign",
            blocking=True,
            object_id="#ui_dialog"
        )
        self.confirmation_dialog.hide()

        self.manager_list = [
            self.saves_manager,
            self.new_button_manager,
            self.edit_button_manager,
            self.delete_button_manager,
            self.confirmation_manager
        ]
        self.optimice_manager = []

        self.update_managers(self.manager_list, update=True, draw=True)

    def check_mouse_input(self, mouse_pos):
        if self.saves_rect.collidepoint(mouse_pos) and self.selection == False:
            self.set_optimice_manager_list([self.saves_manager])
            self.saves_selector.enable()
        elif self.new_button_rect.collidepoint(mouse_pos):
            self.set_optimice_manager_list([self.new_button_manager])
            if self.new_button.check_pressed():
                self.new_button.pressed = False
                dprint("SAVE MENU", "New campaign button clicked.", "BLUE")
                self.set_optimice_manager_list([self.new_button_manager])
                self.new_save.set_preloaded_data(file_id="", name="", desc="", scenes=[])
                self.new_save.update_ui(complete = True)
                self.gameStateManager.set_state('new_save_menu')
        elif self.edit_button_rect.collidepoint(mouse_pos):
            self.set_optimice_manager_list([self.edit_button_manager])
            if self.edit_button.check_pressed():
                self.edit_button.pressed = False
                dprint("SAVE MENU", "Edit campaign button clicked.", "BLUE")
                # Setear los datos en el new_save_menu 
                data = self.get_campaign_data(self.campaign)
                self.new_save.set_preloaded_data(file_id=data["id"], name=data["name"], desc=data["description"], scenes=data["scenes"])
                self.new_save.update_ui()
                self.gameStateManager.set_state('new_save_menu')
        elif self.delete_button_rect.collidepoint(mouse_pos):
            self.set_optimice_manager_list([self.delete_button_manager])
            if self.delete_button.check_pressed():
                self.delete_button.pressed = False
                self.selection = True
                self.set_optimice_manager_list([self.saves_manager, self.confirmation_manager])
                self.confirmation_dialog.show()
                self.confirmation_dialog.rebuild()
                dprint("SAVE MENU", "Delete campaign button clicked.", "BLUE")
        elif self.confirmation_rect.collidepoint(mouse_pos):
            self.set_optimice_manager_list([self.confirmation_manager])
        elif self.confirmation_dialog.confirm_button.check_pressed():
            self.confirmation_dialog.confirm_button.pressed = False
            self.confirmation_dialog.hide()
            self.saves_selector.disable()
            self.save_utils.delete_campaign(self.campaign)
            self.set_optimice_manager_list([self.saves_manager, self.confirmation_manager])
            self.update_ui()
            self.selection = False
            dprint("NEW SAVE", "Campaign deleted.", "GREEN")
        elif self.confirmation_dialog.cancel_button.check_pressed():
            self.confirmation_dialog.cancel_button.pressed = False
            self.confirmation_dialog.hide()
            self.saves_selector.disable()
            self.edit_button.hide()
            self.delete_button.hide()
            self.set_optimice_manager_list([self.saves_manager, self.confirmation_manager, self.delete_button_manager, self.edit_button_manager])
            self.selection = False
            dprint("NEW SAVE", "Campaign deletion canceled.", "GREEN")
        elif self.confirmation_dialog.close_window_button.check_pressed():
            self.confirmation_dialog.close_window_button.pressed = False
            self.confirmation_dialog.hide()
            self.saves_selector.disable()
            self.edit_button.hide()
            self.delete_button.hide()
            self.set_optimice_manager_list([self.saves_manager, self.confirmation_manager, self.delete_button_manager, self.edit_button_manager])
            self.selection = False
            dprint("NEW SAVE", "Campaign deletion canceled.", "GREEN")