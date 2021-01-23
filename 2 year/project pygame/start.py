import pygame
import sys
import os
import subprocess

WIDTH = 900
HEIGHT = 542


class Start:
    def terminate(self):
        pygame.quit()
        sys.exit()

    def load_image(self, name):  # загрузка изображений
        fullname = os.path.join('images', name)
        image = pygame.image.load(fullname)
        return image

    def start_screen(self):
        fon = pygame.transform.scale(Start().load_image('intro.png'), (WIDTH, HEIGHT))  # вставка картинки
        screen.blit(fon, (0, 0))
        font = pygame.font.Font('images/3375.ttf', 30)  # загрузка пользовательского шрифта
        text_rules_coord = 300  # рисую кнопку с правилами игры
        string_rendered = font.render("GAME RULES", 1, pygame.Color((48, 33, 18)))
        intro_rect_rules = string_rendered.get_rect()
        intro_rect_rules.top = text_rules_coord
        intro_rect_rules.x = 570
        text_rules_coord += intro_rect_rules.height
        pygame.draw.rect(screen, (87, 166, 57), (intro_rect_rules.x - 10, intro_rect_rules.y - 10,
                                                 intro_rect_rules.width + 20, intro_rect_rules.height + 20))
        screen.blit(string_rendered, intro_rect_rules)

        text_coord_play = 300  # рисую кнопку с игрой
        string_rendered = font.render("PLAY", 1, pygame.Color((48, 33, 18)))
        intro_rect_play = string_rendered.get_rect()
        intro_rect_play.top = text_coord_play
        intro_rect_play.x = 90
        text_coord_play += intro_rect_play.height
        pygame.draw.rect(screen, (87, 166, 57), (intro_rect_play.x - 10, intro_rect_play.y - 10,
                                                 intro_rect_play.width + 20, intro_rect_play.height + 20))
        screen.blit(string_rendered, intro_rect_play)
        return intro_rect_rules, intro_rect_play  # возвращаю координаты кнопок

    def gamerules_screen(self):
        fon = pygame.transform.scale(Start().load_image('gamerules.png'), (WIDTH, HEIGHT))  # вставка картинок
        screen.blit(fon, (0, 0))
        font = pygame.font.Font('images/3375.ttf', 30)  # загрузка пользовательского шрифта
        text_coord_play = 90  # рисую кнопку
        string_rendered = font.render("PLAY", 1, pygame.Color((48, 33, 18)))
        gamerules_rect_play = string_rendered.get_rect()
        gamerules_rect_play.top = text_coord_play
        gamerules_rect_play.x = 700
        text_coord_play += gamerules_rect_play.height
        pygame.draw.rect(screen, (87, 166, 57), (gamerules_rect_play.x - 10, gamerules_rect_play.y - 10,
                                                 gamerules_rect_play.width + 20, gamerules_rect_play.height + 20))
        screen.blit(string_rendered, gamerules_rect_play)
        return gamerules_rect_play


if __name__ == '__main__':
    pygame.init()
    FPS = 50
    clock = pygame.time.Clock()
    pygame.display.set_caption('shrek swamp')  # вставка названия окна
    pygame.display.set_icon(Start().load_image("icon.png"))  # вставка иконки
    size = width, height = 900, 542
    screen = pygame.display.set_mode(size)
    play = None
    rules = None
    running = True
    check = 0
    while running:
        if check == 0:  # сначала открывается окно с заставкой
            rules, play = Start().start_screen()
        else:  # при нажатии на кнопку - окно с правилами
            play = Start().gamerules_screen()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                Start().terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if (rules.x - 10 <= event.pos[0] <= rules.width + 20 + rules.x - 10) and \
                        (rules.y - 10 <= event.pos[1] <= rules.height + 20 + rules.y - 10):
                    check = 1  # если клик мыши попадает на кнопку, то переход к правилам
                elif (play.x - 10 <= event.pos[0] <= play.width + 20 + play.x - 10) and \
                        (play.y - 10 <= event.pos[1] <= play.height + 20 + play.y - 10):
                    pygame.quit()  # если клик мыши попадает на кнопку, то переход к игре
                    subprocess.call('python level1.py')
                    sys.exit()
        pygame.display.flip()
        clock.tick(FPS)
    pygame.quit()
