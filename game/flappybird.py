import pygame
import sys
import random
from math import floor

pygame.init()


def transform(sprite):
    return pygame.transform.scale2x(sprite)


def load(sprite):
    return pygame.image.load(sprite).convert_alpha()


class Game:

    def __init__(self):
        self.clock = pygame.time.Clock()
        self.surface = Surfaces()
        self.bird = Bird()
        self.pipe = Pipe()
        self.screen = self.surface.screen
        self.event = pygame.event
        self.timer = pygame.USEREVENT
        self.activity = True

    def collision(self):
        for pipe in self.pipe.pipe_list:
            if self.bird.rect_insert().colliderect(pipe):
                return False
            elif pipe.centerx == 100:
                self.surface.high_score += 0.25             # I BSed this part. Too lazy :V
        if self.bird.rect_insert().bottom >= 900 or self.bird.rect_insert().bottom <= -900:
            return False
        return True

    def reset(self):
        self.activity = True
        self.pipe.pipe_list.clear()
        self.bird.x, self.bird.y = 100, 512
        self.bird.movement = self.surface.high_score = 0

    def run(self):
        pygame.time.set_timer(self.timer, 1200)
        pygame.time.set_timer(self.bird.flaps, 125)
        while True:
            for event in self.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE and self.activity:
                        self.bird.fly()
                    if event.key == pygame.K_SPACE and not self.activity:
                        self.reset()
                if event.type == self.timer:
                    self.pipe.pipe_list.extend(self.pipe.get_rec())
                if event.type == self.bird.flaps:
                    if self.bird.idx < 2:
                        self.bird.idx += 1
                    else:
                        self.bird.idx = 0
            self.surface.background()
            if self.activity:
                self.screen.blit(self.bird.rotation(), self.bird.rect_insert())
                self.collision()
                self.bird.falling()
                self.pipe.pipe_generator(self.pipe.move_pipe())
            else:
                self.surface.game_over()
            self.surface.score_display()
            self.surface.draw_floor()
            self.clock.tick(120)
            self.activity = self.collision()
            pygame.display.update()


class Surfaces:

    def __init__(self):
        self.screen = pygame.display.set_mode((576, 1024))
        self.display = pygame.Surface
        self.floor_x_pos = 0
        self.high_score = 0
        self.font = pygame.font.Font("flappy-bird-assets-master/04B_19.TTF", 40)
        self.blocks = [transform(load("flappy-bird-assets-master/sprites/background-day.png")),
                       transform(load("flappy-bird-assets-master/sprites/base.png")),
                       transform(load("flappy-bird-assets-master/sprites/gameover.png"))]

    def fade(self):
        pass

    def score_display(self):
        score_dp = self.font.render(str(floor(self.high_score)), True, (255, 255, 255))
        score_rect = score_dp.get_rect(center=(288, 100))
        self.screen.blit(score_dp, score_rect)

    def draw_floor(self):
        self.screen.blit(self.blocks[1], (self.floor_x_pos, 900))
        self.screen.blit(self.blocks[1], (self.floor_x_pos + 576, 900))
        self.floor_x_pos -= 1
        if self.floor_x_pos <= -576:
            self.floor_x_pos = 0

    def background(self):
        self.screen.blit(self.blocks[0], (0, 0))

    def game_over(self):
        self.screen.blit(self.blocks[2], (100, 300))


class Bird:

    def __init__(self):
        self.x = 100
        self.y = 512
        self.movement = self.idx = 0
        self.up = 10
        self.gravity = 0.25
        self.flaps = pygame.USEREVENT + 1
        self.block = [load("flappy-bird-assets-master/sprites/yellowbird-midflap.png"),
                      load("flappy-bird-assets-master/sprites/yellowbird-downflap.png"),
                      load("flappy-bird-assets-master/sprites/yellowbird-upflap.png")]

    def rotation(self):
        new_bird = pygame.transform.rotozoom(self.block[self.idx], -self.movement * 2.85, 1)
        return transform(new_bird)

    def dead_fall(self):
        pass

    def rect_insert(self):
        picture = self.rotation()
        position = picture.get_rect(center=(self.x, self.y))
        return position

    def falling(self):
        self.movement += self.gravity
        self.y += self.movement
        self.rect_insert()

    def fly(self):
        self.movement = 0
        self.movement -= self.up
        self.y += self.movement
        self.rect_insert()


class Pipe:

    def __init__(self):
        self.pipe = Surfaces()
        self.pipe_surface = transform(load("flappy-bird-assets-master/sprites/pipe-green.png"))
        self.pipe_list = []

    def get_rec(self):
        pipe_pos = random.randrange(400, 800)
        top_pipe = self.pipe_surface.get_rect(midbottom=(700, pipe_pos - 300))
        bottom_pipe = self.pipe_surface.get_rect(midtop=(700, pipe_pos))
        return top_pipe, bottom_pipe

    def pipe_generator(self, pipe_list):
        for pipe in pipe_list:
            if pipe.bottom >= 1020:
                self.pipe.screen.blit(self.pipe_surface, pipe)
            else:
                flip_pipe = pygame.transform.flip(self.pipe_surface, False, True)
                self.pipe.screen.blit(flip_pipe, pipe)

    def move_pipe(self):
        for pipe in self.pipe_list:
            if pipe.right <= 0:
                self.pipe_list.remove(pipe)
            pipe.centerx -= 2.75
        return self.pipe_list


if __name__ == '__main__':
    game = Game()
    game.run()

