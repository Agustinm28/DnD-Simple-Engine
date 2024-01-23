import pygame
from utils.debugger import info, error, dprint
import time

class ResMenu:

    def __init__(self, gameStateManager, engine, mouse, new_save_menu):
        self.gameStateManager = gameStateManager
        self.engine = engine
        self.mouse = mouse
        self.new_save_menu = new_save_menu

    def run(self):
        '''
        Method to show resolution menu.
        '''
        try:

            self.engine.screen.blit(self.engine.ENGINE_BUFFER["main_menu"][0], (0,0))

            scale_x = self.engine.resolution[0] / 1920
            scale_y = self.engine.resolution[1] / 1080

            #max_x = int(400 * scale_x) Este la verdad no se
            max_y = int(850 * scale_y)

            options = self.engine.AVAILABLE_RESOLUTIONS

            coordenates = []
            x = int(50 * scale_x)
            y = int(50 * scale_y)
            widht = int(400 * scale_x)
            height = int(100 * scale_y)

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
                
                res_x = name.split(",")[0].split("(")[1]
                res_y = name.split(",")[1].split(")")[0]
                res = f"{res_x} x {res_y}"

                text = font.render(res, True, color)
                text_rect = text.get_rect(center=rect.center)

                self.engine.screen.blit(scene_image, rect.topleft)
                self.engine.screen.blit(text, text_rect)

            # Get mouse position
            mouse_pos = pygame.mouse.get_pos()

            # Check if mouse is over a button
            for name, rect in rects.items():
                res_x = name.split(",")[0].split("(")[1]
                res_y = name.split(",")[1].split(")")[0]
                self.handle_resolution_event(name, rect, mouse_pos, (int(res_x), int(res_y)))
        except Exception:
            error("Error showing resolution menu")

    def handle_resolution_event(self, button_name, button, mouse_pos, resolution):
        '''
        Method to handle resolution events. Where:
            - button_name: name of the button.
            - button: button object.
            - mouse_pos: mouse position.
            - resolution: resolution to change.
        '''
        try:
            if button.collidepoint(mouse_pos):
                if self.mouse.get_click():
                    self.mouse.set_click('up')
                    if self.engine.audio.MUSIC:
                        self.engine.audio.stop()
                    self.engine.screen.blit(self.engine.ENGINE_BUFFER["main_menu"][0], (0,0))
                    self.engine.update_screen(resolution, self.engine.mode)
                    self.new_save_menu.update_ui(resolution)
                    dprint("OPTIONS MENU", f"Resolution button clicked. Resolution: {resolution}", "BLUE")
        except Exception:
            error("Error handling resolution event")