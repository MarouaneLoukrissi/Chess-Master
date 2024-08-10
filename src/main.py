import pygame
import sys  # helps us quit the app
import moviepy.editor
from const import *
from game import Game
from square import Square
from move import Move
from AI import *

type = "AI"

class Main:
    score = 0
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((BGWIDTH, BGHEIGHT)) #self.screen = <Surface(800x800x32 SW)>
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

    def mainloop(self):
        piece_clicked = False

        def pieces_moves():
            nonlocal piece_clicked
            dragger.Update_mouse(event.pos)
            released_row = (dragger.mouseY - FH_HEIGHT) // SQSIZE
            released_col = dragger.mouseX // SQSIZE

            # create possible move
            initial = Square(dragger.initial_row, dragger.initial_col)
            final = Square(released_row, released_col)
            move = Move(initial, final)

            # valid move ?
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

        while True:
            screen = self.screen
            game = self.game
            board = self.game.board
            dragger = self.game.dragger

            # Draw header
            score = "score={}".format(self.score)
            pygame.draw.rect(screen, self.theme["header_color_left"], (0, 0, WIDTH // 2, 50))
            pygame.draw.rect(screen, self.theme["header_color_right"], (WIDTH // 2, 0, WIDTH // 2, 50))

            header_font = pygame.font.Font(None, 48)
            header_text_left = header_font.render("score={}".format(game.white_p_score), True, self.theme["header_text_color_left"])
            header_text_right = header_font.render("score={}".format(game.black_p_score), True, self.theme["header_text_color_right"])
            screen.blit(header_text_left, (150, 10))
            screen.blit(header_text_right, (550, 10))

            # Draw footer
            pygame.draw.rect(screen, self.theme["footer_color"], (0, BGHEIGHT - 50, WIDTH, 50))
            footer_font = pygame.font.Font(None, 24)
            footer_text = footer_font.render("BY theHaCkErS", True, self.theme["footer_text_color"])
            screen.blit(footer_text, (50, BGHEIGHT - 35))
            footer_text2 = footer_font.render("R: restart / T: theme / Q: quit", True, self.theme["footer_text_color"])
            screen.blit(footer_text2, (570, BGHEIGHT - 35))
            if game.next_player == 'black' and type == "AI":
                game.update_scores()
                game.show_bg(screen)
                game.show_last_move(screen)
                game.show_moves(screen)
                game.show_bg_image(screen)
                game.show_alph_num_bg(screen)
                game.show_pieces(screen)
                game.show_hover(screen)
                pygame.display.update()

                value, newBoard = minimax(board, 2, False)
                game.board = newBoard
                

                if dragger.dragging:
                    dragger.update_blit(screen)
                pygame.display.update()  # Update the screen
                game.next_turn(screen)
                pygame.display.update()
                   
            elif (game.next_player == 'white' and type == "AI") or type == "PVP":
                for event in pygame.event.get():
                    game.update_scores()
                    # quit application
                    if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_q):
                        # Display quit message for a half second
                        message = "QUIT THE GAME"
                        font = pygame.font.Font(None, 30)
                        confirmation_text = font.render(message, True, (255, 255, 255))
                        confirmation_rect = confirmation_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
                        # Create a black box behind the text
                        box_width = 250
                        box_height = 60
                        box_rect = pygame.Rect((WIDTH - box_width) // 2, (HEIGHT - box_height) // 2, box_width, box_height)
                        # Draw the black box
                        pygame.draw.rect(screen, (0, 0, 0), box_rect, border_radius=10)
                        
                        # Draw the text
                        screen.blit(confirmation_text, confirmation_rect)
                        
                        pygame.display.update()
                        # Delay for a half second
                        pygame.time.delay(500)

                        # quit the game
                        pygame.quit()
                        sys.exit()

                    # Click
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        dragger.Update_mouse(event.pos)

                        clicked_row = (dragger.mouseY - FH_HEIGHT) // SQSIZE
                        clicked_col = dragger.mouseX // SQSIZE

                        # If clicked square has a piece?
                        if board.squares[clicked_row][clicked_col].has_piece():
                            piece = board.squares[clicked_row][clicked_col].piece
                            if dragger.dragging and dragger.piece == piece:
                                dragger.undrag_piece()
                                piece_clicked = False
                            elif dragger.dragging and dragger.piece != piece and dragger.piece.color != piece.color:
                                pieces_moves()
                            else:
                                # valid piece (color) ?
                                if piece.color == game.next_player:
                                    # Clear before valid move
                                    piece.clear_moves()
                                    board.calc_moves(piece, clicked_row, clicked_col, bool=True)
                                    dragger.save_initial(event.pos)
                                    dragger.drag_piece(piece)
                                    piece_clicked = True
                        
                        # If a piece was previously clicked or currently being dragged and you clicked on an empty square
                        elif piece_clicked:
                            pieces_moves()

                    elif event.type == pygame.MOUSEMOTION:
                        dragger.Update_mouse(event.pos)
                        
                        # Adjust mouseY to be consistent with other calculations
                        adjusted_mouseY = dragger.mouseY - FH_HEIGHT
                        motion_row = adjusted_mouseY // SQSIZE
                        motion_col = dragger.mouseX // SQSIZE
                        game.set_hover(motion_row, motion_col)
                    
                    elif event.type == pygame.KEYDOWN:
                        # changing themes
                        if event.key == pygame.K_t:
                            game.change_theme(screen)

                        elif event.key == pygame.K_r:
                            # Display restart message for a half second
                            message = "RESTART THE GAME"
                            font = pygame.font.Font(None, 30)
                            confirmation_text = font.render(message, True, (255, 255, 255))
                            confirmation_rect = confirmation_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
                            # Create a black box behind the text
                            box_width = 250
                            box_height = 60
                            box_rect = pygame.Rect((WIDTH - box_width) // 2, (HEIGHT - box_height) // 2, box_width, box_height)
                            # Draw the black box
                            pygame.draw.rect(screen, (0, 0, 0), box_rect, border_radius=10)
                            
                            # Draw the text
                            screen.blit(confirmation_text, confirmation_rect)

                            pygame.display.update()
                            # Delay for a half second
                            pygame.time.delay(500)

                            # Reset the game
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
        draw_text("CHESS", pygame.font.Font("assets/fonts/Champagne&Limousines.ttf", 90), (255, 255, 255), screen, (screen_width // 2)-235, (screen_height // 2) - 310)

        # Play Button
        pygame.draw.rect(screen, GOLD, (300-2, 350-2, 200+4, 50+4), border_radius=10)  # White border
        pygame.draw.rect(screen, GRAY, (300, 350, 200, 50), border_radius=10)
        draw_text('Vs AI', font, WHITE, screen, 400, 375)

        # Vs Player Button
        pygame.draw.rect(screen, GOLD, (300-2, 420-2, 200+4, 50+4), border_radius=10)  # White border
        pygame.draw.rect(screen, GRAY, (300, 420, 200, 50), border_radius=10)
        draw_text('Vs PLAYER', font, WHITE, screen, 400, 445)

        # Exit Button
        pygame.draw.rect(screen, GOLD, (300-2, 490-2, 200+4, 50+4), border_radius=10)  # White border
        pygame.draw.rect(screen, GRAY, (300, 490, 200, 50), border_radius=10)
        draw_text('Exit', font, WHITE, screen, 400, 515)

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if 300 <= mouse_pos[0] <= 500 and 350 <= mouse_pos[1] <= 400:
                    main = Main()
                    main.mainloop()
                elif 300 <= mouse_pos[0] <= 500 and 420 <= mouse_pos[1] <= 470:
                    type = "PVP"
                    main = Main()
                    main.mainloop()
                elif 300 <= mouse_pos[0] <= 500 and 490 <= mouse_pos[1] <= 540:
                    print("Exiting...")  # This is where you would exit the game
                    pygame.quit()
                    sys.exit()

        pygame.display.update()


# Initialize Pygame
pygame.init()

# Set up the screen
screen_width = BGHEIGHT
screen_height = BGHEIGHT
screen2 = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Game Intro")

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Set up fonts
intro_font = pygame.font.SysFont(None, 48)
instructions_font = pygame.font.SysFont(None, 24)
background2 = pygame.image.load("assets/images/background5.jpeg")
background2 = pygame.transform.smoothscale(background2, resolution)

# Function to display text on the screen
def display_text(text, font, color, x, y):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.center = (x, y)
    screen2.blit(text_surface, text_rect)

# Main intro loop
def game_intro():
    intro = True
    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:  # Space key starts the game
                    intro = False
                    main_menu()

        screen2.fill(WHITE)
        # Display main menu image
        screen2.blit(background2, (0, 0))
        # Draw large text above the image
        draw_text("Welcome to Our Chess Game", pygame.font.Font(None, 60), (255, 255, 255), screen, 400, (screen_height // 5))
        draw_text("Press SPACE to start", pygame.font.Font(None, 40), (255, 255, 255), screen, 400, (screen_height // 3))

        pygame.display.update()


pygame.init()

# Set up the screen
screen_width = BGHEIGHT
screen_height = BGHEIGHT
screen1 = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Game Intro")

def video_intro():
    video = moviepy.editor.VideoFileClip("assets/images/chess_intro_900.mp4")
    video.preview()
    game_intro()

video_intro()
