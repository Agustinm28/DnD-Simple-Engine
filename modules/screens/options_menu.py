import pygame
import time

class OptionsMenu:

    RES = None

    def __init__(self, engine, game):
        self.engine = engine
        self.game = game

    def show(self):

        scale_x = self.engine.resolution[0] / 1920
        scale_y = self.engine.resolution[1] / 1080

        #max_x = int(400 * scale_x) Este la verdad no se
        max_y = int(850 * scale_y)

        coordenates = []
        x = int(50 * scale_x)
        y = int(50 * scale_y)
        widht = int(400 * scale_x)
        height = int(100 * scale_y)

        options = ["Resolution", "Fullscreen"]

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

    def handle_button_event(self, button_name, button, mouse_pos):
        if button.collidepoint(mouse_pos):
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.engine.audio.MUSIC:
                        self.engine.audio.stop()
                    if button_name == "Resolution":
                        self.game.OPTIONS = False
                        self.game.RES_OPTIONS = True
                        print("Resolution button clicked")
                    elif button_name == "Fullscreen":
                        if self.engine.ENGINE_BUFFER["fullscreen"]:
                            print("Windowed mode")  
                            self.engine.toggle_fullscreen(mode=False)
                        else:
                            self.engine.toggle_fullscreen(mode=True)
                        print("Fullscreen button clicked")
                    print(f"{button_name} selected")

    def show_resolution_menu(self):

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

    def handle_resolution_event(self, button_name, button, mouse_pos, resolution):
        if button.collidepoint(mouse_pos):
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.engine.audio.MUSIC:
                        self.engine.audio.stop()
                    self.RES = resolution
                    self.game.RES_CHANGE = True
                    print(f"{button_name} selected")
