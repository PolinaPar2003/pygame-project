import pygame
import sys
import os
import subprocess

WIDTH = 900
HEIGHT = 542


class Lose:
    def terminate(self):
        pygame.quit()
        sys.exit()

    def load_image(self, name):  # загрузка изображений
        fullname = os.path.join('images', name)
        image = pygame.image.load(fullname)
        return image

    def lose_screen(self):
        fon = pygame.transform.scale(Lose().load_image('lose.png'), (WIDTH, HEIGHT))  # вставка картинок
        screen.blit(fon, (0, 0))
        font = pygame.font.Font('images/3375.ttf', 30)  # загрузка пользовательского шрифта
        text_coord_play = 40  # рисую кнопку
        string_rendered = font.render("RETURN", 1, pygame.Color((48, 33, 18)))
        close_rect_play = string_rendered.get_rect()
        close_rect_play.top = text_coord_play
        close_rect_play.x = 60
        text_coord_play += close_rect_play.height
        pygame.draw.rect(screen, (87, 166, 57), (close_rect_play.x - 10, close_rect_play.y - 10,
                                                 close_rect_play.width + 20, close_rect_play.height + 20))
        screen.blit(string_rendered, close_rect_play)
        return close_rect_play


if __name__ == '__main__':
    FPS = 50
    pygame.init()
    clock = pygame.time.Clock()
    pygame.display.set_caption('shrek swamp')  # вставка названия окна
    pygame.display.set_icon(Lose().load_image("icon.png"))  # вставка иконки
    size = width, height = 900, 542
    screen = pygame.display.set_mode(size)
    running = True
    while running:
        return_b = Lose().lose_screen()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                Lose().terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if (return_b.x - 10 <= event.pos[0] <= return_b.width + 20 + return_b.x - 10) and \
                        (return_b.y - 10 <= event.pos[1] <= return_b.height + 20 + return_b.y - 10):
                    pygame.quit()  # если клик мыши попадает на кнопку, то переход к игре
                    subprocess.call('python level1.py')
                    sys.exit()
        pygame.display.flip()
        clock.tick(FPS)
    pygame.quit()
