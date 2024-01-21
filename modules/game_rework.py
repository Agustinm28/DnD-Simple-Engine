import time
import pygame
import pygame.gfxdraw
from modules.engine import Engine
from modules.game_state import GameStateManager
from screens.main_menu import MainMenu
from screens.options_menu import OptionsMenu
from screens.exit import Exit
from utils.debugger import info, error, dprint

class Game:

    RUNNING = False

    def __init__(self, resolution:tuple = None, mode = None, save_path:str = None):
        
        self.engine = Engine(resolution=resolution, mode=mode)
        self.clock = pygame.time.Clock()

        self.game_state_manager = GameStateManager('main_menu')
        self.main_menu = MainMenu(self.engine.screen, self.game_state_manager, self.engine)
        self.options_menu = OptionsMenu(self.engine.screen, self.game_state_manager)
        self.exit = Exit(self.engine)

        self.states = {
            'main_menu': self.main_menu,
            'options_menu': self.options_menu,
            'exit': self.exit
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
                elif event.type==pygame.KEYDOWN:
                    if event.key==pygame.K_ESCAPE:
                        dprint('GAME REWORK','Escape key pressed.', 'GREEN')
                    elif event.key==pygame.K_a:
                        dprint('GAME REWORK','Options', 'GREEN')
                        self.game_state_manager.set_state('options_menu')

            # Look for the key of screen to run
            self.states[self.game_state_manager.get_state()].run()

            pygame.display.update()
            self.clock.tick(60)

        self.engine.audio.quit_mixer()
        self.engine.quit_engine()