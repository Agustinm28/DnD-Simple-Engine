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
    SCENE_NAME = None 

    def __init__(self):
        self.engine = Engine()

    def show_scene_menu(self):

        coordenates = []
        x = 50
        y = 50
        widht = 400
        height = 100

        #! ACA SE CARGAN LOS ASSETS DE LAS ESCENAS DE PHAROS EN BUFFER == DESPUES QUITAR
        if not self.LOAD:
            self.engine.load_saved_game("./docs/save_data/000.json")
            self.LOAD = True
        #!##############################################################################

        names = list(self.engine.SCENES_BUFFER.keys())
        font = pygame.font.Font("./assets/fonts/ancient.ttf", 36)
        outline = 2
        color = (44, 33, 46)

        for _ in range(len(self.engine.SCENES_BUFFER)):
            coordenates.append((x, y, widht, height))
            y += 100

            if y > 850:
                y = 50
                x += 400

        rects = {f'{names[i]}': pygame.Rect(coordenates) for i, coordenates in enumerate(coordenates)}

        for rect in rects.values():
            pygame.gfxdraw.box(self.engine.screen, rect, (0, 0, 0, 0))

        # Resize scene buttons image
        scene_image = pygame.transform.scale(self.engine.ENGINE_BUFFER["scene"][0], (400,100))

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

        start = pygame.Rect(50, 50, 400, 100)
        options = pygame.Rect(50, 150, 400, 100)
        exit_game = pygame.Rect(50, 250, 400, 100)

        # Draw buttons
        pygame.gfxdraw.box(self.engine.screen, start, (0, 0, 0, 0))
        pygame.gfxdraw.box(self.engine.screen, options, (0, 0, 0, 0))
        pygame.gfxdraw.box(self.engine.screen, exit_game, (0, 0, 0, 0))

        # Resize images
        image_button_1 = pygame.transform.scale(self.engine.ENGINE_BUFFER["start"][0], (400,100))
        image_button_2 = pygame.transform.scale(self.engine.ENGINE_BUFFER["options"][0], (400,100))
        image_button_3 = pygame.transform.scale(self.engine.ENGINE_BUFFER["exit"][0], (400,100))

        # Add images to buttons
        self.engine.screen.blit(image_button_1, (50,50))
        self.engine.screen.blit(image_button_2, (50,150))
        self.engine.screen.blit(image_button_3, (50,250))

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
        elif exit_game.collidepoint(mouse_pos):
            for event in pygame.event.get(): 
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.RUNNING = False


    def run(self):
        self.RUNNING = True
        self.MAIN_MENU = True
        self.SCENES_MENU = False
        self.SCENE = False
        self.LOAD = False
        self.LOAD_SCREEN = False

        while self.RUNNING:
            for event in pygame.event.get():
                ### Key events
                if event.type == pygame.QUIT:
                    self.RUNNING = False
                elif event.type==pygame.KEYDOWN:
                    if event.key==pygame.K_m: #! Aca tambien, poner una flag o algo para que no pueda activarse si no se cargo antes desde el menu principal
                        if self.SCENES_MENU:
                            self.MAIN_MENU = False
                            self.SCENE = True
                            self.SCENES_MENU = False
                        else:
                            self.MAIN_MENU = False
                            self.SCENE = False
                            self.SCENES_MENU = True
                    elif event.key==pygame.K_h:
                        self.SCENES_MENU = False
                        self.SCENE = False
                        self.MAIN_MENU = True
                        music = self.engine.audio.check()
                        if music is not None:
                            self.engine.audio.stop()
                    elif event.key==pygame.K_ESCAPE:
                        self.RUNNING = False
                    elif event.key==pygame.K_a: #! Ver para que esto funcione solo durante la partida (se peude poner desde el menu)
                        music = self.engine.audio.check()
                        if music is not None:
                            self.engine.audio.stop()
                        self.engine.audio.play("./audio/personalized/El culto a Pharos/battle.mp3")
            
            ### SHOW SCREENS FROM BUFFER
            self.engine.screen.fill((0,0,0))

            if self.MAIN_MENU:
                self.engine.screen.blit(self.engine.ENGINE_BUFFER["main_menu"][0], (0,0))
                self.engine.ENGINE_BUFFER["scenes_menu"][0] = self.engine.ENGINE_BUFFER["main_menu"][0]
                self.show_main_menu()
            elif self.SCENES_MENU:
                self.engine.screen.blit(self.engine.ENGINE_BUFFER["scenes_menu"][0], (0,0))
                self.show_scene_menu()
            elif self.SCENE:
                self.engine.screen.blit(self.engine.SCENES_BUFFER[self.SCENE_NAME][0], (0,0))

            pygame.display.flip()

        pygame.quit()
        sys.exit()
