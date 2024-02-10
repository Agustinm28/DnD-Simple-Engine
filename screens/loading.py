import time


class Loading:

    def __init__(self, gameStateManager, engine, mouse):
        self.gameStateManager = gameStateManager
        self.engine = engine
        self.mouse = mouse
        self.save_path = None
        self.load = False

    def run(self):
        '''
        Method to run the loading screen.
        '''
        if self.load:
            self.engine.load_saved_game(self.save_path)
            self.load = False
            self.gameStateManager.set_state('scenes_menu')

        if not self.load:
            self.engine.screen.blit(self.engine.ENGINE_BUFFER["loading"][0], (0,0))
            self.load = True

    ## Getters and Setters
        
    def get_save_path(self):
        return self.save_path

    def set_save_path(self, save_path):
        self.save_path = save_path