import pygame as pg
from pygame.locals import *
pg.init()

opening_music = pg.mixer.Sound('Game Sounds/opening sound.mp3')
opening_music.set_volume(0.60*opening_music.get_volume())

ingame_bgmusic = pg.mixer.Sound('Game Sounds/space synth music.mp3')

buttonclick = pg.mixer.Sound('Game Sounds/buttonclick.wav')
buttonclick.set_volume(0.40*buttonclick.get_volume())

gameover_sound = pg.mixer.Sound('Game Sounds/game over.wav')

block_blink = pg.mixer.Sound('Game Sounds/block disappears.wav')
block_blink.set_volume(0.66*block_blink.get_volume())

block_hit_ground = pg.mixer.Sound('Game Sounds/block hits ground.wav')
new_highscore = pg.mixer.Sound('Game Sounds/new hs applause.wav')