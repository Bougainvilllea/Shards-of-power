import pygame
from sounds import *
from levels import *
all_pl = pygame.sprite.Group()
grounds = pygame.sprite.Group()
walls = pygame.sprite.Group()
roofs = pygame.sprite.Group()
grounds_game_end = pygame.sprite.Group()

all_balls = pygame.sprite.Group()
all_enemies = pygame.sprite.Group()
all_small_fires = pygame.sprite.Group()
all_lightnings = pygame.sprite.Group()
all_fireballs = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_particles = pygame.sprite.Group()
all_buttons = pygame.sprite.Group()
all_shards = pygame.sprite.Group()
all_hearts = pygame.sprite.Group()

hero_clock = pygame.sprite.Group()

fire_1 = pygame.sprite.Group()
fire_2 = pygame.sprite.Group()
fire_3 = pygame.sprite.Group()

player = pygame.sprite.Group()

all_groups = [all_pl, grounds, walls, roofs, grounds_game_end, all_balls, all_enemies, all_small_fires, all_lightnings,
              all_fireballs, all_sprites, all_particles, hero_clock, fire_1, fire_2, fire_3, all_buttons, all_shards,
              all_hearts,
              player]

s_fireballs = []
s_heart_anim = []
s_split_anim = []
s_boos_anim = []
s_boos_anim_attack = []

s_all_buttons = []

for hearts in range(6):
    heart_img = pygame.transform.scale(pygame.image.load('data/heart_anim/' + str(hearts) + '.png'), (50, 60))
    s_heart_anim.append(heart_img)

for splits in range(8):
    split_img = pygame.transform.scale(pygame.image.load('data/split_eff/' + str(splits) + '.png'), (1500, 900))
    s_split_anim.append(split_img)


class Border(pygame.sprite.Sprite):
    def __init__(self, x, y, size_x, size_y, img, border_type):
        super().__init__(all_pl, all_sprites)
        self.x = x
        self.y = y
        self.image = pygame.Surface((size_x, size_y), pygame.SRCALPHA, 32)
        if img != '-':
            self.img_t = pygame.transform.scale(pygame.image.load(img), (size_x, size_y))
            self.image.blit(self.img_t, (0, 0))
        else:
            self.image.fill((0, 0, 0, 0))
        self.rect = pygame.Rect(self.x, self.y, size_x, size_y)
        if border_type == 'g':
            self.add(grounds)
        elif border_type == 'w':
            self.add(walls)
        elif border_type == 'r':
            self.add(roofs)


class Cube:
    def __init__(self, x, y, size_x, size_y):
        super().__init__()
        Border(x, y, 10, size_y, '-', 'w')
        Border(x, y, size_x, 10, '-', 'g')
        Border(x, y + size_y, size_x, 10, '-', 'r')
        Border(x + size_x - 10, y, 10, size_y, '-', 'w')


class Ball(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(all_balls, all_sprites)
        self.v_1 = random.randint(-5, 5)
        self.v_2 = random.randint(-5, 5)
        self.x = x
        self.y = y
        self.image = pygame.Surface((30, 30), pygame.SRCALPHA, 32)
        pygame.draw.circle(self.image, 'red', (15, 15), 15)
        self.rect = pygame.Rect(self.x, self.y, 30, 30)

    def update(self):
        if pygame.sprite.spritecollideany(self, grounds):
            self.v_2 = -self.v_2
        elif pygame.sprite.spritecollideany(self, walls):
            self.v_1 = -self.v_1
        self.rect = self.rect.move(self.v_1, self.v_2)


class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, size_x, size_y, hp, damage_for=1):
        super().__init__(all_enemies, all_sprites)
        self.damage = damage_for
        self.size_x = size_x
        self.size_y = size_y
        self.x = x
        self.y = y
        self.hp = hp
        self.enemy = True

    def update(self):
        global shield_up, shield_move, hero, enemies_defeated
        coll = pygame.sprite.spritecollide(self, all_fireballs, False)
        for _ in coll:
            if self.hp > 0:
                self.hp -= _.damage
                _.destroy()
                enemies_defeated += 1
                hit_sound.play()

        if pygame.sprite.spritecollideany(self, all_lightnings):
            if shield_up:
                self.hp -= 1
            if shield_move:
                self.hp -= 5

        if self.hp <= 0 and type(self) != FinalBoss:
            self.kill()


class Slime(Enemy):
    def __init__(self, x, y, size_x, size_y, hp, damage_for, skin, speed):
        super().__init__(x, y, size_x, size_y, hp, damage_for)
        self.jump = False
        self.dead = False
        self.speed = speed
        self.speed_const = speed
        self.speed_y = -speed
        self.i = 0
        self.skin = pygame.transform.scale(pygame.image.load(skin), (self.size_x, size_y))
        self.skin_2 = pygame.transform.scale(pygame.image.load('data/slime2.png'), (self.size_x, size_y))
        self.skins = [self.skin, self.skin_2]
        self.image = pygame.Surface((size_x, size_y), pygame.SRCALPHA, 32)
        self.image.blit(self.skin, (0, 0))
        self.rect = pygame.Rect(self.x, self.y, self.size_x, self.size_y)

    def animation(self):
        self.i = 0 if self.i == 1 else 1
        self.image.blit(self.skins[self.i], (0, 0))

    def update(self):
        super().update()
        if self.hp <= 0:
            self.dead = True
        if pygame.sprite.spritecollideany(self, grounds):
            self.speed_y = -self.speed_const

        elif pygame.sprite.spritecollideany(self, walls):
            self.speed = -self.speed

        self.speed_y += 0.1
        self.rect = self.rect.move(self.speed, self.speed_y)


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, size_x, size_y, hp, skin, speed_max, boost, jump, x_space, y_space, fireballs_magic,
                 lightnings_magic, time_magic):
        super().__init__(player)
        global screen
        self.fireballs_magic = fireballs_magic
        self.lightnings_magic = lightnings_magic
        self.time_magic = time_magic
        self.grav_cam = 0
        self.camera_move_y = 0
        self.camera_move = 0
        self.speed_y_cam = 0
        self.x_space = x_space
        self.y_space = y_space
        self.x = x
        self.y = y
        self.size_x = size_x
        self.size_y = size_y
        self.hp = hp
        self.skin_r = pygame.transform.scale(pygame.image.load(skin), (size_x, size_y))
        self.skin_l = pygame.transform.flip(self.skin_r, True, False)
        self.skin_now = 'r'
        self.speed_max = speed_max
        self.speed = 0
        self.inert = -5
        self.jump_power_max = -jump
        self.jump_power = -jump
        self.boost = boost
        self.grav = 5
        self.right_collide = False
        self.left_collide = False
        self.ground_collide = False
        self.roofs_collide = False
        self.grabbed_shard = False
        self.dead = False
        self.heart_beat_play = False

        self.i_2 = 0
        self.i = 0

        self.image = pygame.Surface((self.size_x, size_y), pygame.SRCALPHA, 32)
        self.image.blit(self.skin_r, (0, 0))
        self.rect = pygame.Rect(self.x, self.y, self.size_x, self.size_y)

        if self.rect.x >= width / 2 - 100:
            self.hero_move_allowed = False
        else:
            self.hero_move_allowed = True

        if self.rect.y >= int(height / 2) - 150:
            self.hero_move_allowed_y = False
        else:
            self.hero_move_allowed_y = True

        self.fire_1 = SmallFire(self.rect.x - 25, self.rect.y, 35, 60, 'data/small_fire/0.png')
        fire_1.add(self.fire_1)
        self.fire_2 = SmallFire(self.rect.x - 25, self.rect.y, 35, 60, 'data/small_fire/0.png')
        fire_2.add(self.fire_2)
        self.fire_3 = SmallFire(self.rect.x + 25, self.rect.y, 35, 60, 'data/small_fire/0.png')
        fire_3.add(self.fire_3)

        self.shield_1 = Lightning(self.rect.x, self.rect.y, 50, 150, 50, 'data/anim_shield/0.png', 'r')
        self.shield_2 = Lightning(self.rect.x, self.rect.y, 50, 150, 50, 'data/anim_shield/0.png', 'l')

        self.hero_clock = Clock(self.rect.x, self.rect.y, 250, 250)

    def move_right(self):
        if not self.dead:
            self.skin_now = 'r'

            self.right_collide = False
            self.left_collide = False

            for _ in walls:
                if _.rect.colliderect(self.rect.x + 30, self.rect.y, 10, self.size_y - 10):
                    pygame.draw.rect(screen, 'red', [self.rect.x + 30, self.rect.y, 10, self.size_y - 10])
                    self.left_collide = True

            for _ in walls:
                if _.rect.colliderect(self.rect.x + self.size_x - 40, self.rect.y, 10, self.size_y - 10):
                    pygame.draw.rect(screen, 'red', [self.rect.x + self.size_x - 40, self.rect.y, 10, self.size_y - 10])
                    self.right_collide = True

            if not self.right_collide:
                if self.left_collide:
                    self.speed = 0
                if self.speed < self.speed_max:
                    self.speed += self.boost
                if self.hero_move_allowed:
                    self.rect = self.rect.move(self.speed, 0)
            else:
                self.speed = 0

    def move_left(self):
        if not self.dead:
            self.skin_now = 'l'

            self.left_collide = False
            self.right_collide = False

            for _ in walls:
                if _.rect.colliderect(self.rect.x + 30, self.rect.y, 10, self.size_y - 10):
                    pygame.draw.rect(screen, 'red', [self.rect.x + 30, self.rect.y, 10, self.size_y - 10])
                    self.left_collide = True

            for _ in walls:
                if _.rect.colliderect(self.rect.x + self.size_x - 40, self.rect.y, 10, self.size_y - 10):
                    pygame.draw.rect(screen, 'red', [self.rect.x + self.size_x - 40, self.rect.y, 10, self.size_y - 10])
                    self.right_collide = True

            if not self.left_collide:
                if self.right_collide:
                    self.speed = 0
                if self.speed > -self.speed_max:
                    self.speed -= self.boost
                if self.hero_move_allowed:
                    self.rect = self.rect.move(self.speed, 0)
            else:
                self.speed = 0

    def jump(self):
        global non_boost
        global is_jump
        if not self.dead:
            self.ground_collide = False
            self.roofs_collide = False
            for _ in grounds:
                if _.rect.colliderect(self.rect.x + 30, self.rect.y + 130, self.size_x - 60, self.size_y - 130):
                    self.ground_collide = True

            for _ in roofs:
                if _.rect.colliderect(self.rect.x + 30, self.rect.y, self.size_x - 60, self.size_y - 130):
                    self.roofs_collide = True

            if self.ground_collide:
                self.jump_power = self.jump_power_max
                self.inert = -5
                non_boost = False
                is_jump = False

            if self.roofs_collide:
                non_boost = True

            if not non_boost:
                if self.jump_power >= 0:
                    self.jump_power = 0
                else:
                    self.jump_power += 0.5
                if self.hero_move_allowed_y:
                    self.rect = self.rect.move(0, int(self.jump_power))

    def stand(self):
        self.speed = 0

    def gravity(self):
        global is_jump
        self.ground_collide = False
        for _ in grounds:
            if _.rect.colliderect(self.rect.x + 30, self.rect.y + 130, self.size_x - 60, self.size_y - 130):
                self.ground_collide = True

        if not self.ground_collide:
            is_jump = True
            if is_jump and non_boost:
                if self.inert < 5:
                    self.inert += 0.5
                if self.hero_move_allowed_y:
                    self.rect = self.rect.move(0, int(self.inert))
            if self.hero_move_allowed_y:
                self.rect = self.rect.move(0, int(self.grav))
        else:
            self.inert = -5
            is_jump = False

        if self.ground_collide:
            self.jump_power = -self.jump_power_max

    def damaged(self):
        global invulnerability, attenuation, fight
        if self.hp != '-':
            if self.hp > 24:
                corr = 24
            else:
                corr = self.hp
            for _ in range(corr):
                screen.blit(heart_img, (_ * 60 + 40, 30))
            if self.hp == 1:
                if not self.heart_beat_play:
                    self.heart_beat_play = True
                    heart_beat.play(-1)
            else:
                self.heart_beat_play = False
                heart_beat.stop()
            if self.hp <= 0:
                self.dead_hero()
        else:
            heart_beat.stop()

        if pygame.sprite.spritecollideany(self, all_enemies) and not invulnerability:
            hit = random.choice(s_hero_damaged)
            hit.play()
            self.hp -= 1
            invulnerability = True

        attenuation = False
        for _ in all_enemies:
            if _.rect.colliderect(0, 0, width, height):
                attenuation = True

    def dead_hero(self):
        self.dead = True
        global invulnerability
        invulnerability = True

    def animation(self, directory):
        self.i += 1
        if self.i == 6:
            self.i = 0
        self.skin_r = pygame.transform.scale(pygame.image.load('data/' + directory + str(self.i) + '.png'),
                                             (self.size_x, self.size_y))
        self.skin_l = self.skin_l = pygame.transform.flip(self.skin_r, True, False)
        self.image.fill((0, 0, 0, 0))
        if self.skin_now == 'r':
            self.image.blit(self.skin_r, (0, 0))

        elif self.skin_now == 'l':
            self.image.blit(self.skin_l, (0, 0))

    def animation_stand(self):
        self.animation('anim/')

    def animation_run(self):
        self.animation('anim_run/')

    def animation_jump(self):
        self.animation('anim/')

    def fire(self, point_pos_x, point_pos_y):
        if not self.dead:
            if self.fireballs_magic:
                if self.skin_now == 'r':
                    Fireball(self.rect.x + self.size_x, self.rect.y, 70, 70, 40, 'data/fireball_animation/0.png', 15,
                             point_pos_x,
                             point_pos_y)

                elif self.skin_now == 'l':
                    Fireball(self.rect.x, self.rect.y, 70, 70, 40, 'data/fireball_animation/0.png', 15, point_pos_x,
                             point_pos_y)

    def move_small_fireball(self):
        self.fire_1.move(self.rect.x - 5, self.rect.y - 20)
        self.fire_2.move(self.rect.x + self.size_x + 15, self.rect.y - 20)
        self.fire_3.move(self.rect.x + self.size_x // 2 + 6, self.rect.y - 110)

    def animation_small_fireball(self):
        self.fire_1.animation()
        self.fire_2.animation()
        self.fire_3.animation()

    def shield_up(self):
        if not self.dead:
            if self.lightnings_magic:
                self.shield_1.shield(self.rect.x, self.rect.y)
                self.shield_2.shield(self.rect.x, self.rect.y)

    def shield_move_blast(self):
        if self.lightnings_magic:
            self.shield_1.shield_move()
            self.shield_2.shield_move()

    def animation_shield(self):
        if self.lightnings_magic:
            self.shield_1.animation()
            self.shield_2.animation()

    def clock_move(self):
        if self.time_magic:
            self.hero_clock.clock_move(self.rect.x, self.rect.y)

    def clock_animation(self):
        if self.time_magic:
            self.hero_clock.animation()

    def camera_for_x(self):
        if width / 2 - 90 >= self.rect.x >= width / 2 - 110:
            if -level_now.size_x + width < self.camera_move + -self.speed <= 0:
                for j in all_sprites.sprites():
                    j.rect = j.rect.move(-self.speed, 0)
                self.camera_move += -self.speed
                self.hero_move_allowed = False
            else:
                self.hero_move_allowed = True
        else:
            return self.camera_move

        return self.camera_move

    def camera_for_y(self):
        self.speed_y_cam = 0

        if is_jump:
            self.grav_cam = self.grav
        else:
            self.grav_cam = 0

        self.speed_y_cam += -self.grav_cam

        if is_jump and non_boost:
            self.speed_y_cam += -self.inert

        if not non_boost:
            self.speed_y_cam += -self.jump_power
        if int(height / 2) - 110 <= int(self.rect.y) <= int(height / 2) - 90:
            if -(level_now.size_y - height) <= self.camera_move_y + int(self.speed_y_cam) <= 0:
                self.hero_move_allowed_y = False

                self.camera_move_y += int(self.speed_y_cam)

                for j in all_sprites.sprites():
                    j.rect = j.rect.move(0, int(self.speed_y_cam))

            else:
                self.hero_move_allowed_y = True
        return int(self.camera_move_y)

    def camera_start(self):
        self.camera_move_y = -self.y_space
        self.camera_move = -self.x_space
        for j in all_sprites.sprites():
            j.rect = j.rect.move(int(-self.x_space), int(-self.y_space))


class Lightning(pygame.sprite.Sprite):
    def __init__(self, x, y, size_x, size_y, speed, skin, orientation):
        super().__init__(all_lightnings, all_sprites)
        self.x = x
        self.skin = pygame.transform.scale(pygame.image.load(skin), (size_x, size_y))
        self.y = y
        self.size_x = size_x
        self.size_y = size_y
        self.speed_x = speed
        self.speed_y = -speed
        self.orientation = orientation
        self.skin_r = ''
        self.skin_l = ''
        self.skin_now = 'r'
        self.i_3 = 0

        if orientation == 'r':
            self.skin_now = 'r'
            self.skin = pygame.transform.flip(self.skin, True, False)
        else:
            self.skin_now = 'l'

        self.image = pygame.Surface((size_x, size_y), pygame.SRCALPHA, 32)
        self.image.blit(self.skin, (0, 0))
        self.rect = pygame.Rect(self.x, self.y, self.size_x, self.size_y)

    def shield(self, pos_x, pos_y):
        if self.orientation == 'r':
            self.rect.x, self.rect.y = pos_x + 100, pos_y
        else:
            self.rect.x, self.rect.y = pos_x - 50, pos_y

    def shield_move(self):
        if not time_stop:
            if self.orientation == 'r':
                self.rect = self.rect.move(self.speed_x, 0)
            elif self.orientation == 'l':
                self.rect = self.rect.move(-self.speed_x, 0)

    def animation(self):
        self.i_3 += 1
        if self.i_3 == 6:
            self.i_3 = 0
        self.skin_r = pygame.transform.scale(pygame.image.load('data/' + 'anim_shield/' + str(self.i_3) + '.png'),
                                             (self.size_x, self.size_y))

        self.skin_l = pygame.transform.flip(self.skin_r, True, False)
        self.image.fill((0, 0, 0, 0))
        if self.skin_now == 'l':
            self.image.blit(self.skin_r, (0, 0))

        elif self.skin_now == 'r':
            self.image.blit(self.skin_l, (0, 0))


class Fireball(pygame.sprite.Sprite):
    def __init__(self, x, y, size_x, size_y, damage, skin, speed, point_pos_x, point_pos_y):
        super().__init__(all_fireballs, all_sprites)
        self.rebound_cool = False
        self.point_pos_x = point_pos_x
        self.point_pos_y = point_pos_y
        self.x = x
        self.y = y
        self.size_x = size_x
        self.size_y = size_y
        self.damage = damage
        self.skin = pygame.transform.scale(pygame.image.load(skin), (size_x, size_y))
        self.skin_now = ''
        self.skin_r = ''
        self.skin_l = ''
        self.speed_max = speed
        self.speed_x = speed
        self.speed_y = -speed
        self.jumped = 5
        self.des_x, self.des_y = -1, -1
        self.i = 0

        self.speed_x_have = False
        self.pint_have = False

        self.image = pygame.Surface((size_x, size_y), pygame.SRCALPHA, 32)
        self.image.blit(self.skin, (0, 0))
        self.rect = pygame.Rect(self.x, self.y, self.size_x, self.size_y)
        fire_ball_sound = pygame.mixer.Sound(random.choice(fireball_sounds_s))
        if not mute:
            fire_ball_sound.play()

    def update(self):
        if not self.speed_x_have:
            if self.point_pos_x > self.x:
                self.speed_x = (self.point_pos_x - self.x) / 100
                if self.speed_x < 1:
                    self.speed_x = 2
            elif self.point_pos_x < self.x:
                self.speed_x = -(abs((self.point_pos_x - self.x))) / 100
                if self.speed_x > -1:
                    self.speed_x = -2
            self.speed_x_have = True

        if not time_stop:
            if self.jumped != 0:
                if self.speed_x > 0:
                    self.skin_now = 'l'
                else:
                    self.skin_now = 'r'

                if pygame.sprite.spritecollideany(self, grounds):
                    self.speed_y = -self.speed_max
                    self.jumped -= 1
                    for _ in range(20):
                        a_1 = random.randrange(7, 10)
                        Particle(self.rect.x + self.size_x / 2, self.rect.y + self.size_y, a_1, a_1, 4, 10,
                                 ['data/part/2.png', 'data/part/1.png', 'data/part/0.png'], 0.2, 'g')

                elif pygame.sprite.spritecollideany(self, roofs):
                    for _ in range(20):
                        a_2 = random.randrange(7, 10)
                        Particle(self.rect.x + self.size_x / 2, self.rect.y, a_2, a_2, 4, -10,
                                 ['data/part/2.png', 'data/part/1.png', 'data/part/0.png'], 0.2, 'g')
                    self.speed_y = self.speed_max
                    self.jumped -= 1

                elif pygame.sprite.spritecollideany(self, walls):
                    for _ in range(20):
                        a_3 = random.randrange(7, 10)
                        if self.speed_x < 0:
                            Particle(self.rect.x + self.size_x / 2, self.rect.y, a_3, a_3, -4, 10,
                                     ['data/part/2.png', 'data/part/1.png', 'data/part/0.png'],
                                     0.2, 'w')
                        else:
                            Particle(self.rect.x + self.size_x / 2, self.rect.y, a_3, a_3, 4, 10,
                                     ['data/part/2.png', 'data/part/1.png', 'data/part/0.png'],
                                     0.2, 'w')
                    self.speed_x = -self.speed_x
                    self.jumped -= 1

                self.speed_y += self.point_pos_y / 1500
                self.rect = self.rect.move(self.speed_x, self.speed_y)
            else:
                self.destroy()

    def destroy(self):
        for _ in range(40):
            a_4 = random.randrange(7, 10)
            Particle(self.rect.x + self.size_x / 2, self.rect.y, a_4, a_4, 10, -10, ['data/part/2.png',
                                                                                     'data/part/1.png',
                                                                                     'data/part/0.png'], 0.2,
                     'g')
        self.kill()

    def animation(self, directory):
        self.i += 1
        if self.i == 6:
            self.i = 0
        self.skin_r = pygame.transform.scale(pygame.image.load('data/' + directory + str(self.i) + '.png'),
                                             (self.size_x, self.size_y)).convert_alpha()
        self.image.fill((0, 0, 0, 0))
        if self.skin_now == 'r':
            self.image.blit(self.skin_r, (0, 0))

        elif self.skin_now == 'l':
            self.skin_l = pygame.transform.flip(self.skin_r, True, False).convert_alpha()
            self.image.blit(self.skin_l, (0, 0))

    def animation_fly(self):
        self.animation('fireball_animation/')

    def damage_return(self):
        return self.damage


class SmallFire(pygame.sprite.Sprite):
    def __init__(self, x, y, size_x, size_y, skin):
        super().__init__()
        self.skin = pygame.transform.scale(pygame.image.load(skin), (size_x, size_y))
        self.x = x
        self.y = y
        self.i_2 = 0
        self.size_x = size_x
        self.size_y = size_y
        self.skin_now = 'r'

        self.image = pygame.Surface((size_x, size_y), pygame.SRCALPHA, 32)
        self.image.blit(self.skin, (0, 0))
        self.rect = pygame.Rect(self.x, self.y, self.size_x, self.size_y)

    def move(self, x, y):
        self.rect.x = x - 25
        self.rect.y = y + 50

    def animation(self):
        self.i_2 += 1
        if self.i_2 == 6:
            self.i_2 = 0
        self.skin = pygame.transform.scale(pygame.image.load('data/' + 'small_fire/' + str(self.i_2) + '.png'),
                                           (self.size_x, self.size_y)).convert_alpha()
        self.image.fill((0, 0, 0, 0))
        self.image.blit(self.skin, (0, 0))


class Particle(pygame.sprite.Sprite):
    def __init__(self, x, y, size_x, size_y, speed_x, speed_y, skin, boost, orientation='g', chance=6):
        super().__init__(all_particles, all_sprites)
        self.orientation = orientation
        self.chance = chance
        self.x = x
        self.y = y
        self.size_x = size_x
        self.size_y = size_y
        if orientation == 'g':
            self.speed_x = random.randrange(-speed_x, speed_x)
        else:
            if speed_x > 0:
                self.speed_x = random.randrange(1, speed_x)
            else:
                self.speed_x = -(random.randrange(1, -speed_x))

        if speed_y > 0:
            self.speed_y = random.randrange(1, speed_y)
        else:
            self.speed_y = -(random.randrange(1, -speed_y))

        self.skin = pygame.transform.scale(pygame.image.load(random.choice(skin)), (size_x, size_y)).convert_alpha()
        self.boost = (-boost if self.speed_y > 0 else boost)

        self.image = pygame.Surface((size_x, size_y), pygame.SRCALPHA, 32)
        self.image.blit(self.skin, (0, 0))
        self.rect = pygame.Rect(self.x, self.y, self.size_x, self.size_y)

    def update(self):
        if self.speed_y <= 0 and self.boost < 0:
            self.kill()
        self.speed_y += self.boost
        self.rect = self.rect.move(self.speed_x, self.speed_y)

        if pygame.sprite.spritecollideany(self, grounds_game_end):
            self.kill()
        if pygame.sprite.spritecollideany(self, grounds):
            if random.randrange(0, self.chance) == 0:
                self.kill()


class Clock(pygame.sprite.Sprite):
    def __init__(self, x, y, size_x, size_y):
        super().__init__(hero_clock)
        self.x = x
        self.y = y
        self.size_x = size_x
        self.size_y = size_y
        self.i_2 = 12
        self.i_3 = 12
        self.orientation = 'r'
        self.y_boost = 90
        self.inert = 1
        self.angle = 1

        self.image = pygame.Surface((size_x, size_y), pygame.SRCALPHA, 32)
        self.image.fill((0, 0, 0, 0))
        self.rect = pygame.Rect(self.x, self.y, self.size_x, self.size_y)

        self.skin = pygame.transform.scale(pygame.image.load('data/clock_animation/' + str(self.i_2) + '.png'),
                                           (self.size_x, self.size_y)).convert_alpha()

        self.skin_2 = pygame.transform.scale(pygame.image.load('data/clock_animation11/' + str(self.i_2) + '.png'),
                                             (self.size_x, self.size_y)).convert_alpha()

        self.skin_3 = pygame.transform.scale(pygame.image.load('data/clock_animation_obl/' + str(self.i_2) + '.png'),
                                             (self.size_x, self.size_y)).convert_alpha()
        self.skin_4 = pygame.Surface((self.size_x, self.size_y), pygame.SRCALPHA, 32)

    def clock_move(self, x, y):
        self.rect.x, self.rect.y = x - 76, y - 100

        self.image.fill((0, 0, 0, 0))
        self.image.blit(self.skin_2, (0, 0))
        self.image.blit(self.skin, (0, 0))
        self.image.blit(self.skin_4, (0, 0))
        self.image.blit(self.skin_3, (0, 0))

    def animation(self):
        if time_stop:
            self.i_2 = -1

        if self.i_2 != 12:
            self.i_2 += 1
            if not time_stop:
                tik.play()
                if self.i_2 == 12:
                    for _ in range(25):
                        a_0 = random.randrange(7, 25)
                        Particle(hero.hero_clock.rect.x + hero.hero_clock.size_x / 2,
                                 hero.hero_clock.rect.y + hero.hero_clock.size_y / 2,
                                 a_0, a_0, 6, -10, ['data/part/time_part_1.png', 'data/part/time_part.png'], 0.2, 'g',
                                 2)
                    ult_ready.play()
                    self.skin_4 = pygame.transform.scale(
                        pygame.image.load('data/clock_animation_ult/' + str(0) + '.png'),
                        (self.size_x, self.size_y)).convert_alpha()

            else:
                self.skin_4 = pygame.Surface((self.size_x, self.size_y), pygame.SRCALPHA, 32)

        self.skin = pygame.transform.scale(pygame.image.load('data/clock_animation/' + str(self.i_2) + '.png'),
                                           (self.size_x, self.size_y)).convert_alpha()
        self.skin_2 = pygame.transform.scale(pygame.image.load('data/clock_animation11/' + str(self.i_2) + '.png'),
                                             (self.size_x, self.size_y)).convert_alpha()
        self.skin_3 = pygame.transform.scale(pygame.image.load('data/clock_animation_obl/' + str(self.i_2) + '.png'),
                                             (self.size_x, self.size_y)).convert_alpha()


class BulletShooter(Enemy):
    def __init__(self, x, y, size_x, size_y, hp, skin, orientation, speed, rate=1):
        super().__init__(x, y, size_x, size_y, hp)
        self.timer_anim = 0
        self.st_anim = pygame.time.get_ticks()
        self.speed_x = 0
        self.speed_y = 0
        self.speed = speed
        self.rate = rate
        self.timer = 0
        self.orientation = orientation
        self.st = pygame.time.get_ticks()
        self.dir = skin
        self.skin = pygame.transform.scale(pygame.image.load(self.dir + '0.png'), (self.size_x, self.size_y))

        if self.orientation == 'roof':
            self.speed_y = self.speed
        elif self.orientation == 'ground':
            self.speed_y = -self.speed

        elif self.orientation == 'right':
            self.size_x, self.size_y = self.size_y, self.size_x
            self.speed_x = -self.speed

        elif self.orientation == 'left':
            self.size_x, self.size_y = self.size_y, self.size_x
            self.speed_x = self.speed

        self.image = pygame.Surface((self.size_x, self.size_y), pygame.SRCALPHA, 32)
        self.image.blit(self.skin, (0, 0))
        self.rect = pygame.Rect(self.x, self.y, self.size_x, self.size_y)

    def update(self):
        super().update()
        self.timer_anim = (pygame.time.get_ticks() - self.st_anim) / 100
        self.timer = (pygame.time.get_ticks() - self.st) / 1000

        if self.timer_anim > 5:
            self.timer_anim = 0
            self.st_anim = pygame.time.get_ticks()
            self.animation()
        if self.timer > self.rate:
            self.timer = 0
            self.st = pygame.time.get_ticks()
            Bullet(self.rect.x + self.size_x / 4, self.rect.y + self.size_y / 2, 50, 50, 1, 1,
                   'data/part/bullet.png', self.speed_x, self.speed_y)

    def animation(self):
        global i
        if self.orientation == 'roof':
            self.skin = pygame.transform.flip(
                pygame.transform.scale(pygame.image.load(self.dir + str(i) + '.png'), (self.size_x, self.size_y)),
                False, True)

        elif self.orientation == 'ground':
            self.skin = pygame.transform.scale(pygame.image.load(self.dir + str(i) + '.png'),
                                               (self.size_x, self.size_y))
        elif self.orientation == 'right':
            self.skin = pygame.transform.scale(
                pygame.transform.rotate(pygame.image.load(self.dir + str(i) + '.png'), 90), (self.size_x, self.size_y))

        elif self.orientation == 'left':
            self.skin = pygame.transform.scale(
                pygame.transform.rotate(pygame.image.load(self.dir + str(i) + '.png'), 270), (self.size_x, self.size_y))

        self.image.fill((0, 0, 0, 0))
        self.image.blit(self.skin.convert_alpha(), (0, 0))


class Walker(Enemy):
    def __init__(self, x, y, size_x, size_y, hp, skin, speed_y, speed_x):
        super().__init__(x, y, size_x, size_y, hp)

        self.timer_anim = 0
        self.st_anim = pygame.time.get_ticks()

        self.speed = speed_x
        self.grav = speed_y
        self.dir = skin
        self.skin = pygame.transform.scale(pygame.image.load(self.dir + '0.png'), (size_x, size_y))

        self.image = pygame.Surface((self.size_x, self.size_y), pygame.SRCALPHA, 32)
        self.image.blit(self.skin, (0, 0))
        self.rect = pygame.Rect(self.x, self.y, self.size_x, self.size_y)

    def update(self):
        super().update()
        self.timer_anim = (pygame.time.get_ticks() - self.st_anim) / 100

        if self.timer_anim > 5:
            self.timer_anim = 0
            self.st_anim = pygame.time.get_ticks()
            self.animation()

        if pygame.sprite.spritecollideany(self, walls):
            self.speed = -self.speed

        if not pygame.sprite.spritecollideany(self, grounds):
            self.rect = self.rect.move(0, self.grav)

        self.rect = self.rect.move(self.speed, 0)

    def animation(self):
        global i
        self.image.fill((0, 0, 0, 0))
        if self.speed > 0:
            self.skin = pygame.transform.flip(pygame.transform.scale(pygame.image.load(self.dir + str(i) + '.png'),
                                                                     (self.size_x, self.size_y)), True, False)
        else:
            self.skin = pygame.transform.scale(pygame.image.load(self.dir + str(i) + '.png'),
                                               (self.size_x, self.size_y))

        self.image.blit(self.skin.convert_alpha(), (0, 0))


class Push(Enemy):
    def __init__(self, x, y, size_x, size_y, hp, skin, speed):
        super().__init__(x, y, size_x, size_y, hp)
        self.speed_max = speed
        self.speed_saver = speed
        self.speed_x = speed
        self.dir = skin
        self.vision = 500
        self.rate = 2
        self.timer = 0
        self.st = pygame.time.get_ticks()
        self.timer_anim = 0
        self.st_anim = pygame.time.get_ticks()

        self.skin = pygame.transform.scale(pygame.image.load(self.dir + str(i) + '.png'), (size_x, size_y))

        self.image = pygame.Surface((self.size_x, self.size_y), pygame.SRCALPHA, 32)
        self.image.blit(self.skin, (0, 0))
        self.rect = pygame.Rect(self.x, self.y, self.size_x, self.size_y)

    def update(self):
        super().update()
        self.timer_anim = (pygame.time.get_ticks() - self.st_anim) / 100

        if self.timer_anim > 5:
            self.timer_anim = 0
            self.st_anim = pygame.time.get_ticks()
            self.animation()

        if pygame.sprite.spritecollideany(self, walls):
            self.speed_x = -self.speed_x
            self.speed_saver = self.speed_x
            self.skin = pygame.transform.flip(self.skin, False, True)
            self.vision = -self.vision

        for _ in player:
            if _.rect.colliderect(self.rect.x, self.rect.y, self.vision, self.size_y):
                if self.speed_x != 0:
                    self.speed_saver = self.speed_x
                self.speed_x = 0

                self.timer = (pygame.time.get_ticks() - self.st) / 1000

                if self.timer > self.rate:
                    self.timer = 0
                    self.st = pygame.time.get_ticks()
                    Bullet(self.rect.x + self.size_x / 4, self.rect.y + self.size_y / 2 - 50, 50, 50, 1, 1,
                           'data/part/bullet.png',
                           self.speed_saver, 0)
                    Bullet(self.rect.x + self.size_x / 4, self.rect.y + self.size_y / 2 - 50, 50, 50, 1, 1,
                           'data/part/bullet.png',
                           self.speed_saver, 1)
                    Bullet(self.rect.x + self.size_x / 4, self.rect.y + self.size_y / 2 - 50, 50, 50, 1, 1,
                           'data/part/bullet.png',
                           self.speed_saver, -1)
            else:
                if self.speed_saver == 0:
                    self.speed_saver = self.speed_max
                    self.vision = -self.vision
                self.speed_x = self.speed_saver

        if not pygame.sprite.spritecollideany(self, grounds):
            self.rect = self.rect.move(0, 5)

        for _ in range(abs(self.speed_x)):
            if pygame.sprite.spritecollideany(self, walls):
                self.speed_x = -self.speed_x
                self.speed_saver = self.speed_x
                self.skin = pygame.transform.flip(self.skin, False, True)
                self.vision = -self.vision
                self.rect = self.rect.move(self.speed_x // abs(self.speed_x), 0)
                break
            else:
                self.rect = self.rect.move(self.speed_x // abs(self.speed_x), 0)

    def animation(self):
        global i
        self.image.fill((0, 0, 0, 0))
        self.skin = pygame.transform.scale(pygame.image.load(self.dir + str(i) + '.png'), (self.size_x, self.size_y))
        self.image.blit(self.skin.convert_alpha(), (0, 0))


class LaserShooter(Enemy):
    def __init__(self, x, y, size_x, size_y, hp, skin, orientation):
        super().__init__(x, y, size_x, size_y, hp)
        self.orientation = orientation
        self.timer = 0
        self.st = pygame.time.get_ticks()
        self.play_charge = False

        self.timer_anim = 0
        self.st_anim = pygame.time.get_ticks()

        if self.orientation == 'r':
            self.vision = 700
        else:
            self.vision = -700

        self.dir = skin
        self.skin = pygame.transform.scale(pygame.image.load(self.dir + str(i) + '.png'), (size_x, size_y))

        self.image = pygame.Surface((self.size_x, self.size_y), pygame.SRCALPHA, 32)
        self.image.blit(self.skin, (0, 0))
        self.rect = pygame.Rect(self.x, self.y, self.size_x, self.size_y)

    def update(self):
        super().update()
        self.timer_anim = (pygame.time.get_ticks() - self.st_anim) / 100
        if self.timer_anim > 5:
            self.timer_anim = 0
            self.st_anim = pygame.time.get_ticks()
            self.animation()

        for _ in player:
            if _.rect.colliderect(self.rect.x, self.rect.y, self.vision, self.size_y):
                self.timer = (pygame.time.get_ticks() - self.st) / 1000
                if self.timer > 1:
                    shoot_laser.play()
                    self.timer = 0
                    self.st = pygame.time.get_ticks()
                    if self.orientation == 'r':
                        Laser(self.rect.x + self.size_x, self.rect.y, 10000, 50, 1000, 1, 'data/part/laser.png', 1)

                    else:
                        Laser(self.rect.x - 10000, self.rect.y, 10000, 50, 1000, 1, 'data/part/laser.png', 1)

                if not self.play_charge:
                    self.play_charge = True
                    charge_laser.play()

            else:
                self.play_charge = False
                self.timer = 0
                self.st = pygame.time.get_ticks()
        if not pygame.sprite.spritecollideany(self, grounds):
            self.rect = self.rect.move(0, 5)

    def animation(self):
        global i
        self.image.fill((0, 0, 0, 0))
        if self.orientation == 'r':
            self.skin = pygame.transform.scale(pygame.image.load(self.dir + str(i) + '.png'),
                                               (self.size_x, self.size_y))
        else:
            self.skin = pygame.transform.flip(pygame.transform.scale(pygame.image.load(self.dir + str(i) + '.png'),
                                                                     (self.size_x, self.size_y)), True, False)
        self.image.blit(self.skin.convert_alpha(), (0, 0))


class Bullet(Enemy):
    def __init__(self, x, y, size_x, size_y, hp, damage_for, skin, speed_x, speed_y):
        super().__init__(x, y, size_x, size_y, hp, damage_for)
        self.speed_x = speed_x
        self.speed_y = speed_y
        self.skin = pygame.transform.scale(pygame.image.load(skin), (size_x, size_y))

        self.image = pygame.Surface((size_x, size_y), pygame.SRCALPHA, 32)
        self.image.blit(self.skin, (0, 0))
        self.rect = pygame.Rect(self.x, self.y, self.size_x, self.size_y)

    def update(self):
        super().update()
        if pygame.sprite.spritecollideany(self, all_pl):
            self.kill()
        self.rect = self.rect.move(self.speed_x, self.speed_y)


class Laser(Enemy):
    def __init__(self, x, y, size_x, size_y, hp, damage_for, skin, timer_laser):
        super().__init__(x, y, size_x, size_y, hp, damage_for)
        self.skin = pygame.transform.scale(pygame.image.load(skin), (abs(size_x), abs(size_y)))
        self.timer = timer_laser
        self.timer_past = 0
        self.st = pygame.time.get_ticks()

        self.image = pygame.Surface((size_x, size_y), pygame.SRCALPHA, 32)
        self.image.blit(self.skin, (0, 0))
        self.rect = pygame.Rect(self.x, self.y, self.size_x, self.size_y)

    def update(self):
        super().update()
        self.timer_past = (pygame.time.get_ticks() - self.st) / 1000

        if self.timer_past > self.timer:
            self.kill()


class Heart(pygame.sprite.Sprite):
    def __init__(self, x, y, size_x, size_y, skin):
        super().__init__(all_hearts, all_sprites)
        self.skin = pygame.transform.scale(pygame.image.load(skin), (abs(size_x), abs(size_y)))
        self.x, self.y, = x, y
        self.size_x, self.size_y = size_x, size_y

        self.image = pygame.Surface((size_x, size_y), pygame.SRCALPHA, 32)
        self.image.blit(self.skin, (0, 0))
        self.rect = pygame.Rect(self.x, self.y, self.size_x, self.size_y)

    def update(self):
        if pygame.sprite.spritecollideany(self, player):
            if hero.hp < 5:
                hero.hp += 1
                self.kill()
                heart_up.play()


class Level(pygame.sprite.Sprite):
    def __init__(self, fon, fon_coll, size_x, size_y, hero_x, hero_y, space_x, space_y, enemies, cubes, level_name,
                 fireballs_m,
                 lightnings_m, time_m, shard, music):
        super().__init__()
        self.music = music
        self.level_name = level_name
        self.fon = fon
        if fon_coll != '-':
            self.fon_coll = pygame.transform.scale(pygame.image.load(fon_coll), (size_x, size_y + 10))
        else:
            self.fon_coll = '-'
        self.space_x = space_x
        self.space_y = space_y
        self.size_x = size_x
        self.size_y = size_y
        self.hero_x = hero_x
        self.hero_y = hero_y
        self.fireballs_m = fireballs_m
        self.lightnings_m = lightnings_m
        self.time_m = time_m

        for shard_i in shard:
            Shard(*shard_i)
        for en in enemies:
            enemies_dict[en[0]](*en[1:])
        for cube in cubes:
            Cube(*cube)
        Border(0, 0, size_x, 20, '-', 'r')
        Border(0, size_y - 20, size_x, 20, '-', 'g')
        grounds_game_end.add(Border(-100000, -20, 200000, 20, '-', 'g'))
        grounds_game_end.add(Border(-100000, size_y + 20, 200000, 20, '-', 'g'))
        Border(0, 0, 20, size_y, '-', 'w')
        Border(size_x - 20, 0, 20, size_y, '-', 'w')


class Button(pygame.sprite.Sprite):
    def __init__(self, x, y, size_x, size_y, skin, mess):
        super().__init__(all_buttons)
        self.mess = mess
        self.x = x
        self.y = y
        self.skin = pygame.transform.scale(pygame.image.load(skin), (size_x, size_y))
        self.size_x = size_x
        self.size_y = size_y

        self.image = pygame.Surface((size_x, size_y), pygame.SRCALPHA, 32)
        self.image.blit(self.skin, (0, 0))
        self.rect = pygame.Rect(self.x, self.y, self.size_x, self.size_y)

    def update(self, pos_x, pos_y):
        if self.rect.collidepoint(pos_x, pos_y):
            return True
        return False


class Shard(pygame.sprite.Sprite):
    def __init__(self, x, y, size_x, size_y, skin, level_shard):
        super().__init__(all_shards, all_sprites)
        self.x = x
        self.y = y
        self.size_x = size_x
        self.size_y = size_y
        self.dir = skin
        self.skin = pygame.transform.scale(pygame.image.load(self.dir + str(i) + '.png'), (size_x, size_y))
        self.level_shard = level_shard
        self.grab_shard = False

        self.image = pygame.Surface((size_x, size_y), pygame.SRCALPHA, 32)
        self.image.blit(self.skin, (0, 0))
        self.rect = pygame.Rect(self.x, self.y, self.size_x, self.size_y)

        self.timer_anim = 0
        self.st_anim = pygame.time.get_ticks()

    def update(self, shard_grabbed):
        self.timer_anim = (pygame.time.get_ticks() - self.st_anim) / 100
        if self.timer_anim > 1:
            self.timer_anim = 0
            self.st_anim = pygame.time.get_ticks()
            self.animation()

        if pygame.sprite.spritecollideany(all_shards.sprites()[0], player):
            self.grab_shard = True
        else:
            self.grab_shard = False
        if self.grab_shard:
            screen.blit(pygame.image.load('data/buttons/e.png'), (self.rect.x - 20, self.rect.y - 100))
        if shard_grabbed:
            level_load(levels_di[self.level_shard], True)
            pygame.mixer.music.pause()
            self.kill()

    def animation(self):
        global i
        self.image.fill((0, 0, 0, 0))
        self.skin = pygame.transform.scale(pygame.image.load(self.dir + str(i) + '.png'), (self.size_x, self.size_y))
        self.image.blit(self.skin.convert_alpha(), (0, 0))


class FinalBoss(Enemy):
    def __init__(self, x, y, size_x, size_y, hp, skin):
        super().__init__(x, y, size_x, size_y, hp)
        self.skin = pygame.transform.scale(pygame.image.load(skin), (size_x, size_y))
        for boss in range(6):
            s_boos_anim.append(pygame.transform.scale(pygame.image.load('data/boss_anim/' + str(boss) + '.png'),
                                                      (self.size_x, self.size_y)))
            s_boos_anim_attack.append(
                pygame.transform.scale(pygame.image.load('data/boss_attack_anim/' + str(boss) + '.png'),
                                       (self.size_x, self.size_y)))

        self.bullet_speed_x = 7
        self.bullet_speed_y = 1
        self.timer_diagonal = 0
        self.st_diagonal = pygame.time.get_ticks()

        self.timer_pre_laser = 0
        self.st_pre_laser = pygame.time.get_ticks()
        self.laser_pos_apply = False
        self.laser_sound = False
        self.laser_pos = 0

        self.attack_s = ['bullet_diagonal', 'laser_on_pl', 'laser_on_pl', 'laser_on_pl', 'spam_mouse',
                         'bullet_for_hero']
        self.attacking = False
        self.attack_type = random.choice(self.attack_s)
        self.attack_timer = 0
        self.attack_st = pygame.time.get_ticks()
        self.ticks_get_attack = False

        self.image = pygame.Surface((self.size_x, self.size_y), pygame.SRCALPHA, 32)
        self.image.blit(self.skin, (0, 0))
        self.rect = pygame.Rect(self.x, self.y, self.size_x, self.size_y)

        self.barrier_timer = 0
        self.barrier_off = False
        self.rest = False
        self.rest_play = False
        self.barrier_st = pygame.time.get_ticks()
        self.barrier = Laser(self.rect.x - 100, self.rect.y - 500, 100, 1300, 2000, 1, 'data/part/boss_bar.png', 1000)

        self.hero_time_heal = 0
        self.st_heal = pygame.time.get_ticks()

        self.heal = 0
        self.st_heal_st = pygame.time.get_ticks()

    def update(self):
        super().update()
        if hero.rect.colliderect(self.rect.x - 1320, self.rect.y - 1000, 2000, 2000):
            if self.hp <= 0:
                rest_sound.stop()
                if self.barrier != '-':
                    self.barrier.kill()
                boss_dead.play()
                Shard(self.rect.x + self.size_x // 2, self.rect.y + self.size_y, 60, 60, 'data/white_shards_anim/',
                      'level_6')
                self.kill()
            self.animation()
            self.heal = (pygame.time.get_ticks() - self.st_heal_st) / 100

            if hero.hp < 5 and not hero.dead:
                self.hero_time_heal = (pygame.time.get_ticks() - self.st_heal) / 1000
                if self.hero_time_heal > 20:
                    Heart(hero.rect.x, hero.rect.y, 1, 1, 'data/heart_anim/0.png')
                    self.hero_time_heal = 0
                    self.st_heal = pygame.time.get_ticks()

            if hero.hp < 5 and not hero.dead:
                if self.heal > 4:
                    b = random.randrange(20, 25)
                    Particle(random.randrange(hero.rect.x, hero.rect.x + hero.size_x), hero.rect.y + 50, b, b, -2, -4,
                             ['data/part/h1.png', 'data/part/h0.png', 'data/part/h2.png'],
                             0,
                             'w', 50)
                    Particle(random.randrange(hero.rect.x, hero.rect.x + hero.size_x), hero.rect.y + 50, b, b, -2, -4,
                             ['data/part/h1.png', 'data/part/h0.png', 'data/part/h2.png'],
                             0,
                             'w', 50)
                    self.heal = 0
                    self.st_heal_st = pygame.time.get_ticks()

            if not self.barrier_off:
                self.barrier_timer = (pygame.time.get_ticks() - self.barrier_st) / 100
                if self.barrier_timer > 150:
                    self.barrier_off = True
                    self.rest = True
                    self.attacking = False
                    self.barrier.kill()
                    self.barrier = '-'
                    self.barrier_timer = 0
                    self.barrier_st = pygame.time.get_ticks()

            if self.barrier_off:
                self.barrier_timer = (pygame.time.get_ticks() - self.barrier_st) / 100
                if self.barrier_timer > 50:
                    self.barrier_off = False
                    self.rest = False
                    self.barrier_timer = 0
                    self.barrier_st = pygame.time.get_ticks()
                    if self.barrier == '-':
                        self.barrier = Laser(self.rect.x - 100, self.rect.y - 500, 100, 1300, 2000, 1,
                                             'data/part/boss_bar.png', 1000)

            if not self.rest:
                rest_sound.stop()
                self.rest_play = False
                if not self.attacking:
                    self.attack_timer = (pygame.time.get_ticks() - self.attack_st) / 100
                    if not self.ticks_get_attack:
                        self.attack_st = pygame.time.get_ticks()
                        self.ticks_get_attack = True

                if self.attack_timer > 5:
                    random.choice(s_boss_cast).play()
                    self.attack_type = random.choice(self.attack_s)
                    self.attack_timer = 0
                    self.ticks_get_attack = False
                    self.attacking = True

                if self.attack_type == 'bullet_diagonal' and self.attacking:
                    if self.bullet_diagonal() == 'end':
                        self.attacking = False

                if self.attack_type == 'laser_on_pl' and self.attacking:
                    if self.laser_on_pl() == 'end':
                        self.attacking = False

                if self.attack_type == 'spam_mouse' and self.attacking:
                    if self.spam_mouse() == 'end':
                        self.attacking = False

                if self.attack_type == 'bullet_for_hero' and self.attacking:
                    if self.bullet_for_hero() == 'end':
                        self.attacking = False
            else:
                if not self.rest_play:
                    self.rest_play = True
                    rest_sound.play(-1)

    def bullet_diagonal(self):
        if self.bullet_speed_y < 10:
            self.timer_diagonal = (pygame.time.get_ticks() - self.st_diagonal) / 100

            if self.timer_diagonal > 3:
                self.bullet_speed_y += 1
                self.timer_diagonal = 0
                self.st_diagonal = pygame.time.get_ticks()

                Bullet(self.rect.x, self.rect.y, 50, 50, 1, 1,
                       'data/part/bullet.png',
                       -self.bullet_speed_x, self.bullet_speed_y)

                Bullet(self.rect.x, self.rect.y + self.size_y - 50, 50, 50, 1, 1,
                       'data/part/bullet.png',
                       -self.bullet_speed_x, -self.bullet_speed_y)
            return 'process'
        else:
            self.bullet_speed_y = 1
            return 'end'

    def bullet_for_hero(self):
        Bullet(self.rect.x, hero.rect.y - 50, 50, 50, 1, 1,
               'data/part/bullet.png',
               -5, 2)
        Bullet(self.rect.x, hero.rect.y, 50, 50, 1, 1,
               'data/part/bullet.png',
               -5, 0)
        Bullet(self.rect.x, hero.rect.y + 50, 50, 50, 1, 1,
               'data/part/bullet.png',
               -5, -2)
        return 'end'

    def laser_on_pl(self):
        if self.st_pre_laser == '-':
            self.st_pre_laser = pygame.time.get_ticks()

        self.timer_pre_laser = (pygame.time.get_ticks() - self.st_pre_laser) / 100

        if not self.laser_pos_apply:
            self.laser_pos_apply = True
            self.laser_pos = random.choice([0, self.size_y / 2, self.size_y])

        if self.timer_pre_laser > 20:
            shoot_laser.play()
            self.laser_sound = False
            self.st_pre_laser = '-'
            self.timer_pre_laser = 0
            self.laser_pos_apply = False
            Laser(self.rect.x - 1350, self.rect.y + self.laser_pos, 1350, 50, 1000, 1, 'data/part/laser.png', 1)
            return 'end'
        else:
            if not self.laser_sound:
                self.laser_sound = True
                charge_laser.play()
            pygame.draw.rect(screen, 'red', [self.rect.x - 1350, self.rect.y + self.laser_pos, 1350, 10])
            return 'process'

    def spam_mouse(self):
        Walker(self.rect.x, self.rect.y - self.size_y / 2, 100, 150, 30, 'data/anim_walker_gr/', 7, -2)
        return 'end'

    def animation(self):
        global i
        self.image.fill((0, 0, 0, 0))
        self.skin = s_boos_anim_attack[i] if self.attacking else s_boos_anim[i]
        self.image.blit(self.skin.convert_alpha(), (0, 0))


enemies_dict = {'slime': Slime, 'bullet_shooter': BulletShooter, 'walker': Walker, 'push': Push, 'laser': Laser,
                'laser_shooter': LaserShooter, 'heart': Heart, 'final_boss': FinalBoss}


def za_world():
    global time_stop
    if not hero.dead:
        if hero.time_magic:
            if not time_stop:
                time_stop = True
                time_stop_sound.play()


if __name__ == '__main__':
    pygame.init()
    size = width, height = 1500, 900
    pygame.display.set_caption('Shards of power')

    screen = pygame.display.set_mode(size, pygame.SCALED)
    inv = pygame.Surface(screen.get_rect().size, pygame.SRCALPHA, 32)
    white = pygame.Surface(screen.get_rect().size, pygame.SRCALPHA, 32)
    white.fill((255, 255, 255, 255))
    black = pygame.Surface(screen.get_rect().size, pygame.SRCALPHA, 32)
    black.fill((0, 0, 0, 230))
    pre_dead = pygame.transform.scale(pygame.image.load('data/part/pre_dead.png'), (width, height)).convert_alpha()
    fon_world = ''
    fon_world_coll = ''
    hero = ''

    time_load_level = 0
    load_sound = False
    level_to_load = ''

    fps = 60
    time_invulnerability = 0
    time_fire_ammo = 0
    time_shield_move = 0
    time_stop_timer = 0
    colour_time = 0
    point_fire = (0, 0)
    i = 0
    i_2 = 0
    i_main = 0
    i_main_2 = 0
    time_clock = 16
    fire_ammo = 3
    hero_animation = 'stand'
    light = '-'
    move_fon = 0
    t = 0
    enemies_defeated = 0

    s_menu_fon = []
    s_world_fon = []

    time_stop = False
    invulnerability = False
    running = True
    is_jump = True
    non_boost = True
    fire = False
    shield_up = False
    shield_move = False
    sound_play_lightning = False
    step_sound = False
    time_stop_allowed = True
    shard_fire = True
    shard_lightnings = True
    shard_time = True
    grab_shard = False
    menu_is_load = False
    mini_window = False
    fon_revers_anim = False
    pre_music = True
    attenuation = False
    fight = False
    dead_buttons = False
    load_light = False

    progress_save = open('data/saves/progress_save.txt', 'r+', encoding='UTF-8')
    progress_load = levels_di[progress_save.readlines()[-1]]

    mute_file = open('data/saves/sounds.txt', 'r+', encoding='UTF-8')
    mute = [True if mute_file.readlines()[-1] == 'mute' else False][0]

    pygame.mixer.music.load(menu[-1])
    if mute:
        for _ in s_sounds:
            _.set_volume(0)
        pygame.mixer.music.set_volume(0)
    else:
        pygame.mixer.music.set_volume(0.2)

    pygame.mixer.music.play(-1)

    level_now = Level(*levels_di['menu'])
    level_now_s = menu


    def menu_load(level):
        global level_now, fon_world, fon_world_coll, hero, load_sound, time_load_level, level_to_load,\
            menu_is_load, pre_music, grab_shard, fight, attenuation, fon_revers_anim
        fon_revers_anim = False
        fight = False
        attenuation = False
        grab_shard = False
        menu_is_load = True
        screen.fill('black')
        screen.blit(pygame.transform.scale(pygame.image.load('data/part/sts.png'), (width, height)).convert_alpha(),
                    (0, 0))
        pygame.display.flip()
        for i_i in range(1, 50):
            s_menu_fon.append(
                pygame.transform.scale(pygame.image.load('data/menu_fon/' + '0 (' + str(i_i) + ')' + '.jpg'),
                                       (width, height)).convert_alpha())
        for groups in all_groups:
            for item in groups:
                item.kill()

        s_all_buttons.clear()

        level_now = Level(*level)
        fon_world = pygame.image.load('data/menu_fon/0 (1).jpg')
        if level_now.fon_coll != '-':
            fon_world_coll = level_now.fon_coll.convert_alpha()
        else:
            fon_world_coll = '-'
        hero = Player(level_now.hero_x, level_now.hero_y, 0, 0, '-', 'data/anim/0.png', 0, 0, 0, level_now.space_x,
                      level_now.space_y, False, False, False)

        step_sound_rock.set_volume(0)
        if not pre_music and not mute:
            pygame.mixer.music.load(level_now.music)
            pygame.mixer.music.set_volume(0.2)
            pygame.mixer.music.play(-1)

        hero.camera_start()

        for li in all_lightnings:
            li.kill()

        s_all_buttons.append(Button(660, 750, 200, 100, 'data/buttons/quit.png', 'quit_button'))
        s_all_buttons.append(Button(660, 500, 200, 100, 'data//buttons/play.png', 'continue'))
        s_all_buttons.append(Button(610, 620, 300, 100, 'data//buttons/new game.png', 'new_game'))
        s_all_buttons.append(
            Button(50, 770, 100, 100, 'data/buttons/muted.png' if mute else 'data/buttons/mute.png', 'mute'))
        s_all_buttons.append(Button(535, 350, 450, 150, 'data/buttons/prev.png', '-'))


    def level_load(level, sound_eff=True):
        global level_now, fon_world, fon_world_coll, hero, load_sound, time_load_level, level_to_load,\
            menu_is_load, pre_music, grab_shard, fight, attenuation, level_now_s, fon_revers_anim

        fon_revers_anim = False
        pre_music = False
        menu_is_load = False
        fight = False
        attenuation = False

        if not sound_eff:
            grab_shard = False
            for groups in all_groups:
                for item in groups:
                    item.kill()

            s_all_buttons.clear()
            level_now_s = level[:]
            level_now = Level(*level)

            progress_save.write('\n' + level_now.level_name)

            if level_now.fon_coll != '-':
                fon_world_coll = level_now.fon_coll.convert_alpha()
            else:
                fon_world_coll = '-'

            screen.fill('black')
            screen.blit(pygame.transform.scale(pygame.image.load('data/part/sts.png'), (width, height)).convert_alpha(),
                        (0, 0))
            pygame.display.flip()
            s_menu_fon.clear()
            s_world_fon.clear()
            for i_i in range(0, 12):
                s_world_fon.append(
                    pygame.transform.scale(pygame.image.load(level_now.fon + str(i_i) + '.png'),
                                           (level_now.size_x, level_now.size_y)).convert_alpha())

            hero = Player(level_now.hero_x, level_now.hero_y, 100, 150, 5, 'data/anim/0.png', 6, 1, 23,
                          level_now.space_x,
                          level_now.space_y, level_now.fireballs_m, level_now.lightnings_m, level_now.time_m)

            if not mute:
                pygame.mixer.music.load(level_now.music)
                pygame.mixer.music.set_volume(0.2)
                pygame.mixer.music.play(-1)

            if not mute:
                step_sound_rock.set_volume(0.3)

            hero.camera_start()
        else:
            level_to_load = level
            load_sound = True
            level_load_sound.play()


    menu_load(menu)

    clock = pygame.time.Clock()
    timer = pygame.USEREVENT + 1
    pygame.time.set_timer(timer, 1000)

    k_clock = pygame.time.Clock()
    timer_animation = pygame.USEREVENT + 2
    pygame.time.set_timer(timer_animation, 200)

    kk_clock = pygame.time.Clock()
    timer_animation_2 = pygame.USEREVENT + 3
    pygame.time.set_timer(timer_animation_2, 100)

    kkk_clock = pygame.time.Clock()
    timer_animation_3 = pygame.USEREVENT + 4
    pygame.time.set_timer(timer_animation_3, 300)

    cloc = pygame.time.Clock()
    timer_animation_4 = pygame.USEREVENT + 5
    pygame.time.set_timer(timer_animation_4, 100)
    #  ----------------------------------------------------------------------------------
    # Border(0, 775, width + 1000, 20, '-', 'g')
    # Border(0, 0, 20, height, '-', 'w')
    # Border(0, 0, width + 1000, 20, '-', 'r')
    # Cube(1000, 400, 400, 400)
    # Cube(1500, 600, 400, 200)
    # Cube(500, 100, 600, 30)
    #  x, y, size_x, size_y, hp, skin, speed_max, boost, jump
    #  ----------------------------------------------------------------------------------

    while running:
        clock.tick(fps)
        keys = pygame.key.get_pressed()
        mouse = pygame.mouse.get_pressed(5)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_e:
                    if not grab_shard:
                        if pygame.sprite.spritecollideany(all_shards.sprites()[0], player):
                            grab_shard = True
                        else:
                            grab_shard = False

                if event.key == pygame.K_ESCAPE and not hero.dead:
                    if not mini_window:
                        if not menu_is_load:
                            s_all_buttons.append(
                                Button(width / 2 - 150, height / 2 + 70, 200, 100, 'data/buttons/quit.png',
                                       'quit_button'))
                            s_all_buttons.append(
                                Button(width / 2 - 150, height / 2 - 50, 200, 100, 'data/buttons/menu.png', 'menu'))
                            mini_window = True

                    else:
                        if not menu_is_load:
                            for _ in all_buttons:
                                _.kill()
                            s_all_buttons.clear()
                            mini_window = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                for button in s_all_buttons:
                    if button.update(event.pos[0], event.pos[1]):
                        if button.mess == 'quit_button':
                            running = False

                        if button.mess == 'continue':
                            level_load(progress_load, False)

                        if button.mess == 'mute':
                            if mute:
                                mute = False
                                mute_file.write('\n' + 'not_mute')
                                button.image.fill((0, 0, 0, 0))
                                button.image.blit(pygame.transform.scale(pygame.image.load('data/buttons/mute.png'),
                                                                         (button.size_x, button.size_y)), (0, 0))
                                pygame.mixer.music.set_volume(0.2)
                                for _ in range(len(s_sounds)):
                                    s_sounds[_].set_volume(s_sounds_default[_])
                            else:
                                mute = True
                                pygame.mixer.music.set_volume(0)
                                button.image.fill((0, 0, 0, 0))
                                button.image.blit(pygame.transform.scale(pygame.image.load('data/buttons/muted.png'),
                                                                         (button.size_x, button.size_y)), (0, 0))
                                for _ in s_sounds:
                                    _.set_volume(0)
                                mute_file.write('\n' + 'mute')

                        if button.mess == 'menu':
                            mini_window = False
                            menu_load(menu)

                        if button.mess == 'retry':
                            level_load(level_now_s, True)

                        if button.mess == 'new_game':
                            level_load(level_1, False)

            if event.type == timer:

                if time_stop:
                    time_clock = 0

                if time_clock != 16:
                    time_clock += 1
                hero.clock_animation()

                if fire_ammo < 3:
                    time_fire_ammo += 1
                    if time_fire_ammo == 4:
                        fire_ammo += 1
                        time_fire_ammo = 0

                if not time_stop:
                    if invulnerability:
                        time_invulnerability += 1
                        if time_invulnerability == 2:
                            invulnerability = False
                            time_invulnerability = 0
                else:
                    invulnerability = True
                    time_invulnerability = 1

                if shield_move:
                    if not time_stop:
                        time_shield_move += 1
                        if time_shield_move == 2:
                            shield_move = False
                            time_shield_move = 0

                if time_stop:
                    time_stop_timer += 1
                    if time_stop_timer == 6:
                        if not mute:
                            pygame.mixer.music.set_volume(0.2)
                        time_stop = False
                        time_stop_timer = 0
                    elif time_stop_timer == 5:
                        time_zero_sound.play()

                if time_stop:
                    rest_sound.stop()
                    invulnerability = True
                    time_invulnerability = 1

            if event.type == timer_animation:
                if not mute and not time_stop:
                    if attenuation and not fight:
                        pygame.mixer.music.set_volume(pygame.mixer.music.get_volume() - 0.01)

                    elif not attenuation and fight:
                        pygame.mixer.music.set_volume(pygame.mixer.music.get_volume() - 0.01)

                    if pygame.mixer.music.get_volume() <= 0 and not fight:
                        fight = True
                        for _ in all_enemies:
                            if type(_) == FinalBoss:
                                pygame.mixer.music.load('data/sounds/mb_boss.mp3')
                                break
                            else:
                                pygame.mixer.music.load('data/sounds/' + random.choice(
                                    ['fight1.mp3', 'fight2.mp3', 'fight3.mp3', 'fight4.mp3', 'fight5.mp3',
                                     'fight6.mp3']))
                        pygame.mixer.music.set_volume(0.2)
                        pygame.mixer.music.play(-1)

                    if not attenuation and fight and pygame.mixer.music.get_volume() <= 0:
                        fight = False
                        pygame.mixer.music.load(level_now.music)
                        pygame.mixer.music.set_volume(0.2)
                        pygame.mixer.music.play(-1)
                    elif not attenuation and not fight:
                        pygame.mixer.music.set_volume(0.2)

                i += 1
                if i == 6:
                    i = 0
                if hero_animation == 'stand':
                    hero.animation_stand()
                elif hero_animation == 'run':
                    hero.animation_run()
                elif hero_animation == 'jump':
                    hero.animation_jump()
                if invulnerability and t == 1 and not time_stop:
                    t = 0
                    hero.image.fill((0, 0, 0, 0))
                else:
                    t = 1

                if fire_ammo > 0:
                    hero.animation_small_fireball()

                if not time_stop:  # time_stop
                    if menu_is_load:
                        a = random.randrange(7, 15)
                        for _ in range(5):
                            Particle(random.randrange(-width, level_now.size_x), level_now.size_y, a, a, 4, -4,
                                     ['data/part/pip1.png', 'data/part/pip2.png', 'data/part/pip3.png',
                                      'data/part/pip4.png'], 0, 'w', 50)
                    if level_now.level_name == 'level_4':
                        c = random.randrange(5, 8)
                        for _ in range(6):
                            Particle(random.randrange(0, level_now.size_x), 0, c, c, 5, 6,
                                     ['data/part/0i.png', 'data/part/1i.png', 'data/part/2i.png'], 0, 'w', 50)

                    for fireballs in all_fireballs.sprites():
                        fireballs.animation_fly()
                heart_img = s_heart_anim[i]

            if event.type == timer_animation_2:
                if load_sound and time_load_level != 70:
                    time_load_level += 1
                if time_load_level == 70:
                    time_load_level = 0
                    load_sound = False
                    level_load(level_to_load, False)
                if time_load_level == 50:
                    level_load_sound_rev.play()

                if time_stop:
                    if shield_up:
                        hero.animation_shield()
                else:
                    hero.animation_shield()

            if event.type == timer_animation_3:
                if load_sound:
                    if i_2 != 6:
                        i_2 += 1
                else:
                    i_2 = 0

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if fire_ammo != 0:
                        fire_ammo -= 1
                        fire = True
                        point_fire = event.pos

            if event.type == timer_animation_4:
                if not time_stop:
                    if menu_is_load:
                        if i_main == 48:
                            fon_revers_anim = True
                        elif i_main == 1:
                            fon_revers_anim = False

                        if fon_revers_anim:
                            i_main -= 1
                        else:
                            i_main += 1
                        fon_world = s_menu_fon[i_main]
                    else:
                        if i_main_2 == 10:
                            fon_revers_anim = True
                        elif i_main_2 == 0:
                            fon_revers_anim = False

                        if fon_revers_anim:
                            i_main_2 -= 1
                        else:
                            i_main_2 += 1
                        fon_world = s_world_fon[i_main_2]

        if keys[pygame.K_a] and keys[pygame.K_d]:
            step_sound = False
            step_sound_rock.stop()
            hero_animation = 'stand'
            hero.stand()

        elif keys[pygame.K_d]:
            if not step_sound and not is_jump:
                step_sound = True
                step_sound_rock.play(-1)

            hero_animation = 'run'
            hero.move_right()

        elif keys[pygame.K_a]:
            if not step_sound and not is_jump:
                step_sound = True
                step_sound_rock.play(-1)

            hero_animation = 'run'
            hero.move_left()
        else:
            step_sound = False
            step_sound_rock.stop()

        if is_jump:
            step_sound = False
            step_sound_rock.stop()

        if not keys[pygame.K_a] and not keys[pygame.K_d]:
            hero_animation = 'stand'
            hero.stand()

        if keys[pygame.K_w]:
            hero_animation = 'jump'
            is_jump = True
            hero.jump()
        else:
            if is_jump:
                non_boost = True

        if keys[pygame.K_g] and keys[pygame.K_o] and keys[pygame.K_d]:
            if not menu_is_load:
                hero.hp = 100

        if keys[pygame.K_m] and keys[pygame.K_i] and keys[pygame.K_n]:
            if not menu_is_load:
                hero.hp = 5

        if fire:
            hero.fire(*point_fire)
            fire = False

        sd = hero.camera_for_x(), hero.camera_for_y()

        screen.blit(fon_world, sd)
        if fon_world_coll != '-':
            screen.blit(fon_world_coll, sd)
        all_pl.draw(screen)

        if mouse[2]:
            if hero.lightnings_magic:
                if not shield_move and not sound_play_lightning:
                    sound_play_lightning = True
                    shield_up_sound.play(-1)
        else:
            if hero.lightnings_magic:
                shield_up_sound.stop()
                sound_play_lightning = False

        if shield_move:
            hero.shield_move_blast()
            all_lightnings.draw(screen)

        if not time_stop:  # time stop
            all_enemies.update()
            all_particles.update()
            all_fireballs.update()

        all_particles.draw(screen)
        all_enemies.draw(screen)
        all_fireballs.draw(screen)
        all_shards.draw(screen)
        all_shards.update(grab_shard)
        all_hearts.update()
        all_hearts.draw(screen)

        hero.gravity()
        hero.damaged()
        hero.move_small_fireball()
        hero.clock_move()

        time_stop_allowed = True

        if hero.hero_clock.i_2 != 12:
            time_stop_allowed = False

        if time_stop:
            if colour_time != 254:
                colour_time += 2
            inv.fill((colour_time, colour_time, colour_time, colour_time))
            inv.blit(screen, (0, 0), None, pygame.BLEND_RGB_SUB)
            screen.blit(inv, (0, 0))
            if colour_time != 254:
                white.fill((255, 255, 255, 255 - colour_time))
                screen.blit(white, (0, 0))
            pygame.mixer.music.set_volume(pygame.mixer.music.get_volume() - 0.001)
        else:
            colour_time = 0

        if keys[pygame.K_q]:
            if time_stop_allowed:
                za_world()

        if hero.fireballs_magic:
            if fire_ammo > 0:
                fire_2.draw(screen)
            if fire_ammo > 1:
                fire_1.draw(screen)
            if fire_ammo > 2:
                fire_3.draw(screen)

        if time_clock != 16:
            hero_clock.draw(screen)

        if not hero.dead:
            if mouse[2]:
                if hero.lightnings_magic:
                    if not shield_move:
                        time_shield_move = 0
                        shield_up = True
                        shield_move = False
                        hero.shield_up()
                        all_lightnings.draw(screen)
            else:
                if hero.lightnings_magic:
                    if shield_up:
                        shield_sound.play()
                        shield_move = True
                        shield_up = False

        player.draw(screen)

        if level_now.level_name == 'level_1':
            if not load_light:
                load_light = True
                light = pygame.transform.scale(pygame.image.load('data/cave/light.png'),
                                               (level_now.size_x, level_now.size_y)).convert_alpha()
            screen.blit(light, (sd[0], sd[1]))

        if hero.hp == 1:
            screen.blit(pre_dead, (0, 0))

        if hero.dead:
            pygame.mixer.music.set_volume(0)
            screen.blit(black, (0, 0))
            if not dead_buttons:
                s_all_buttons.append(
                    Button(width / 2 - 150, height / 2 - 170, 200, 100, 'data/buttons/retry.png', 'retry'))
                s_all_buttons.append(
                    Button(width / 2 - 150, height / 2 - 50, 200, 100, 'data/buttons/menu.png', 'menu'))
                s_all_buttons.append(
                    Button(width / 2 - 150, height / 2 + 70, 200, 100, 'data/buttons/quit.png', 'quit_button'))
                dead_buttons = True

        else:
            dead_buttons = False

        if mini_window:
            screen.blit(black, (0, 0))
        all_buttons.draw(screen)

        if load_sound:
            screen.blit(s_split_anim[i_2].convert_alpha(), (0, 0))
        if time_load_level >= 30:
            screen.blit(s_split_anim[-1].convert_alpha(), (0, 0))

        if not menu_is_load and not running:
            progress_save.close()
        pygame.display.flip()
    pygame.quit()
