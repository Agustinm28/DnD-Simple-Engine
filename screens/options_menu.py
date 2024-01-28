import json
import pygame
import pygame_gui
from utils.debugger import info, error, dprint

class OptionsMenu:

    def __init__(self, gameStateManager, engine, mouse):
        self.gameStateManager = gameStateManager
        self.engine = engine
        self.mouse = mouse

        self.update_ui()

    def run(self):
        try:

            if self.gameStateManager.get_last_state() != 'main_menu':
                self.gameStateManager.set_last_state('main_menu')

            self.engine.screen.blit(self.engine.ENGINE_BUFFER["main_menu"][0], (0,0))
            self.set_handler(True)

            self.update_managers(self.optimice_manager, update=True, draw=True)
            self.update_managers(self.manager_list, update=False, draw=True)

            mouse_pos = pygame.mouse.get_pos()
            self.check_mouse_input(mouse_pos)

        except Exception:
            error("Error showing options menu")
    
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
        self.actual_resolution = f"{self.engine.resolution[0]} x {self.engine.resolution[1]}"
        mode_status = self.engine.ENGINE_BUFFER["fullscreen"]
        if mode_status:
            self.actual_mode = "Fullscreen"
        else:
            self.actual_mode = "Windowed"

        self.scale_x = self.engine.resolution[0] / 1920
        self.scale_y = self.engine.resolution[1] / 1080
 
        self.widht = int(300 * self.scale_x)
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

        # Resolution label
        self.resolution_label_rect = pygame.Rect(self.position_x*2, self.position_y, self.widht, self.height)
        self.resolution_label_manager = pygame_gui.UIManager(self.engine.resolution, theme_path=self.engine.ENGINE_BUFFER["theme"])
        self.resolution_label_label = pygame_gui.elements.UILabel(relative_rect=self.resolution_label_rect, manager=self.resolution_label_manager, object_id="#ui_label", text="Resolution")

        self.resolutions = []
        for resolution in self.engine.AVAILABLE_RESOLUTIONS:
            self.resolutions.append(f"{resolution[0]} x {resolution[1]}")

        # Resolution dropdown selector
        self.resolution_dropdown_rect = pygame.Rect(self.position_x, self.position_y*2, self.widht*1.5, self.height)
        self.resolution_dropdown_manager = pygame_gui.UIManager(self.engine.resolution, theme_path=self.engine.ENGINE_BUFFER["theme"])
        self.resolution_dropdown = pygame_gui.elements.UIDropDownMenu(
            options_list=self.resolutions,
            relative_rect=self.resolution_dropdown_rect,
            manager=self.resolution_dropdown_manager,
            starting_option=self.actual_resolution,
            object_id="#ui_dropdown"
        )

        # Window label
        self.window_label_rect = pygame.Rect(self.position_x*12, self.position_y, self.widht, self.height)
        self.window_label_manager = pygame_gui.UIManager(self.engine.resolution, theme_path=self.engine.ENGINE_BUFFER["theme"])
        self.window_label_label = pygame_gui.elements.UILabel(relative_rect=self.window_label_rect, manager=self.window_label_manager, object_id="#ui_label", text="Window mode")

        
        # Window mode button
        self.window_button_rect = pygame.Rect(self.position_x*12, self.position_y*2, self.widht, self.height)
        self.window_button_manager = pygame_gui.UIManager(self.engine.resolution, theme_path=self.engine.ENGINE_BUFFER["theme"])
        self.window_button = pygame_gui.elements.UIButton(
            relative_rect=self.window_button_rect,
            manager=self.window_button_manager,
            text=self.actual_mode,
            object_id="#ui_button"
        )

        self.manager_list = [
            self.resolution_label_manager,
            self.window_label_manager,
            self.window_button_manager,
            self.resolution_dropdown_manager
        ]
        self.optimice_manager = []

        self.update_managers(self.manager_list, update=True, draw=True)
    
    def check_mouse_input(self, mouse_pos):
        # Manager updating
        if self.resolution_label_rect.collidepoint(mouse_pos):
            self.set_optimice_manager_list([self.resolution_label_manager])
        elif self.resolution_dropdown_rect.collidepoint(mouse_pos):
            self.set_optimice_manager_list([self.resolution_dropdown_manager])
        elif self.window_label_rect.collidepoint(mouse_pos):
            self.set_optimice_manager_list([self.window_label_manager])
        elif self.window_button_rect.collidepoint(mouse_pos):
            self.set_optimice_manager_list([self.window_button_manager])
            if self.window_button.check_pressed():
                self.window_button.pressed = False
                if self.actual_mode == "Fullscreen":
                    self.actual_mode = "Windowed"
                    self.engine.toggle_fullscreen(mode=False)
                else:
                    self.actual_mode = "Fullscreen"
                    self.engine.toggle_fullscreen(mode=True)
                self.update_ui()

        # Actions
        elif self.resolution_dropdown.selected_option != self.actual_resolution:
            self.engine.screen.blit(self.engine.ENGINE_BUFFER["main_menu"][0], (0,0))
            res_x = int(self.resolution_dropdown.selected_option.split(" x ")[0])
            res_y = int(self.resolution_dropdown.selected_option.split(" x ")[1])
            new_resolution = (res_x, res_y)
            self.engine.update_screen(new_resolution, self.engine.mode)
            self.actual_resolution = self.resolution_dropdown.selected_option
            self.update_ui()
            dprint("OPTIONS MENU", f"Resolution changed to {self.actual_resolution}", "BLUE")
            