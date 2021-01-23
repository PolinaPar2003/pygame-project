import pygame
import sys
import os

WIDTH = 900
HEIGHT = 542


class End:
    def terminate(self):
        pygame.quit()
        sys.exit()

    def load_image(self, name):  # загрузка изображений
        fullname = os.path.join('images', name)
        image = pygame.image.load(fullname)
        return image

    def end_screen(self):
        fon = pygame.transform.scale(End().load_image('end.png'), (WIDTH, HEIGHT))  # вставка картинки
        screen.blit(fon, (0, 0))
        font = pygame.font.Font('3375.ttf', 30)  # загрузка пользовательского шрифта
        text_coord_cont = 440  # рисую кнопку
        string_rendered = font.render("CONTINUE", 1, pygame.Color((48, 33, 18)))
        close_rect_cont = string_rendered.get_rect()
        close_rect_cont.top = text_coord_cont
        close_rect_cont.x = 60
        text_coord_cont += close_rect_cont.height
        pygame.draw.rect(screen, (87, 166, 57), (close_rect_cont.x - 10, close_rect_cont.y - 10,
                                                 close_rect_cont.width + 20, close_rect_cont.height + 20))
        screen.blit(string_rendered, close_rect_cont)
        return close_rect_cont

    def thanks_screen(self):  # все аналогично предыдущему
        fon = pygame.transform.scale(End().load_image('thanks.png'), (WIDTH, HEIGHT))
        screen.blit(fon, (0, 0))
        font = pygame.font.Font('3375.ttf', 30)
        text_coord_cont = 440
        string_rendered = font.render("CONTINUE", 1, pygame.Color((48, 33, 18)))
        close_rect_cont = string_rendered.get_rect()
        close_rect_cont.top = text_coord_cont
        close_rect_cont.x = 440
        text_coord_cont += close_rect_cont.height
        pygame.draw.rect(screen, (87, 166, 57), (close_rect_cont.x - 10, close_rect_cont.y - 10,
                                                 close_rect_cont.width + 20, close_rect_cont.height + 20))
        screen.blit(string_rendered, close_rect_cont)
        return close_rect_cont

    def heart_screen(self):  # все аналогично предыдущему
        fon = pygame.transform.scale(End().load_image('heart.jpg'), (WIDTH, HEIGHT))
        screen.blit(fon, (0, 0))
        font = pygame.font.Font('3375.ttf', 30)
        text_coord_close = 440
        string_rendered = font.render("CLOSE", 1, pygame.Color((48, 33, 18)))
        close_rect_close = string_rendered.get_rect()
        close_rect_close.top = text_coord_close
        close_rect_close.x = 690
        text_coord_close += close_rect_close.height
        pygame.draw.rect(screen, (87, 166, 57), (close_rect_close.x - 10, close_rect_close.y - 10,
                                                 close_rect_close.width + 20, close_rect_close.height + 20))
        screen.blit(string_rendered, close_rect_close)
        return close_rect_close


if __name__ == '__main__':
    FPS = 50
    pygame.init()
    clock = pygame.time.Clock()
    pygame.display.set_caption('shrek swamp')  # вставка названия окна
    pygame.display.set_icon(End().load_image("icon.png"))  # вставка иконки
    size = width, height = 900, 542
    screen = pygame.display.set_mode(size)
    continue_b = None
    close = None
    running = True
    check = 0
    while running:
        if check == 0:  # сначала открывается окно с концом
            continue_b = End().end_screen()
        elif check == 1:  # при нажатии на кнопку - благодарность
            continue_b = End().thanks_screen()
        else:
            close = End().heart_screen()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                End().terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if (continue_b.x - 10 <= event.pos[0] <= continue_b.width + 20 + continue_b.x - 10) and \
                        (continue_b.y - 10 <= event.pos[1] <= continue_b.height + 20 + continue_b.y - 10):
                    check += 1  # если клик мыши попадает на кнопку, то переход к благодарности
                elif (close.x - 10 <= event.pos[0] <= close.width + 20 + close.x - 10) and \
                        (close.y - 10 <= event.pos[1] <= close.height + 20 + close.y - 10):
                    running = False  # если клик мыши попадает на кнопку, то закрытие окна
        pygame.display.flip()
        clock.tick(FPS)
    pygame.quit()
