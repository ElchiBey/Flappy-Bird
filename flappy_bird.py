import random
import pygame


# Extensions:
#   {
#       Better Visual:
#           background image; bird image; an image for pipes with different length.
#
#       Audio:
#           background music; jump sound.
#
#       By my option:
#           infinity gameplay; created 2 moving pipes as obstacles and a gap between them, instead of fixed separated
#           ones
#   }


class Obstacles:
    def __init__(self, screen, speed, y):
        self.screen = screen
        self.x = 1200
        self.y = y
        self.speed = speed
        self.image1 = pygame.image.load("pipe.png").convert_alpha()
        self.image2 = pygame.image.load("pipe.png").convert_alpha()
        self.image1 = pygame.transform.rotozoom(self.image1, 0, 0.65)
        self.image2 = pygame.transform.rotozoom(self.image2, 180, 0.65)

    def render(self):
        w1, h1 = self.image1.get_rect().size
        w2, h2 = self.image2.get_rect().size

        self.screen.blit(self.image1, (self.x - w1 / 2, self.y - h1 / 2 + 350))
        self.screen.blit(self.image2, (self.x - w2 / 2, self.y - h2 / 2 - 350))

    def update(self):
        self.x -= self.speed

        w, h = self.image1.get_rect().size

        if self.x <= - w / 2:
            self.x = 1200
            newY = random.randint(140, 560)
            self.y = newY


class Bird:
    def __init__(self, speedY, screen, image):
        self.posX = 200
        self.speedY = speedY
        self.screen = screen

        self.image = pygame.image.load(image).convert_alpha()
        self.image = pygame.transform.rotozoom(self.image, 0, 0.2)

        self.posY = 350 - self.image.get_height()

    def update(self):
        # Jump
        self.posY -= self.speedY
        self.speedY -= 0.5

    def render(self):
        w, h = self.image.get_rect().size
        self.screen.blit(self.image, (self.posX - w / 2, self.posY - h / 2))


class App:

    def __init__(self):
        self.bird = None
        self.running = False
        self.clock = None
        self.screen = None
        self.obstacle = None

    def run(self):
        self.init()
        while self.running:
            self.update()
            self.render()
        self.cleanUp()

    def init(self):
        self.screen = pygame.display.set_mode((1200, 700))
        pygame.display.set_caption("Flappy Ricardo Milos")

        self.clock = pygame.time.Clock()
        self.running = True
        self.bird = Bird(1, self.screen, "ricardo.png")

        y = random.randint(140, 560)
        self.obstacle = Obstacles(self.screen, 6, y)

        pygame.mixer.init()
        pygame.mixer.music.load("backSound.wav")
        pygame.mixer.music.play(-1)

    def update(self):
        w, h = self.bird.image.get_rect().size
        w1, h1 = self.obstacle.image1.get_rect().size
        w2, h2 = self.obstacle.image2.get_rect().size

        # Check Collisions
        if self.bird.posY + h / 2 >= 700 or self.bird.posY - h / 2 <= 0:
            print("YOU LOST! TRY NEXT TIME!!!")
            self.running = False

        if (self.obstacle.x - w1 / 2 - w / 2 + 20 <= self.bird.posX <= self.obstacle.x + w1 / 2 + w / 2 - 25 and
            self.obstacle.y - h1 / 2 + 350 - h / 2 + 25 <= self.bird.posY <= 700) or \
                (self.obstacle.x - w2 / 2 - w / 2 + 20 <= self.bird.posX <= self.obstacle.x + w2 / 2 + w / 2 - 29 and
                 self.obstacle.y + h2 / 2 - 350 + h / 2 - 16 >= self.bird.posY >= 0):
            print("YOU LOST! TRY NEXT TIME!!!")
            self.running = False

        self.events()
        self.bird.update()
        self.obstacle.update()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

        keys = pygame.key.get_pressed()
        mouse_presses = pygame.mouse.get_pressed()
        if keys[pygame.K_SPACE] or mouse_presses[0]:
            pygame.mixer.init()
            sound = pygame.mixer.Sound("jumpSound.wav")
            sound.play()
            self.bird.speedY = 8

    def render(self):
        self.screen.fill((0, 0, 0))

        background = pygame.image.load("background.png")
        self.screen.blit(background, (0, 0))

        self.bird.render()
        self.obstacle.render()

        pygame.display.flip()
        self.clock.tick(60)

    def cleanUp(self):
        pass


if __name__ == "__main__":
    app = App()
    app.run()
