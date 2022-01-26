import pygame
pygame.mixer.pre_init(44100, -16, 1, 512)
pygame.init()

hero_damaged = pygame.mixer.Sound('data/sounds/hero_damaged.wav')
hero_damaged_2 = pygame.mixer.Sound('data/sounds/hero_damaged2.wav')

cast_1 = pygame.mixer.Sound('data/sounds/cast.wav')
cast_1.set_volume(0.1)

cast_2 = pygame.mixer.Sound('data/sounds/cast1.wav')
cast_2.set_volume(0.1)

cast_3 = pygame.mixer.Sound('data/sounds/cast2.wav')
cast_3.set_volume(0.1)

cast_4 = pygame.mixer.Sound('data/sounds/cast3.wav')
cast_4.set_volume(0.1)

rest_sound = pygame.mixer.Sound('data/sounds/rest.wav')
rest_sound.set_volume(0.1)

boss_dead = pygame.mixer.Sound('data/sounds/dead.wav')
boss_dead.set_volume(0.2)

hero_damaged.set_volume(0.2)
hero_damaged_2.set_volume(0.2)

s_hero_damaged = [hero_damaged, hero_damaged_2]
s_boss_cast = [cast_1, cast_2, cast_3, cast_4]

heart_up = pygame.mixer.Sound('data/sounds/heart_up.wav')
heart_up.set_volume(0.5)

charge_laser = pygame.mixer.Sound('data/sounds/charge_laser.wav')
charge_laser.set_volume(0.1)

shoot_laser = pygame.mixer.Sound('data/sounds/blast_shoot.wav')
shoot_laser.set_volume(0.1)

tik = pygame.mixer.Sound('data/sounds/tik_1.wav')
tik.set_volume(0.1)

ult_ready = pygame.mixer.Sound('data/sounds/ult_ready.wav')
ult_ready.set_volume(0.2)

shield_sound = pygame.mixer.Sound('data/sounds/blast_shield_sound.wav')
shield_sound.set_volume(0.1)

shield_up_sound = pygame.mixer.Sound('data/sounds/shield_up_sound.wav')
shield_up_sound.set_volume(0.2)

step_sound_rock = pygame.mixer.Sound('data/sounds/steps_rock.wav')
step_sound_rock.set_volume(0.4)

time_stop_sound = pygame.mixer.Sound('data/sounds/time_stop_sound.wav')
time_stop_sound.set_volume(0.5)

time_zero_sound = pygame.mixer.Sound('data/sounds/time_zero_sound.wav')
time_zero_sound.set_volume(0.5)

hit_sound = pygame.mixer.Sound('data/sounds/hit_sound.wav')
hit_sound.set_volume(0.3)

level_load_sound = pygame.mixer.Sound('data/sounds/level_load_sound.wav')
level_load_sound.set_volume(0.3)

level_load_sound_rev = pygame.mixer.Sound('data/sounds/split_sound_rev.wav')
level_load_sound_rev.set_volume(0.2)

heart_beat = pygame.mixer.Sound('data/sounds/heartbeat.wav')
heart_beat.set_volume(0.3)

fire_ball_sound_0 = pygame.mixer.Sound('data/sounds/fireball_sound0.wav')
fire_ball_sound_1 = pygame.mixer.Sound('data/sounds/fireball_sound1.wav')
fire_ball_sound_2 = pygame.mixer.Sound('data/sounds/fireball_sound2.wav')

fireball_sounds_s = [fire_ball_sound_2, fire_ball_sound_1, fire_ball_sound_0]

s_sounds = [*fireball_sounds_s, *s_hero_damaged, *s_boss_cast, shoot_laser, tik, ult_ready, shield_sound,
            shield_up_sound, step_sound_rock, time_stop_sound,
            time_zero_sound, hit_sound, level_load_sound, level_load_sound_rev, charge_laser, heart_up, heart_beat,
            rest_sound]

s_sounds_default = [_.get_volume() for _ in s_sounds]