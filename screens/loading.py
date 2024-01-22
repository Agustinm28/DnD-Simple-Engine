class Loading:

    def __init__(self, gameStateManager, engine, mouse):
        self.gameStateManager = gameStateManager
        self.engine = engine
        self.mouse = mouse
        self.save_path = None

    def run(self):
        
        #self.engine.screen.blit(self.engine.ENGINE_BUFFER["loading"][0], (0,0))
        
        self.engine.load_saved_game(self.save_path)
        self.gameStateManager.set_state('scenes_menu')

    def set_save_path(self, save_path):
        self.save_path = save_path