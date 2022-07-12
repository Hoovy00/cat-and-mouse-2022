import pygame
import pygame.freetype

class Game(object):
    """this class handles the base game features"""
    def __init__(self):
        """initializes the class"""
        pygame.init()
        self.FONT = pygame.freetype.Font("/usr/share/fonts/opentype/urw-base35/NimbusRoman-Italic.otf", 24)

        self.game_objects = []

    def add_game_objects(self, *game_objects):
        """ activates add_game_object """
        for game_object in game_objects:
            self.add_game_object(game_object)

    def add_game_object(self, game_object):
        """appends game objects"""
        self.game_objects.append(game_object)

    def get_game_objects_with_attribute(self, attribute_name):
        """returns attributes with specific attributes"""
        return [game_object for game_object in self.game_objects if hasattr(game_object, attribute_name)]

    def draw(self):
        """used to store things that need to be drawn"""
        drawables = self.get_game_objects_with_attribute("draw")
        for drawable in drawables:
            drawable.draw()

    def handle_movement(self):
        """used to store things that need to move"""
        movables = self.get_game_objects_with_attribute("handle_movement")
        for movable in movables:
            movable.handle_movement()

    def handle_collisions(self):
        """used to store things that need to collide"""
        collidables = self.get_game_objects_with_attribute("handle_collisions")
        for collidable in collidables:
            collidable.handle_collisions(collidables)

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
            self.handle_movement()
            self.handle_collisions()
            pygame.display.update()

        pygame.quit()

class ScoreIndicator(object):
    """this creates the individual numbers and circles on the sides"""
    def __init__(self, score_indicators, label, position, color, label_locations, screen):
        """initializes the class"""
        self.color = color
        self.position = position
        self.score_indicators = score_indicators
        self.label = label
        self.label_location = label_locations
        self.win = screen.win

    def draw(self):
        """draws the circles"""
        pygame.draw.circle(self.win, self.color, self.position, 20, 20)
        self.score_indicators.GAME_FONT.render_to(self.win, self.label_location, self.label, Color.BLACK)

class ScoreIndicators(object):
    """creates the tools to make the numbers and circles on the sides"""
    def __init__(self, game, screen):
        """initializes the class"""
        self.GAME_FONT = game.FONT
        self.children = []
        self.screen = screen

    def add_top(self, label):
        """tools for the top circles and numbers"""
        position_x = int(label) * Board.GRID_HEIGHT - Board.GRID_HEIGHT/2
        label_location_x = position_x - 5 * len(label)
        self.children.append(ScoreIndicator(self, label, (position_x, 5), Color.GREEN, (label_location_x, 2), self.screen))

    def add_side(self, label):
        """tools for the side circles and numbers"""
        position_y = int(label) * Board.GRID_WIDTH - Board.GRID_WIDTH/2
        label_location_x = 1114-7*len(label)
        self.children.append(ScoreIndicator(self, label, (1120, position_y), Color.RED, (label_location_x, position_y-10), self.screen))

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

class Color(object):
    """several colors for use later"""
    WHITE = (178, 178, 178)
    BLACK = (0, 0, 0)
    BLUE = (0, 0, 178)
    RED = (178, 0, 0)
    GREEN = (0, 178, 0)
    BACKGROUND = (161, 133, 106)

class Mouse(object):
    """mouse player functions"""
    WIDTH = Player.WIDTH
    HEIGHT = Player.HEIGHT
    STARTING_GRID_POSITION_X = 5
    STARTING_GRID_POSITION_Y = 3
    def __init__(self, screen, game):
        """initializes the mouse"""
        self.x = (Screen.WIDTH/Board.COLUMNS*(Mouse.STARTING_GRID_POSITION_X-1)) + Board.LINE_WIDTH
        self.y = (Screen.HEIGHT/Board.ROWS*(Mouse.STARTING_GRID_POSITION_Y-1)) + Board.LINE_WIDTH
        self.speed = Player.VELOCITY
        self.is_dead = False
        self.win = screen.win
        self.start_x = self.STARTING_GRID_POSITION_X*66
        self.start_y = self.STARTING_GRID_POSITION_Y*65
        self.FONT = game.FONT
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

    def handle_collisions(self, collidables):
        """makes the mouse "die" if it tuches the cat"""
        for collidable in collidables:
            if collidable is self:
                continue
            if self.x >= collidable.x and self.x <= collidable.x + Player.WIDTH and self.y >= collidable.y and self.y <= collidable.y + Player.HEIGHT:
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
        pygame.draw.rect(self.win, Color.WHITE, (self.x, self.y, Mouse.WIDTH, Mouse.HEIGHT))
        self.draw_start_position()

    def draw_start_position(self):
        """this adds the text "mouse" to indicate where the mouse is supposed to start"""
        self.FONT.render_to(self.win, (self.start_x, self.start_y), "Mouse", (0, 0, 0))

class Cat(object):
    """cat player functions"""
    WIDTH = Player.WIDTH
    HEIGHT = Player.HEIGHT
    STARTING_GRID_POSITION_X = 9
    STARTING_GRID_POSITION_Y = 10
    def __init__(self, screen, game):
        """initializes the cat"""
        self.x = (Screen.WIDTH/Board.COLUMNS*(Cat.STARTING_GRID_POSITION_X-1)) + Board.LINE_WIDTH
        self.y = (Screen.HEIGHT/Board.ROWS*(Cat.STARTING_GRID_POSITION_Y-1)) + Board.LINE_WIDTH
        self.speed = Player.VELOCITY
        self.win = screen.win
        self.FONT = game.FONT

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

    def handle_collisions(self, collidables):
        """triggers the mouse's "death" when it tuches the cat, somehow"""
        pass

    def draw(self):
        """draws the cat"""
        pygame.draw.rect(self.win, Color.WHITE, (self.x, self.y, Cat.WIDTH, Cat.HEIGHT))
        self.draw_start_position()

    def get_location(self):
        """returns Cat's x and y"""
        return (self.x, self.y)

    def draw_start_position(self):
        """this adds the text "cat" to indicate where the cat is supposed to start"""
        self.FONT.render_to(self.win, ((self.STARTING_GRID_POSITION_X*74), (self.STARTING_GRID_POSITION_Y*75)), "Cat", (0, 0, 0))

class Board(object):
    """creates the game area"""
    LINE_WIDTH = 5
    COLUMNS = 14
    ROWS = 11
    GRID_HEIGHT = int(Screen.HEIGHT/ROWS)
    GRID_WIDTH = int(Screen.WIDTH/COLUMNS)
    def __init__(self, screen):
        """initializes the game area"""
        self.win = screen.win

    def draw(self):
        """draws the game board"""
        pygame.draw.rect(self.win, Color.BACKGROUND, (0, 0, Board.GRID_WIDTH*Board.COLUMNS, Board.GRID_HEIGHT*Board.ROWS))
        self.draw_vertical_lines(Board.COLUMNS+1)
        self.draw_horizontal_lines(Board.ROWS+1)

    def draw_horizontal_lines(self, num):
        """tells the draw function what part to draw"""
        for i in range(num):
            pygame.draw.rect(self.win, Color.BLACK, (0, Board.GRID_HEIGHT*i, Screen.WIDTH, Board.LINE_WIDTH))

    def draw_vertical_lines(self, num):
        """tells the draw function what part to draw"""
        for i in range(num):
            pygame.draw.rect(self.win, Color.BLACK, (Board.GRID_WIDTH * i, 0, Board.LINE_WIDTH, Screen.HEIGHT))

class Wall(object):
    """everything to do with the walls"""

    def __init__(self, x, y, screen):
        """initalizes the walls"""
        self.win = screen.win
        self.x = x
        self.y = y

    def draw(self):
        """draws the walls"""
        width = Board.GRID_WIDTH - Board.LINE_WIDTH
        height = Board.GRID_HEIGHT - Board.LINE_WIDTH
        pygame.draw.rect(self.win, Color.BLUE, (Board.GRID_WIDTH*self.x + Board.LINE_WIDTH, Board.GRID_HEIGHT*self.y + Board.LINE_WIDTH, width, height))

game = Game()

class Setup(object):
    """primarily stores information"""
    @staticmethod
    def __init__(self, screen):
        """initalizes the setup"""
        pass

    def game_setup():
        """this is the "main setup" """
        screen = Screen()
        cat = Cat(screen, game)
        mouse = Mouse(screen, game)
        board = Board(screen)
        score_indicators = ScoreIndicators(game, screen)

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
        game.add_game_objects(board)
        for x, y in wall_location:
            game.add_game_object(Wall(x, y, screen))
        game.add_game_objects(score_indicators, cat, mouse)

        for column in range(Board.COLUMNS):
            score_indicators.add_top(str(column + 1))

        for row in range(Board.ROWS):
            score_indicators.add_side(str(row + 1))

Setup.game_setup()

game.play()
