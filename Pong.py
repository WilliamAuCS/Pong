import pygame
import sys
import random
from pygame.locals import *


class Ball(object):

    x = 320
    y = 240

    ball_image = pygame.image.load('Pong_Ball.png')
    ball_stretched = pygame.transform.scale(ball_image, (55, 55))

    ball_x = 307
    ball_y = 228
    ball_col = pygame.Rect(ball_x, ball_y, 25, 25)

    pygame.mixer.init()
    pickUpSound = pygame.mixer.Sound('ball_sound.wav')
    pickUpSound.set_volume(0.8)

    def __init__(self, vx, vy, radius, b_color):

        self.vx = vx
        self.vy = vy
        self.initial_x = -0.1
        self.initial_y = 0.1
        self.radius = radius
        self.b_color = b_color

    # Start ball from new game
    def start_move(self):
        self.initial_x = random.choice((0.3, 0.4, 0.5, 0.6))
        self.initial_y = random.choice((0.3, 0.4, 0.5, 0.6))
        if random.choice((0, 1)) == 0:
            self.initial_x *= -1
        if random.choice((0, 1)) == 0:
            self.initial_y *= -1

    # Move ball/bouncing off Paddles
    def move(self):
        Ball.x += self.initial_x
        Ball.y += self.initial_y
        Ball.ball_x += self.initial_x
        Ball.ball_y += self.initial_y
        Ball.ball_col = pygame.Rect(Ball.ball_x, Ball.ball_y, 25, 25)
        if Ball.ball_col.colliderect(Paddle.mid_col_AI) or Ball.ball_col.colliderect(Paddle.mid_col_plr):
            self.initial_x *= -1
            Ball.pickUpSound.play()
        elif (Ball.ball_col.colliderect(Paddle.top_col_AI) or Ball.ball_col.colliderect(Paddle.bot_col_AI) or
              Ball.ball_col.colliderect(Paddle.top_col_plr) or Ball.ball_col.colliderect(Paddle.bot_col_plr)):
            self.initial_y *= -1
            Ball.pickUpSound.play()

    def draw(self, surface):
        pygame.draw.rect(Game.screen, Game.BLACK, Ball.ball_col, 1)
        pygame.draw.circle(surface, self.b_color, (int(Ball.x), int(Ball.y)), self.radius, 0)
        Game.screen.blit(Ball.ball_stretched, (Ball.x - 28, Ball.y - 29))

    def rect(self):
        return pygame.Rect(Ball.x - self.radius, Ball.y - self.radius, 2 * self.radius, 2 * self.radius)


class Paddle(object):
    # Paddle sprites
    player_image = pygame.image.load('Blue_Paddle.png')
    AI_image = pygame.image.load('Red_Paddle.png')
    player_stretched_mid = pygame.transform.scale(player_image, (45, 115))
    player_stretched_sides = pygame.transform.scale(AI_image, (115, 45))

    # Mid_AI colliders
    mid_x_AI = 20
    mid_y_AI = 220
    mid_col_AI = pygame.Rect(mid_x_AI, mid_y_AI, 10, 80)

    # Mid_plr colliders
    mid_x_plr = 600
    mid_y_plr = 220
    mid_col_plr = pygame.Rect(mid_x_plr, mid_y_plr, 10, 80)

    # Side_AI colliders
    side_x_AI = 20
    side_y_AI_top = 20
    side_y_AI_bot = 450
    top_col_AI = pygame.Rect(side_x_AI, side_y_AI_top, 80, 10)
    bot_col_AI = pygame.Rect(side_x_AI, side_y_AI_bot, 80, 10)

    # Side_plr colliders
    side_x_plr = 540
    side_y_plr_top = 20
    side_y_plr_bot = 450
    top_col_plr = pygame.Rect(side_x_plr, side_y_plr_top, 80, 10)
    bot_col_plr = pygame.Rect(side_x_plr, side_y_plr_bot, 80, 10)

    def __init__(self, x, y, width, height, p_color):

        self.s_v_x = x
        self.s_v_y = y

        self.s_h_x = x
        self.s_h_y = y

        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vx = 0.7
        self.vy = 0.7
        self.p_color = p_color

    def draw(self, screen, vert):
        pygame.draw.rect(Game.screen, Game.BLACK, Paddle.mid_col_AI, 1)
        pygame.draw.rect(Game.screen, Game.BLACK, Paddle.mid_col_plr, 1)
        pygame.draw.rect(Game.screen, Game.BLACK, Paddle.top_col_AI, 1)
        pygame.draw.rect(Game.screen, Game.BLACK, Paddle.bot_col_AI, 1)
        pygame.draw.rect(Game.screen, Game.BLACK, Paddle.top_col_plr, 1)
        pygame.draw.rect(Game.screen, Game.BLACK, Paddle.bot_col_plr, 1)
        if vert:
            Game.screen.blit(Paddle.player_stretched_mid, (self.s_v_x - 18, self.s_v_y - 18))
        else:
            Game.screen.blit(Paddle.player_stretched_sides, (self.s_h_x - 18, self.s_h_y - 18))
        pygame.draw.rect(screen, self.p_color, self.rect())

    def AI_vertical(self):
        if Ball.y > self.y + 40 and self.y <= 370:
            self.y += self.vy
            self.s_v_y += self.vy
        elif Ball.y < self.y + 40 and self.y >= 30:
            self.y -= self.vy
            self.s_v_y -= self.vy
        Paddle.mid_y_AI = self.y
        Paddle.mid_col_AI = pygame.Rect(Paddle.mid_x_AI, Paddle.mid_y_AI, 10, 80)

    def AI_horizontal(self):
        if Ball.x > self.x + 40 and self.x <= 240:
            self.x += self.vx
            self.s_h_x += self.vx
            Paddle.col_side_x = self.x
        elif Ball.x < self.x + 40 and self.x >= 80:
            self.x -= self.vx
            self.s_h_x -= self.vx
            Paddle.col_side_x = self.x
        Paddle.side_x_AI = self.x
        Paddle.top_col_AI = pygame.Rect(Paddle.side_x_AI, Paddle.side_y_AI_top, 80, 10)
        Paddle.bot_col_AI = pygame.Rect(Paddle.side_x_AI, Paddle.side_y_AI_bot, 80, 10)

    # Moving Player vertically
    def move_vertical(self, direction):
        if direction is True:
            if self.y <= 370:
                self.y += self.vy
                self.s_v_y += self.vy
        else:
            if self.y >= 30:
                self.y -= self.vy
                self.s_v_y -= self.vy
        Paddle.mid_y_plr = self.y
        Paddle.mid_col_plr = pygame.Rect(Paddle.mid_x_plr, Paddle.mid_y_plr, 10, 80)

    # Moving Player horizontally
    def move_horizontal(self, direction):
        if direction is True:
            if self.x <= 560:
                self.x += self.vx
                self.s_h_x += self.vx
        else:
            if self.x >= 320:
                self.x -= self.vx
                self.s_h_x -= self.vx
        Paddle.side_x_plr = self.x
        Paddle.top_col_plr = pygame.Rect(Paddle.side_x_plr, Paddle.side_y_plr_top, 80, 10)
        Paddle.bot_col_plr = pygame.Rect(Paddle.side_x_plr, Paddle.side_y_plr_bot, 80, 10)

    def rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)


def check_if_scored():
    if Ball.x >= 628 or (Ball.x > 320 and Ball.y < 18) or (Ball.x > 320 and Ball.y > 462):
        Game.AI_score += 1
        Game.game_start = True
    elif Ball.x <= 12 or (Ball.x < 320 and Ball.y < 18) or (Ball.x < 320 and Ball.y > 462):
        Game.plr_score += 1
        Game.game_start = True
    if Game.AI_score == 11 and Game.AI_score > Game.plr_score + 1:
        Game.AI_games += 1
        Game.AI_score = 0
        Game.plr_score = 0
    elif Game.plr_score == 11 and Game.plr_score > Game.AI_score + 1:
        Game.plr_games += 1
        Game.plr_score = 0
        Game.AI_score = 0
    if Game.AI_games == 3 or Game.plr_games == 3:
        end_screen(Game.AI_games, Game.plr_games)


font_name = pygame.font.match_font('comicsans')


def draw_score(surface, text, size, x, y):      # Drawing score to screen
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, Game.WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surface.blit(text_surface, text_rect)


def end_screen(AI_score, plr_score):

    Game.screen.fill(Game.BLACK)
    if AI_score > plr_score:
        pygame.mixer.music.load('game_over.wav')
        pygame.mixer.music.play(0, 0)

        font = pygame.font.Font(font_name, 80)
        text_surface = font.render("AI Wins!", True, Game.WHITE)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (320, 75)
        Game.screen.blit(text_surface, text_rect)
    else:
        pygame.mixer.music.load('level_win.mp3')
        pygame.mixer.music.play(0, 0)

        font = pygame.font.Font(font_name, 80)
        text_surface = font.render("You Win!!!", True, Game.WHITE)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (320, 75)
        Game.screen.blit(text_surface, text_rect)
    while True:
        pygame.time.delay(100)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        font = pygame.font.Font(font_name, 50)
        text_surface = font.render("Press SPACE to play again", True, Game.WHITE)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (320, 350)
        Game.screen.blit(text_surface, text_rect)
        pygame.display.update()
        key_pressed = pygame.key.get_pressed()

        if key_pressed[pygame.K_SPACE]:
            break
    reset()


def reset():
    Game.AI_score = 0
    Game.plr_score = 0
    Game.game_start = True
    Game.plr_games = 0
    Game.AI_games = 0


class Game(object):

    # Game colors
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)

    AI_score = 0
    plr_score = 0
    AI_games = 0
    plr_games = 0

    SCREENSIZE = (640, 480)
    screen = pygame.display.set_mode(SCREENSIZE)

    game_start = True

    def __init__(self):

        pygame.init()

        self.ball = Ball(3, 3, 12, Game.BLACK)

        pygame.display.set_caption("Pong!")
        self.front_name = pygame.font.match_font('arial')

        # AI Size
        self.mid_AI = Paddle(20, 220, 10, 80, Game.BLACK)
        self.top_AI = Paddle(20, 20, 80, 10, Game.BLACK)
        self.bot_AI = Paddle(20, 450, 80, 10, Game.BLACK)

        # Player Size
        self.mid_plr = Paddle(600, 220, 10, 80, Game.BLACK)
        self.top_plr = Paddle(540, 20, 80, 10, Game.BLACK)
        self.bot_plr = Paddle(540, 450, 80, 10, Game.BLACK)

    def AI_movement(self):
        Paddle.AI_vertical(self.mid_AI)
        Paddle.AI_horizontal(self.top_AI)
        Paddle.AI_horizontal(self.bot_AI)

    def get_input(self):    # Getting player input
        key_pressed = pygame.key.get_pressed()

        if key_pressed[pygame.K_UP]:
            Paddle.move_vertical(self.mid_plr, False)
        elif key_pressed[pygame.K_DOWN]:
            Paddle.move_vertical(self.mid_plr, True)

        if key_pressed[pygame.K_RIGHT]:
            Paddle.move_horizontal(self.top_plr, True)
            Paddle.move_horizontal(self.bot_plr, True)
        elif key_pressed[pygame.K_LEFT]:
            Paddle.move_horizontal(self.top_plr, False)
            Paddle.move_horizontal(self.bot_plr, False)

    def play(self):
        Game.game_start = True
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
            # Randomizing initial ball speed/angle
            if Game.game_start is True:
                Ball.x = 320
                Ball.y = 240
                Ball.ball_x = 307
                Ball.ball_y = 228
                Ball.start_move(self.ball)
                Game.game_start = False
            Ball.move(self.ball)
            check_if_scored()
            self.get_input()
            self.AI_movement()
            self.draw()

    def draw(self):
        # Draw board/ball
        Game.screen.fill(Game.BLACK)
        # Drawing net
        net_increment = 5
        for x in range(0, 24):
            pygame.draw.line(Game.screen, Game.WHITE, (320, net_increment), (320, net_increment + 10), 2)
            net_increment += 20

        # Drawing score to screen
        draw_score(Game.screen, str(self.AI_score), 25, 180, 10)
        draw_score(Game.screen, str(self.plr_score), 25, 460, 10)

        # Drawing games to screen
        draw_score(Game.screen, str(self.AI_games), 25, 300, 10)
        draw_score(Game.screen, str(self.plr_games), 25, 340, 10)

        self.ball.draw(Game.screen)

        # Draw AI
        self.mid_AI.draw(Game.screen, True)
        self.top_AI.draw(Game.screen, False)
        self.bot_AI.draw(Game.screen, False)

        # Draw Player
        self.mid_plr.draw(Game.screen, True)
        self.top_plr.draw(Game.screen, False)
        self.bot_plr.draw(Game.screen, False)

        pygame.display.update()


if __name__ == "__main__":

    Game().play()
