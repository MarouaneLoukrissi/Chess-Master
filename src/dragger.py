import pygame

from const import *

class Dragger:

    def __init__(self):
        self.piece = None
        self.dragging = False
        self.mouseX = 0
        self.mouseY = 0
        self.initialX = 0
        self.initialY = 0
        self.initial_row = 0
        self.initial_col = 0

    # other methods

    def Update_mouse(self, pos):
        self.mouseX, self.mouseY = pos # (xcor, ycor)

    def save_initial(self, pos):

        self.initial_row = (pos[1]-FH_HEIGHT) // SQSIZE
        self.initial_col = pos[0] // SQSIZE
        self.initialY = (FH_HEIGHT + self.initial_row * SQSIZE) + (SQSIZE // 2)
        self.initialX = (self.initial_col * SQSIZE) + (SQSIZE // 2)

    def drag_piece(self, piece):
        self.piece = piece
        self.dragging = True

    def undrag_piece(self):
        self.piece = None
        self.dragging = False

    # blit method

    def update_blit(self, surface):
        # avatar
        self.piece.set_avatar(size=801)
        avatar = self.piece.avatar
        # img
        img = pygame.image.load(avatar)
        # rect
        img_center = (self.initialX, self.initialY)
        self.piece.avatar_rect = img.get_rect(center=img_center)
        # blit
        surface.blit(img, self.piece.avatar_rect)