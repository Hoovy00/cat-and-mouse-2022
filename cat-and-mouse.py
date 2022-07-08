import pygame
import pygame.freetype

class Game(object):
    """this class handles the base game features"""
    def __init__(self):
        """initializes the class"""
        pygame.init()

    def draw(self):
        board.draw()
        walls.draw()
        lines.draw()
        mouse.draw()
        cat.draw()
        cat.draw_start_position()
        mouse.draw_start_position()
        score_indicators.draw()

    def movement(self):
        cat.handle_movement()
        mouse.handle_movement()

    def collisions(self):
        mouse.handle_collision(cat)

    def play(self):    
        """main game loop"""
        run = True
        while run:
            pygame.time.delay(15)
            
            """stops the program when you hit the X button"""
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
            self.draw()
            self.movement()
            self.collisions()
            pygame.display.update()

        pygame.quit()

class ScoreIndicator(object):
    """this creates the individual numbers and circles on the sides"""
    def __init__(self,score_indicators,label,position,color,label_location):
        """initializes the class"""
        self.color = color
        self.position = position
        self.score_indicators = score_indicators
        self.label = label
        self.label_location = label_location

    def draw(self):
        """draws the circles"""
        pygame.draw.circle(screen.win, self.color,
            self.position, 20, 20)
        self.score_indicators.GAME_FONT.render_to(screen.win, self.label_location, self.label, (0, 0, 0))

class ScoreIndicators(object):
    """creates the tools to make the numbers and circles on the sides"""
    def __init__(self):
        """initializes the class"""
        self.GAME_FONT = pygame.freetype.Font("/usr/share/fonts/opentype/urw-base35/NimbusRoman-Italic.otf", 24)
        self.children = []

    def add_top(self, label, position, color, label_location):
        """tools for the top circles and numbers"""
        self.children.append( ScoreIndicator(self, label, position, color, label_location ))

    def add_side(self, label, position, color, label_location):
        """tools for the side circles and numbers"""
        self.children.append( ScoreIndicator(self, label, position, color, label_location ))

    def draw(self):
        """draws them"""
        for child in self.children:
            child.draw()

class Screen(object):
    "creates the window that the game is played in"
    def __init__(self):
        """initializes the game window"""
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

"""several colors for use later"""
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
    STARTING_GRID_POSITION_X = 5
    STARTING_GRID_POSITION_Y = 3
    def __init__(self,screen):
        self.x = (Screen.WIDTH/Board.COLUMNS*(Mouse.STARTING_GRID_POSITION_X-1)) + Board.LINE_WIDTH
        self.y = (Screen.HEIGHT/Board.ROWS*(Mouse.STARTING_GRID_POSITION_Y-1)) + Board.LINE_WIDTH
        self.speed = Player.VELOCITY
        self.is_dead = False
        self.win = screen.win

    def handle_movement(self):
        """handles Mouse's movement"""

        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.x -= self.speed
        if keys[pygame.K_d]:
            self.x += self.speed
        if keys[pygame.K_w]:
            self.y -= self.speed
        if keys[pygame.K_s]:
            self.y += self.speed

    def handle_collision(self,cat):
        """makes the mouse "die" if it tuches the cat"""
        if self.x >= cat.x and self.x <= cat.x + Player.WIDTH and self.y >= cat.y and self.y <= cat.y + Player.HEIGHT:
            self.is_dead = True

        if self.is_dead:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_r]:
                self.is_dead = False
                self.speed = Player.VELOCITY
            else:
               self.speed = 0
    
    def draw(self):
        """draws the mouse"""
        pygame.draw.rect(self.win, COLOR_WHITE, (self.x, self.y, Mouse.WIDTH, Mouse.HEIGHT))
    
    def draw_start_position(self):
        """this adds the text "mouse" to indicate where the mouse is supposed to start"""
        score_indicators.GAME_FONT.render_to(screen.win, ((self.STARTING_GRID_POSITION_X*66), (self.STARTING_GRID_POSITION_Y*65)), "Mouse", (0, 0, 0))

class Cat(object):
    """cat player functions"""
    WIDTH = Player.WIDTH
    HEIGHT = Player.HEIGHT
    STARTING_GRID_POSITION_X = 9
    STARTING_GRID_POSITION_Y = 10
    def __init__(self,screen):
        """initializes the cat"""
        self.x = (Screen.WIDTH/Board.COLUMNS*(Cat.STARTING_GRID_POSITION_X-1)) + Board.LINE_WIDTH
        self.y = (Screen.HEIGHT/Board.ROWS*(Cat.STARTING_GRID_POSITION_Y-1)) + Board.LINE_WIDTH
        self.speed = Player.VELOCITY
        self.win = screen.win

    def handle_movement(self):
        """handles movement"""
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
        """draws the cat"""
        pygame.draw.rect(self.win, COLOR_WHITE, (self.x, self.y, Cat.WIDTH, Cat.HEIGHT))
     
    def get_location(self):
        """returns Cat's x and y"""
        return (self.x, self.y)

    def draw_start_position(self):
        """this adds the text "cat" to indicate where the cat is supposed to start"""
        score_indicators.GAME_FONT.render_to(screen.win, ((self.STARTING_GRID_POSITION_X*74), (self.STARTING_GRID_POSITION_Y*75)), "Cat", (0, 0, 0))

class Board(object):
    """creates the game area"""
    LINE_WIDTH = 5
    COLUMNS = 14
    ROWS = 11
    GRID_HEIGHT = int(Screen.HEIGHT/ROWS)
    GRID_WIDTH = int(Screen.WIDTH/COLUMNS)
    def __init__(self):
        """initializes the game area"""
        self.win = screen.win

    def draw(self):
        """draws the game board"""
        pygame.draw.rect(self.win, COLOR_BACKGROUND, (0,0, Board.GRID_WIDTH*Board.COLUMNS, Board.GRID_HEIGHT*Board.ROWS))

class Walls(object):
    """everything to do with the walls"""

    def __init__(self):
        """initalizes the walls"""
        self.win = screen.win

    def draw(self):
        """draws the walls"""
        width = Board.GRID_WIDTH - Board.LINE_WIDTH
        height = Board.GRID_HEIGHT - Board.LINE_WIDTH
        for x,y in wall_location:
            pygame.draw.rect(self.win, COLOR_BLUE, (Board.GRID_WIDTH*x + Board.LINE_WIDTH, Board.GRID_HEIGHT*y + Board.LINE_WIDTH, width, height))


class Lines(object):
    def __init__(self):
        self.win = screen.win    
    def draw(self):
        """draws the lines"""
        self.draw_vertical_lines(15)
        self.draw_horizontal_lines(12)

    def draw_horizontal_lines(self,  num):
        """tells the draw function what part to draw"""
        for i in range(num):
            pygame.draw.rect(self.win, COLOR_BLACK, (0,Board.GRID_HEIGHT*i, Screen.WIDTH, Board.LINE_WIDTH))

    def draw_vertical_lines(self, num):
        """tells the draw function what part to draw"""
        for i in range(num):                
            pygame.draw.rect(self.win, COLOR_BLACK, (Board.GRID_WIDTH * i,0, Board.LINE_WIDTH, Screen.HEIGHT))
  
"""used to call the classes"""
screen = Screen()
cat = Cat(screen)
mouse = Mouse(screen)
walls = Walls()
lines = Lines()
board = Board()
game = Game()
score_indicators = ScoreIndicators()

wall_location = [
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

score_indicators.add_top("1", (40, 5), COLOR_GREEN, (35, 2) )
score_indicators.add_top("2", (120, 5), COLOR_GREEN, (115, 2) )
score_indicators.add_top("3", (200, 5), COLOR_GREEN, (195, 2) )
score_indicators.add_top("4", (280, 5), COLOR_GREEN, (275, 2) )
score_indicators.add_top("5", (360, 5), COLOR_GREEN, (355, 2) )
score_indicators.add_top("6", (440, 5), COLOR_GREEN, (435, 2) )
score_indicators.add_top("7", (520, 5), COLOR_GREEN, (515, 2) )
score_indicators.add_top("8", (600, 5), COLOR_GREEN, (595, 2) )
score_indicators.add_top("9", (680, 5), COLOR_GREEN, (675, 2) )
score_indicators.add_top("10", (760, 5), COLOR_GREEN, (750, 2) )
score_indicators.add_top("11", (840, 5), COLOR_GREEN, (830, 2) )
score_indicators.add_top("12", (920, 5), COLOR_GREEN, (910, 2) )
score_indicators.add_top("13", (1000, 5), COLOR_GREEN, (990, 2) )
score_indicators.add_top("14", (1080, 5), COLOR_GREEN, (1069, 2) )

score_indicators.add_side("1", (1120, 40), COLOR_RED, (1107, 30) )
score_indicators.add_side("2", (1120, 120), COLOR_RED, (1107, 110) )
score_indicators.add_side("3", (1120, 200), COLOR_RED, (1107, 190) )
score_indicators.add_side("4", (1120, 280), COLOR_RED, (1107, 270) )
score_indicators.add_side("5", (1120, 360), COLOR_RED, (1107, 350) )
score_indicators.add_side("6", (1120, 440), COLOR_RED, (1107, 430) )
score_indicators.add_side("7", (1120, 520), COLOR_RED, (1107, 510) )
score_indicators.add_side("8", (1120, 600), COLOR_RED, (1107, 590) )
score_indicators.add_side("9", (1120, 680), COLOR_RED, (1107, 670) )
score_indicators.add_side("10", (1120, 760), COLOR_RED, (1100, 750) )
score_indicators.add_side("11", (1120, 840), COLOR_RED, (1100, 830) )

game.play()