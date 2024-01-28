import time
import pygame
import pygame.gfxdraw
from modules.engine import Engine
from modules.game_state import GameStateManager
from modules.image import ImageUtils
from screens.main_menu import MainMenu
from screens.options_menu import OptionsMenu
from screens.res_menu import ResMenu
from screens.save_menu import SaveMenu
from screens.scene import Scene
from screens.scenes_menu import SceneMenu
from screens.loading import Loading
from screens.new_save_menu import NewSaveMenu
from screens.repository import Repository
from modules.exit import Exit
from modules.save import Save
from utils.debugger import info, error, dprint
from modules.mouse import Mouse

class Game:

    RUNNING = False

    def __init__(self, resolution:tuple = None, mode = None):
        
        self.engine = Engine(resolution=resolution, mode=mode)
        self.clock = pygame.time.Clock()
        self.mouse = Mouse()
        self.exit = Exit()
        self.image_optimizer = ImageUtils()
        self.save = Save()

        self.game_state_manager = GameStateManager('main_menu')

        self.repository = Repository(self.game_state_manager, self.engine, self.mouse, self.image_optimizer)
        self.loading = Loading(self.game_state_manager, self.engine, self.mouse)
        self.new_save_menu = NewSaveMenu(self.game_state_manager, self.engine, self.mouse, self.repository, self.image_optimizer, self.save)
        self.save_menu = SaveMenu(self.game_state_manager, self.engine, self.mouse, self.loading, self.new_save_menu, self.save, self.repository)
        self.main_menu = MainMenu(self.game_state_manager, self.engine, self.mouse, self.exit, self.repository, self.save_menu)
        self.options_menu = OptionsMenu(self.game_state_manager, self.engine, self.mouse)
        self.scene = Scene(self.game_state_manager, self.engine, self.mouse)
        self.res_menu = ResMenu(self.game_state_manager, self.engine, self.mouse, self.new_save_menu)
        self.scenes_menu = SceneMenu(self.game_state_manager, self.engine, self.mouse, self.scene)

        self.states = {
            'main_menu': self.main_menu,
            'options_menu': self.options_menu,
            'res_menu': self.res_menu,
            'save_menu': self.save_menu,
            'new_save_menu': self.new_save_menu,
            'loading': self.loading,
            'scenes_menu': self.scenes_menu,
            'repository': self.repository,
            'scene': self.scene
        }

    def run(self):
        '''
        Method to run the game.
        '''
        self.RUNNING = True

        while self.RUNNING:
            events = pygame.event.get()
            for event in events:
                ### Key events
                if event.type == pygame.QUIT:
                    self.RUNNING = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.mouse.set_click('down')
                elif event.type == pygame.MOUSEBUTTONUP:
                    self.mouse.set_click('up')
                elif event.type==pygame.KEYDOWN:
                    if event.key==pygame.K_ESCAPE:
                        if self.engine.audio.MUSIC:
                            self.engine.audio.stop()
                        self.new_save_menu.set_handler(False)
                        self.repository.set_handler(False)
                        self.game_state_manager.set_state(self.game_state_manager.get_last_state())
                
                if self.new_save_menu.get_handler():
                    self.new_save_menu.handle_events(event)

                if self.repository.get_handler():
                    self.repository.handle_events(event)

                if self.save_menu.get_handler():
                    self.save_menu.handle_events(event)

                if self.options_menu.get_handler():
                    self.options_menu.handle_events(event)

            # Look for the key of screen to run
            self.states[self.game_state_manager.get_state()].run()

            if self.exit.get_status():
                self.RUNNING = False

            pygame.display.update()
            self.clock.tick(60)

        self.engine.audio.quit_mixer()
        self.engine.quit_engine()