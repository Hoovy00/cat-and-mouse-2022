import pygame
import pygame.freetype

class Game(object):
    def __init__(self):
        pygame.init()

        self.GAME_FONT = pygame.freetype.Font("/usr/share/fonts/opentype/urw-base35/NimbusRoman-Italic.otf", 24)    
    
    def play(self):    
        run = True
        #main game loop
        while run:
            pygame.time.delay(15)
            
            #stops the program when you hit the X button
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

            cat.movement()
            mouse.movement(cat)
            board.draw()
            mouse.draw()
            cat.draw()
            def draw_vertical_score_indicator_background():
                """draws upper numbers"""
                self.GAME_FONT.render_to(screen.win, (35, 2), "1", (0, 0, 0))
                self.GAME_FONT.render_to(screen.win, (115, 2), "2", (0, 0, 0))
                self.GAME_FONT.render_to(screen.win, (195, 2), "3", (0, 0, 0))
                self.GAME_FONT.render_to(screen.win, (275, 2), "4", (0, 0, 0))
                self.GAME_FONT.render_to(screen.win, (355, 2), "5", (0, 0, 0))
                self.GAME_FONT.render_to(screen.win, (435, 2), "6", (0, 0, 0))
                self.GAME_FONT.render_to(screen.win, (515, 2), "7", (0, 0, 0))
                self.GAME_FONT.render_to(screen.win, (595, 2), "8", (0, 0, 0))
                self.GAME_FONT.render_to(screen.win, (675, 2), "9", (0, 0, 0))
                self.GAME_FONT.render_to(screen.win, (750, 2), "10", (0, 0, 0))
                self.GAME_FONT.render_to(screen.win, (830, 2), "11", (0, 0, 0))
                self.GAME_FONT.render_to(screen.win, (910, 2), "12", (0, 0, 0))
                self.GAME_FONT.render_to(screen.win, (990, 2), "13", (0, 0, 0))
                self.GAME_FONT.render_to(screen.win, (1069, 2), "14", (0, 0, 0))

            def draw_horizontal_score_indicator_background():
                """draws vertical numbers"""
                self.GAME_FONT.render_to(screen.win, (1107, 30), "1", (0, 0, 0))
                self.GAME_FONT.render_to(screen.win, (1107, 110), "2", (0, 0, 0))
                self.GAME_FONT.render_to(screen.win, (1107, 190), "3", (0, 0, 0))
                self.GAME_FONT.render_to(screen.win, (1107, 270), "4", (0, 0, 0))
                self.GAME_FONT.render_to(screen.win, (1107, 350), "5", (0, 0, 0))
                self.GAME_FONT.render_to(screen.win, (1107, 430), "6", (0, 0, 0))
                self.GAME_FONT.render_to(screen.win, (1107, 510), "7", (0, 0, 0))
                self.GAME_FONT.render_to(screen.win, (1107, 590), "8", (0, 0, 0))
                self.GAME_FONT.render_to(screen.win, (1107, 670), "9", (0, 0, 0))
                self.GAME_FONT.render_to(screen.win, (1100, 750), "10", (0, 0, 0))
                self.GAME_FONT.render_to(screen.win, (1100, 830), "11", (0, 0, 0))

            draw_vertical_score_indicator_background()
            draw_horizontal_score_indicator_background()

            #draws the indicators of starting points
            self.GAME_FONT.render_to(screen.win, (330, 190), "Mouse", (0, 0, 0))
            self.GAME_FONT.render_to(screen.win, (660, 750), "Cat", (0, 0, 0))

            pygame.display.update()

        pygame.quit()

class Screen(object):
    def __init__(self):
        self.win = pygame.display.set_mode((Screen.WIDTH, Screen.HEIGHT))
        pygame.display.set_caption("Cat and Mouse")
    """stores screen size"""
    WIDTH = 1120
    HEIGHT = 880

class Player(object):
    """stores player size and speed"""
    WIDTH = 75
    HEIGHT = 75
    VELOCITY = 5

#several colors for use later
COLOR_WHITE = (178,178,178)
COLOR_BLACK = (0,0,0)
COLOR_BLUE = (0,0,178)
COLOR_RED = (178,0,0)
COLOR_GREEN = (0,178,0)
COLOR_BACKGROUND = (161, 133, 106)


class Mouse(object):
    """mouse player functions"""
    WIDTH = Player.WIDTH
    HEIGHT = Player.HEIGHT
    START_X_GRID = 5
    START_Y_GRID = 3
    def __init__(self,screen):
        self.x = (Screen.WIDTH/Board.COLUMNS*(Mouse.START_X_GRID-1)) + Board.line_WIDTH
        self.y = (Screen.HEIGHT/Board.ROWS*(Mouse.START_Y_GRID-1)) + Board.line_WIDTH
        self.speed = Player.VELOCITY
        self.is_dead = False
        self.win = screen.win

    #handles Mouse's movement
    def movement(self,cat):

        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.x -= self.speed
        if keys[pygame.K_d]:
            self.x += self.speed
        if keys[pygame.K_w]:
            self.y -= self.speed
        if keys[pygame.K_s]:
            self.y += self.speed
        
        if self.x >= cat.x and self.x <= cat.x + Player.WIDTH and self.y >= cat.y and self.y <= cat.y + Player.HEIGHT:
            self.is_dead = True

        if self.is_dead:
            if keys[pygame.K_r]:
                self.is_dead = False
                self.speed = Player.VELOCITY
            else:
               self.speed = 0
    
    def draw(self):
        pygame.draw.rect(self.win, (COLOR_WHITE), (self.x, self.y, Mouse.WIDTH, Mouse.HEIGHT))




class Cat(object):
    """cat player functions"""
    WIDTH = Player.WIDTH
    HEIGHT = Player.HEIGHT
    START_X_GRID = 9
    START_Y_GRID = 10
    def __init__(self,screen):
        self.x = (Screen.WIDTH/Board.COLUMNS*(Cat.START_X_GRID-1)) + Board.line_WIDTH
        self.y = (Screen.HEIGHT/Board.ROWS*(Cat.START_Y_GRID-1)) + Board.line_WIDTH
        self.speed = Player.VELOCITY
        self.win = screen.win

    # handles movement
    def movement(self):
        
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.x += self.speed
        if keys[pygame.K_UP]:
            self.y -= self.speed
        if keys[pygame.K_DOWN]:
            self.y += self.speed

    def draw(self):
        pygame.draw.rect(self.win, (COLOR_WHITE), (self.x, self.y, Cat.WIDTH, Cat.HEIGHT))

     
    # returns Cat's x and y
    def location(self):
        return (self.x, self.y)

class Board(object):
    """game area"""
    line_WIDTH = 5
    COLUMNS = 14
    ROWS = 11
    def __init__(self,screen):
        self.win = screen.win
    #draws the game board
    def draw(self):
        W = int(Screen.WIDTH/Board.COLUMNS)
        H = int(Screen.HEIGHT/Board.ROWS)
        pygame.draw.rect(self.win, (COLOR_BACKGROUND), (0,0, W*Board.COLUMNS, H*Board.ROWS))
        #draws the vertical lines
        def draw_vertical_lines(num):
            for i in range(num):                
                pygame.draw.rect(self.win, (COLOR_BLACK), (W * i,0, Board.line_WIDTH, Screen.HEIGHT))
        draw_vertical_lines(15)
        #draws the horizontal lines
        def draw_horizontal_lines(num):
            for i in range(num):
                pygame.draw.rect(self.win, (COLOR_BLACK), (0,H*i, Screen.WIDTH, Board.line_WIDTH))
        draw_horizontal_lines(12)
        #draws the walls
        def draw_walls(walls):
            width = W - Board.line_WIDTH
            height = H - Board.line_WIDTH
            for x,y in walls:
                pygame.draw.rect(self.win, (COLOR_BLUE), (W*x + Board.line_WIDTH, H*y + Board.line_WIDTH, width, height))
        walls = [
            (0, 1), (6, 0), (7, 0), (13, 0),
            (3, 1), (4, 1), (9, 1), (10, 1),
            (2, 2), (3, 2), (10, 2), (11, 2), (12, 2),
            (5, 3), (7, 3), (8, 3),
            (1, 4), (3, 4), (10, 4), (12, 4),
            (3, 5), (5, 5), (8, 5), (10, 5),
            (1, 6), (3, 6), (10, 6), (12, 6),
            (5, 7), (6, 7), (8, 7),
            (1, 8), (2, 8), (3, 8), (10, 8), (11, 8), (12, 8),
            (3, 9), (9, 9), (10, 9), 
            (0, 10), (6, 10), (7, 10), (13, 10)
        ]
        draw_walls(walls)
        
        # the circles on the sides
        pygame.draw.circle(self.win, COLOR_GREEN,
            [40, 5], 20, 20)
        pygame.draw.circle(self.win, COLOR_GREEN,
            [120, 5], 20, 20)
        pygame.draw.circle(self.win, COLOR_GREEN,
            [200, 5], 20, 20)
        pygame.draw.circle(self.win, COLOR_GREEN,
            [280, 5], 20, 20)
        pygame.draw.circle(self.win, COLOR_GREEN,
            [360, 5], 20, 20)
        pygame.draw.circle(self.win, COLOR_GREEN,
            [440, 5], 20, 20)
        pygame.draw.circle(self.win, COLOR_GREEN,
            [520, 5], 20, 20)  
        pygame.draw.circle(self.win, COLOR_GREEN,
            [600, 5], 20, 20)
        pygame.draw.circle(self.win, COLOR_GREEN,
            [680, 5], 20, 20)
        pygame.draw.circle(self.win, COLOR_GREEN,
            [760, 5], 20, 20)
        pygame.draw.circle(self.win, COLOR_GREEN,
            [840, 5], 20, 20)
        pygame.draw.circle(self.win, COLOR_GREEN,
            [920, 5], 20, 20)
        pygame.draw.circle(self.win, COLOR_GREEN,
            [1000, 5], 20, 20)
        pygame.draw.circle(self.win, COLOR_GREEN,
            [1080, 5], 20, 20)
  
        pygame.draw.circle(self.win, COLOR_RED,
            [1120, 40], 20, 20)
        pygame.draw.circle(self.win, COLOR_RED,
            [1120, 120], 20, 20)
        pygame.draw.circle(self.win, COLOR_RED,
            [1120, 200], 20, 20)
        pygame.draw.circle(self.win, COLOR_RED,
            [1120, 280], 20, 20)
        pygame.draw.circle(self.win, COLOR_RED,
            [1120, 360], 20, 20)
        pygame.draw.circle(self.win, COLOR_RED,
            [1120, 440], 20, 20)
        pygame.draw.circle(self.win, COLOR_RED,
            [1120, 520], 20, 20) 
        pygame.draw.circle(self.win, COLOR_RED,
            [1120, 600], 20, 20)
        pygame.draw.circle(self.win, COLOR_RED,
            [1120, 680], 20, 20)
        pygame.draw.circle(self.win, COLOR_RED,
            [1120, 760], 20, 20)
        pygame.draw.circle(self.win, COLOR_RED,
            [1120, 840], 20, 20)

     
#used to call the classes
screen = Screen()
cat = Cat(screen)
mouse = Mouse(screen)
board = Board(screen)
game = Game()
game.play()
