from utils.debugger import dprint, error
import pygame

class SceneMenu:

    def __init__(self, gameStateManager, engine, mouse, scene):
        self.gameStateManager = gameStateManager
        self.engine = engine
        self.mouse = mouse
        self.scene = scene

    def run(self):
        try:

            self.engine.screen.blit(self.engine.ENGINE_BUFFER["scenes_menu"][0], (0,0))

            scale_x = self.engine.resolution[0] / 1920
            scale_y = self.engine.resolution[1] / 1080

            #max_x = int(400 * scale_x) Este la verdad no se
            max_y = int(850 * scale_y)

            coordenates = []
            x = int(50 * scale_x)
            y = int(50 * scale_y)
            widht = int(400 * scale_x)
            height = int(100 * scale_y)

            names = list(self.engine.SCENES_BUFFER.keys())
            font_size = int(36 * min(scale_x, scale_y))
            font = pygame.font.Font("./assets/fonts/ancient.ttf", font_size)
            color = (44, 33, 46)

            for l in range(len(self.engine.SCENES_BUFFER)):
                coordenates.append((x, y, widht, height))
                y += height

                if y > max_y:
                    y = int(50 * scale_y)
                    x += widht

            rects = {f'{names[i]}': pygame.Rect(coordenates) for i, coordenates in enumerate(coordenates)}

            for rect in rects.values():
                pygame.gfxdraw.box(self.engine.screen, rect, (0, 0, 0, 0))

            # Resize scene buttons image
            scene_image = pygame.transform.scale(self.engine.ENGINE_BUFFER["scene"][0], (widht,height))

            # Add images to buttons
            for name, rect in rects.items():
                text = font.render(name, True, color)
                text_rect = text.get_rect(center=rect.center)

                self.engine.screen.blit(scene_image, rect.topleft)
                self.engine.screen.blit(text, text_rect)

            # Get mouse position
            mouse_pos = pygame.mouse.get_pos()

            # Check if mouse is over a button
            for name, rect in rects.items():
                self.handle_button_event(name, rect, mouse_pos)
        except Exception:
            error("Error showing scene menu")

    def handle_button_event(self, button_name, button, mouse_pos):
        '''
        Method to handle button events. Where:
            - button_name: name of the button.
            - button: button rect.
            - mouse_pos: mouse position.
        '''
        if button.collidepoint(mouse_pos):
            if self.mouse.get_click():
                self.mouse.set_click('up')
                dprint("SCENES MENU", f"{button_name} selected", "CYAN")
                if self.engine.audio.MUSIC:
                    self.engine.audio.stop()
                self.engine.audio.play(self.engine.SCENES_BUFFER[f"{button_name}"][1])
                self.engine.ENGINE_BUFFER["scenes_menu"][0] = self.engine.SCENES_BUFFER[f"{button_name}"][0]
                self.scene.set_scene(button_name)
                self.gameStateManager.set_state('scene')