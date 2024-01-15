import pygame
import pygame.gfxdraw
from modules.audio import Audio
from modules.engine import Engine
import sys

class Game:

    RUNNING = False # Check if game is running
    MAIN_MENU = False # Check if main menu is running
    SCENES = False # Check if scenes menu is running
    SCENE = False # Check if scene is running
    LOAD = False # Check if campaign data is loaded
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
        # if tavern.collidepoint(mouse_pos):
        #     for event in pygame.event.get(): 
        #         if event.type == pygame.MOUSEBUTTONDOWN:
        #             self.reset_buffer()
        #             music = self.audio.check()
        #             if music is not None:
        #                 self.audio.stop()
        #             self.add_image("./images/personalized/El culto a Pharos/scenes/tavern.jpeg")
        #             self.audio.play("./audio/personalized/El culto a Pharos/Tavern.mp3")
        #             self.SCENES = False
        #             self.SCENE = True
        #             print("Tavern selected")
        # elif travel_path.collidepoint(mouse_pos):
        #     for event in pygame.event.get(): 
        #         if event.type == pygame.MOUSEBUTTONDOWN:
        #             self.reset_buffer()
        #             music = self.audio.check()
        #             if music is not None:
        #                 self.audio.stop()
        #             self.add_image("./images/personalized/El culto a Pharos/scenes/travel_path.jpg")
        #             self.audio.play("./audio/personalized/El culto a Pharos/travel_path.mp3")
        #             self.SCENES = False
        #             self.SCENE = True
        #             print("Travel selected")
        # elif betian.collidepoint(mouse_pos):
        #     for event in pygame.event.get(): 
        #         if event.type == pygame.MOUSEBUTTONDOWN:
        #             self.reset_buffer()
        #             music = self.audio.check()
        #             if music is not None:
        #                 self.audio.stop()
        #             self.add_image("./images/personalized/El culto a Pharos/scenes/betian.png")
        #             self.audio.play("./audio/personalized/El culto a Pharos/betian.mp3")
        #             self.SCENES = False
        #             self.SCENE = True
        #             print("Betian selected")
        # elif posada.collidepoint(mouse_pos):
        #     for event in pygame.event.get(): 
        #         if event.type == pygame.MOUSEBUTTONDOWN:
        #             self.reset_buffer()
        #             music = self.audio.check()
        #             if music is not None:
        #                 self.audio.stop()
        #             self.add_image("./images/personalized/El culto a Pharos/scenes/posada.jpeg")
        #             self.audio.play("./audio/personalized/El culto a Pharos/posada.mp3")
        #             self.SCENES = False
        #             self.SCENE = True
        #             print("Posada selected")
        # elif bedroom.collidepoint(mouse_pos):
        #     for event in pygame.event.get(): 
        #         if event.type == pygame.MOUSEBUTTONDOWN:
        #             self.reset_buffer()
        #             music = self.audio.check()
        #             if music is not None:
        #                 self.audio.stop()
        #             self.add_image("./images/personalized/El culto a Pharos/scenes/bedroom.jpg")
        #             self.audio.play("./audio/personalized/El culto a Pharos/posada.mp3")
        #             self.SCENES = False
        #             self.SCENE = True
        #             print("Bedroom selected")
        # elif field.collidepoint(mouse_pos):
        #     for event in pygame.event.get(): 
        #         if event.type == pygame.MOUSEBUTTONDOWN:
        #             self.reset_buffer()
        #             music = self.audio.check()
        #             if music is not None:
        #                 self.audio.stop()
        #             self.add_image("./images/personalized/El culto a Pharos/scenes/field.jpeg")
        #             self.audio.play("./audio/personalized/El culto a Pharos/field.mp3")
        #             self.SCENES = False
        #             self.SCENE = True
        #             print("Field selected")
        # elif farm_outside.collidepoint(mouse_pos):
        #     for event in pygame.event.get(): 
        #         if event.type == pygame.MOUSEBUTTONDOWN:
        #             self.reset_buffer()
        #             music = self.audio.check()
        #             if music is not None:
        #                 self.audio.stop()
        #             self.add_image("./images/personalized/El culto a Pharos/scenes/fence.jpeg")
        #             self.audio.play("./audio/personalized/El culto a Pharos/fence.mp3")
        #             self.SCENES = False
        #             self.SCENE = True
        #             print("Farm outside selected")
        # elif morwen_farm.collidepoint(mouse_pos):
        #     for event in pygame.event.get(): 
        #         if event.type == pygame.MOUSEBUTTONDOWN:
        #             self.reset_buffer()
        #             music = self.audio.check()
        #             if music is not None:
        #                 self.audio.stop()
        #             self.add_image("./images/personalized/El culto a Pharos/scenes/farm.png")
        #             self.audio.play("./audio/personalized/El culto a Pharos/farm.mp3")
        #             self.SCENES = False
        #             self.SCENE = True
        #             print("Morwen farm selected")
        # elif herbolist.collidepoint(mouse_pos):
        #     for event in pygame.event.get(): 
        #         if event.type == pygame.MOUSEBUTTONDOWN:
        #             self.reset_buffer()
        #             music = self.audio.check()
        #             if music is not None:
        #                 self.audio.stop()
        #             self.add_image("./images/personalized/El culto a Pharos/scenes/herbalist.jpeg")
        #             self.audio.play("./audio/personalized/El culto a Pharos/herbalist.mp3")
        #             self.SCENES = False
        #             self.SCENE = True
        #             print("Herbolist selected")
        # elif garden.collidepoint(mouse_pos):
        #     for event in pygame.event.get(): 
        #         if event.type == pygame.MOUSEBUTTONDOWN:
        #             self.reset_buffer()
        #             music = self.audio.check()
        #             if music is not None:
        #                 self.audio.stop()
        #             self.add_image("./images/personalized/El culto a Pharos/scenes/herbalist.jpeg")
        #             self.audio.play("./audio/personalized/El culto a Pharos/herbalist.mp3")
        #             self.SCENES = False
        #             self.SCENE = True
        #             print("Garden selected")
        # elif temple_outside.collidepoint(mouse_pos):
        #     for event in pygame.event.get(): 
        #         if event.type == pygame.MOUSEBUTTONDOWN:
        #             self.reset_buffer()
        #             music = self.audio.check()
        #             if music is not None:
        #                 self.audio.stop()
        #             self.add_image("./images/personalized/El culto a Pharos/scenes/temple_out.jpg")
        #             self.audio.play("./audio/personalized/El culto a Pharos/temple_out.mp3")
        #             self.SCENES = False
        #             self.SCENE = True
        #             print("Temple outside selected")
        # elif temple.collidepoint(mouse_pos):
        #     for event in pygame.event.get(): 
        #         if event.type == pygame.MOUSEBUTTONDOWN:
        #             self.reset_buffer()
        #             music = self.audio.check()
        #             if music is not None:
        #                 self.audio.stop()
        #             self.add_image("./images/personalized/El culto a Pharos/scenes/temple.png")
        #             self.audio.play("./audio/personalized/El culto a Pharos/temple.mp3")
        #             self.SCENES = False
        #             self.SCENE = True
        #             print("Temple selected")
        # elif sanctorum.collidepoint(mouse_pos):
        #     for event in pygame.event.get(): 
        #         if event.type == pygame.MOUSEBUTTONDOWN:
        #             self.reset_buffer()
        #             music = self.audio.check()
        #             if music is not None:
        #                 self.audio.stop()
        #             self.add_image("./images/personalized/El culto a Pharos/scenes/temple.png")
        #             self.audio.play("./audio/personalized/El culto a Pharos/sanctorum.mp3")
        #             self.SCENES = False
        #             self.SCENE = True
        #             print("Sanctorum selected")

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
        self.SCENES = False
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
                        self.MAIN_MENU = False
                        self.SCENE = False
                        self.SCENES_MENU = True
                    elif event.key==pygame.K_h:
                        self.SCENES = False
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
                self.show_main_menu()
            elif self.SCENES_MENU:
                self.engine.screen.blit(self.engine.ENGINE_BUFFER["main_menu"][0], (0,0))
                self.show_scene_menu()
            elif self.SCENE:
                self.engine.screen.blit(self.engine.SCENES_BUFFER[self.SCENE_NAME][0], (0,0))

            pygame.display.flip()

        pygame.quit()
        sys.exit()
