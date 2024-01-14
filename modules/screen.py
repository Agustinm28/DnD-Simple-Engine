import pygame
import pygame.gfxdraw
import sys
import os

class Screen:

    RUNNING = False
    SCENES = False
    SCENE = False
    IMAGE_BUFFER = []
    IMAGE_INDEX = 0

    def __init__(self, resolution:tuple = None, mode = pygame.FULLSCREEN, caption:str = "Board"):
        self.resolution = resolution
        self.mode = mode
        self.caption = caption
        
        pygame.init()
        self.screen = self.set_screen(self.resolution, self.mode, self.caption)
        self.add_image("./images/generic/main/start.jpg")

    def set_screen(self, resolution:tuple = None, mode = pygame.FULLSCREEN, caption:str = "Board"):
        if resolution is None:
            screen_width, screen_height = pygame.display.get_surface().get_size()
            resolution = (screen_width, screen_height)
        screen = pygame.display.set_mode(resolution, mode)
        pygame.display.set_caption(caption)

        return screen

    def reset_buffer(self):
        self.IMAGE_BUFFER = []
        self.IMAGE_INDEX = 0

    def add_image(self, image_path:str):
        image = pygame.image.load(image_path)
        self.IMAGE_BUFFER.append(image)

    def add_images_folder(self, folder_path:str):
        # Get images from folder
        images = []
        for image in os.listdir(folder_path):
            images.append(image)

        # Sort images
        images.sort()

        # Add images to buffer
        self.reset_buffer()
        for image in images:
            self.add_image(folder_path + "/" + image)

    def return_home(self):
        self.reset_buffer()
        self.add_image("./images/generic/main/start.jpg")

    def show_scene_menu(self):
        tavern = pygame.Rect(50, 50, 400, 100)
        travel_path = pygame.Rect(50, 150, 400, 100)
        betian = pygame.Rect(50, 250, 400, 100)
        posada = pygame.Rect(50, 350, 400, 100)
        bedroom = pygame.Rect(50, 450, 400, 100)
        field = pygame.Rect(50, 550, 400, 100)
        farm_outside = pygame.Rect(50, 650, 400, 100)
        morwen_farm = pygame.Rect(50, 750, 400, 100)
        herbolist = pygame.Rect(50, 850, 400, 100)
        garden = pygame.Rect(450, 50, 400, 100)
        temple_outside = pygame.Rect(450, 150, 400, 100)
        temple = pygame.Rect(450, 250, 400, 100)

        # Draw buttons
        pygame.gfxdraw.box(self.screen, tavern, (0, 0, 0, 0))
        pygame.gfxdraw.box(self.screen, travel_path, (0, 0, 0, 0))
        pygame.gfxdraw.box(self.screen, betian, (0, 0, 0, 0))
        pygame.gfxdraw.box(self.screen, posada, (0, 0, 0, 0))
        pygame.gfxdraw.box(self.screen, bedroom, (0, 0, 0, 0))
        pygame.gfxdraw.box(self.screen, field, (0, 0, 0, 0))
        pygame.gfxdraw.box(self.screen, farm_outside, (0, 0, 0, 0))
        pygame.gfxdraw.box(self.screen, morwen_farm, (0, 0, 0, 0))
        pygame.gfxdraw.box(self.screen, herbolist, (0, 0, 0, 0))
        pygame.gfxdraw.box(self.screen, garden, (0, 0, 0, 0))
        pygame.gfxdraw.box(self.screen, temple_outside, (0, 0, 0, 0))
        pygame.gfxdraw.box(self.screen, temple, (0, 0, 0, 0))

        # Add images to buttons
        tavern_image = pygame.image.load("./images/personalized/El culto a Pharos/assets/tavern.png")
        travel_path_image = pygame.image.load("./images/personalized/El culto a Pharos/assets/travel_path.png")
        betian_image = pygame.image.load("./images/personalized/El culto a Pharos/assets/betian.png")
        posada_image = pygame.image.load("./images/personalized/El culto a Pharos/assets/posada.png")
        bedroom_image = pygame.image.load("./images/personalized/El culto a Pharos/assets/bedroom.png")
        field_image = pygame.image.load("./images/personalized/El culto a Pharos/assets/field_path.png")
        farm_outside_image = pygame.image.load("./images/personalized/El culto a Pharos/assets/farm_out.png")
        morwen_farm_image = pygame.image.load("./images/personalized/El culto a Pharos/assets/morwen_farm.png")
        herbolist_image = pygame.image.load("./images/personalized/El culto a Pharos/assets/herbalist.png")
        garden_image = pygame.image.load("./images/personalized/El culto a Pharos/assets/herbalist_garden.png")
        temple_outside_image = pygame.image.load("./images/personalized/El culto a Pharos/assets/temple_out.png")
        temple_image = pygame.image.load("./images/personalized/El culto a Pharos/assets/pelor_temple.png")

        # Resize images
        tavern_image = pygame.transform.scale(tavern_image, (400,100))
        travel_path_image = pygame.transform.scale(travel_path_image, (400,100))
        betian_image = pygame.transform.scale(betian_image, (400,100))
        posada_image = pygame.transform.scale(posada_image, (400,100))
        bedroom_image = pygame.transform.scale(bedroom_image, (400,100))
        field_image = pygame.transform.scale(field_image, (400,100))
        farm_outside_image = pygame.transform.scale(farm_outside_image, (400,100))
        morwen_farm_image = pygame.transform.scale(morwen_farm_image, (400,100))
        herbolist_image = pygame.transform.scale(herbolist_image, (400,100))
        garden_image = pygame.transform.scale(garden_image, (400,100))
        temple_outside_image = pygame.transform.scale(temple_outside_image, (400,100))
        temple_image = pygame.transform.scale(temple_image, (400,100))

        # Add images to buttons
        self.screen.blit(tavern_image, (50,50))
        self.screen.blit(travel_path_image, (50,150))
        self.screen.blit(betian_image, (50,250))
        self.screen.blit(posada_image, (50,350))
        self.screen.blit(bedroom_image, (50,450))
        self.screen.blit(field_image, (50,550))
        self.screen.blit(farm_outside_image, (50,650))
        self.screen.blit(morwen_farm_image, (50,750))
        self.screen.blit(herbolist_image, (50,850))
        self.screen.blit(garden_image, (450,50))
        self.screen.blit(temple_outside_image, (450,150))
        self.screen.blit(temple_image, (450,250))

        # Get mouse position
        mouse_pos = pygame.mouse.get_pos()

        # Check if mouse is over a button
        if tavern.collidepoint(mouse_pos):
            for event in pygame.event.get(): 
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.reset_buffer()
                    self.add_image("./images/personalized/El culto a Pharos/scenes/tavern.jpeg")
                    self.SCENES = False
                    self.SCENE = True
                    print("Tavern selected")
        elif travel_path.collidepoint(mouse_pos):
            for event in pygame.event.get(): 
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.reset_buffer()
                    self.add_image("./images/personalized/El culto a Pharos/scenes/travel_path.jpg")
                    self.SCENES = False
                    self.SCENE = True
                    print("Travel selected")
        elif betian.collidepoint(mouse_pos):
            for event in pygame.event.get(): 
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.reset_buffer()
                    self.add_image("./images/personalized/El culto a Pharos/scenes/betian.png")
                    self.SCENES = False
                    self.SCENE = True
                    print("Betian selected")
        elif posada.collidepoint(mouse_pos):
            for event in pygame.event.get(): 
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.reset_buffer()
                    self.add_image("./images/personalized/El culto a Pharos/scenes/posada.jpeg")
                    self.SCENES = False
                    self.SCENE = True
                    print("Posada selected")
        elif bedroom.collidepoint(mouse_pos):
            for event in pygame.event.get(): 
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.reset_buffer()
                    self.add_image("./images/personalized/El culto a Pharos/scenes/bedroom.jpg")
                    self.SCENES = False
                    self.SCENE = True
                    print("Bedroom selected")
        elif field.collidepoint(mouse_pos):
            for event in pygame.event.get(): 
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.reset_buffer()
                    self.add_image("./images/personalized/El culto a Pharos/scenes/field.jpeg")
                    self.SCENES = False
                    self.SCENE = True
                    print("Field selected")
        elif farm_outside.collidepoint(mouse_pos):
            for event in pygame.event.get(): 
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.reset_buffer()
                    self.add_image("./images/personalized/El culto a Pharos/scenes/fence.jpeg")
                    self.SCENES = False
                    self.SCENE = True
                    print("Farm outside selected")
        elif morwen_farm.collidepoint(mouse_pos):
            for event in pygame.event.get(): 
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.reset_buffer()
                    self.add_image("./images/personalized/El culto a Pharos/scenes/farm.png")
                    self.SCENES = False
                    self.SCENE = True
                    print("Morwen farm selected")
        elif herbolist.collidepoint(mouse_pos):
            for event in pygame.event.get(): 
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.reset_buffer()
                    self.add_image("./images/personalized/El culto a Pharos/scenes/herbalist.jpeg")
                    self.SCENES = False
                    self.SCENE = True
                    print("Herbolist selected")
        elif garden.collidepoint(mouse_pos):
            for event in pygame.event.get(): 
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.reset_buffer()
                    self.add_image("./images/personalized/El culto a Pharos/scenes/herbalist.jpeg")
                    self.SCENES = False
                    self.SCENE = True
                    print("Garden selected")
        elif temple_outside.collidepoint(mouse_pos):
            for event in pygame.event.get(): 
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.reset_buffer()
                    self.add_image("./images/personalized/El culto a Pharos/scenes/temple_out.jpg")
                    self.SCENES = False
                    self.SCENE = True
                    print("Temple outside selected")
        elif temple.collidepoint(mouse_pos):
            for event in pygame.event.get(): 
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.reset_buffer()
                    self.add_image("./images/personalized/El culto a Pharos/scenes/temple.png")
                    self.SCENES = False
                    self.SCENE = True
                    print("Temple selected")

    def show_main_menu(self):
        start = pygame.Rect(50, 50, 400, 100)
        options = pygame.Rect(50, 150, 400, 100)
        exit_game = pygame.Rect(50, 250, 400, 100)

        # Draw buttons
        pygame.gfxdraw.box(self.screen, start, (0, 0, 0, 0))
        pygame.gfxdraw.box(self.screen, options, (0, 0, 0, 0))
        pygame.gfxdraw.box(self.screen, exit_game, (0, 0, 0, 0))

        # Add images to buttons
        image_button_1 = pygame.image.load("./images/assets/start.png")
        image_button_2 = pygame.image.load("./images/assets/options.png")
        image_button_3 = pygame.image.load("./images/assets/exit.png")

        # Resize images
        image_button_1 = pygame.transform.scale(image_button_1, (400,100))
        image_button_2 = pygame.transform.scale(image_button_2, (400,100))
        image_button_3 = pygame.transform.scale(image_button_3, (400,100))

        # Add images to buttons
        self.screen.blit(image_button_1, (50,50))
        self.screen.blit(image_button_2, (50,150))
        self.screen.blit(image_button_3, (50,250))

        # Get mouse position
        mouse_pos = pygame.mouse.get_pos()

        # Check if mouse is over a button
        if start.collidepoint(mouse_pos):
            for event in pygame.event.get(): 
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.SCENES = True
                    print("Start button clicked")
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
        self.SCENES = False
        self.SCENE = False
        while self.RUNNING:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.RUNNING = False
                elif event.type==pygame.KEYDOWN:
                    if event.key==pygame.K_RIGHT:
                        if self.IMAGE_INDEX < len(self.IMAGE_BUFFER)-1:
                            self.IMAGE_INDEX += 1
                        else:
                            print("No images left")
                            pass
                    elif event.key==pygame.K_LEFT:
                        if self.IMAGE_INDEX > 0:
                            self.IMAGE_INDEX -= 1
                        else:
                            print("No images left")
                            pass
                    elif event.key==pygame.K_m:
                        self.SCENES = not self.SCENES
                        self.SCENE = False
                    elif event.key==pygame.K_h:
                        self.SCENES = False
                        self.SCENE = False
                        self.return_home()
                    elif event.key==pygame.K_ESCAPE:
                        self.RUNNING = False
            
            self.screen.fill((0,0,0))
            if self.SCENES:
                self.screen.blit(self.IMAGE_BUFFER[self.IMAGE_INDEX], (0,0))
                self.show_scene_menu()
            elif self.SCENE:
                self.screen.blit(self.IMAGE_BUFFER[self.IMAGE_INDEX], (0,0))
            else:
                self.screen.blit(self.IMAGE_BUFFER[self.IMAGE_INDEX], (0,0))
                self.show_main_menu()

            pygame.display.flip()

        pygame.quit()
        sys.exit()
