import pygame
import sys  # helps us quit the app
import moviepy.editor
from const import *
from game import Game
from square import Square
from move import Move
from AI import *

type = "AI"
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (45, 45, 45)

class Main:
    
    score = 0

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((BGWIDTH, BGHEIGHT))  # self.screen = <Surface(800x800x32 SW)>
        pygame.display.set_caption('Chess Game')
        self.game = Game()
        self.theme = {
            "header_color_left": BLACK,
            "header_color_right": WHITE,
            "header_text_color_left": WHITE,
            "header_text_color_right": BLACK,
            "footer_color": WHITE,
            "footer_text_color": BLACK
        }
    def draw_header(self):
        pygame.draw.rect(self.screen, self.theme["header_color_left"], (0, 0, WIDTH // 2, 50))
        pygame.draw.rect(self.screen, self.theme["header_color_right"], (WIDTH // 2, 0, WIDTH // 2, 50))

        header_font = pygame.font.Font(None, 48)
        header_text_left = header_font.render("score={}".format(self.game.white_p_score), True, self.theme["header_text_color_left"])
        header_text_right = header_font.render("score={}".format(self.game.black_p_score), True, self.theme["header_text_color_right"])
        self.screen.blit(header_text_left, (150, 10))
        self.screen.blit(header_text_right, (550, 10))
    def draw_footer(self):
        # Draw footer
        pygame.draw.rect(self.screen, self.theme["footer_color"], (0, BGHEIGHT - 50, WIDTH, 50))
        footer_font = pygame.font.Font(None, 24)
        footer_text = footer_font.render("BY theHaCkErS", True, self.theme["footer_text_color"])
        self.screen.blit(footer_text, (50, BGHEIGHT - 35))
        footer_text2 = footer_font.render("R: restart / T: theme", True, self.theme["footer_text_color"])
        self.screen.blit(footer_text2, (600, BGHEIGHT - 35))

    def mainloop(self):
        piece_clicked = False  # ///\\\

        def pieces_moves():
            nonlocal piece_clicked
            dragger.Update_mouse(event.pos)
            released_row = (dragger.mouseY - FH_HEIGHT) // SQSIZE
            released_col = dragger.mouseX // SQSIZE

            # create possible move
            initial = Square(dragger.initial_row, dragger.initial_col)
            final = Square(released_row, released_col)
            move = Move(initial, final)

            # valid move?
            if board.valid_move(dragger.piece, move):
                # normal capture
                captured = board.squares[released_row][released_col].has_piece()
                board.move(dragger.piece, move)
                game.update_scores()

                board.set_true_en_passant(dragger.piece)

                # sounds
                game.show_bg(screen)
                game.show_last_move(screen)
                game.show_moves(screen)
                game.show_bg_image(screen)
                game.show_alph_num_bg(screen)
                game.show_pieces(screen)
                game.show_hover(screen)
                if dragger.dragging:
                    dragger.update_blit(screen)
                pygame.display.update()  # Update the screen
                game.play_sound(captured)
                game.next_turn(screen)

            dragger.undrag_piece()
            piece_clicked = False

        while True:  # ila makantch had while dik screen ghatla3 daghya wgha tamchi f7alha flblassa

            screen = self.screen
            game = self.game
            board = self.game.board
            dragger = self.game.dragger

           
            # Handle AI move
            if game.next_player == 'black' and type == "AI":
                value, newBoard = minimax(board, 2, False)
                game.board = newBoard
                game.update_scores()
                game.next_turn(screen)

            # Handle Player move or PVP mode
            elif (game.next_player == 'white' and type == "AI") or type == "PVP":
                for event in pygame.event.get():
                    # quit application
                    if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_q):
                        # Display quit message for a half second
                        message = "QUIT THE GAME"
                        font = pygame.font.Font(None, 30)
                        confirmation_text = font.render(message, True, (255, 255, 255))
                        confirmation_rect = confirmation_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
                        box_width = 250
                        box_height = 60
                        box_rect = pygame.Rect((WIDTH - box_width) // 2, (HEIGHT - box_height) // 2, box_width, box_height)
                        pygame.draw.rect(screen, (0, 0, 0), box_rect, border_radius=10)
                        screen.blit(confirmation_text, confirmation_rect)
                        pygame.display.update()
                        pygame.time.delay(500)
                        pygame.quit()
                        sys.exit()

                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        dragger.Update_mouse(event.pos)
                        clicked_row = (dragger.mouseY - FH_HEIGHT) // SQSIZE
                        clicked_col = dragger.mouseX // SQSIZE

                        if board.squares[clicked_row][clicked_col].has_piece():
                            piece = board.squares[clicked_row][clicked_col].piece
                            if dragger.dragging and dragger.piece == piece:
                                dragger.undrag_piece()
                                piece_clicked = False
                            elif dragger.dragging and dragger.piece != piece and dragger.piece.color != piece.color:
                                pieces_moves()
                            else:
                                if piece.color == game.next_player:
                                    piece.clear_moves()
                                    board.calc_moves(piece, clicked_row, clicked_col, bool=True)
                                    dragger.save_initial(event.pos)
                                    dragger.drag_piece(piece)
                                    piece_clicked = True
                        elif piece_clicked:
                            pieces_moves()

                    elif event.type == pygame.MOUSEMOTION:
                        motion_row = event.pos[1] // SQSIZE
                        motion_col = event.pos[0] // SQSIZE
                        game.set_hover(motion_row, motion_col)

                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_t:
                            game.change_theme(screen)
                        elif event.key == pygame.K_r:
                            message = "RESTART THE GAME"
                            font = pygame.font.Font(None, 30)
                            confirmation_text = font.render(message, True, (255, 255, 255))
                            confirmation_rect = confirmation_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
                            box_width = 250
                            box_height = 60
                            box_rect = pygame.Rect((WIDTH - box_width) // 2, (HEIGHT - box_height) // 2, box_width, box_height)
                            pygame.draw.rect(screen, (0, 0, 0), box_rect, border_radius=10)
                            screen.blit(confirmation_text, confirmation_rect)
                            pygame.display.update()
                            pygame.time.delay(500)
                            game.reset()
                            game = self.game
                            dragger = self.game.dragger
                            board = self.game.board
                            piece_clicked = False

            # Show methods
            game.show_bg(screen)
            game.show_last_move(screen)
            game.show_moves(screen)
            game.show_bg_image(screen)
            game.show_alph_num_bg(screen)
            game.show_pieces(screen)
            game.show_hover(screen)
            if dragger.dragging:
                dragger.update_blit(screen)
            self.draw_header()
            self.draw_footer()
            pygame.display.update()  # Update the screen


# Initialize Pygame
pygame.init()

# Set up the screen
screen_width = BGWIDTH
screen_height = BGHEIGHT
resolution = (screen_width, screen_height)
screen = pygame.display.set_mode((screen_width, screen_height))
background = pygame.image.load("assets/images/background1.jpg")
pygame.display.set_caption("Menu Example")

# Load main menu image
background = pygame.transform.smoothscale(background, resolution)

# Colors
WHITE = (255, 255, 255)
GRAY = (45, 45, 45)

# Fonts
font = pygame.font.Font(None, 36)

def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect(center=(x, y))
    surface.blit(textobj, textrect)

def main_menu():
    global type
    GOLD = (255, 215, 0)  # Gold color for the border
    while True:
        screen.fill(WHITE)

        # Display main menu image
        screen.blit(background, (0, 0))
        
        # Draw large text above the image
        draw_text("CHESS", pygame.font.Font("assets/fonts/Champagne&Limousines.ttf", 90), (255, 255, 255), screen, (screen_width // 2) - 235, (screen_height // 2) - 310)

        # Play Button
        pygame.draw.rect(screen, GOLD, (300 - 2, 350 - 2, 200 + 4, 50 + 4), border_radius=10)  # White border
        pygame.draw.rect(screen, GRAY, (300, 350, 200, 50), border_radius=10)
        draw_text('Vs AI', font, WHITE, screen, 400, 375)

        # Vs Player Button
        pygame.draw.rect(screen, GOLD, (300 - 2, 450 - 2, 200 + 4, 50 + 4), border_radius=10)  # White border
        pygame.draw.rect(screen, GRAY, (300, 450, 200, 50), border_radius=10)
        draw_text('Vs Player', font, WHITE, screen, 400, 475)

        # Quit Button
        pygame.draw.rect(screen, GOLD, (300 - 2, 550 - 2, 200 + 4, 50 + 4), border_radius=10)  # White border
        pygame.draw.rect(screen, GRAY, (300, 550, 200, 50), border_radius=10)
        draw_text('Quit', font, WHITE, screen, 400, 575)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if 300 <= event.pos[0] <= 500 and 350 <= event.pos[1] <= 400:
                    type = "AI"
                    main_game()
                if 300 <= event.pos[0] <= 500 and 450 <= event.pos[1] <= 500:
                    type = "PVP"
                    main_game()
                if 300 <= event.pos[0] <= 500 and 550 <= event.pos[1] <= 600:
                    pygame.quit()
                    sys.exit()

        pygame.display.update()

def main_game():
    main = Main()
    main.mainloop()

if __name__ == "__main__":
    main_menu()
    
