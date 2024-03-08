from utils.debugger import dprint, error
import pygame

class Scene:

    def __init__(self, gameStateManager, engine, mouse):
        self.gameStateManager = gameStateManager
        self.engine = engine
        self.mouse = mouse
        self.scene = None
        self.handler = False
        self.battle = False

    def run(self):
        '''
        Method to run the scene.
        '''
        try:
            if self.gameStateManager.get_last_state() != 'save_menu':
                self.gameStateManager.set_last_state('save_menu')

            self.set_handler(True)

            self.engine.screen.blit(self.engine.SCENES_BUFFER[self.scene][0], (0,0))

        except Exception:
            error("Error showing scene")

    ## Getters and Setters

    def get_scene(self):
        return self.scene

    def set_scene(self, scene):
        self.scene = scene

    def get_handler(self):
        return self.handler
    
    def set_handler(self, handler):
        self.handler = handler

    def handle_events(self, event):

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                if self.battle == False:
                    self.battle = True
                    self.engine.audio.play(self.engine.ENGINE_BUFFER['battle'])
                    dprint("BATTLE", "Battle activated", "MAGENTA")
                else:
                    self.battle = False
                    if self.engine.SCENES_BUFFER[f"{self.scene}"][1] == None:
                        self.engine.audio.stop()
                    else:
                        self.engine.audio.play(self.engine.SCENES_BUFFER[f"{self.scene}"][1])
                    dprint("BATTLE", "Battle deactivated", "MAGENTA")
            elif event.key == pygame.K_m:
                self.gameStateManager.set_state('scenes_menu')