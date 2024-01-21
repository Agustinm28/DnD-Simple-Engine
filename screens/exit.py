class Exit:

    def __init__(self, engine):
        self.engine = engine

    def run(self):
        self.engine.audio.quit_mixer()
        self.engine.quit_engine()