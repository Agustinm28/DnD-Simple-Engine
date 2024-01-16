import pygame
import pygame.gfxdraw
from modules.audio import Audio
from modules.engine import Engine
import sys

class Game:

    RUNNING = False # Check if game is running
    MAIN_MENU = False # Check if main menu is running
    SCENES_MENU = False # Check if scenes menu is running
    SCENE = False # Check if scene is running
    LOAD = False # Check if campaign data is loaded
    LOAD_SCREEN = False # Check if load screen is running
    OPTIONS = False # Check if options menu is running
    SCENE_NAME = None 

    def __init__(self, resolution:tuple = None, mode = None):
        self.engine = Engine(
            resolution=resolution, 
            mode=mode
            )

    def show_scene_menu(self):

        scale_x = self.engine.resolution[0] / 1920
        scale_y = self.engine.resolution[1] / 1080

        #max_x = int(400 * scale_x) Este la verdad no se
        max_y = int(850 * scale_y)

        coordenates = []
        x = int(50 * scale_x)
        y = int(50 * scale_y)
        widht = int(400 * scale_x)
        height = int(100 * scale_y)

        #! ACA SE CARGAN LOS ASSETS DE LAS ESCENAS DE PHAROS EN BUFFER == DESPUES QUITAR
        if not self.LOAD:
            self.engine.load_saved_game("./docs/save_data/000.json")
            self.LOAD = True
        #!##############################################################################

        names = list(self.engine.SCENES_BUFFER.keys())
        font_size = int(36 * min(scale_x, scale_y))
        font = pygame.font.Font("./assets/fonts/ancient.ttf", font_size)
        color = (44, 33, 46)

        for l in range(len(self.engine.SCENES_BUFFER)):
            coordenates.append((x, y, widht, height))
            y += height

            if y > max_y:
                y = int(50 * scale_y)
                x += widht

        rects = {f'{names[i]}': pygame.Rect(coordenates) for i, coordenates in enumerate(coordenates)}

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
                    music = self.engine.audio.check()
                    if music is not None:
                        self.engine.audio.stop()
                    self.engine.audio.play(self.engine.SCENES_BUFFER[f"{button_name}"][1])
                    self.engine.ENGINE_BUFFER["scenes_menu"][0] = self.engine.SCENES_BUFFER[f"{button_name}"][0]
                    self.show_scene(button_name)
                    print(f"{button_name} selected")

    def show_scene(self, scene_name):
        self.MAIN_MENU = False
        self.SCENES_MENU = False
        self.SCENE = True
        self.SCENE_NAME = scene_name

    def show_main_menu(self):

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
                    print("Start button clicked")
                    self.engine.screen.blit(self.engine.ENGINE_BUFFER["loading"][0], (0,0))
                    self.MAIN_MENU = False
                    self.SCENES_MENU = True
        elif options.collidepoint(mouse_pos):
            for event in pygame.event.get(): 
                if event.type == pygame.MOUSEBUTTONDOWN:
                    print("Options button clicked")
                    self.MAIN_MENU = False
                    self.OPTIONS = True
        elif exit_game.collidepoint(mouse_pos):
            for event in pygame.event.get(): 
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.RUNNING = False

    def show_option_menu(self):
        scale_x = self.engine.resolution[0] / 1920
        scale_y = self.engine.resolution[1] / 1080

        widht = int(400 * scale_x)
        height = int(100 * scale_y)

        position_x = int(50 * scale_x)
        position_y = int(50 * scale_y)

        resolution = pygame.Rect(position_x, position_y, widht, height)
        mode = pygame.Rect(position_x, position_y*3, widht, height)

        # Draw buttons
        pygame.gfxdraw.box(self.engine.screen, resolution, (0, 0, 0, 0))
        pygame.gfxdraw.box(self.engine.screen, mode, (0, 0, 0, 0))

        # Resize images
        image_button_1 = pygame.transform.scale(self.engine.ENGINE_BUFFER["scene"][0], (widht, height))
        image_button_2 = pygame.transform.scale(self.engine.ENGINE_BUFFER["scene"][0], (widht, height))

        # Add images to buttons
        self.engine.screen.blit(image_button_1, (position_x,position_y))
        self.engine.screen.blit(image_button_2, (position_x,position_y*3))

        # Get mouse position
        mouse_pos = pygame.mouse.get_pos()

        # Check if mouse is over a button
        if resolution.collidepoint(mouse_pos):
            for event in pygame.event.get(): 
                if event.type == pygame.MOUSEBUTTONDOWN:
                    print("Resolution button clicked")
        elif mode.collidepoint(mouse_pos):
            for event in pygame.event.get(): 
                if event.type == pygame.MOUSEBUTTONDOWN:
                    print("Mode button clicked")

    def run(self):
        self.RUNNING = True
        self.MAIN_MENU = True
        self.SCENES_MENU = False
        self.SCENE = False
        self.LOAD = False
        self.LOAD_SCREEN = False
        self.OPTIONS = False

        while self.RUNNING:
            for event in pygame.event.get():
                ### Key events
                if event.type == pygame.QUIT:
                    self.RUNNING = False
                elif event.type==pygame.KEYDOWN:
                    if event.key==pygame.K_m:
                        if not self.MAIN_MENU:
                            if self.SCENES_MENU and self.SCENE:
                                self.SCENES_MENU = False
                            elif not self.SCENES_MENU and self.SCENE:
                                self.SCENES_MENU = True
                            elif self.SCENES_MENU and not self.SCENE:
                                pass
                    elif event.key==pygame.K_ESCAPE: #! Si se sale al menu principal, que se descargue la memoria, cartel para usuario
                        self.SCENES_MENU = False
                        self.SCENE = False
                        self.OPTIONS = False
                        self.MAIN_MENU = True
                        music = self.engine.audio.check()
                        if music is not None:
                            self.engine.audio.stop()
                    elif event.key==pygame.K_a: #! Ver para que esto funcione solo durante la partida (se peude poner desde el menu)
                        music = self.engine.audio.check()
                        if music is not None:
                            self.engine.audio.stop()
                        self.engine.audio.play("./assets/audio/personalized/El culto a Pharos/battle.mp3")
            
            ### SHOW SCREENS FROM BUFFER
            self.engine.screen.fill((0,0,0))

            if self.MAIN_MENU:
                self.engine.screen.blit(self.engine.ENGINE_BUFFER["main_menu"][0], (0,0))
                self.engine.ENGINE_BUFFER["scenes_menu"][0] = self.engine.ENGINE_BUFFER["main_menu"][0]
                self.show_main_menu()
            elif self.SCENES_MENU and self.SCENE:
                self.engine.screen.blit(self.engine.SCENES_BUFFER[self.SCENE_NAME][0], (0,0))
                self.show_scene_menu()
            elif self.SCENES_MENU:
                self.engine.screen.blit(self.engine.ENGINE_BUFFER["scenes_menu"][0], (0,0))
                self.show_scene_menu()
            elif self.SCENE:
                self.engine.screen.blit(self.engine.SCENES_BUFFER[self.SCENE_NAME][0], (0,0))
            elif self.OPTIONS:
                self.engine.screen.blit(self.engine.ENGINE_BUFFER["main_menu"][0], (0,0))
                self.show_option_menu()

            pygame.display.flip()

        pygame.quit()
        sys.exit()
