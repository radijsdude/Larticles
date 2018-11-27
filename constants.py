
testing = True

body_base_commands = ['command_move',
                      'command_rotate_left', 'command_rotate_right',
                      'command_regenerate',
                      'command_split',
                      'command_give']
body_attack_commands = ['command_eat',
                        'command_attack',
                        'command_freeze',
                        'command_wall_1','command_wall_2'
                        ]
body_memory_commands = ['command_memory_1_set', 'command_memory_1_value', 'command_memory_1_erase']
body_speak_commands = ['command_voice_speak', 'command_voice_1_value', 'command_voice_2_value']

body_state_commands = ['command_set_state', 'command_erase_state', 'command_state_value']
body_reflect_commands = ['command_reflect_1']
body_sentient_commands = body_state_commands + body_reflect_commands

body_commands = body_base_commands + body_attack_commands \
                + body_memory_commands + body_speak_commands \
                + body_sentient_commands
sight = ['see_red', 'see_green', 'see_blue', 'see_health', 'see_happyness',
         'see_state', 'see_frozen', 'see_attacking',
         'see_distance_0', 'see_distance_1', 'see_distance_2',
         'see_looking', 'see_orientation']
ddddd = ['north', 'south',
         'west', 'westwest', 'east', 'easteast',
         'northwest', 'northwestwest',
         'northeast', 'northeasteast',
         'southwest', 'southeast',
         'northnorth', 'northnorthnorth',
         'northnorthwest', 'northnorthwestwest',
         'northnortheast', 'northnortheasteast']
surounding_sense = []
for i in ddddd:
    surounding_sense.append('sense_' + str(i))
print(surounding_sense)
sense = [
    'sense_memory_1', 'sense_health',
    'sense_sound_1', 'sense_sound_2',
    'sense_happy', 'sense_killed', 'sense_state',
    'sense_alive_0', 'sense_alive_1', 'sense_alive_2',
    'sense_frozen',
    'sense_pos_x', 'sense_pos_y',
    'sense_clock', 'sense_reflect_1']

body_perception = sight + sense + surounding_sense

brain_all_neuron_names = body_commands + body_perception
body_hidden_names = []

for i in range(20):
    body_hidden_names.append('Hidden_' + str(i))
brain_all_neuron_names += body_hidden_names

print('brain size: ', len(brain_all_neuron_names))


handler_random_mutationrate = 2
handler_mutationrate = 90
handler_click_error = 0.8
handler_random_larticles_amount = 300

neuron_learningrate = 0.5
neurons_connectiondepth = 4


body_colour_newborn = [1, 1, 1]
body_colour_inactive = [0, 1, 0]
body_colour_regenerating = [0, 0, 1]
body_colour_eating = [1, 0, 0]
body_colour_attacking_eating = [1, 0.5, 0]
body_colour_attacking_regenerating = [0, 0.5, 1]
body_colour_attacking_else = [1, 1, 0]
body_colour_wall = [0.3, 0.3, 0.3]


body_directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]




import math
import itertools
import random
import time
import subprocess
import pickle
import os
import sys
import copy

os.environ['SDL_VIDEO_WINDOW_POS'] = '%i,%i' % (0, 30)

import pygame

pygame.font.init()

myfont10 = pygame.font.SysFont('Comic Sans MS', 10)
myfont11 = pygame.font.SysFont('Comic Sans MS', 11)
myfont12 = pygame.font.SysFont('Comic Sans MS', 12)
myfont15 = pygame.font.SysFont('Comic Sans MS', 15)
myfont20 = pygame.font.SysFont('Comic Sans MS', 20)
myfont30 = pygame.font.SysFont('Comic Sans MS', 30)
myfont40 = pygame.font.SysFont('Comic Sans MS', 40)
myfont50 = pygame.font.SysFont('Comic Sans MS', 50)
myfont75 = pygame.font.SysFont('Comic Sans MS', 75)
myfont100 = pygame.font.SysFont('Comic Sans MS', 100)
myfont150 = pygame.font.SysFont('Comic Sans MS', 150)

wit = (255, 255, 255)
zwart = (0, 0, 0)
rood = (255, 0, 0)
groen = (0, 255, 0)
blauw = (0, 0, 255)
geel = (255, 255, 0)
oranje = (255, 160, 0)
grijs = (190, 200, 200)
grijsdonker = (50,50,50)
paars = [211, 14, 237]


class Screen():
    def __init__(self):
        pass
    def initialize(self):
        pygame.init()
        self.display = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.x, self.y = self.display.get_size()
        pygame.display.set_caption('Larticles')
        self.clock = pygame.time.Clock()
        self.fullscreen = True
        if testing:
            self.toggle_fullscreen()
    def toggle_fullscreen(self):
        self.fullscreen = not self.fullscreen
        if self.fullscreen:
            self.display = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        else:
            self.display = pygame.display.set_mode(self.display.get_size(), pygame.RESIZABLE)


screen = Screen()



constant_grid_size = 100
constant_suns = int(2 / 10000 * constant_grid_size ** 2 + 0.5)
handler_amount_larticles = int(constant_grid_size ** 2 / 8)

body_health_bar = 500
body_max_health = 2 * body_health_bar
body_suffer = -body_health_bar/(constant_grid_size)
body_splitrate_red = 1.2
body_splitrate_attacker = 1
body_eat_damage = body_health_bar / 5
body_attack_damage = body_eat_damage
body_freeztime = 3
body_freeze_delay = 5
body_wall_drain = 1
body_eat_health_gain = 0.6
body_regenrate = 3
body_clock_interval = 10

brain_min_dna_length = int(2)
brain_max_dna_length = int(len(brain_all_neuron_names))
neuron_weight_size = 100
neuron_weight_scale = 10
brain_drain_scale = 100 * len(brain_all_neuron_names)












