import pygame
import random
import math

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)


class Bullet(pygame.sprite.Sprite):
    """ This class represents the bullet. """

    def __init__(self, start_x, start_y, dest_x, dest_y, velocity):
        """
        It takes in the starting x and y location.
        It also takes in the destination x and y position.
        """

        # Call the parent class (Sprite) constructor
        super().__init__()

        # Set up the image for the bullet
        self.image = pygame.Surface([2, 2])
        self.image.fill(YELLOW)

        self.rect = self.image.get_rect()

        # Move the bullet to our starting location
        self.rect.x = start_x
        self.rect.y = start_y

        # Because rect.x and rect.y are automatically converted
        # to integers, we need to create different variables that
        # store the location as floating point numbers. Integers
        # are not accurate enough for aiming.
        self.floating_point_x = start_x
        self.floating_point_y = start_y

        # Calculation the angle in radians between the start points
        # and end points. This is the angle the bullet will travel.
        x_diff = dest_x - start_x
        y_diff = dest_y - start_y
        angle = math.atan2(y_diff, x_diff)

        # Taking into account the angle, calculate our change_x
        # and change_y. Velocity is how fast the bullet travels.
        self.change_x = math.cos(angle) * velocity
        self.change_y = math.sin(angle) * velocity

    def update(self):
        """ Move the bullet. """

        # The floating point x and y hold our more accurate location.
        self.floating_point_y += self.change_y
        self.floating_point_x += self.change_x

        # The rect.x and rect.y are converted to integers.
        self.rect.y = int(self.floating_point_y)
        self.rect.x = int(self.floating_point_x)

        # If the bullet flies of the screen, get rid of it.
        if self.rect.x < 0 or self.rect.x > SCREEN_WIDTH or self.rect.y < 0 or self.rect.y > SCREEN_HEIGHT:
            self.kill()


class Player(pygame.sprite.Sprite):
    """ Class to represent the player. """

    def __init__(self, color, screen_width, screen_height):
        """ Create the player image. """
        super().__init__()
        self.width = 4
        self.height = 4
        self.image = pygame.Surface([self.width, self.height])
        self.image.fill(color)
        self.rect = self.image.get_rect()

        # -- Attributes
        # Set start location
        self.rect.x = screen_width/2
        self.rect.y = screen_height/2
        # Set speed vector
        self.change_x = 0
        self.change_y = 0

    def changespeed(self, width, height):
        """ Change the speed of the player"""
        self.change_x += width
        self.change_y += height

    def update(self):
        """ Find a new position for the player"""
        self.rect.x += self.change_x
        self.rect.y += self.change_y
        if self.rect.x > SCREEN_WIDTH - self.width:
            self.rect.x = SCREEN_WIDTH - self.width
        elif self.rect.x < 0:
            self.rect.x = 0
        if self.rect.y > SCREEN_HEIGHT - self.height:
            self.rect.y = SCREEN_HEIGHT - self.height
        elif self.rect.y < 0:
            self.rect.y = 0


# Initialize Pygame
pygame.init()

# Set the height and width of the screen
SCREEN_WIDTH = 320
SCREEN_HEIGHT = 240

screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])

# Set the title of the window
pygame.display.set_caption('BulletHell_ML')

'''
icon = None
pygame.display.set_icon(icon)
'''

# Used to manage how fast the screen updates
clock = pygame.time.Clock()

# Number of bullets
N_BULLET = 50

# Set a velocity of the bullet
bullet_vel_max = 3
bullet_vel_min = 0.7

font = pygame.font.SysFont(None, 25)
smallfont = pygame.font.SysFont("comicsansms", 12)
medfont = pygame.font.SysFont("comicsansms", 16)
largefont = pygame.font.SysFont("comicsansms", 20)


def text_objects(text, color, size):
    if size == "small":
        textSurface = smallfont.render(text, True, color)
    elif size == "medium":
        textSurface = medfont.render(text, True, color)
    elif size == "large":
        textSurface = largefont.render(text, True, color)

    return textSurface, textSurface.get_rect()


def message_to_screen(msg, color, y_displace=0, size="small"):
    textSurf, textRect = text_objects(msg, color, size)
    textRect.center = (SCREEN_WIDTH / 2), (SCREEN_HEIGHT / 2) + y_displace
    screen.blit(textSurf, textRect)


def score(score):
    text = smallfont.render("Score: " + str(score), True, WHITE)
    screen.blit(text, [0, 0])


def randomBulletGenerater():
    # Set a start location for the bullet
    rand = random.random()
    if rand < 0.25:
        start_x = 0
        start_y = random.randrange(SCREEN_HEIGHT)
    elif rand < 0.50:
        start_x = SCREEN_WIDTH
        start_y = random.randrange(SCREEN_HEIGHT)
    elif rand < 0.75:
        start_x = random.randrange(SCREEN_WIDTH)
        start_y = 0
    else:
        start_x = random.randrange(SCREEN_WIDTH)
        start_y = SCREEN_HEIGHT

    # Set a destination for the bullet
    dest_x = random.randrange(SCREEN_WIDTH)
    dest_y = random.randrange(SCREEN_HEIGHT)

    # Set a velocity of the bullet
    velocity = random.uniform(bullet_vel_min, bullet_vel_max)
    return start_x, start_y, dest_x, dest_y, velocity


def game_intro():
    intro = True

    while intro:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    intro = False
                if event.key == pygame.K_q:
                    pygame.quit()
                    quit()

        screen.fill(BLACK)
        message_to_screen("Welcome to BulletHell Training",
                          WHITE,
                          -100,
                          "large")

        message_to_screen("Press C to play, P to pause or Q to quit.",
                          WHITE,
                          )

        pygame.display.update()
        clock.tick(15)


def game_loop():
    # Loop until the user clicks the close button.
    game_exit = False
    game_over = False

    center_x = SCREEN_WIDTH / 2
    center_y = SCREEN_HEIGHT / 2

    # This is a list of 'sprites.' Each block in the program is
    # added to this list. The list is managed by a class called 'Group.'
    bullet_list = pygame.sprite.Group()

    # This is a list of every sprite. All blocks and the player block as well.
    all_sprites_list = pygame.sprite.Group()

    # Generate bullet for first time
    for i in range(N_BULLET):

        # Set a start location for the bullet
        start_x, start_y, dest_x, dest_y, velocity = randomBulletGenerater()

        # This represents a bullet
        # def __init__(self, start_x, start_y, dest_x, dest_y, velocity):
        bullet = Bullet(start_x, start_y, dest_x, dest_y, velocity)

        # Add the block to the list of objects
        bullet_list.add(bullet)
        all_sprites_list.add(bullet)

    # Create a WHITE player block
    player = Player(WHITE, SCREEN_WIDTH, SCREEN_HEIGHT)

    all_sprites_list.add(player)

    # for Timer
    frame_count = 0
    frame_rate = 60
    start_time = 90

    # -------- Main Program Loop -----------
    while not game_exit:

        if game_over:
            message_to_screen("Game Over",
                              RED,
                              -50,
                              "large")

            message_to_screen("Total Score: {}".format(frame_count),
                             WHITE,
                             -20,
                             "medium")

            message_to_screen("Press C to play, P to pause or Q to quit.",
                              WHITE,
                              +10)

            pygame.display.update()

        while game_over:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_over = False
                    game_exit = True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_exit = True
                        game_over = False
                    if event.key == pygame.K_c:
                        game_loop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_exit = True

            # Set the speed based on the key pressed
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player.changespeed(-1, 0)
                elif event.key == pygame.K_RIGHT:
                    player.changespeed(1, 0)
                elif event.key == pygame.K_UP:
                    player.changespeed(0, -1)
                elif event.key == pygame.K_DOWN:
                    player.changespeed(0, 1)

            # Reset speed when key goes up
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    player.changespeed(1, 0)
                elif event.key == pygame.K_RIGHT:
                    player.changespeed(-1, 0)
                elif event.key == pygame.K_UP:
                    player.changespeed(0, 1)
                elif event.key == pygame.K_DOWN:
                    player.changespeed(0, -1)

        all_sprites_list.update()

        # Clear the screen
        screen.fill(BLACK)

        # Keep the number of bullets
        if len(bullet_list) < N_BULLET:
            start_x, start_y, dest_x, dest_y, velocity = randomBulletGenerater()

            # This represents a bullet
            # def __init__(self, start_x, start_y, dest_x, dest_y, velocity):
            bullet = Bullet(start_x, start_y, dest_x, dest_y, velocity)

            # Add the block to the list of objects
            bullet_list.add(bullet)
            all_sprites_list.add(bullet)

        # See if the player block has collided with anything.
        game_over = pygame.sprite.spritecollide(player, bullet_list, True)

        # Only move and process game logic if the game isn't over.
        if not game_over:

            # Draw all the spites
            all_sprites_list.draw(screen)

            # ________Timer_Start________
            # --- Timer going up ---
            # Calculate total seconds
            total_seconds = frame_count // frame_rate

            # Divide by 60 to get total minutes
            minutes = total_seconds // 60

            # Use modulus (remainder) to get seconds
            seconds = total_seconds % 60
            '''
            # Use python string formatting to format in leading zeros
            output_string = "Time: {0:02}:{1:02}".format(minutes, seconds)

            # Blit to the screen
            text = font.render(output_string, True, WHITE)
            screen.blit(text, [0, 0])
            '''

            # Use python string formatting to format in leading zeros
            output_string = "Score: {}".format(frame_count)

            # Blit to the screen
            text = font.render(output_string, True, WHITE)
            screen.blit(text, [0, 0])

            # --- Timer going down ---
            # --- Timer going up ---
            # Calculate total seconds
            total_seconds = start_time - (frame_count // frame_rate)
            if total_seconds < 0:
                total_seconds = 0

            # Divide by 60 to get total minutes
            minutes = total_seconds // 60

            # Use modulus (remainder) to get seconds
            seconds = total_seconds % 60

            # Blit to the screen
            text = font.render(output_string, True, BLACK)

            screen.blit(text, [250, 280])

            # ALL CODE TO DRAW SHOULD GO ABOVE THIS COMMENT
            frame_count += 1
            # Timer_end


        # Go ahead and update the screen with what we've drawn.
        pygame.display.flip()

        # Limit to 60 frames per second
        clock.tick(60)

    pygame.quit()
    quit()


game_intro()
game_loop()