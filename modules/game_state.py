class GameStateManager:

    def __init__(self, currentState):
        self.currentState = currentState
        self.lastState = currentState

    def get_state(self):
        return self.currentState
    
    def set_state(self, state):
        self.currentState = state

    def get_last_state(self):
        return self.lastState
    
    def set_last_state(self, state):
        self.lastState = state