class Loading:

    def __init__(self, gameStateManager, engine, mouse):
        self.gameStateManager = gameStateManager
        self.engine = engine
        self.mouse = mouse
        self.save_path = None

    def run(self):
        '''
        Method to run the loading screen.
        '''
        
        self.engine.load_saved_game(self.save_path)
        self.gameStateManager.set_state('scenes_menu')

    ## Getters and Setters
        
    def get_save_path(self):
        return self.save_path

    def set_save_path(self, save_path):
        self.save_path = save_path