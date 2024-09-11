import pygame_widgets
from pygame_widgets.button import Button

class ClickableButton:
    def __init__(self, txt, widthHeight=tuple, xy=tuple) -> None:
        self.txt = txt
        self.widthHeight = widthHeight
        self.xy = xy
        self.btn = None
        # self.cb = whenClicked

    def draw(self, screen):
        if self.btn:
            return

        self.btn = Button(
            screen, # surface to place button on
            self.xy[0],  # X-coordinate of top left corner
            self.xy[1],  # Y-coordinate of top left corner
            self.widthHeight[0],  # Width
            self.widthHeight[1],  # Height
            text=self.txt,
            fontSize=50, margin=20,
            inactiveColour=(200, 50, 0),  # Color of button when not being interacted with
            hoverColour=(150, 0, 0),  # Color of button when being hovered over
            pressedColour=(0, 200, 20),  # Color of button when being clicked
            radius=20,
            onClick=lambda: print("clicked")
        )
