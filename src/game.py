import pygame
import sys
import os
from const import *
from boardtemp import Board
from dragger import Dragger
from square import Square
from sound import Sound

class Game:

    def __init__(self):
        self.next_player = 'white'
        self.hovered_sqr = None
        self.board = Board()
        self.dragger = Dragger()
        #Standard themes
        self.themes = [GRAY,BLUE,GREEN,BROWN]                                        #0
        #Current theme
        self.theme = self.themes[0]                                                  #0
        #Current theme's placement within the standard themes  
        self.idx=0                                                                 #0 
        #Current font
        self.font = pygame.font.SysFont('Courrier', 18, bold=True)                   #0
        #Moving sound
        self.move_sound = Sound(os.path.join('assets/sounds/move.wav'))              #0
        #Capturing sound
        self.capture_sound = Sound(os.path.join('assets/sounds/capture.wav'))        #0
        self.white_p_score=0
        self.black_p_score=0

    def change_theme(self, surface):  
        def winner(message, text_color, box_color):
            # Display quit message for a half second
            font = pygame.font.Font(None, 30)
            confirmation_text = font.render(message, True, text_color)
            confirmation_rect = confirmation_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
            
            # Create a green box behind the text
            box_width = 200
            box_height = 60
            box_rect = pygame.Rect((WIDTH - box_width) // 2, (HEIGHT - box_height) // 2, box_width, box_height)
            # Draw the green box
            pygame.draw.rect(surface, box_color, box_rect)
            
            # Draw the text
            surface.blit(confirmation_text, confirmation_rect)

            pygame.display.update()
            # Delay for a half second
            pygame.time.delay(300)

            self.theme=self.themes[self.idx]                                                       #0
        self.idx +=1
        self.idx %= len(self.themes)
        # Display theme message for a half second
        if self.idx == 0: 
            message = "GRAY THEME" 
            text_color = (255, 255, 255)
            box_color = (128, 128, 128)
        elif self.idx == 1: 
            message = "BLUE THEME" 
            text_color = (255, 255, 255)
            box_color = (60, 95, 135)
        elif self.idx == 2: 
            message = "GREEN THEME"
            text_color = (255, 255, 255)
            box_color = (119, 154, 88)
        elif self.idx == 3: 
            message = "BROWN THEME"
            text_color = (255, 255, 255)
            box_color = (139, 69, 19)

        winner(message, text_color, box_color)

        pygame.display.update()

        # Delay for a half second
        pygame.time.delay(500)

        self.theme=self.themes[self.idx]
          
    """Display the board's surface"""
    def show_bg(self, surface):
        theme = self.theme
        
        for row in range(ROWS):
            for col in range(COLS):
                # color
                color = theme.bg.light if (row + col) % 2 == 0 else theme.bg.dark
                # rect
                rect = (col * SQSIZE,FH_HEIGHT+ row * SQSIZE, SQSIZE, SQSIZE)
                # blit
                pygame.draw.rect(surface, color, rect) # fills the part of the "screen" defined by the "rect" w/ the "color" specified

                # row coordinates
                if col == 0:
                    # color
                    color = theme.bg.dark if row % 2 == 0 else theme.bg.light
                    # label
                    lbl = self.font.render(str(ROWS-row), 1, color)
                    lbl_pos = (5, 5 + FH_HEIGHT +row * SQSIZE)
                    # blit
                    surface.blit(lbl, lbl_pos)

                # col coordinates
                if row == 7:
                    # color
                    color = theme.bg.dark if (row + col) % 2 == 0 else theme.bg.light
                    # label
                    lbl = self.font.render(Square.get_alphacol(col), 1, color)
                    lbl_pos = (col * SQSIZE + SQSIZE - 20, HEIGHT - FH_HEIGHT - 20)
                    # blit
                    surface.blit(lbl, lbl_pos)
    def show_bg_image(self, surface):
            bg_img = pygame.image.load("assets/images/wood.png")
            bg_img.set_alpha(70)
            bg_img1 = pygame.image.load("assets/images/wood1.jpg")
            bg_img1.set_alpha(80)
            bg_img_center = WIDTH // 2, HEIGHT // 2
            surface.blit(bg_img, bg_img.get_rect(center = bg_img_center))
            surface.blit(bg_img1, bg_img1.get_rect(center = bg_img_center))
                
    def show_alph_num_bg(self, surface):
        theme = self.theme
        for row in range(ROWS):
            for col in range(COLS):
                # row coordinates
                if col == 0:
                    # color
                    color = theme.bg.dark if row % 2 == 0 else theme.bg.light
                    # label
                    lbl = self.font.render(str(ROWS - row), 1, color) # setting antialias=True helps improve the visual quality of rendered text by reducing pixelation and providing smoother edges.
                    lbl_pos = (5, 5 +FH_HEIGHT+ row * SQSIZE)
                    # blit
                    surface.blit(lbl, lbl_pos)
                
                elif row == 7:
                    # color
                    color = theme.bg.dark if (row + col) % 2 == 0 else theme.bg.light
                    # label
                    lbl = self.font.render(Square.get_alphacol(col), 1, color) # setting antialias=True helps improve the visual quality of rendered text by reducing pixelation and providing smoother edges.
                    lbl_pos = (col * SQSIZE + SQSIZE - 20, BGHEIGHT - FH_HEIGHT - 20)
                    # blit
                    surface.blit(lbl, lbl_pos)
    
    """Display the pieces"""
    def show_pieces(self, surface):
        for row in range(ROWS):
            for col in range(COLS):
                # piece ?
                if self.board.squares[row][col].has_piece():
                    piece = self.board.squares[row][col].piece
                    
                    # all pieces except dragger piece
                    if piece is not self.dragger.piece:
                        piece.set_avatar(size=80)
                        img = pygame.image.load(piece.avatar) # This function renext_players a surface representing the piece(which we store in img)
                        img_center = col * SQSIZE + SQSIZE // 2,FH_HEIGHT+ row * SQSIZE + SQSIZE // 2
                        piece.avatar_rect = img.get_rect(center=img_center) #to access the surface’s rect attribute
                        # a rect object can be defined by ; the x- and y-coordinates of the top, bottom, left, and right edges of the rectangle, as well as the center. You can set any of these values to determine the current position of the rect. 
                        surface.blit(img, piece.avatar_rect)

    """Show the selected piece's valid moves"""
    def show_moves(self, surface):
        theme = self.theme

        if self.dragger.dragging:
            piece = self.dragger.piece

            # loop all valid moves
            for move in piece.moves:
                # color
                color = theme.moves.light if (move.final.row + move.final.col) % 2 == 0 else theme.moves.dark
                # rect
                rect = (move.final.col * SQSIZE,FH_HEIGHT+ move.final.row * SQSIZE, SQSIZE, SQSIZE)
                # blit
                pygame.draw.rect(surface, color, rect)

    """Display previous move of the game"""
    def show_last_move(self, surface):
        theme = self.theme

        if self.board.last_move:
            initial = self.board.last_move.initial
            final = self.board.last_move.final

            for pos in [initial, final]:
                # color
                color = theme.trace.light if (pos.row + pos.col) % 2 == 0 else theme.trace.dark
                # rect
                rect = (pos.col * SQSIZE,FH_HEIGHT+ pos.row * SQSIZE, SQSIZE, SQSIZE)
                # blit
                pygame.draw.rect(surface, color, rect)

    """Highlight the square the mouse is on"""
    def show_hover(self, surface):
        if self.hovered_sqr:
            # color
            color = (180, 180, 0)
            # rect
            rect = (self.hovered_sqr.col* SQSIZE, FH_HEIGHT+ self.hovered_sqr.row* SQSIZE, SQSIZE, SQSIZE)
            # blit
            pygame.draw.rect(surface, color, rect, width=3)

    # other methods

    def next_turn(self, screen):
        def winner(message, text_color, box_color):
            # Display quit message for a half second
                font = pygame.font.Font(None, 30)
                confirmation_text = font.render(message, True, text_color)
                confirmation_rect = confirmation_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
                
                # Create a green box behind the text
                box_width = 800
                box_height = 80
                box_rect = pygame.Rect((WIDTH - box_width) // 2, (HEIGHT - box_height) // 2, box_width, box_height)
                # Draw the green box
                pygame.draw.rect(screen, box_color, box_rect)
                
                # Draw the text
                screen.blit(confirmation_text, confirmation_rect)

                pygame.display.update()
                # Delay for a half second
                pygame.time.delay(3000)
                # quit the game
                pygame.quit()
                sys.exit() #une fonction utilisée pour quitter le programme Python en cours d'exécution de manière explicite.
                
        self.next_player = 'white' if self.next_player == 'black' else 'black'
        
        # self.validMoves = []
        gameStatus = self.board.game_status(self.next_player)
        if gameStatus == 0:
            print("Game is not over")
        elif gameStatus == 1:
            pygame.time.delay(100)
            print("CHECKMATE")
            if self.next_player == 'white':
                print("the winner is black!")
                message = "THE WINNER IS BLACK!"
                text_color = (255,255,255)
                box_color = (0, 255, 0)
                winner(message, text_color, box_color)
            elif self.next_player == 'black':
                print("the winner is white!")
                message = "THE WINNER IS WHITE!"
                text_color = (255,255,255)
                box_color = (0, 255, 0)
                winner(message, text_color, box_color)
                
        else:
            pygame.time.delay(100)
            print("STALEMATE")
            print("it's a draw!")
            message = "IT IS A DRAW!"
            text_color = (255,255,255)
            box_color = (0, 255, 0)
            winner(message, text_color, box_color)
                
    def set_hover(self, row, col):
         if(Square.in_range(row,col)):                                               #1
          self.hovered_sqr = self.board.squares[row][col]

    def play_sound(self, captured=False):
        if captured:
            self.capture_sound.play()
        else:
            self.move_sound.play()

    def reset(self):
        self.__init__()
    def update_scores(self):
        self.white_p_score=10040
        self.black_p_score=10040
        for row in range(ROWS):
            for col in range(COLS):
                if self.board.squares[row][col].has_piece():
                    piece = self.board.squares[row][col].piece
                    if piece.color == 'white':
                       self.black_p_score=self.black_p_score-piece.value
                    elif piece.color == 'black':
                        self.white_p_score=self.white_p_score+piece.value