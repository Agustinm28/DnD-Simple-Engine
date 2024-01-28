from utils.debugger import dprint, error
import pygame

class Scene:

    def __init__(self, gameStateManager, engine, mouse):
        self.gameStateManager = gameStateManager
        self.engine = engine
        self.mouse = mouse
        self.scene = None

    def run(self):
        try:
            if self.gameStateManager.get_last_state() != 'save_menu':
                self.gameStateManager.set_last_state('save_menu')

            self.engine.screen.blit(self.engine.SCENES_BUFFER[self.scene][0], (0,0))

            keys = pygame.key.get_pressed()
            if keys[pygame.K_m]:
                self.gameStateManager.set_state('scenes_menu')

        except Exception:
            error("Error showing scene")

    def set_scene(self, scene):
        self.scene = scene