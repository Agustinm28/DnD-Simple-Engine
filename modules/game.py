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

        for name, rect in rects.items():
            self.engine.screen.blit(scene_image, rect.topleft)
            

        ##############################################################

        # tavern = pygame.Rect(50, 50, 400, 100)
        # travel_path = pygame.Rect(50, 150, 400, 100)
        # betian = pygame.Rect(50, 250, 400, 100)
        # posada = pygame.Rect(50, 350, 400, 100)
        # bedroom = pygame.Rect(50, 450, 400, 100)
        # field = pygame.Rect(50, 550, 400, 100)
        # farm_outside = pygame.Rect(50, 650, 400, 100)
        # morwen_farm = pygame.Rect(50, 750, 400, 100)
        # herbolist = pygame.Rect(50, 850, 400, 100)
        # garden = pygame.Rect(450, 50, 400, 100)
        # temple_outside = pygame.Rect(450, 150, 400, 100)
        # temple = pygame.Rect(450, 250, 400, 100)
        # sanctorum = pygame.Rect(450, 350, 400, 100)

        # # Draw buttons
        # pygame.gfxdraw.box(self.screen, tavern, (0, 0, 0, 0))
        # pygame.gfxdraw.box(self.screen, travel_path, (0, 0, 0, 0))
        # pygame.gfxdraw.box(self.screen, betian, (0, 0, 0, 0))
        # pygame.gfxdraw.box(self.screen, posada, (0, 0, 0, 0))
        # pygame.gfxdraw.box(self.screen, bedroom, (0, 0, 0, 0))
        # pygame.gfxdraw.box(self.screen, field, (0, 0, 0, 0))
        # pygame.gfxdraw.box(self.screen, farm_outside, (0, 0, 0, 0))
        # pygame.gfxdraw.box(self.screen, morwen_farm, (0, 0, 0, 0))
        # pygame.gfxdraw.box(self.screen, herbolist, (0, 0, 0, 0))
        # pygame.gfxdraw.box(self.screen, garden, (0, 0, 0, 0))
        # pygame.gfxdraw.box(self.screen, temple_outside, (0, 0, 0, 0))
        # pygame.gfxdraw.box(self.screen, temple, (0, 0, 0, 0))
        # pygame.gfxdraw.box(self.screen, sanctorum, (0, 0, 0, 0))

        # # Add images to buttons
        # tavern_image = pygame.image.load("./images/personalized/El culto a Pharos/assets/tavern.png")
        # travel_path_image = pygame.image.load("./images/personalized/El culto a Pharos/assets/travel_path.png")
        # betian_image = pygame.image.load("./images/personalized/El culto a Pharos/assets/betian.png")
        # posada_image = pygame.image.load("./images/personalized/El culto a Pharos/assets/posada.png")
        # bedroom_image = pygame.image.load("./images/personalized/El culto a Pharos/assets/bedroom.png")
        # field_image = pygame.image.load("./images/personalized/El culto a Pharos/assets/field_path.png")
        # farm_outside_image = pygame.image.load("./images/personalized/El culto a Pharos/assets/farm_out.png")
        # morwen_farm_image = pygame.image.load("./images/personalized/El culto a Pharos/assets/morwen_farm.png")
        # herbolist_image = pygame.image.load("./images/personalized/El culto a Pharos/assets/herbalist.png")
        # garden_image = pygame.image.load("./images/personalized/El culto a Pharos/assets/herbalist_garden.png")
        # temple_outside_image = pygame.image.load("./images/personalized/El culto a Pharos/assets/temple_out.png")
        # temple_image = pygame.image.load("./images/personalized/El culto a Pharos/assets/pelor_temple.png")
        # sanctorum_image = pygame.image.load("./images/personalized/El culto a Pharos/assets/sanctorum.png")

        # # Resize images
        # tavern_image = pygame.transform.scale(tavern_image, (400,100))
        # travel_path_image = pygame.transform.scale(travel_path_image, (400,100))
        # betian_image = pygame.transform.scale(betian_image, (400,100))
        # posada_image = pygame.transform.scale(posada_image, (400,100))
        # bedroom_image = pygame.transform.scale(bedroom_image, (400,100))
        # field_image = pygame.transform.scale(field_image, (400,100))
        # farm_outside_image = pygame.transform.scale(farm_outside_image, (400,100))
        # morwen_farm_image = pygame.transform.scale(morwen_farm_image, (400,100))
        # herbolist_image = pygame.transform.scale(herbolist_image, (400,100))
        # garden_image = pygame.transform.scale(garden_image, (400,100))
        # temple_outside_image = pygame.transform.scale(temple_outside_image, (400,100))
        # temple_image = pygame.transform.scale(temple_image, (400,100))
        # sanctorum_image = pygame.transform.scale(sanctorum_image, (400,100))

        # # Add images to buttons
        # self.screen.blit(tavern_image, (50,50))
        # self.screen.blit(travel_path_image, (50,150))
        # self.screen.blit(betian_image, (50,250))
        # self.screen.blit(posada_image, (50,350))
        # self.screen.blit(bedroom_image, (50,450))
        # self.screen.blit(field_image, (50,550))
        # self.screen.blit(farm_outside_image, (50,650))
        # self.screen.blit(morwen_farm_image, (50,750))
        # self.screen.blit(herbolist_image, (50,850))
        # self.screen.blit(garden_image, (450,50))
        # self.screen.blit(temple_outside_image, (450,150))
        # self.screen.blit(temple_image, (450,250))
        # self.screen.blit(sanctorum_image, (450,350))

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

        while self.RUNNING:
            for event in pygame.event.get():
                ### Key events
                if event.type == pygame.QUIT:
                    self.RUNNING = False
                elif event.type==pygame.KEYDOWN:
                    if event.key==pygame.K_m:
                        self.SCENES = not self.SCENES
                        self.SCENE = False
                    elif event.key==pygame.K_h:
                        self.SCENES = False
                        self.SCENE = False
                        self.MAIN_MENU = True
                        music = self.audio.check()
                        if music is not None:
                            self.audio.stop()
                    elif event.key==pygame.K_ESCAPE:
                        self.RUNNING = False
                    elif event.key==pygame.K_a: #! Ver para que esto funcione solo durante la partida (se peude poner desde el menu)
                        music = self.audio.check()
                        if music is not None:
                            self.audio.stop()
                        self.audio.play("./audio/personalized/El culto a Pharos/battle.mp3")
            
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
