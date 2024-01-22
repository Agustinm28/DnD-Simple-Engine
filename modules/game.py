import time
import pygame
import pygame.gfxdraw
from modules.engine import Engine
from modules.game_state import GameStateManager
from screens.main_menu import MainMenu
from screens.options_menu import OptionsMenu
from screens.res_menu import ResMenu
from screens.save_menu import SaveMenu
from screens.scene import Scene
from screens.scenes_menu import SceneMenu
from screens.loading import Loading
from modules.exit import Exit
from utils.debugger import info, error, dprint
from modules.mouse import Mouse

class Game:

    RUNNING = False

    def __init__(self, resolution:tuple = None, mode = None, save_path:str = None):
        
        self.engine = Engine(resolution=resolution, mode=mode)
        self.clock = pygame.time.Clock()
        self.mouse = Mouse()
        self.exit = Exit()

        self.game_state_manager = GameStateManager('main_menu')
        self.main_menu = MainMenu(self.game_state_manager, self.engine, self.mouse, self.exit)
        self.options_menu = OptionsMenu(self.game_state_manager, self.engine, self.mouse)
        self.res_menu = ResMenu(self.game_state_manager, self.engine, self.mouse)
        self.loading = Loading(self.game_state_manager, self.engine, self.mouse)
        self.save_menu = SaveMenu(self.game_state_manager, self.engine, self.mouse, self.loading)
        self.scene = Scene(self.game_state_manager, self.engine, self.mouse)
        self.scenes_menu = SceneMenu(self.game_state_manager, self.engine, self.mouse, self.scene)

        self.states = {
            'main_menu': self.main_menu,
            'options_menu': self.options_menu,
            'res_menu': self.res_menu,
            'save_menu': self.save_menu,
            'loading': self.loading,
            'scenes_menu': self.scenes_menu,
            'scene': self.scene
        }

    def run(self):
        '''
        Method to run the game.
        '''
        self.RUNNING = True

        while self.RUNNING:
            for event in pygame.event.get():
                ### Key events
                if event.type == pygame.QUIT:
                    self.RUNNING = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.mouse.set_click('down')
                elif event.type == pygame.MOUSEBUTTONUP:
                    self.mouse.set_click('up')
                elif event.type==pygame.KEYDOWN:
                    if event.key==pygame.K_ESCAPE:
                        dprint('GAME REWORK','Escape key pressed.', 'GREEN')
                        if self.engine.audio.MUSIC:
                            self.engine.audio.stop()
                        self.game_state_manager.set_state('main_menu')
                    elif event.key==pygame.K_p:
                        dprint('GAME REWORK','Options', 'GREEN')
                        self.game_state_manager.set_state('options_menu')

            # Look for the key of screen to run
            self.states[self.game_state_manager.get_state()].run()

            if self.exit.get_status():
                self.RUNNING = False

            pygame.display.update()
            self.clock.tick(60)

        self.engine.audio.quit_mixer()
        self.engine.quit_engine()