import pygame

class Mouse:

    def __init__(self):
        self.click = False

    def get_click(self):
        '''
        Method to get mouse button.
        '''
        return self.click
    
    def set_click(self, status):
        '''
        Method to get mouse button down.
        '''
        if status == "down":
            self.click = True
        elif status == "up":
            self.click = False

    def get_mouse_pos(self):
        '''
        Method to get mouse position.
        '''
        return pygame.mouse.get_pos()