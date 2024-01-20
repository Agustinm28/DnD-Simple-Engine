import json
import os
import pygame
from utils.debugger import dprint, error

class SavesMenu:

    def __init__(self, engine, game):
        self.engine = engine
        self.game = game

    def show(self):
        '''
        Method to show saves menu.
        '''
        try:
            scale_x = self.engine.resolution[0] / 1920
            scale_y = self.engine.resolution[1] / 1080

            #max_x = int(400 * scale_x) Este la verdad no se
            max_y = int(850 * scale_y)

            coordenates = []
            x = int(50 * scale_x)
            y = int(50 * scale_y)
            widht = int(400 * scale_x)
            height = int(100 * scale_y)

            paths = ['./docs/save_data/' + save for save in os.listdir('./docs/save_data')]
            saves = []

            # Read every save file and get the name, then append it to saves list in the format (name, path)
            for path in paths:
                with open(path, "r") as save_file:
                    data = json.load(save_file)
                    saves.append((data["name"], path))

            saves.append(("+ New campaign", None))

            font_size = int(36 * min(scale_x, scale_y))
            font = pygame.font.Font("./assets/fonts/ancient.ttf", font_size)
            color = (44, 33, 46)

            for l in range(len(saves)):
                coordenates.append((x, y, widht, height))
                y += height

                if y > max_y:
                    y = int(50 * scale_y)
                    x += widht

            rects = {f'{saves[i][0]}': [pygame.Rect(coordenates), saves[i][1]] for i, coordenates in enumerate(coordenates)}

            for rect in rects.values():
                pygame.gfxdraw.box(self.engine.screen, rect[0], (0, 0, 0, 0))

            # Resize scene buttons image
            scene_image = pygame.transform.scale(self.engine.ENGINE_BUFFER["scene"][0], (widht,height))

            # Add images to buttons
            for name, rect in rects.items():
                text = font.render(name, True, color)
                rect_value = rect[0]
                text_rect = text.get_rect(center=rect_value.center)

                self.engine.screen.blit(scene_image, rect_value.topleft)
                self.engine.screen.blit(text, text_rect)

            # Get mouse position
            mouse_pos = pygame.mouse.get_pos()

            # Check if mouse is over a button
            for name, rect in rects.items():
                self.handle_button_event(name, rect[0], mouse_pos, rect[1])
        except Exception:
            error("Error showing saves menu")

    def handle_button_event(self, button_name, button, mouse_pos, save_path):
        '''
        Method to handle button events. Where:
            - button_name: name of the button.
            - button: button object.
            - mouse_pos: mouse position.
        '''
        try:
            if button.collidepoint(mouse_pos):
                for event in pygame.event.get():
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if self.engine.audio.MUSIC:
                            self.engine.audio.stop()
                        if button_name == "+ New campaign":
                            dprint("SAVES MENU", f"New campaign", "BLUE")
                        else:
                            self.engine.screen.blit(self.engine.ENGINE_BUFFER["loading"][0], (0,0))
                            self.game.save_path = save_path
                            self.game.SAVE_MENU = False
                            self.game.SCENES_MENU = True
                            
        except Exception:
            error("Error handling button event")