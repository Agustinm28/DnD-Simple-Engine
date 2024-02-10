import pygame
from utils.debugger import dprint, error

class MainMenu:

    def __init__(self, gameStateManager, engine, mouse, exit_class, repository, save_menu):
        self.gameStateManager = gameStateManager
        self.engine = engine
        self.mouse = mouse
        self.exit_class = exit_class
        self.repository = repository
        self.save_menu = save_menu

        self.language = self.engine.ENGINE_BUFFER["language"]["main_menu"]

    def run(self):
        '''
        Method to run the main menu.
        '''
        try:
            self.engine.screen.blit(self.engine.ENGINE_BUFFER["main_menu"][0], (0,0))
            self.engine.ENGINE_BUFFER["scenes_menu"][0] = self.engine.ENGINE_BUFFER["main_menu"][0]
            self.language = self.engine.ENGINE_BUFFER["language"]["main_menu"]

            scale_x = self.engine.resolution[0] / 1920
            scale_y = self.engine.resolution[1] / 1080

            #max_x = int(400 * scale_x) Este la verdad no se
            max_y = int(850 * scale_y)

            coordenates = []
            x = int(50 * scale_x)
            y = int(50 * scale_y)
            widht = int(400 * scale_x)
            height = int(100 * scale_y)

            options = [self.language["start_button"], self.language["repository_button"], self.language["options_button"], self.language["exit_button"]]

            font_size = int(36 * min(scale_x, scale_y))
            font = pygame.font.Font("./assets/fonts/ancient.ttf", font_size)
            color = (44, 33, 46)

            for l in range(len(options)):
                coordenates.append((x, y, widht, height))
                y += height

                if y > max_y:
                    y = int(50 * scale_y)
                    x += widht

            rects = {f'{options[i]}': pygame.Rect(coordenates) for i, coordenates in enumerate(coordenates)}

            for rect in rects.values():
                pygame.gfxdraw.box(self.engine.screen, rect, (0, 0, 0, 0))

            # Resize scene buttons image
            scene_image = pygame.transform.scale(self.engine.ENGINE_BUFFER["scene"][0], (widht,height))

            # Add images to buttons
            for name, rect in rects.items():
                text = font.render(name, True, color)
                text_rect = text.get_rect(center=rect.center)

                self.engine.screen.blit(scene_image, rect.topleft)
                self.engine.screen.blit(text, text_rect)

            # Get mouse position
            mouse_pos = pygame.mouse.get_pos()

            # Check if mouse is over a button
            for name, rect in rects.items():
                self.handle_button_event(name, rect, mouse_pos)
        except Exception:
            error("Error showing options menu")

    def handle_button_event(self, button_name, button, mouse_pos):
        '''
        Method to handle button events. Where:
            - button_name: name of the button.
            - button: button object.
            - mouse_pos: mouse position.
        '''
        try:
            if button.collidepoint(mouse_pos):
                if self.mouse.get_click():
                    self.mouse.set_click('up')
                    if self.engine.audio.MUSIC:
                        self.engine.audio.stop()
                    if button_name == self.language["start_button"]:
                        dprint("MAIN MENU", "Start button clicked.", "BLUE")
                        self.save_menu.update_ui()
                        self.gameStateManager.set_state('save_menu')
                    elif button_name == self.language["repository_button"]:
                        dprint("MAIN MENU", "Repository button clicked.", "BLUE")
                        self.repository.update_ui()
                        self.gameStateManager.set_state('repository')
                    elif button_name == self.language["options_button"]:
                        dprint("MAIN MENU", "Options button clicked.", "BLUE")
                        self.gameStateManager.set_state('options_menu')
                    elif button_name == self.language["exit_button"]:
                        self.exit_class.set_status(True)

        except Exception:
            error("Error handling button event")