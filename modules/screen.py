import pygame
import sys
import os

class Screen:

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
        button_1 = pygame.Rect(50, 50, 100, 30)
        button_2 = pygame.Rect(200, 50, 100, 30)

        # Draw buttons
        pygame.draw.rect(self.screen, (255,0,0), button_1)
        pygame.draw.rect(self.screen, (255,0,0), button_2)

        # Add images to buttons
        # image_button_1 = pygame.image.load("./images/generic/main/start.jpg")
        # image_button_2 = pygame.image.load("./images/generic/main/start.jpg")

        # self.screen.blit(image_button_1, (50,50))
        # self.screen.blit(image_button_2, (200,50))

        # Get mouse position
        mouse_pos = pygame.mouse.get_pos()

        # Check if mouse is over a button
        if button_1.collidepoint(mouse_pos):
            if pygame.mouse.get_pressed()[0]:
                self.add_images_folder("./images/generic/forest")
                self.IMAGE_INDEX = 0
                print("Button 1 clicked")
        elif button_2.collidepoint(mouse_pos):
            if pygame.mouse.get_pressed()[0]:
                print("Button 2 clicked")

    def run(self):
        running = True
        show_menu = False
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
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
                    elif event.key==pygame.K_c:
                        show_menu = not show_menu
                    elif event.key==pygame.K_h:
                        show_menu = False
                        self.return_home()
                    elif event.key==pygame.K_ESCAPE:
                        running = False
            
            self.screen.fill((0,0,0))
            if show_menu:
                self.screen.blit(self.IMAGE_BUFFER[self.IMAGE_INDEX], (0,0))
                self.show_scene_menu()
            else:
                self.screen.blit(self.IMAGE_BUFFER[self.IMAGE_INDEX], (0,0))

            pygame.display.flip()

        pygame.quit()
        sys.exit()
