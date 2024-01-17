import time
import pygame
import pygame.gfxdraw
from modules.audio import Audio
from modules.engine import Engine
from modules.screens.scene_menu import SceneMenu
from modules.screens.main_menu import MainMenu
from modules.screens.options_menu import OptionsMenu
import sys

class Game:

    RUNNING = False # Check if game is running
    MAIN_MENU = False # Check if main menu is running
    SCENES_MENU = False # Check if scenes menu is running
    SCENE = False # Check if scene is running
    LOAD = False # Check if campaign data is loaded
    LOAD_SCREEN = False # Check if load screen is running
    OPTIONS = False # Check if options menu is running
    RES_OPTIONS = False # Check if resolution options are running
    RES_CHANGE = False # Check if resolution is changed
    SCENE_NAME = None 

    def __init__(self, resolution:tuple = None, mode = None):
        self.engine = Engine(
            resolution=resolution, 
            mode=mode
            )
        self.main_menu = MainMenu(self.engine, self)
        self.options_menu = OptionsMenu(self.engine, self)
        self.scene_menu = SceneMenu(self.engine, self)

    def show_scene(self, scene_name):
        self.MAIN_MENU = False
        self.SCENES_MENU = False
        self.SCENE = True
        self.SCENE_NAME = scene_name

    def run(self):
        self.RUNNING = True
        self.MAIN_MENU = True
        self.SCENES_MENU = False
        self.SCENE = False
        self.LOAD = False
        self.LOAD_SCREEN = False
        self.OPTIONS = False
        self.RES_OPTIONS = False
        self.RES_CHANGE = False

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
                    elif event.key==pygame.K_a: #! Ver para que esto funcione solo durante la partida (se puede poner desde el menu)
                        music = self.engine.audio.check()
                        if music is not None:
                            self.engine.audio.stop()
                        self.engine.audio.play("./assets/audio/personalized/El culto a Pharos/battle.mp3")
            
            ### SHOW SCREENS FROM BUFFER
            self.engine.screen.fill((0,0,0))

            if self.MAIN_MENU:
                self.engine.screen.blit(self.engine.ENGINE_BUFFER["main_menu"][0], (0,0))
                self.engine.ENGINE_BUFFER["scenes_menu"][0] = self.engine.ENGINE_BUFFER["main_menu"][0]
                self.main_menu.show()
            elif self.RES_CHANGE:
                self.engine.screen.blit(self.engine.ENGINE_BUFFER["main_menu"][0], (0,0))
                self.engine.update_screen(self.options_menu.RES, pygame.FULLSCREEN | pygame.DOUBLEBUF)
                self.RES_CHANGE = False
                self.RES_OPTIONS = False
                self.OPTIONS = True
            elif self.SCENES_MENU and self.SCENE:
                self.engine.screen.blit(self.engine.SCENES_BUFFER[self.SCENE_NAME][0], (0,0))
                self.scene_menu.show()
            elif self.SCENES_MENU:
                self.engine.screen.blit(self.engine.ENGINE_BUFFER["scenes_menu"][0], (0,0))
                self.scene_menu.show()
            elif self.SCENE:
                self.engine.screen.blit(self.engine.SCENES_BUFFER[self.SCENE_NAME][0], (0,0))
            elif self.OPTIONS:
                self.engine.screen.blit(self.engine.ENGINE_BUFFER["main_menu"][0], (0,0))
                self.options_menu.show()
            elif self.RES_OPTIONS:
                self.engine.screen.blit(self.engine.ENGINE_BUFFER["main_menu"][0], (0,0))
                self.options_menu.show_resolution_menu()

            pygame.display.flip()

        self.engine.audio.quit_mixer()
        pygame.quit()
        sys.exit()
