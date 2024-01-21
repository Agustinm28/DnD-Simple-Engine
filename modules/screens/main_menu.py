import pygame
from utils.debugger import dprint, error

class MainMenu:

    def __init__(self, engine, game):
        self.engine = engine
        self.game = game

    def show(self):
        '''
        Method to show main menu.
        '''
        try:
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
            pygame.gfxdraw.box(self.engine.screen, start, (0, 0, 0, 0))
            pygame.gfxdraw.box(self.engine.screen, options, (0, 0, 0, 0))
            pygame.gfxdraw.box(self.engine.screen, exit_game, (0, 0, 0, 0))

            # Resize images
            image_button_1 = pygame.transform.scale(self.engine.ENGINE_BUFFER["start"][0], (widht, height))
            image_button_2 = pygame.transform.scale(self.engine.ENGINE_BUFFER["options"][0], (widht, height))
            image_button_3 = pygame.transform.scale(self.engine.ENGINE_BUFFER["exit"][0], (widht, height))

            # Add images to buttons
            self.engine.screen.blit(image_button_1, (position_x,position_y))
            self.engine.screen.blit(image_button_2, (position_x,position_y*3))
            self.engine.screen.blit(image_button_3, (position_x,position_y*5))

            # Get mouse position
            mouse_pos = pygame.mouse.get_pos()
            
            # Check if mouse is over a button
            if start.collidepoint(mouse_pos):
                for event in pygame.event.get(): 
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        dprint("MAIN MENU", "Start button clicked.", "BLUE")
                        self.game.MAIN_MENU = False
                        self.game.SAVE_MENU = True
            elif options.collidepoint(mouse_pos):
                for event in pygame.event.get(): 
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        dprint("MAIN MENU", "Options button clicked.", "BLUE")
                        self.game.MAIN_MENU = False
                        self.game.OPTIONS = True
            elif exit_game.collidepoint(mouse_pos):
                for event in pygame.event.get(): 
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        self.game.RUNNING = False
        except Exception:
            error("Error showing main menu")