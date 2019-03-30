import pygame
import random

pygame.init()
pygame.mixer.music.load('Eat.ogg')

s_width = 700
s_height = 700
p_width = 600
p_height = 600
tile_size = 30

top_x = (s_width - p_width) / 2
top_y = (s_height - p_height) / 2

velocity = 15

clock = pygame.time.Clock()
title = pygame.font.SysFont('comicsansms', 24).render('Classic Snake', True, (255, 255, 255))
game_over_text = pygame.font.SysFont('comicsansms', 50).render('Game Over', True, (255, 255, 255))


class Snake(object):

    def __init__(self):
        self.x = int(s_width/2)
        self.y = int(s_height/2)
        self.speed = 1
        self.score = 0
        self.tail_pos = [[self.x - tile_size, self.y]]
        self.direction = 'right'


    def eat(self):

        last_tail = self.tail_pos[len(self.tail_pos) - 1]
        if len(self.tail_pos) > 1:

            next_to_last_tail = self.tail_pos[len(self.tail_pos) - 2]

            if next_to_last_tail[0] > last_tail[0]:
                new_tail = [last_tail[0] - tile_size, last_tail[1]]
            elif next_to_last_tail[0] < last_tail[0]:
                new_tail = [last_tail[0] + tile_size, last_tail[1]]
            elif next_to_last_tail[1] > last_tail[1]:
                new_tail = [last_tail[0], last_tail[1] - tile_size]
            else:
                new_tail = [last_tail[0], last_tail[1] + tile_size]
        else:
            if last_tail[0] < self.x:
                new_tail = [last_tail[0] - tile_size, last_tail[1]]
            elif last_tail[0] > self.x:
                new_tail = [last_tail[0] + tile_size, last_tail[1]]
            elif last_tail[1] > self.y:
                new_tail = [last_tail[0], last_tail[1] - tile_size]
            else:
                new_tail = [last_tail[0], last_tail[1] + tile_size]

        print(new_tail)
        self.tail_pos.append(new_tail)
        self.score += 1


    def draw(self, surface):
        pygame.draw.rect(surface, (0, 255, 0), (self.x, self.y, tile_size, tile_size))
        for i in range(len(self.tail_pos)):
            pygame.draw.rect(surface, (0, 255, 0), (self.tail_pos[i][0], self.tail_pos[i][1], tile_size, tile_size,))

    def move(self):

        for i in range(len(self.tail_pos) - 1, 0, -1):
            print(self.tail_pos[i], self.tail_pos[i-1])
            self.tail_pos[i] = self.tail_pos[i - 1]
            print(self.tail_pos[i], self.tail_pos[i - 1])

        self.tail_pos[0] = [self.x, self.y]
        if len(self.tail_pos) > 1:
            print(self.tail_pos[1], self.tail_pos[0])

        if self.direction == 'left':
            self.x -= self.speed*tile_size
        elif self.direction == 'right':
            self.x += self.speed*tile_size
        elif self.direction == 'up':
            self.y -= self.speed*tile_size
        elif self.direction == 'down':
            self.y += self.speed*tile_size

        print(self.x, self.y, self.tail_pos)


class Food(object):

    def __init__(self, snake):
        snake_part = True
        while snake_part:
            snake_part = False
            self.x = random.randint(0, (p_width / tile_size) - 1)
            self.x = self.x * tile_size + (s_width - p_width) / 2
            self.y = random.randint(0, (p_height / tile_size) - 1)
            self.y = self.y * tile_size + (s_height - p_height) / 2
            if self.y == snake.y and self.x == snake.x:
                snake_part = True
            else:
                for [x, y] in snake.tail_pos:
                    if self.x == x and self.y == y:
                        snake_part = True

    def draw(self, surface):
        pygame.draw.rect(surface, (255, 0, 0), (self.x, self.y, tile_size, tile_size))


def draw_screen(surface, snake):
    pygame.display.set_caption('Snake')

    surface.fill((139, 69, 19))
    for i in range(3):
        pygame.draw.rect(surface, (0, 0, 0), (i, i, s_width - i*2, s_height - i*2), 1)

    pygame.draw.rect(surface, (0, 0, 0), (top_x, top_y, p_width, p_height))

    pygame.draw.line(surface, (0, 0, 0), (0, 0), (s_width, s_height), 3)
    pygame.draw.line(surface, (0, 0, 0), (s_width - 1, 0), (0, s_height), 3)

    score = pygame.font.SysFont('comicsansms', 18).render('Score: {}'.format(snake.score), True, (255, 255, 255))

    surface.blit(score, [s_width / 2 - score.get_width() / 2, top_y + p_height + score.get_height() / 2])
    surface.blit(title, [s_width / 2 - title.get_width() / 2, top_y / 2 - title.get_height() / 2])


def is_game_over(snake):
    if snake.x >= (s_width + p_width) / 2 or snake.x <= (s_width - p_width) / 2 - tile_size:
        return True
    if snake.y >= (s_height + p_height) / 2 or snake.y <= (s_height - p_height) / 2 - tile_size:
        return True

    for [x, y] in snake.tail_pos:
        if snake.x == x and snake.y == y:
            return True

    return False


def main(velocity):

    surface = pygame.display.set_mode((s_width, s_height))

    snake = Snake()
    food = Food(snake)

    game_over = False
    while not game_over:

        clock.tick(velocity)

        if snake.x == food.x and snake.y == food.y:
            pygame.mixer.music.play()
            snake.eat()
            food = Food(snake)
            velocity += 0.25

        snake.move()

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                game_over = True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    if snake.direction != 'down' and snake.tail_pos[0][1] >= snake.y:
                        snake.direction = 'up'
                if event.key == pygame.K_DOWN:
                    if snake.direction != 'up' and snake.tail_pos[0][1] <= snake.y:
                        snake.direction = 'down'
                if event.key == pygame.K_LEFT:
                    if snake.direction != 'right' and snake.tail_pos[0][0] >= snake.x:
                        snake.direction = 'left'
                if event.key == pygame.K_RIGHT:
                    if snake.direction != 'left' and snake.tail_pos[0][0] <= snake.x:
                        snake.direction = 'right'


        draw_screen(surface, snake)
        snake.draw(surface)
        food.draw(surface)

        game_over = is_game_over(snake)
        if game_over:
            pygame.mixer.music.load('GameOver.ogg')
            pygame.mixer.music.play()
            surface.blit(game_over_text, [s_width / 2 - game_over_text.get_width() / 2, s_height / 2 - game_over_text.get_height() / 2])
            pygame.display.update(pygame.Rect([s_width / 2 - game_over_text.get_width() / 2, s_height / 2 - game_over_text.get_height() / 2, game_over_text.get_width(), game_over_text.get_height()]))
            pygame.time.delay(10000)
        else:
            pygame.display.update()

if __name__ == '__main__':
    main(velocity)