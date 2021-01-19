import pygame
import os
import subprocess


class LevelFirst:  # класс для генерации уровня
    def generate_level(self, level):  # генерация уровня из файла с картой
        new_player, x, y = None, None, None
        for y in range(len(level)):
            for x in range(len(level[y])):
                if level[y][x] == '.':
                    Tile('swamp', x, y)
                elif level[y][x] == '+':
                    Tile('river', x, y)
                elif level[y][x] == '/':
                    Tile('path_round_left_up', x, y)
                elif level[y][x] == '"':
                    Tile('path_round_left_down', x, y)
                elif level[y][x] == '#':
                    Tile('path_center', x, y)
                elif level[y][x] == '*':
                    Tile('sprike_down', x, y)
                elif level[y][x] == '$':
                    Tile('path_center', x, y)
                    Tile('zhuk', x, y)
                elif level[y][x] == '-':
                    Tile('swamp2', x, y)
                elif level[y][x] == '&':
                    Tile('grass', x, y)
                elif level[y][x] == '=':
                    Tile('path_round_right_down', x, y)
                elif level[y][x] == '%':
                    Tile('path_round_right_up', x, y)
                elif level[y][x] == '^':
                    Tile('path_str_up', x, y)
                elif level[y][x] == '(':
                    Tile('path_str_left', x, y)
                elif level[y][x] == ')':
                    Tile('path_str_right', x, y)
                elif level[y][x] == ',':
                    Tile('path_str_down', x, y)
                elif level[y][x] == ';':
                    Tile('path_str_right', x, y)
                    Tile('zhuk', x, y)
                elif level[y][x] == ':':
                    Tile('path_str_down', x, y)
                    Tile('zhuk', x, y)
                elif level[y][x] == '?':
                    Tile('path_str_left', x, y)
                    Tile('zhuk', x, y)
                elif level[y][x] == '}':
                    Tile('path_str_up', x, y)
                    Tile('zhuk', x, y)
                elif level[y][x] == '{':
                    Tile('path_round_right_up', x, y)
                    Tile('zhuk', x, y)
                elif level[y][x] == ']':
                    Tile('path_round_right_down', x, y)
                    Tile('zhuk', x, y)
                elif level[y][x] == '[':
                    Tile('path_round_left_down', x, y)
                    Tile('zhuk', x, y)
                elif level[y][x] == '|':
                    Tile('path_round_left_up', x, y)
                    Tile('zhuk', x, y)
                elif level[y][x] == '~':
                    Tile('path_gor', x, y)
                elif level[y][x] == '_':
                    Tile('path_vert', x, y)
                elif level[y][x] == '!':
                    Tile('target', x, y)
                else:
                    Tile('path_center', x, y)
                    new_player = Player(player_image, 6, 1, x, y)
        return new_player, x, y

    def decor(self):  # некоторые украшения
        Tile('image_grass', 10, 4.5)
        Tile('image_plant', 0, 0)
        Tile('image_seaweed', 3, 3)
        Tile('image_house', 1, 7)
        Tile('image_tree', 4, 9.5)
        Tile('image_swamp', 12, 2)
        Tile('image_big_tree', 13, 11)

    def load_image(self, name, colorkey=None):  # загрузка картинки
        fullname = os.path.join('images', name)
        image = pygame.image.load(fullname)
        return image

    def load_level(self, filename):  # загрузка уровня из текстового файла с картой
        filename = "levels/" + filename
        with open(filename, 'r') as mapFile:
            level_map = [line.strip() for line in mapFile]
        max_width = max(map(len, level_map))
        return list(map(lambda x: x.ljust(max_width, '.'), level_map))


class Tile(pygame.sprite.Sprite):  # класс для расставления спрайтов в окне pygame
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(tile_width * pos_x, tile_height * pos_y)
        if 'path' in tile_type or tile_type == 'target':
            mozhno_group.add(all_sprites.sprites()[-1])
            if 'target' in tile_type:
                target_group.add(all_sprites.sprites()[-1])
              # по названию спрайта проверяю можно ли будет персонажу ходить
            # по нему или нет и добавляю в соответствующую группу
        elif 'zhuk' in tile_type:
            zhuk_group.add(all_sprites.sprites()[-1])
        elif 'sprike' in tile_type:
            sprike_group.add(all_sprites.sprites()[-1])
        else:
            nelzay_group.add(all_sprites.sprites()[-1])


class Player(pygame.sprite.Sprite):  # класс для спрайта и передвижения персонажа
    def __init__(self, sheet, columns, rows, x, y):
        super().__init__(player_group, all_sprites)
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(x * tile_width, y * tile_height)

    def cut_sheet(self, sheet, columns, rows):  # обрезка спрайта
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def update(self):  # движение спрайта
        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.image = self.frames[self.cur_frame]

    def move_right(self):  # движение вправо
        self.rect.x += 45
        if not pygame.sprite.spritecollide(player, nelzay_group, False):  # проверяю, сталкивается ли спрайт
            pygame.sprite.spritecollide(player, zhuk_group, True)  # с спрайтом, на который ему нельзя заходить, если нет - движение вправо
            if pygame.sprite.spritecollide(player, target_group, False):
                global on_target
                on_target = True
            if not pygame.sprite.spritecollide(player, sprike_group, False):
                pass
            else:
                for i in pygame.sprite.spritecollide(player, sprike_group, False):
                    if i.image == tile_images['sprike_down']:
                        Tile('sprike_up', i.rect.x // tile_width, i.rect.y // tile_height)
                    else:
                        global player_die
                        player_die = True
        else:  # если да, то идет проверка, что он сталкивается именно правым концом
            self.rect.x -= 45

    def move_left(self):
        self.rect.x -= 45
        if not pygame.sprite.spritecollide(player, nelzay_group, False):
            pygame.sprite.spritecollide(player, zhuk_group, True)
            if pygame.sprite.spritecollide(player, target_group, False):
                global on_target
                on_target = True
            if not pygame.sprite.spritecollide(player, sprike_group, False):
                pass
            else:
                for i in pygame.sprite.spritecollide(player, sprike_group, False):
                    if i.image == tile_images['sprike_down']:
                        Tile('sprike_up', i.rect.x // tile_width, i.rect.y // tile_height)
                    else:
                        global player_die
                        player_die = True
        else:
            self.rect.x += 45

    def move_up(self):
        self.rect.y += 45
        if not pygame.sprite.spritecollide(player, nelzay_group, False):
            pygame.sprite.spritecollide(player, zhuk_group, True)
            if pygame.sprite.spritecollide(player, target_group, False):
                global on_target
                on_target = True
            if not pygame.sprite.spritecollide(player, sprike_group, False):
                pass
            else:
                for i in pygame.sprite.spritecollide(player, sprike_group, False):
                    if i.image == tile_images['sprike_down']:
                        Tile('sprike_up', i.rect.x // tile_width, i.rect.y // tile_height)
                    else:
                        global player_die
                        player_die = True
        else:
            self.rect.y -= 45

    def move_down(self):
        self.rect.y -= 45
        if not pygame.sprite.spritecollide(player, nelzay_group, False):
            pygame.sprite.spritecollide(player, zhuk_group, True)
            if pygame.sprite.spritecollide(player, target_group, False):
                global on_target
                on_target = True
            if not pygame.sprite.spritecollide(player, sprike_group, False):
                pass
            else:
                for i in pygame.sprite.spritecollide(player, sprike_group, False):
                    if i.image == tile_images['sprike_down']:
                        Tile('sprike_up', i.rect.x // tile_width, i.rect.y // tile_height)
                    else:
                        global player_die
                        player_die = True
        else:
            self.rect.y += 45


if __name__ == '__main__':
    pygame.init()
    all_sprites = pygame.sprite.Group()
    mozhno_group = pygame.sprite.Group()
    nelzay_group = pygame.sprite.Group()
    sprike_group = pygame.sprite.Group()
    zhuk_group = pygame.sprite.Group()
    target_group = pygame.sprite.Group()
    player_group = pygame.sprite.Group()
    FPS = 20
    clock = pygame.time.Clock()
    pygame.display.set_icon(LevelFirst().load_image("icon.png"))  # загрузка иконки
    pygame.display.set_caption('shrek swamp')
    size = width, height = 675, 675
    screen = pygame.display.set_mode(size)
    tile_images = {
        'path_round_left_up': LevelFirst().load_image('path1.png'),
        'river': LevelFirst().load_image('swamp1.png'),
        'sprike_down': LevelFirst().load_image('sprike1.png'),
        'zhuk': LevelFirst().load_image('zhuk.png'),
        'path_round_right_up': LevelFirst().load_image('path4.png'),
        'swamp': LevelFirst().load_image('swamp3.png'),
        'swamp2': LevelFirst().load_image('swamp4.png'),
        'grass': LevelFirst().load_image('grass.png'),
        'sprike_up': LevelFirst().load_image('sprike2.png'),
        'path_round_left_down': LevelFirst().load_image('path2.png'),
        'path_round_right_down': LevelFirst().load_image('path3.png'),
        'path_center': LevelFirst().load_image('path5.png'),
        'path_gor': LevelFirst().load_image('path_gor.png'),
        'path_vert': LevelFirst().load_image('path_vert.png'),
        'path_str_up': LevelFirst().load_image('path6.png'),
        'path_str_left': LevelFirst().load_image('path7.png'),
        'path_str_down': LevelFirst().load_image('path8.png'),
        'path_str_right': LevelFirst().load_image('path9.png'),
        'zhuk_str_right': LevelFirst().load_image('zhuk_right.png'),
        'zhuk_str_down': LevelFirst().load_image('zhuk_down.png'),
        'zhuk_str_left': LevelFirst().load_image('zhuk_left.png'),
        'zhuk_str_up': LevelFirst().load_image('zhuk_up.png'),
        'zhuk_round_right': LevelFirst().load_image('zhuk_round_right.png'),
        'zhuk_round_right2': LevelFirst().load_image('zhuk_round_right2.png'),
        'zhuk_round_left2': LevelFirst().load_image('zhuk_round_left2.png'),
        'zhuk_round_left': LevelFirst().load_image('zhuk_round_left.png'),
        'target': LevelFirst().load_image('target.png'),
        'image_plant': LevelFirst().load_image("plant.png"),
        'image_seaweed': LevelFirst().load_image("seaweed.png"),
        'image_wood': LevelFirst().load_image("wood.png"),
        'image_tree': LevelFirst().load_image("tree.png"),
        'image_swamp': LevelFirst().load_image("swamp5.png"),
        'image_big_tree': LevelFirst().load_image("tree2.png"),
        'image_house': LevelFirst().load_image("house.png"),
        'image_grass': LevelFirst().load_image("grass2.png"),
        'lose': LevelFirst().load_image('lose.png')
    }
    player_image = LevelFirst().load_image("shrek_idet.png")
    player_die = False
    on_target = False
    tile_width = tile_height = 45
    player, level_x, level_y = LevelFirst().generate_level(LevelFirst().load_level('level 1.0.txt'))
    LevelFirst().decor()
    running = True
    while running:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:  # если нажата правая стрелка
                    x = player.rect.x // tile_width  # "запоминаю" нахождение персонажа на поле
                    y = player.rect.y // tile_height
                    player.kill()  # "убиваю" его
                    player = Player(LevelFirst().load_image("shrek_idet.png"), 6, 1, x, y)  # и на его место вставляю
                    s = 0  # определенный спрайт (в зависимости от направления движения)
                    player.move_right()  # проверка на движение в том направлении и само движение, если оно возможно
                    while s < 6:  # обновление спрайта (тк он должен двигаться во время передвижения, т е должны
                        clock.tick(FPS)  # изменяться картинки (их 6, поэтому обновление происходит 6 раз)
                        player.update()
                        all_sprites.draw(screen)
                        player_group.draw(screen)
                        sprike_group.draw(screen)
                        pygame.display.flip()
                        s += 1
                if event.key == pygame.K_LEFT:
                    x = player.rect.x // tile_width
                    y = player.rect.y // tile_height
                    player.kill()
                    player = Player(LevelFirst().load_image("shrek_idet7.png"), 6, 1, x, y)
                    s = 0
                    player.move_left()
                    while s < 6:
                        clock.tick(FPS)
                        player.update()
                        all_sprites.draw(screen)
                        player_group.draw(screen)
                        pygame.display.flip()
                        s += 1
                if event.key == pygame.K_UP:
                    x = player.rect.x // tile_width
                    y = player.rect.y // tile_height
                    player.kill()
                    player = Player(LevelFirst().load_image("shrek_up.png"), 1, 1, x, y)
                    player.move_down()
                    clock.tick(FPS)
                    player.update()
                    all_sprites.draw(screen)
                    player_group.draw(screen)
                    pygame.display.flip()
                if event.key == pygame.K_DOWN:
                    x = player.rect.x // tile_width
                    y = player.rect.y // tile_height
                    player.kill()
                    player = Player(LevelFirst().load_image("shrek_down.png"), 1, 1, x, y)
                    player.move_up()
                    clock.tick(FPS)
                    player.update()
                    all_sprites.draw(screen)
                    player_group.draw(screen)
                    pygame.display.flip()
        if len(zhuk_group.sprites()) == 0 and on_target:
            x = player.rect.x // tile_width
            y = player.rect.y // tile_height
            player.kill()
            player = Player(LevelFirst().load_image("shrek_win.png"), 6, 1, x, y)
            running = False
            s = 0
            while s < 6:
                clock.tick(FPS)
                player.update()
                all_sprites.draw(screen)
                player_group.draw(screen)
                pygame.display.flip()
                s += 1
        if player_die:
            x = player.rect.x // tile_width
            y = player.rect.y // tile_height
            player.kill()
            player = Player(LevelFirst().load_image("shrek_umer.png"), 6, 1, x, y)
            s = 0
            while s < 6:
                clock.tick(FPS)
                player.update()
                all_sprites.draw(screen)
                player_group.draw(screen)
                pygame.display.flip()
                s += 1
        all_sprites.draw(screen)
        player_group.draw(screen)
        zhuk_group.draw(screen)
        pygame.display.flip()
        if player_die:
            running = False
            pygame.quit()
            subprocess.call('python lose.py')
    pygame.quit()
