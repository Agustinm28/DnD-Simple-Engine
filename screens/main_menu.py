import pygame
from utils.debugger import dprint, error

class MainMenu:

    def __init__(self, display, gameStateManager, engine):
        self.display = display
        self.gameStateManager = gameStateManager
        self.engine = engine
        self.clicked = False

    def run(self):
        try:

            self.display.blit(self.engine.ENGINE_BUFFER["main_menu"][0], (0,0))
            self.engine.ENGINE_BUFFER["scenes_menu"][0] = self.engine.ENGINE_BUFFER["main_menu"][0]

            scale_x = self.engine.resolution[0] / 1920
            scale_y = self.engine.resolution[1] / 1080

            widht = int(400 * scale_x)
            height = int(100 * scale_y)

            position_x = int(50 * scale_x)
            position_y = int(50 * scale_y)

            start = pygame.Rect(position_x, position_y, widht, height)
            options = pygame.Rect(position_x, position_y*3, widht, height)
            exit_game = pygame.Rect(position_x, position_y*5, widht, height)

            # Draw buttons
            pygame.gfxdraw.box(self.display, start, (0, 0, 0, 0))
            pygame.gfxdraw.box(self.display, options, (0, 0, 0, 0))
            pygame.gfxdraw.box(self.display, exit_game, (0, 0, 0, 0))

            # Resize images
            image_button_1 = pygame.transform.scale(self.engine.ENGINE_BUFFER["start"][0], (widht, height))
            image_button_2 = pygame.transform.scale(self.engine.ENGINE_BUFFER["options"][0], (widht, height))
            image_button_3 = pygame.transform.scale(self.engine.ENGINE_BUFFER["exit"][0], (widht, height))

            # Add images to buttons
            self.display.blit(image_button_1, (position_x,position_y))
            self.display.blit(image_button_2, (position_x,position_y*3))
            self.display.blit(image_button_3, (position_x,position_y*5))

            # Get mouse position
            mouse_pos = pygame.mouse.get_pos()

            # Check if mouse is over a button
            if start.collidepoint(mouse_pos):
                if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                    self.clicked = True
                    dprint("MAIN MENU", "Start button clicked.", "BLUE")
            elif options.collidepoint(mouse_pos):
                if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                    self.clicked = True
                    dprint("MAIN MENU", "Options button clicked.", "BLUE")
                    self.gameStateManager.set_state('options_menu')
            elif exit_game.collidepoint(mouse_pos):
                if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                    self.clicked = True
                    self.gameStateManager.set_state('exit')

            if pygame.mouse.get_pressed()[0] == 0:
                self.clicked = False

            self.engine.restart_buffer(buffer="SCENES")
            
        except Exception:
            error("Error showing main menu")