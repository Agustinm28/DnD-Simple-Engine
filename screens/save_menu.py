import json
import os
import pygame
from utils.debugger import dprint, error
import time
import pygame_gui

class SaveMenu:

    def __init__(self, gameStateManager, engine, mouse, loading, new_save):
        self.gameStateManager = gameStateManager
        self.engine = engine
        self.mouse = mouse
        self.loading = loading
        self.new_save = new_save

        self.update_ui()
     
    def run(self):
        try:

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
        self.selection = False
        self.campaign = None

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
        self.font = pygame.font.Font("./assets/fonts/ancient.ttf", font_size)

        with open("./docs/theme.json", "r") as f:
            theme = json.load(f)
        
        theme["#name_input"]["font"][0]["size"] = str(font_size)
        theme["#desc_input"]["font"][0]["size"] = str(font_size)

        with open("./docs/theme.json", "w") as f:
            json.dump(theme, f, indent=4)

        # Saves selector
        self.saves_rect = pygame.Rect(self.position_x*10, self.position_y, self.widht*1.5, self.height*12)
        self.saves_manager = pygame_gui.UIManager(self.engine.resolution, theme_path=self.engine.ENGINE_BUFFER["theme"])
        self.saves_selector = pygame_gui.elements.UISelectionList(relative_rect=self.saves_rect, manager=self.saves_manager, object_id="#saves_selector", item_list=self.saves)

        # New campaign button
        self.new_button_rect = pygame.Rect(self.position_x*16, self.position_y*16, self.widht/2, self.height)
        self.new_button_manager = pygame_gui.UIManager(self.engine.resolution, theme_path=self.engine.ENGINE_BUFFER["theme"])
        self.new_button = pygame_gui.elements.UIButton(
            relative_rect=self.new_button_rect,
            manager=self.new_button_manager,
            text="+ New campaign",
            object_id="#new_button"
        )

        self.manager_list = [
            self.saves_manager,
            self.new_button_manager
        ]
        self.optimice_manager = []

        self.update_managers(self.manager_list, update=True, draw=True)

    def check_mouse_input(self, mouse_pos):
        if self.saves_rect.collidepoint(mouse_pos) and self.selection == False:
            self.saves_selector.pressed = False
            self.saves_selector.enable()
            self.set_optimice_manager_list([self.saves_manager])
            self.campaign = self.saves_selector.get_single_selection()
            if self.campaign != None:
                self.set_optimice_manager_list([self.saves_manager])
                #! Que aparezcan los botones para cargar, editar u borrar
        elif self.new_button_rect.collidepoint(mouse_pos):
            self.set_optimice_manager_list([self.new_button_manager])
            if self.new_button.check_pressed():
                self.new_button.pressed = False
                dprint("SAVE MENU", "New campaign button clicked.", "BLUE")
                self.set_optimice_manager_list([self.new_button_manager])
                self.new_save.update_ui(complete = True)
                self.gameStateManager.set_state('new_save_menu')

        #! ACA DEJO LA LOGICA DE CARGAR UNA PARTIDA
        # self.engine.screen.blit(self.engine.ENGINE_BUFFER["loading"][0], (0,0))
        # self.loading.set_save_path(save_path)
        # self.gameStateManager.set_state('loading')
