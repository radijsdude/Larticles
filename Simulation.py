import math
import itertools
import random
import os
import time
import subprocess
import pickle

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

from constants import *


def recalc_grid(x, y):
    if x >= constant_grid_size:
        xx = x - constant_grid_size
    elif x < 0:
        xx = constant_grid_size + x
    else:
        xx = int(x)
    if y >= constant_grid_size:
        yy = y - constant_grid_size
    elif y < 0:
        yy = constant_grid_size + y
    else:
        yy = int(y)
    return xx, yy


def recalc_blit(x, y, gx, gy):
    dx = x + gx
    dy = y + gy
    if dx < 0:
        dx = constant_grid_size + dx
    elif dx >= constant_grid_size:
        dx = dx - constant_grid_size
    if dy < 0:
        dy = constant_grid_size + dy
    elif dy >= constant_grid_size:
        dy = dy - constant_grid_size
    dx += 1
    dy += 1
    return dx, dy


class Axon():
    def __init__(self, neuron):
        self.neuron = neuron
        self.weight = random.randrange(-neuron_weight_size, neuron_weight_size + 1) / neuron_weight_scale

    def __repr__(self):
        return 'weight: ' + str(self.weight) + ' * potential: ' + str(self.neuron.potential)


def Dendrite_set_weight(axon, weight):
    axon.weight = weight


def Dendrite_get(axon):
    return axon.neuron.name, axon.weight


def Dendrite_fire(axon):
    return axon.weight * Neuron_calculate(axon.neuron)


class Neuron():
    def __init__(self, name):
        self.name = name
        self.dendrites = {}
        self.potential = 0
        self.error = 0

    def __repr__(self):
        return str(self.name) + ' => ' + str(self.potential) + ' <= ' + str(self.dendrites)


def Neuron_set_potential(neuron, potential):
    neuron.potential = potential


def Neuron_get_connections(neuron):
    con = []
    for name in neuron.dendrites:
        con.append([neuron.name, name, neuron.dendrites[name].weight])
    return con


def Neuron_connect(neuron1, neuron2, weight=None):
    dendrite = Axon(neuron2)
    if weight != None:
        Dendrite_set_weight(dendrite, weight)
    neuron1.dendrites[neuron2.name] = dendrite
    t = Neuron_test_connection(neuron1, neurons_connectiondepth)
    if not t:
        neuron1.dendrites.pop(neuron2.name)
    return t


def Neuron_disconnect(neuron, name):
    if name in neuron.dendrites:
        neuron.dendrites.pop(name)


def Neuron_test_connection(neuron, connectiondepth):
    n = connectiondepth
    n -= 1
    r = True
    if n >= 0:
        if len(neuron.dendrites) != 0:
            for dendrite in neuron.dendrites:
                t = Neuron_test_connection(neuron.dendrites[dendrite].neuron, n)
                if t == False:
                    r = False
    else:
        r = False
    return r


def sigmoid(potential, derivative=False):
    if not derivative:
        if potential > -100:
            return 1 / (1 + math.exp(-potential))
        else:
            return 0
    else:
        return potential * (1 - potential)


def Neuron_calculate(neuron):
    if len(neuron.dendrites) != 0:
        x = 0
        for dendrite in neuron.dendrites:
            x += Dendrite_fire(neuron.dendrites[dendrite])
        neuron.potential = sigmoid(x)
    return neuron.potential


def Neuron_add_error(neuron, error):
    neuron.error = error


def Neuron_correct(neuron):
    gradient = neuron.error * sigmoid(neuron.potential, derivative=True)
    for dendrite in neuron.dendrites:
        delta_weight = neuron_learningrate * neuron.dendrites[dendrite].neuron.potential * gradient
        neuron.dendrites[dendrite].weight += delta_weight
        Neuron_add_error(neuron.dendrites[dendrite].neuron, gradient * neuron.dendrites[dendrite].weight)
        Neuron_correct(neuron.dendrites[dendrite].neuron)
    neuron.error = 0
    Neuron_calculate(neuron)


def Test_Neuron():
    print(' ')
    print(' ')
    print('Test Neuron')
    print(' ')
    print(' ')
    n1 = Neuron(1)
    n2 = Neuron(2)
    n3 = Neuron(3)
    n1.potential = 0.5
    n2.potential = 0.5
    Neuron_connect(n3, n1, 2)
    Neuron_connect(n3, n2, 3)

    s = 0.1234567890123456789
    for i in range(5001):
        y = Neuron_calculate(n3)
        e = s - y
        Neuron_add_error(n3, e)
        Neuron_correct(n3)
        if i % 500 == 0:
            print(i, n3.potential)
    print('get connections')
    print(Neuron_calculate(n3))
    print(' ')
    print(' ')
    print('End Test Neuron')
    print(' ')
    print(' ')


class Body():
    def __init__(self):
        self.x = 0
        self.y = 0

        self.direction = random.choice(body_directions)

        self.health = int(body_health_bar)
        self.previous_health = self.health
        self.regen = 0
        self.body_drain = 0
        self.regenerating = False
        self.happy = 0

        self.colour = body_colour_newborn

        self.reflect_1 = 0
        self.reflect_2 = 0
        self.reflect_3 = 0

        self.memory_1 = 0
        self.memory_2 = 0

        self.voice_1 = 0
        self.voice_2 = 0
        self.voice_3 = 0

        self.sound_1 = 0
        self.sound_2 = 0
        self.sound_3 = 0
        self.s1 = 0
        self.s2 = 0
        self.s3 = 0

        self.clock_timer = 0
        self.clock = 0

        self.dna_saved = None
        self.dna_saved_name = None
        self.dna_choose = 'self'

        self.eating = False
        self.talking = False
        self.give_health = False
        self.thinking = False
        self.memorizing = False
        self.attacking = False
        self.whispering = False
        self.freezing = False
        self.wall = False

        self.frozen = False
        self.freeztime = 0
        self.freezedelay = 0

        self.killer = 0

        self.kills = 0

        self.state = 0

    def get(self):
        properties = {}
        properties['pos'] = self.x, self.y
        properties['direction'] = self.direction
        properties['health'] = self.health
        properties['regen'] = self.regen
        properties['body drain'] = self.body_drain
        properties['regenerating'] = self.regenerating
        properties['happy'] = self.happy
        properties['colour'] = self.colour
        properties['memory 1'] = self.memory_1
        properties['memory 2'] = self.memory_2
        properties['voice 1'] = self.voice_1
        properties['voice 2'] = self.voice_2
        properties['voice 3'] = self.voice_3
        properties['sound 1'] = self.sound_1
        properties['sound 2'] = self.sound_2
        properties['sound 3'] = self.sound_3
        properties['eating'] = self.eating
        properties['talking'] = self.talking
        properties['giving health'] = self.give_health
        properties['thinking'] = self.thinking
        properties['memorizing'] = self.memorizing
        properties['attacking'] = self.attacking
        properties['whispering'] = self.whispering
        properties['freezing'] = self.freezing
        properties['freeztime'] = self.freeztime
        properties['killer'] = self.killer
        properties['kills'] = self.kills
        properties['state'] = self.state
        properties['wall'] = self.wall
        properties['freeze delay'] = self.freezedelay
        sx, sy = Body_pos_to_sense(self.x, self.y)
        properties['sense_pos_x'] = sx
        properties['sense_pos_y'] = sy
        properties['clock'] = self.clock
        properties['clock timer'] = self.clock_timer
        dna = False
        if self.dna_saved != None:
            dna = True
        properties['dna saved'] = dna
        if dna:
            length = len(self.dna_saved)
        else:
            length = -1
        properties['dna saved length'] = length
        properties['dna saved name'] = self.dna_saved_name
        properties['dna saved choose'] = self.dna_choose

        return properties


def Body_get_surounding_pos(x, y, direction):
    dx, dy = int(x + direction[0]), int(y + direction[1])
    north = recalc_grid(dx, dy)

    dx, dy = int(x + 2 * direction[0]), int(y + 2 * direction[1])
    northnorth = recalc_grid(dx, dy)

    dx, dy = int(x + 3 * direction[0]), int(y + 3 * direction[1])
    northnorthnorth = recalc_grid(dx, dy)

    dx, dy = int(x + 4 * direction[0]), int(y + 4 * direction[1])
    northnorthnorthnorth = recalc_grid(dx, dy)

    dx, dy = int(x - direction[0]), int(y - direction[1])
    south = recalc_grid(dx, dy)

    if direction == (1, 0):
        left = [0, 1]
    elif direction == (0, 1):
        left = [-1, 0]
    elif direction == (-1, 0):
        left = [0, -1]
    else:
        left = [1, 0]

    dx, dy = int(x + left[0]), int(y + left[1])
    west = recalc_grid(dx, dy)

    dx, dy = int(x + 2 * left[0]), int(y + 2 * left[1])
    westwest = recalc_grid(dx, dy)

    dx, dy = int(x - left[0]), int(y - left[1])
    east = recalc_grid(dx, dy)

    dx, dy = int(x - 2 * left[0]), int(y - 2 * left[1])
    easteast = recalc_grid(dx, dy)

    dx, dy = int(x + left[0] + direction[0]), int(y + left[1] + direction[1])
    northwest = recalc_grid(dx, dy)

    dx, dy = int(x + 2 * left[0] + direction[0]), int(y + 2 * left[1] + direction[1])
    northwestwest = recalc_grid(dx, dy)

    dx, dy = int(x + left[0] + 2 * direction[0]), int(y + left[1] + 2 * direction[1])
    northnorthwest = recalc_grid(dx, dy)

    dx, dy = int(x + left[0] + 3 * direction[0]), int(y + left[1] + 3 * direction[1])
    northnorthnorthwest = recalc_grid(dx, dy)

    dx, dy = int(x + 2 * left[0] + 2 * direction[0]), int(y + 2 * left[1] + 2 * direction[1])
    northnorthwestwest = recalc_grid(dx, dy)

    dx, dy = int(x + 3 * left[0] + 2 * direction[0]), int(y + 3 * left[1] + 2 * direction[1])
    northnorthwestwestwest = recalc_grid(dx, dy)

    dx, dy = int(x - left[0] + direction[0]), int(y - left[1] + direction[1])
    northeast = recalc_grid(dx, dy)

    dx, dy = int(x - 2 * left[0] + direction[0]), int(y - 2 * left[1] + direction[1])
    northeasteast = recalc_grid(dx, dy)

    dx, dy = int(x - left[0] + 2 * direction[0]), int(y - left[1] + 2 * direction[1])
    northnortheast = recalc_grid(dx, dy)

    dx, dy = int(x - left[0] + 3 * direction[0]), int(y - left[1] + 3 * direction[1])
    northnorthnortheast = recalc_grid(dx, dy)

    dx, dy = int(x - 2 * left[0] + 2 * direction[0]), int(y - 2 * left[1] + 2 * direction[1])
    northnortheasteast = recalc_grid(dx, dy)

    dx, dy = int(x - 3 * left[0] + 2 * direction[0]), int(y - 3 * left[1] + 2 * direction[1])
    northnortheasteasteast = recalc_grid(dx, dy)

    dx, dy = int(x + left[0] - direction[0]), int(y + left[1] - direction[1])
    southwest = recalc_grid(dx, dy)

    dx, dy = int(x - left[0] - direction[0]), int(y - left[1] - direction[1])
    southeast = recalc_grid(dx, dy)

    return {'north': north, 'south': south,
            'west': west, 'westwest': westwest, 'east': east, 'easteast': easteast,
            'northwest': northwest, 'northwestwest': northwestwest,
            'northeast': northeast, 'northeasteast': northeasteast,
            'southwest': southwest, 'southeast': southeast,
            'northnorth': northnorth, 'northnorthnorth': northnorthnorth, 'northnorthnorthnorth': northnorthnorthnorth,
            'northnorthnorthwest': northnorthnorthwest, 'northnorthnortheast': northnorthnortheast,
            'northnorthwest': northnorthwest, 'northnorthwestwest': northnorthwestwest,
            'northnorthwestwestwest': northnorthwestwestwest,
            'northnortheast': northnortheast, 'northnortheasteast': northnortheasteast,
            'northnortheasteasteast': northnortheasteasteast}


def check_looking(larticle1, larticle2):
    t1 = int(larticle1.body.x + larticle1.body.direction[0]) == larticle2.body.x
    t2 = int(larticle1.body.y + larticle1.body.direction[1]) == larticle2.body.y
    t3 = int(larticle1.body.x + larticle1.body.direction[0]) == larticle1.body.x
    t4 = int(larticle2.body.y + larticle2.body.direction[1]) == larticle1.body.y
    t = t1 and t2 and t3 and t4
    return t


def Body_sense(surounding):
    potentials = {}
    for name in surounding:
        n = 'sense_' + name
        if surounding[name] != None:
            potentials[n] = 1
        else:
            potentials[n] = 0
    return potentials


def See(larticle_seeing, larticle_seen, none=False):
    d = {}
    d['see_red'] = 0
    d['see_green'] = 0
    d['see_blue'] = 0
    d['see_health'] = 0
    d['see_happyness'] = 0
    d['see_state'] = 0
    d['see_frozen'] = 0
    d['see_attacking'] = 0
    d['see_looking'] = 0
    d['see_orientation'] = 1 / 2
    # r g b health happyness state distance
    if not none:
        d['see_red'] = larticle_seen.body.colour[0]
        d['see_green'] = larticle_seen.body.colour[1]
        d['see_blue'] = larticle_seen.body.colour[2]
        d['see_health'] = larticle_seen.body.health / larticle_seeing.body.health
        d['see_happyness'] = larticle_seen.body.happy
        d['see_state'] = larticle_seen.body.state
        d['see_frozen'] = int(larticle_seen.body.frozen)
        d['see_attacking'] = int(larticle_seen.body.attacking)
        if int(-larticle_seen.body.direction[0]) == int(larticle_seeing.body.direction[0]):
            if int(-larticle_seen.body.direction[1]) == int(larticle_seeing.body.direction[1]):
                d['see_looking'] = 1
                d['see_orientation'] = 0
        if int(larticle_seen.body.direction[0]) == int(larticle_seeing.body.direction[0]):
            if int(larticle_seen.body.direction[1]) == int(larticle_seeing.body.direction[1]):
                d['see_orientation'] = 1

    return d


def Body_see(larticle, surounding):
    # r g b health happyness state distance
    distance = {'see_distance_0': 0, 'see_distance_1': 0, 'see_distance_2': 0, 'see_distance_3': 0}
    if surounding['north'] != None:
        see = See(larticle, surounding['north'])
    else:
        if surounding['northnorth'] != None:
            see = See(larticle, surounding['northnorth'])
            distance['see_distance_0'] = 1
        else:
            if surounding['northnorthnorth'] != None:
                see = See(larticle, surounding['northnorthnorth'])
                distance['see_distance_0'] = 1
                distance['see_distance_1'] = 1
            else:
                if surounding['northnorthnorthnorth'] != None:
                    see = See(larticle, surounding['northnorthnorthnorth'])
                    distance['see_distance_0'] = 1
                    distance['see_distance_1'] = 1
                    distance['see_distance_2'] = 1
                else:
                    see = See(None, None, True)
                    distance['see_distance_0'] = 1
                    distance['see_distance_1'] = 1
                    distance['see_distance_2'] = 1
                    distance['see_distance_3'] = 1
    d = {}
    for i in see:
        d[i] = see[i]
    for i in distance:
        d[i] = distance[i]
    return d


def Body_move(larticle):
    x = int(larticle.body.direction[0] + larticle.body.x)
    y = int(larticle.body.direction[1] + larticle.body.y)
    dx, dy = recalc_grid(x, y)
    larticle.body.x = dx
    larticle.body.y = dy


def Body_rotate_right(direction):
    d = ()
    if direction == (1, 0):
        d = (0, 1)
    elif direction == (0, 1):
        d = (-1, 0)
    elif direction == (-1, 0):
        d = (0, -1)
    elif direction == (0, -1):
        d = (1, 0)
    return d


def Body_rotate_left(direction):
    d = ()
    if direction == (1, 0):
        d = (0, -1)
    elif direction == (0, -1):
        d = (-1, 0)
    elif direction == (-1, 0):
        d = (0, 1)
    elif direction == (0, 1):
        d = (1, 0)
    return d


def Body_regenerate(larticle, surounding):
    t = body_regenrate

    if surounding['north'] != None:
        if surounding['north'].body.regenerating:
            t += body_regenrate
    if surounding['south'] != None:
        if surounding['south'].body.regenerating:
            t += body_regenrate
    if surounding['west'] != None:
        if surounding['west'].body.regenerating:
            t += body_regenrate
    if surounding['east'] != None:
        if surounding['east'].body.regenerating:
            t += body_regenrate
    larticle.body.health += t

    return t


def Body_eat(larticle_win, larticle_lose):
    c = body_eat_health_gain * body_eat_damage * (1 / 2 + larticle_win.body.health / (2 * body_health_bar))
    if not larticle_lose.body.wall:
        h = larticle_lose.body.health
        if h > c:
            larticle_win.body.health += c
        else:
            larticle_win.body.health += body_eat_health_gain * h
        larticle_lose.body.health -= c
        if larticle_lose.body.health <= 0:
            larticle_win.body.kills += 1
            larticle_win.body.killer = 1


def Body_attack(larticle_attacking, larticle_attacked):
    if not larticle_attacked.body.wall:
        larticle_attacked.body.health -= body_attack_damage * (
            1 / 2 + larticle_attacking.body.health / (2 * body_health_bar))

    if larticle_attacked.body.health <= 0:
        larticle_attacking.body.kills += 1
        larticle_attacking.body.killer = 1


def Body_freeze(larticle_frozen):
    larticle_frozen.body.freeztime = body_freeztime


def Body_give(larticle_give, larticle_gain):
    if larticle_give.body.health > abs(body_eat_damage):
        larticle_give.body.health -= body_eat_damage
        larticle_gain.body.health += body_eat_damage


def Body_speak(larticle_speaker, larticle_listener):
    scale = 1
    front = False
    if int(larticle_speaker.body.x + larticle_speaker.body.direction[0]) == larticle_listener.body.x:
        if int(larticle_speaker.body.y + larticle_speaker.body.direction[1]) == larticle_listener.body.y:
            front = True
    if not front:
        d = ((larticle_speaker.body.x - larticle_listener.body.x) ** 2 + (
            larticle_speaker.body.y - larticle_listener.body.y) ** 2) ** (1 / 2)
        scale = float(1 / (d + 1))
    larticle_listener.body.sound_1 += larticle_speaker.body.voice_1 * scale
    larticle_listener.body.sound_2 += larticle_speaker.body.voice_2 * scale
    larticle_listener.body.sound_3 += larticle_speaker.body.voice_3 * scale


def Body_save_dna(larticles_saving, larticle_saved):
    larticles_saving.body.dna_saved = larticle_saved.brain.dna
    larticles_saving.body.dna_saved_name = larticle_saved.name


def Body_command(larticle, commands, surounding):
    result = []
    body = larticle.body
    body.body_drain = 0
    body.regen = 0
    x, y = int(body.x + body.direction[0]), int(body.y + body.direction[1])
    r2 = surounding['north']
    body.colour = body_colour_inactive

    body.voice_1 = commands['command_voice_1_value']
    body.voice_2 = commands['command_voice_2_value']
    body.voice_3 = commands['command_voice_3_value']

    happy = body.health - body.previous_health
    if happy > 0:
        body.happy = 1
    else:
        body.happy = 0

    body.reflect_1 = commands['command_reflect_1']
    body.reflect_2 = commands['command_reflect_2']
    body.reflect_3 = commands['command_reflect_3']

    if commands['command_memory_1_set'] > 0.5:
        body.memory_1 = commands['command_memory_1_value']
    if commands['command_memory_1_erase']:
        body.memory_1 = 0
    if commands['command_memory_2_set'] > 0.5:
        body.memory_1 = commands['command_memory_2_value']
    if commands['command_memory_2_erase']:
        body.memory_1 = 0

    if commands['command_memorize'] > 0.5:
        result.append('memorize')
        body.memorizing = True
    else:
        body.memorizing = False
    if commands['command_think'] > 0.5:
        result.append('think')
        body.thinking = True
    else:
        body.thinking = False
    if commands['command_set_state'] > 0.5:
        body.state = commands['command_state_value']
    if commands['command_erase_state'] > 0.5:
        body.state = 0

    if commands['command_voice_whisper'] > 0.5:
        body.whispering = True
        if r2 != None:
            if int(body.x) == int(r2.body.x + r2.body.direction[0]):
                if int(y) == int(r2.body.y + r2.body.direction[1]):
                    Body_speak(larticle, r2)
    else:
        body.whispering = False

    if commands['command_voice_speak'] > 0.5:
        body.talking = True
        for pos in surounding:
            if surounding[pos] != None:
                Body_speak(larticle, surounding[pos])
    else:
        body.talking = False

    if commands['command_wall_1'] > 0.5 and commands['command_wall_2'] > 0.5:
        body.wall = True
        body.health -= body_wall_drain
    else:
        body.wall = False

    if commands['command_regenerate'] > 0.5 and not body.wall:
        result.append('regenerate')
        body.regenerating = True
        body.colour = body_colour_regenerating
        body.regen = Body_regenerate(larticle, surounding)
    else:
        body.regenerating = False

    if commands['command_eat'] >= 0.5 and not body.wall:
        if not body.regenerating:
            body.eating = True
            body.colour = body_colour_eating
            if r2 != None:
                Body_eat(larticle, r2)
        else:
            body.eating = False
    else:
        body.eating = False

    if commands['command_attack'] > 0.5 and not body.wall:
        body.attacking = True
        if body.regenerating:
            body.colour = body_colour_attacking_regenerating
        else:
            if body.colour == body_colour_inactive:
                body.colour = body_colour_attacking_else
            else:
                body.colour = body_colour_attacking_eating
        if r2 != None:
            Body_attack(larticle, r2)
    else:
        body.attacking = False

    if commands['command_freeze'] > 0.5 and not body.frozen and not body.wall:
        if body.freezedelay == 0:
            body.freezedelay = body_freeze_delay
            body.freezing = True
            if r2 != None:
                Body_freeze(r2)
    else:
        body.freezing = False

    if commands['command_give'] > 0.5 and not body.wall:
        body.give_health = True
        if r2 != None:
            Body_give(larticle, r2)
        else:
            result.append('move')
    else:
        body.give_health = False

    if body.freezing:
        if body.regenerating:
            body.colour = [0.4, body.colour[1], body.colour[2]]
        elif body.eating:
            body.colour = [body.colour[0], body.colour[1], 0.4]
        else:
            body.colour = [1 / 2, 1, 1 / 2]

    if body.wall:
        body.colour = body_colour_wall

    if commands['command_dna_save'] > 0.5:
        if r2 != None:
            Body_save_dna(larticle, r2)

    if commands['command_dna_erase'] > 0.5:
        body.dna_saved = None
        body.dna_saved_name = None

    if commands['command_dna_choose'] > 0.5:
        body.dna_choose = 'other'
    else:
        body.dna_choose = 'self'

    if commands['command_split'] >= 0.5 and not body.wall:
        if body.regenerating:
            if r2 == None:
                minh = body_health_bar + body_health_bar / 10
                if body.health > minh:
                    body.health -= body_health_bar
                    result.append('split')
                    if commands['command_dna_choose'] > 0.5 and larticle.body.dna_saved != None:
                        result.append('dna_other')



        else:
            rs2 = surounding['south']
            if rs2 == None:
                minh = body_splitrate_red * (body_health_bar + body_health_bar / 10)
                if body.health > minh:
                    body.health -= body_splitrate_red * body_health_bar
                    result.append('split')
                    if commands['command_dna_choose'] > 0.5 and larticle.body.dna_saved != None:
                        result.append('dna_other')

    if commands['command_rotate_right'] > 0.5 and not body.wall and not commands['command_rotate_left'] > 0.5:
        pass
    if commands['command_rotate_left'] > 0.5 and not body.wall and not commands['command_rotate_right'] > 0.5:
        pass

    if commands['command_move'] > 0.5 and not body.frozen and not body.wall and not body.regenerating:
        pass

    larticle.body.clock_timer += 1
    larticle.body.clock = 0
    if larticle.body.clock_timer >= body_clock_interval:
        larticle.body.clock = 1
        larticle.body.clock_timer = 0

    if body.freezedelay > 0:
        body.freezedelay -= 1

    if body.freeztime > 0:
        body.frozen = True
        body.freeztime -= 1
    else:
        body.frozen = False


    if not body.colour == body_colour_inactive:
        t = body_suffer * (1 + body.health / body_health_bar)
        body.body_drain = abs(t)
        body.health += t

    if body.attacking and body.regenerating:
        if body.health > 2 * body_max_health:
            body.health = 2 * body_max_health
    else:
        if body.health > body_max_health:
            body.health = body_max_health

    return result


def Body_pos_to_sense(x, y):
    sx = 1 / 2 * math.sin(2 * x / (constant_grid_size) * 2 * math.pi) + 0.5
    sy = 1 / 2 * math.sin(2 * y / (constant_grid_size) * 2 * math.pi) + 0.5
    return sx, sy


def Body_to_brain(larticle, surounding, t=False):
    see = Body_see(larticle, surounding)
    sense = Body_sense(surounding)

    sx, sy = Body_pos_to_sense(larticle.body.x, larticle.body.y)

    frozen = 0
    if larticle.body.frozen:
        frozen = 1

    sound = voice_scale([larticle.body.sound_1, larticle.body.sound_2, larticle.body.sound_3])
    others = {'sense_health': larticle.body.health / body_health_bar, 'sense_happy': larticle.body.happy,
              'sense_alive_0': 1, 'sense_alive_1': larticle.body.clock_timer % 2,
              'sense_alive_2': int(larticle.body.clock_timer % 3 == 0),
              'sense_memory_1': larticle.body.memory_1, 'sense_memory_2': larticle.body.memory_2,
              'sense_sound_1': sound[0], 'sense_sound_2': sound[1],
              'sense_sound_3': sound[2],
              'sense_killed': larticle.body.killer, 'sense_frozen': frozen,
              'sense_pos_x': sx,
              'sense_pos_y': sy,
              'sense_clock': larticle.body.clock,
              'sense_reflect_1': larticle.body.reflect_1, 'sense_reflect_2': larticle.body.reflect_2,
              'sense_reflect_3': larticle.body.reflect_3}
    result = {}
    for i in see:
        result[i] = see[i]
    for i in sense:
        result[i] = sense[i]
    for i in others:
        result[i] = others[i]
    if not t:
        larticle.body.sound_1 = 0
        larticle.body.sound_2 = 0
        larticle.body.sound_3 = 0
        larticle.body.killer = 0
    return result


class Brain():
    def __init__(self, dna=None):
        self.neurons = {}
        for i in brain_all_neuron_names:
            self.neurons[i] = Neuron(i)
        self.dna = dna
        if self.dna == None:
            self.dna = Brain_create_random_dna()
        Brain_set_dna(self, self.dna)


def Brain_create_random_dna():
    p = list(itertools.permutations(brain_all_neuron_names, 2))
    length = random.randrange(brain_min_dna_length, brain_max_dna_length)
    dna = []

    for i in range(length):
        t = True
        while t:

            n1, n2 = random.choice(p)
            if n1 != n2 and n1 not in body_perception:
                r2 = random.randrange(-neuron_weight_size, neuron_weight_size + 1) / neuron_weight_scale
                dna.append([n1, n2, r2])
                t = False
    return dna


def Brain_set_dna(brain, dna):
    for neuron1, neuron2, weight in dna:
        if neuron1 not in brain.neurons:
            brain.neurons[neuron1] = Neuron(neuron1)
        if neuron2 not in brain.neurons:
            brain.neurons[neuron2] = Neuron(neuron2)
        Neuron_connect(brain.neurons[neuron1], brain.neurons[neuron2], weight)


def Brain_get_dna(larticle):
    dna = []
    for name in brain_all_neuron_names:
        dna += Neuron_get_connections(larticle.brain.neurons[name])
    larticle.brain.dna = dna
    return dna


def Brain_mutate(larticle):
    r1 = random.randrange(0, 100)
    if 0 <= r1 < 33:
        if len(larticle.brain.dna) != 0:
            r2 = random.randrange(0, len(larticle.brain.dna))
            Neuron_disconnect(larticle.brain.neurons[larticle.brain.dna[r2][0]], larticle.brain.dna[r2][1])
            larticle.brain.dna.pop(r2)

    elif 33 <= r1 < 66:
        n1 = random.choice(list(brain_all_neuron_names))
        n2 = random.choice(list(brain_all_neuron_names))
        if n1 != n2 and n1 not in body_perception:
            r2 = random.randrange(-neuron_weight_size, neuron_weight_size + 1) / neuron_weight_scale
            if n1 not in larticle.brain.neurons:
                larticle.brain.neurons[n1] = Neuron(n1)
            if n2 not in larticle.brain.neurons:
                larticle.brain.neurons[n2] = Neuron(n2)
            tt = Neuron_connect(larticle.brain.neurons[n1], larticle.brain.neurons[n2], r2)
            if tt:
                larticle.brain.dna.append([n1, n2, r2])

    else:
        if len(larticle.brain.dna) != 0:
            r2 = random.randrange(0, len(larticle.brain.dna))
            r3 = random.randrange(-neuron_weight_size, neuron_weight_size + 1) / neuron_weight_scale
            larticle.brain.dna[r2][-1] = r3
            Neuron_connect(larticle.brain.neurons[larticle.brain.dna[r2][0]],
                           larticle.brain.neurons[larticle.brain.dna[r2][0]], r3)


def Brain_learn(larticle, memory):
    invoer = memory[0]
    uitvoer = memory[1]
    for i in invoer:
        Neuron_set_potential(larticle.brain.neurons[i], invoer[i])
    for i in larticle.brain.neurons:
        Neuron_calculate(larticle.brain.neurons[i])
    for i in uitvoer:
        y = 0
        if uitvoer[i] > 0.5:
            y = 1
        error = y - larticle.brain.neurons[i].potential
        Neuron_add_error(larticle.brain.neurons[i], error)
        Neuron_correct(larticle.brain.neurons[i])


def Brain_to_body(larticle, inputs):
    result = {}
    for name in inputs:
        Neuron_set_potential(larticle.brain.neurons[name], inputs[name])
    for name in body_commands:
        result[name] = Neuron_calculate(larticle.brain.neurons[name])
    return result


larticle_memory_size = 20


class Larticle():
    def __init__(self, name, dna=None):
        self.name = name
        self.body = Body()
        self.brain = Brain(dna)
        self.time_alive = 0
        self.brain_drain = (len(self.brain.dna)) * brain_drain_scale
        self.splits = 0
        self.memory = []
        self.previous_memory = []
        self.generation = 0


def Larticle_simulate(larticle, surounding):
    larticle.time_alive += 1
    forbrain = Body_to_brain(larticle, surounding)
    forbody = Brain_to_body(larticle, forbrain)
    larticle.previous_memory = [forbody, forbrain]
    return forbody


def Larticle_doe(larticle, forbody, surounding):
    r = Body_command(larticle, forbody, surounding)

    if 'memorize' in r:
        if len(larticle.memory) < larticle_memory_size:
            if larticle.previous_memory != []:
                larticle.memory.append(larticle.previous_memory)
        else:
            larticle.memory.pop(0)
            if larticle.previous_memory != []:
                larticle.memory.append(larticle.previous_memory)
    if 'think' in r:
        if len(larticle.memory) > 0:
            memory = random.choice(larticle.memory)
            Brain_learn(larticle, memory)

    larticle.body.health -= larticle.brain_drain
    return r


def Larticle_mutate(larticle):
    Brain_mutate(larticle)


def Larticle_score(larticle):
    score = int(larticle.time_alive * larticle.body.health * (larticle.splits + 1) * (larticle.body.kills / 10 + 1))
    return score


class Handler():
    def __init__(self, display=None):
        print(' ')
        print(' ')
        print('Initializing Handler Constants.')
        print(' ')
        print(' ')
        self.count = 0
        self.died = 0
        self.solardeaths = 0
        self.epoch = 0
        self.splits = 0
        self.larticles = {}
        self.random_larticles = []
        self.previous_amount_kills = 0

        self.eaters = 0
        self.stupids = 0
        self.regenerators = 0
        self.newbies = 0
        self.attacking = 0
        self.walls = 0

        self.suns = []
        self.positions = {}

        self.visual = False

        self.selected_larticle = None
        self.selected_neuron = None

        self.frames = []

        print(' ')
        print(' ')
        print('Initializing Handler.')
        print(' ')
        print(' ')

        Handler_initialize(display, self)


def Handler_create_random_larticles(n):
    random_larticles = []
    for i in range(int(n)):
        l = Larticle('Random' + str(i))
        random_larticles.append(l)
    return random_larticles


def Handler_initialize(display, handler):
    Pygame_display = display
    print(' ')
    print('Placing Larticles.')
    print(' ')
    s1 = "In this world"
    s2 = "is the destiny of mankind controlled"
    s3 = "by some transcendental entity "
    s3b = "or law...?"
    s3bb = ''
    s4 = "Is it like the hand of God "
    s4b = "hovering above?"
    s4bb = ''
    s5 = "At least it is true "
    s5b = "that man has no control"
    s6 = "even over his own will."
    ls = [s1, s2, s3, s3b, s3bb, s4, s4b, s4bb, s5, s5b, s6]
    t = [200, 200, 300, 100]
    b = [800, 200, 200, 200]
    handler.epoch = 0
    tt = 0
    if display != None:
        textsurface = myfont30.render(ls[0], False, [250, 250, 250])
        Pygame_display.blit(textsurface, [200, 500, 100, 100])
        textsurface = myfont75.render('LOADING', False, [250, 250, 250])
        Pygame_display.blit(textsurface, t)
        textsurface = myfont75.render(str(0) + ' %', False, [250, 250, 250])
        Pygame_display.blit(textsurface, b)
        pygame.display.update()
        if not testing:
            pygame.time.wait(500)

    p = -1
    for i in range(handler_amount_larticles):
        larticle = Larticle('Big Bang Larticle: ' + str(i))
        Handler_place_larticle(handler, larticle)
        if i % int(handler_amount_larticles / 10) == 0:
            p += 1
            perc = p * 10
            print(str(perc), '%')
            if display != None:
                Pygame_display.fill([0, 0, 0])
                if tt < len(ls):
                    textsurface = myfont30.render(ls[tt], False, [250, 250, 250])
                    Pygame_display.blit(textsurface, [200, 500, 100, 100])
                textsurface = myfont75.render(str(perc) + ' %', False, [250, 250, 250])
                Pygame_display.blit(textsurface, b)
                textsurface = myfont75.render('LOADING', False, [250, 250, 250])
                Pygame_display.blit(textsurface, t)
                pygame.display.update()
                if not testing:
                    pygame.time.wait(1000)
                tt += 1
    if display != None:
        Pygame_display.fill([0, 0, 0])
        textsurface = myfont30.render(ls[-1], False, [250, 250, 250])
        Pygame_display.blit(textsurface, [200, 500, 100, 100])
        textsurface = myfont75.render(str(100) + ' %', False, [250, 250, 250])
        Pygame_display.blit(textsurface, b)
        textsurface = myfont75.render('LOADING', False, [250, 250, 250])
        Pygame_display.blit(textsurface, t)
        pygame.display.update()
        if not testing:
            pygame.time.wait(2000)
        tt += 1

    Handler_get_all_positions(handler)
    print(' ')
    print('Placing Larticles Done.')
    print(' ')

    if display != None:
        Pygame_display.fill([0, 0, 0])

        t = [200, 200, 300, 100]
        textsurface = myfont50.render('Appending Random Brains..', False, [250, 250, 250])
        Pygame_display.blit(textsurface, t)
        pygame.display.update()

    print(' ')
    print(' ')
    print('Creating random Larticles')
    print(' ')
    print(' ')

    handler.random_larticles += Handler_create_random_larticles(1000)

    print(' ')
    print(' ')
    print('Creating random Larticles done.')
    print(' ')
    print(' ')

    print(' ')
    print('Handler Initializing Succesfull.')
    print(' ')


def Handler_get_all_positions(handler):
    pos = {}
    doubles = []
    for name in handler.larticles:
        x, y = int(handler.larticles[name].body.x), int(handler.larticles[name].body.y)
        x, y = recalc_grid(x, y)
        s = str(x) + '_' + str(y)

        if s not in pos:
            pos[s] = name
        else:
            print('Double: ', name)
            doubles.append(name)
    for name in doubles:
        if name in handler.larticles:
            handler.larticles.pop(name)
    handler.positions = pos
    return pos


def Handler_get_surrounding_positions(handler, larticle):
    positions = Body_get_surounding_pos(larticle.body.x, larticle.body.y, larticle.body.direction)
    ss = {}
    for position in positions:
        sx, sy = recalc_grid(positions[position][0], positions[position][1])
        s1 = str(sx) + '_' + str(sy)
        ss[position] = s1
    l = {}
    for position in ss:
        if ss[position] in handler.positions:
            if handler.positions[ss[position]] in handler.larticles:
                l[position] = handler.larticles[handler.positions[ss[position]]]
            else:
                l[position] = None
        else:
            l[position] = None
    return l


def Handler_check_pos(handler, x, y):
    s = str(int(x)) + '_' + str(int(y))
    if s in handler.positions:
        return False
    return True


def Handler_check_around(handler, x, y):
    p1x, p1y = x + 1, y
    p2x, p2y = x - 1, y
    p3x, p3y = x, y + 1
    p4x, p4y = x, y - 1
    r = [[int(x), int(y)], [int(p1x), int(p1y)], [int(p2x), int(p2y)], [int(p3x), int(p3y)], [int(p4x), int(p4y)]]
    for pos in r:
        s = str(int(pos[0])) + '_' + str(int(pos[1]))
        if s in handler.positions:
            return False
    return True


def Handler_place_larticle(handler, larticle):
    t = True
    tt = 0
    ranx = None
    rany = None
    while t:
        tt += 1
        ranx = random.randrange(0, int(constant_grid_size))
        rany = random.randrange(0, int(constant_grid_size))
        r1 = Handler_check_around(handler, ranx, rany)
        if r1:
            handler.count += 1
            larticle.body.x = int(ranx)
            larticle.body.y = int(rany)
            rs = str(ranx) + '_' + str(rany)
            handler.positions[rs] = larticle.name
            handler.larticles[larticle.name] = larticle
            t = False
        if tt > 50:
            print('larticle handler place larticle while break')
            break
    return ranx, rany


def Handler_run(handler, autoselect=False):
    print('Epoch: ', handler.epoch)
    handler.eaters = 0
    handler.stupids = 0
    handler.regenerators = 0
    handler.newbies = 0
    handler.walls = 0
    handler.attacking = 0
    handler.epoch += 1
    died = []
    strongest_score = 0
    strongest_name = ''

    handler.suns = []
    for i in range(constant_suns):
        handler.suns.append([random.randrange(0, constant_grid_size), random.randrange(0, constant_grid_size)])

    for name in list(handler.larticles.keys()):

        larticle = handler.larticles[name]

        body = larticle.body
        x0 = int(body.x)
        y0 = int(body.y)
        s0 = str(x0) + '_' + str(y0)
        handler.positions.pop(s0)

        if [x0, y0] not in handler.suns:

            if body.health > 0:

                t = Larticle_score(larticle)
                if t > strongest_score:
                    strongest_name = name
                    strongest_score = t

                if body.colour == [1, 1, 1]:
                    handler.newbies += 1
                if body.wall:
                    handler.walls += 1
                if body.attacking:
                    handler.attacking += 1

                if body.eating:
                    handler.eaters += 1
                elif body.regenerating:
                    handler.regenerators += 1
                else:
                    if not body.wall:
                        handler.stupids += 1

                surounding = Handler_get_surrounding_positions(handler, larticle)
                forbody = Larticle_simulate(larticle, surounding)

                move = False
                rotate = False

                if forbody['command_rotate_right'] > 0.5 and not body.wall and not forbody[
                    'command_rotate_left'] > 0.5:
                    rotate = 'right'
                    body.direction = Body_rotate_right(body.direction)

                if forbody['command_rotate_left'] > 0.5 and not body.wall and not forbody[
                    'command_rotate_right'] > 0.5:
                    rotate = 'left'
                    body.direction = Body_rotate_left(body.direction)

                if forbody['command_move'] > 0.5 and not body.frozen and not body.wall and not forbody[
                    'command_regenerate'] > 0.5:
                    sx, sy = int(body.x + body.direction[0]), int(body.y + body.direction[1])
                    sx, sy = recalc_grid(sx, sy)
                    ss = str(sx) + '_' + str(sy)
                    if ss not in handler.positions:
                        move = True
                        Body_move(larticle)

                x = int(body.x)
                y = int(body.y)
                direction = body.direction
                s = str(x) + '_' + str(y)
                handler.positions[s] = larticle.name

                sur = {}
                if rotate != False and not move:
                    if rotate == 'right':
                        sur['north'] = surounding['west']
                        sur['west'] = surounding['south']
                        sur['south'] = surounding['east']
                        sur['east'] = surounding['north']
                    if rotate == 'left':
                        sur['north'] = surounding['east']
                        sur['east'] = surounding['south']
                        sur['south'] = surounding['west']
                        sur['west'] = surounding['north']
                elif move and rotate == False:
                    sur['north'] = surounding['northnorth']
                    sur['south'] = None
                    sur['west'] = surounding['northwest']
                    sur['east'] = surounding['northeast']
                elif move and rotate != False:
                    if rotate == 'right':
                        sur['north'] = surounding['westwest']
                        sur['west'] = surounding['southwest']
                        sur['south'] = None
                        sur['east'] = surounding['northwest']
                    if rotate == 'left':
                        sur['north'] = surounding['easteast']
                        sur['west'] = surounding['northeast']
                        sur['south'] = None
                        sur['east'] = surounding['southeast']
                else:
                    sur = surounding

                surounding = sur

                result = Larticle_doe(larticle, forbody, surounding)

                if 'split' in result:

                    r = random.randrange(0, 100)

                    if r > handler_death_at_birth:

                        if body.regenerating:
                            if not body.attacking:
                                t = surounding['north']
                                dx, dy = int(x + direction[0]), int(y + direction[1])
                                ldir = []
                                for i in body_directions:
                                    if i != (-direction[0], -direction[1]):
                                        ldir.append(i)
                            else:
                                t = surounding['south']
                                dx, dy = int(x - direction[0]), int(y - direction[1])
                                ldir = []
                                for i in body_directions:
                                    if i != direction:
                                        ldir.append(i)
                        else:
                            t = surounding['south']
                            dx, dy = int(x - direction[0]), int(y - direction[1])
                            ldir = []
                            for i in body_directions:
                                if i != direction:
                                    ldir.append(i)
                        dx, dy = recalc_grid(dx, dy)

                        if t == None:
                            handler.count += 1
                            handler.splits += 1
                            larticle.splits += 1
                            name = str(larticle.name.split('_')[0]) + '_' + str(handler.epoch) + '_' + str(
                                handler.splits)

                            r = random.randrange(0, 100)
                            if r <= handler_mutationrate:
                                r2 = random.randrange(0, 100)
                                if r2 >= handler_random_mutationrate:
                                    if forbody['command_dna_choose'] > 0.5 and body.dna_saved != None:
                                        l = Larticle(name, larticle.body.dna_saved)
                                        l.body.dna_saved = larticle.brain.dna
                                    else:
                                        Brain_get_dna(larticle)
                                        l = Larticle(name, larticle.brain.dna)
                                        l.body.dna_saved = larticle.body.dna_saved
                                    Larticle_mutate(l)

                                else:
                                    l = handler.random_larticles[0]
                                    handler.random_larticles.pop(0)
                                    l.name += 'Ancesters epoch of birth: ' + str(handler.epoch)
                            else:
                                l = Larticle(name, larticle.brain.dna)
                            l.body.x = dx
                            l.body.y = dy
                            l.body.direction = random.choice(ldir)
                            l.memory = larticle.memory
                            l.generation = larticle.generation + 1
                            if l.name not in handler.larticles:
                                handler.larticles[l.name] = l
                                handler.positions[str(dx) + '_' + str(dy)] = l.name
                            else:
                                print('Double split name!')

            else:
                died.append(name)
        else:
            died.append(name)
            handler.solardeaths += 1


    for name in died:
        handler.died += 1
        handler.larticles.pop(name)
    if autoselect:
        if strongest_name in handler.larticles:
            handler.selected_larticle = handler.larticles[strongest_name]


def Handler_set_visual(handler):
    handler.visual = not handler.visual


def Handler_reset_selected(handler):
    handler.selected_larticle = None
    handler.selected_neuron = None


def Handler_kill_selected(handler):
    if handler.selected_larticle.name in handler.larticles:
        handler.larticles.pop(handler.selected_larticle.name)


def map_color(color):
    r = color[0] * 250 + 50
    g = color[1] * 250 + 50
    b = color[2] * 250 + 50
    if r > 255:
        r = 255
    if g > 255:
        g = 255
    if b > 255:
        b = 255
    return [r, g, b]


def state_color(larticle):
    c = larticle.body.state * 150
    colour = list(larticle.body.colour)
    colour = map_color(colour)
    colour[0] += c - 50
    colour[1] += c - 50
    colour[2] += c - 50
    if colour[0] > 255:
        colour[0] = 255
    if colour[1] > 255:
        colour[1] = 255
    if colour[2] > 255:
        colour[2] = 255
    return colour


def Handler_get_larticle_properties(larticle):
    properties = larticle.body.get()
    properties['age'] = larticle.time_alive
    properties['name'] = larticle.name
    properties['brain drain'] = larticle.brain_drain
    properties['splits'] = larticle.splits
    properties['dna length'] = len(larticle.brain.dna)
    properties['neuron amount'] = len(larticle.brain.neurons)
    properties['memorized length'] = len(larticle.memory)
    properties['score'] = Larticle_score(larticle)
    properties['generation'] = larticle.generation
    return properties


def Handler_blits_frame(display, handler, scale, x, y, gx, gy, mx=None, my=None):
    pygame_windows_size = constant_screensize_x,constant_screensize_y
    Pygame_display = display
    wx, wy = Pygame_display.get_size()

    if handler.visual:
        d = 50
        c = [d, d, d]
        for i in range(constant_grid_size):
            pygame.draw.line(Pygame_display, c, [x, i * scale + scale / 2 + y],
                             [x + constant_grid_size * scale, i * scale + scale / 2 + y])
            pygame.draw.line(Pygame_display, c, [i * scale + scale / 2 + x, y],
                             [i * scale + scale / 2 + x, y + constant_grid_size * scale])

    pygame.draw.rect(Pygame_display, [0, 0, 0],
                     [pygame_windows_size[1], 0, pygame_windows_size[0], pygame_windows_size[0]])

    textsurface = myfont12.render('Epoch: ' + str(handler.epoch), False, (250, 250, 250))
    Pygame_display.blit(textsurface, (wy + 10, 0))

    textsurface = myfont12.render('Larticles: ' + str(len(handler.larticles)), False, (250, 250, 250))
    Pygame_display.blit(textsurface, (wy + 10, 15))

    textsurface = myfont12.render('Died: ' + str(handler.died), False, (250, 250, 250))
    Pygame_display.blit(textsurface, (wy + 10, 30))

    textsurface = myfont12.render('Solar Deaths: ' + str(handler.solardeaths), False, (255, 227, 15))
    Pygame_display.blit(textsurface, (wy + 10, 45))

    textsurface = myfont12.render('Splits: ' + str(handler.splits), False, (250, 250, 250))
    Pygame_display.blit(textsurface, (wy + 10, 60))

    textsurface = myfont12.render('Deaths: ' + str(handler.died - handler.previous_amount_kills), False,
                                  (255, 255, 255))
    Pygame_display.blit(textsurface, (wy + 170, 0))
    handler.previous_amount_kills = handler.died

    textsurface = myfont12.render('Newborns: ' + str(handler.newbies), False, (250, 250, 250))
    Pygame_display.blit(textsurface, (wy + 170, 15))

    textsurface = myfont12.render('Eaters: ' + str(handler.eaters), False, (250, 100, 100))
    Pygame_display.blit(textsurface, (wy + 170, 30))

    textsurface = myfont12.render('Conservatives: ' + str(handler.stupids), False, (100, 250, 100))
    Pygame_display.blit(textsurface, (wy + 170, 45))

    textsurface = myfont12.render('Regenerators: ' + str(handler.regenerators), False, (100, 100, 250))
    Pygame_display.blit(textsurface, (wy + 170, 60))

    textsurface = myfont12.render('Walls: ' + str(handler.walls), False, (125, 125, 125))
    Pygame_display.blit(textsurface, (wy + 170, 75))

    textsurface = myfont12.render('Attackers: ' + str(handler.attacking), False, (250, 150, 100))
    Pygame_display.blit(textsurface, (wy + 170, 90))

    textsurface = myfont12.render('Surface Area: ' + str(constant_grid_size ** 2), False, (150, 150, 150))
    Pygame_display.blit(textsurface, (wy + 340, 0))

    textsurface = myfont12.render('Amount of suns: ' + str(constant_suns), False, (255, 227, 15))
    Pygame_display.blit(textsurface, (wy + 340, 15))


def Handler_blits_map(display, handler, scale, x, y, gx, gy, mx=None, my=None):
    Pygame_display = display
    wx, wy = Pygame_display.get_size()

    pos = {}
    doubles = []

    for name in handler.larticles:
        larticle = handler.larticles[name]
        lx = int(larticle.body.x)
        ly = int(larticle.body.y)
        ls = str(lx) + '_' + str(ly)

        lx, ly = recalc_blit(lx, ly, gx, gy)
        if ls not in pos:
            pos[ls] = name
        else:
            doubles.append(name)

        if mx != None and my != None:
            if mx < wy:
                if abs(lx * scale - handler_click_error * scale) <= mx - x <= abs(
                                        lx * scale + handler_click_error * scale) and abs(
                                    ly * scale - handler_click_error * scale) <= my - y <= abs(
                                    ly * scale + handler_click_error * scale):
                    handler.selected_larticle = larticle
        if - 50 < lx * scale + x < wy and - 50 < ly * scale + y < wy:
            if not handler.visual:
                k = map_color(larticle.body.colour)
            else:
                k = state_color(larticle)
            pygame.draw.circle(Pygame_display, k,
                               [int(lx * scale + x), int(ly * scale + y)],
                               int(scale / 2))

            if handler.visual:
                if larticle.body.talking:
                    kleur = [250, 100, 250]
                else:
                    kleur = [0, 0, 0]

                d = 2

                if larticle.body.frozen:
                    pygame.draw.circle(Pygame_display, [250, 250, 250],
                                       [int(lx * scale + x), int(ly * scale + y)],
                                       int(scale / 2 + 1), d)

                if larticle.body.give_health:
                    direction = Body_rotate_right(larticle.body.direction)
                    pygame.draw.circle(Pygame_display, [255, 227, 15],
                                       [int((lx - direction[0] / 8) * scale + x),
                                        int((ly - direction[1] / 8) * scale + y)], int(scale / 10))
                pygame.draw.line(Pygame_display, kleur,
                                 [int((lx + larticle.body.direction[0] / 2) * scale + x),
                                  int((ly + larticle.body.direction[1] / 2) * scale + y)],
                                 [int(lx * scale + x), int(ly * scale + y)], int(scale / 5))

                if larticle.body.thinking and len(larticle.memory) > 0:
                    pygame.draw.circle(Pygame_display, [255, 227, 15],
                                       [int((lx - larticle.body.direction[0] / 8) * scale + x),
                                        int((ly - larticle.body.direction[1] / 8) * scale + y)], int(scale / 10))

                if larticle.body.memorizing:
                    pygame.draw.circle(Pygame_display, [255, 227, 15],
                                       [int((lx - larticle.body.direction[0] / 4) * scale + x),
                                        int((ly - larticle.body.direction[1] / 4) * scale + y)], int(scale / 10))

                if larticle.body.dna_saved != None:
                    direction = Body_rotate_left(larticle.body.direction)
                    pygame.draw.circle(Pygame_display, [255, 227, 15],
                                       [int((lx - direction[0] / 8) * scale + x),
                                        int((ly - direction[1] / 8) * scale + y)], int(scale / 10))
                    if larticle.body.dna_choose == 'other':
                        pygame.draw.circle(Pygame_display, [255, 227, 15],
                                           [int((lx - direction[0] / 4) * scale + x),
                                            int((ly - direction[1] / 4) * scale + y)], int(scale / 10))


            else:
                pygame.draw.line(Pygame_display, [0, 0, 0],
                                 [int((lx + larticle.body.direction[0] / 2) * scale + x),
                                  int((ly + larticle.body.direction[1] / 2) * scale + y)],
                                 [int(lx * scale + x), int(ly * scale + y)], int(scale / 5))



    for sun in handler.suns:
        sx, sy = recalc_blit(sun[0],sun[1],gx,gy)
        if int(sx * scale + x) < wy:
            pygame.draw.circle(Pygame_display, [255, 227, 15],
                               [int(sx * scale + x), int(sy * scale + y)],
                               int(scale), int(scale / 2))

    for name in doubles:
        print('Double: ', name)
        if name in handler.larticles:
            x, y = handler.larticles[name].body.x, handler.larticles[name].body.y
            s = str(x) + '_' + str(y)
            print('Pos: ', x, y)
            print('Age: ', handler.larticles[name].time_alive)
            print('Commands', handler.larticles[name].previous_memory)
            if pos[s] in handler.larticles:
                l = handler.larticles[pos[s]]
                print('  Larticle now at pos: ', l.name)
                print('  pos', l.body.x, l.body.y)
                print('  age', l.time_alive)
                print('  Commands', l.previous_memory)
            else:
                print('  Larticle at pos not found')
            print('Deleted.')
            handler.larticles.pop(name)
            handler.died += 1
        else:
            print('Not found.')

    handler.positions = pos


def voice_scale(s):
    m = max([s[0], s[1], s[2]])
    s1, s2, s3 = s
    if m != 0:
        c1 = float(s1 / m)
        c2 = float(s2 / m)
        c3 = float(s3 / m)
    else:
        c1, c2, c3 = 0, 0, 0
    return c1, c2, c3


def Handler_show_selected_larticle(display, handler, scale, x, y, gx, gy, mx=None, my=None):
    Pygame_display = display
    wx, wy = Pygame_display.get_size()
    show_x, show_y = int(wy), int(wy * 3 / 4)
    show_scale = 25
    s = 5
    dd = show_scale + s
    pygame.draw.rect(Pygame_display, [100, 100, 100], [show_x, show_y, 10 * dd, 7 * dd], 5)

    larticle = handler.selected_larticle

    body = larticle.body
    larticle_direction = (0, -1)
    lx, ly = recalc_blit(body.x, body.y, gx, gy)
    if 0 <= int(lx * scale + x) <= wy:
        pygame.draw.circle(Pygame_display, [211, 14, 237], [int(lx * scale + x),
                                                            int(ly * scale + y)],
                           int(scale * 3), int(scale))

    t = 0
    tt = show_scale + s
    d = 0
    ddd = 300
    sound_pos = [int(show_x + show_scale + s), int(show_y - 50)]
    s1, s2, s3 = larticle.brain.neurons['sense_sound_1'].potential, larticle.brain.neurons['sense_sound_2'].potential, \
                 larticle.brain.neurons['sense_sound_3'].potential
    sound = voice_scale([s1, s2, s3])
    sound = int(sound[0] * 250), int(sound[1] * 250), int(sound[2] * 250)
    pygame.draw.circle(Pygame_display, [sound[0], sound[0], sound[0]], sound_pos, int(show_scale / 2))
    pygame.draw.circle(Pygame_display, [sound[1], sound[1], sound[1]], [sound_pos[0] + show_scale + s, sound_pos[1]],
                       int(show_scale / 2))
    pygame.draw.circle(Pygame_display, [sound[2], sound[2], sound[2]],
                       [sound_pos[0] + 2 * (show_scale + s), sound_pos[1]], int(show_scale / 2))

    pygame.draw.circle(Pygame_display, [250, 250, 250], sound_pos, int(show_scale / 2), 5)
    pygame.draw.circle(Pygame_display, [250, 250, 250], [sound_pos[0] + show_scale + s, sound_pos[1]],
                       int(show_scale / 2), 5)
    pygame.draw.circle(Pygame_display, [250, 250, 250],
                       [sound_pos[0] + 2 * (show_scale + s), sound_pos[1]], int(show_scale / 2), 5)

    textsurface = myfont10.render('Sound 1', False, [250, 250, 250])
    Pygame_display.blit(textsurface, [int(sound_pos[0] - show_scale), int(sound_pos[1] + show_scale)])
    s1 = str(s1)
    if len(s1) > 5:
        s1 = s1[:5]
    s2 = str(s2)
    if len(s2) > 5:
        s2 = s2[:5]
    s3 = str(s3)
    if len(s3) > 5:
        s3 = s3[:5]
    textsurface = myfont10.render(str(s1), False, [250, 250, 250])
    Pygame_display.blit(textsurface, [int(sound_pos[0] - show_scale), int(sound_pos[1] + 2 * show_scale)])

    textsurface = myfont10.render('Sound 2', False, [250, 250, 250])
    Pygame_display.blit(textsurface, [int(sound_pos[0] + show_scale + s - show_scale / 2), sound_pos[1] + show_scale])
    textsurface = myfont10.render(str(s2), False, [250, 250, 250])
    Pygame_display.blit(textsurface,
                        [int(sound_pos[0] + show_scale + s - show_scale / 2), sound_pos[1] + 2 * show_scale])

    textsurface = myfont10.render('Sound 3', False, [250, 250, 250])
    Pygame_display.blit(textsurface, [int(sound_pos[0] + 2 * (show_scale + s)), sound_pos[1] + show_scale])
    textsurface = myfont10.render(str(s3), False, [250, 250, 250])
    Pygame_display.blit(textsurface, [int(sound_pos[0] + 2 * (show_scale + s)), sound_pos[1] + 2 * show_scale])

    if larticle.previous_memory != []:
        perception = larticle.previous_memory[1]
        commands = larticle.previous_memory[0]
        for command in list(sorted(commands.keys())):
            if command == 'command_eat' and command == 'command_split':
                if commands[command] > 0.5:
                    kleur = [100, 250, 100]
                else:
                    kleur = [250, 100, 100]
            elif command == 'command_voice_1_value' or command == 'command_voice_2_value' or command == 'command_voice_3_value':
                if commands[command] != 0:
                    kleur = [100, 250, 100]
                else:
                    kleur = [250, 100, 100]
            else:
                if commands[command] > 0.5:
                    kleur = [100, 250, 100]
                else:
                    kleur = [250, 100, 100]
            st = command
            if (command == 'command_eat' or command == 'command_move') and larticle.body.regenerating:
                st += ' (Not allowed)'
            if t * tt > wy - 300:
                d += 1
                t = 0
            px, py = int(wy + 350 + d * ddd), int(200 + t * tt)
            pygame.draw.circle(Pygame_display, kleur,
                               [px, py], int(show_scale / 2))
            textsurface = myfont12.render(str(st), False, kleur)
            Pygame_display.blit(textsurface, [px + show_scale, py - show_scale / 2])
            t += 1

        p = Body_get_surounding_pos(5, 5, [0, -1])
        surounding = Handler_get_surrounding_positions(handler, larticle)

        for i in p:
            kleur = [250, 250, 250]
            if perception['sense_' + i] == 0:
                pygame.draw.circle(Pygame_display, kleur, [show_x + dd * p[i][0], show_y + dd * p[i][1]],
                                   int(show_scale / 2), 5)
            else:
                pygame.draw.circle(Pygame_display, kleur, [show_x + dd * p[i][0], show_y + dd * p[i][1]],
                                   int(show_scale / 2))

        d = 1
        d += perception['see_distance_0']
        d += perception['see_distance_1']
        d += perception['see_distance_2']
        c = [perception['see_red'], perception['see_green'], perception['see_blue']]
        if c != [0, 0, 0]:
            colour = map_color(c)
            pygame.draw.circle(Pygame_display, colour,
                               [int(show_x + d * larticle_direction[0] * dd + 5 * dd),
                                int(show_y + d * larticle_direction[1] * dd + 5 * dd)], int(show_scale / 2 + 2))

            if perception['see_looking']:
                pygame.draw.line(Pygame_display, [0, 0, 0],
                                 [int(show_x + 5 * dd),
                                  int(show_y + d * larticle_direction[1] * dd + 5 * dd)], [int(show_x + 5 * dd),
                                                                                           int(show_y + d *
                                                                                               larticle_direction[
                                                                                                   1] * dd + 5 * dd + show_scale / 2)],
                                 5)

        k = map_color(larticle.body.colour)
        pygame.draw.circle(Pygame_display, k,
                           [show_x + 5 * dd, show_y + 5 * dd],
                           int(show_scale / 2))

        if larticle.body.talking:
            kleur = [250, 100, 250]
        else:
            kleur = [0, 0, 0]

        d = 5

        if larticle.body.frozen:
            pygame.draw.circle(Pygame_display, [250, 250, 250],
                               [show_x + 5 * dd, show_y + 5 * dd],
                               int(show_scale), d)

        k = [250, 250, 250]

        if larticle.body.give_health:
            direction = Body_rotate_right(larticle_direction)
            pygame.draw.circle(Pygame_display, k,
                               [int(show_x + 5 * dd - direction[0] / 6 * show_scale),
                                int(show_y + 5 * dd - direction[1] / 6 * show_scale)], int(show_scale / 10))
        pygame.draw.line(Pygame_display, kleur,
                         [int(show_x + 5 * dd + larticle_direction[0] / 2 * show_scale),
                          int(show_y + 5 * dd + larticle_direction[1] / 2 * show_scale)],
                         [show_x + 5 * dd, show_y + 5 * dd], int(show_scale / 5))

        if larticle.body.thinking and len(larticle.memory) > 0:
            pygame.draw.circle(Pygame_display, k,
                               [int(show_x + 5 * dd - larticle_direction[0] / 6 * show_scale),
                                int(show_y + 5 * dd - larticle_direction[1] / 6 * show_scale)], int(show_scale / 10))

        if larticle.body.memorizing:
            pygame.draw.circle(Pygame_display, k,
                               [int(show_x + 5 * dd - larticle_direction[0] / 3 * show_scale),
                                int(show_y + 5 * dd - larticle_direction[1] / 3 * show_scale)], int(show_scale / 10))

        if larticle.body.dna_saved != None:
            direction = Body_rotate_left(larticle_direction)
            pygame.draw.circle(Pygame_display, k,
                               [int(show_x + 5 * dd - direction[0] / 6 * show_scale),
                                int(show_y + 5 * dd - direction[1] / 6 * show_scale)], int(show_scale / 10))
            if larticle.body.dna_choose == 'other':
                pygame.draw.circle(Pygame_display, k,
                                   [int(show_x + 5 * dd - direction[0] / 3 * show_scale),
                                    int(show_y + 5 * dd - direction[1] / 3 * show_scale)], int(show_scale / 10))


def Handler_blits_selected_larticle(display, handler, scale, x, y, gx, gy, mx=None, my=None):
    pygame_windows_size = constant_screensize_x,constant_screensize_y
    Pygame_display = display
    wx, wy = Pygame_display.get_size()

    selected = handler.selected_larticle

    dy = 120
    if selected != None:
        body = selected.body
        brain = selected.brain
        Brain_get_dna(selected)
        lx, ly = recalc_blit(body.x, body.y, gx, gy)
        if 0 <= int(lx * scale + x) <= wy:
            pygame.draw.circle(Pygame_display, [211, 14, 237], [int(lx * scale + x),
                                                                int(ly * scale + y)],
                               int(scale * 3), int(scale))
        properties = Handler_get_larticle_properties(selected)
        i = 0
        for prop in list(sorted(properties.keys())):
            i += 1
            textsurface = myfont12.render(str(prop) + ': ' + str(properties[prop]), False, (250, 250, 250))
            Pygame_display.blit(textsurface, (pygame_windows_size[1] + 20, dy + (i + 1) * 15))

        r = 225
        t = len(brain.neurons)
        tt = 0
        tttt = 0
        tttttt = 0
        pos = {}
        dx = 250
        for neuron in sorted(brain.neurons.keys()):

            pos[neuron] = [r * math.cos(2 * math.pi * tt / t) + wx - r - 150,
                           r * math.sin(2 * math.pi * tt / t) + wy - r - 50]
            tt += 1
            n = brain.neurons[neuron].name
            if n.split('_')[0] != 'hidden':
                p = brain.neurons[neuron].potential
                if n != 'command_split' and n != 'command_eat':
                    if p > 0.5:
                        kleur = [100, 250, 100]
                    else:
                        kleur = [250, 100, 100]
                else:
                    if p >= 0.5:
                        kleur = [100, 250, 100]
                    else:
                        kleur = [250, 100, 100]
                textsurface = myfont12.render(
                    n + ' = ' + str(p)[0:6],
                    False,
                    kleur)
                if n in body_perception:
                    Pygame_display.blit(textsurface, (wy + dx, dy + 12 * tttt))
                    tttt += 1
                elif n in body_commands:
                    Pygame_display.blit(textsurface, (wy + 2 * dx - 20, dy + 12 * tttttt))
                    tttttt += 1

        for name1, name2, weight in brain.dna:
            kleur = [0, 250, 0]
            if weight < 0:
                kleur = [250, 0, 0]
            if name1 in pos and name2 in pos:
                pygame.draw.line(Pygame_display, kleur, pos[name1], pos[name2], int(abs(weight) + 1))
            else:
                print(name1, name2, weight)

        size = 5
        for name in pos:
            if mx != None and my != None:
                if pos[name][0] - size < mx < pos[name][0] + size and pos[name][1] - size < my < pos[name][
                    1] + size:
                    handler.selected_neuron = brain.neurons[name]
            kleur = [250, 100, 100]
            if name != 'command_eat' or name != 'command_split':
                if brain.neurons[name].potential > 0.5:
                    kleur = [100, 250, 100]
            else:
                if brain.neurons[name].potential >= 0.5:
                    kleur = [100, 250, 100]
            pygame.draw.circle(Pygame_display, kleur,
                               [int(pos[name][0]), int(pos[name][1])],
                               int(size))

        if handler.selected_neuron != None:

            if handler.selected_neuron.name in body_perception:
                kleur = [100, 250, 100]
            elif handler.selected_neuron.name in body_commands:
                kleur = [250, 100, 100]
            else:
                kleur = [100, 100, 250]
            textsurface = myfont12.render(str(handler.selected_neuron.name) + ': ' + str(
                brain.neurons[handler.selected_neuron.name].potential), False,
                                          kleur)
            Pygame_display.blit(textsurface, (wy + 10, wy - 30))

            if handler.selected_neuron.name in pos:
                pygame.draw.circle(Pygame_display, [250, 250, 250],
                                   [int(pos[handler.selected_neuron.name][0]),
                                    int(pos[handler.selected_neuron.name][1])],
                                   int(size * 3), 4)
            connections = Neuron_get_connections(brain.neurons[handler.selected_neuron.name])
            names = []
            for name1, name2, weight in connections:
                names.append(name2)
                pygame.draw.line(Pygame_display, [250, 0, 250], pos[name1], pos[name2], 3)
            names2 = []
            for name in names:
                conn = Neuron_get_connections(brain.neurons[name])
                for name1, name2, weight in conn:
                    names2.append(name2)
                    pygame.draw.line(Pygame_display, [250, 0, 250], pos[name1], pos[name2], 3)
            names3 = []
            for name in names2:
                conn = Neuron_get_connections(brain.neurons[name])
                for name1, name2, weight in conn:
                    names3.append(name2)
                    pygame.draw.line(Pygame_display, [250, 0, 250], pos[name1], pos[name2], 3)
            for name in names3:
                conn = Neuron_get_connections(brain.neurons[name])
                for name1, name2, weight in conn:
                    pygame.draw.line(Pygame_display, [250, 0, 250], pos[name1], pos[name2], 3)


class Simulation():
    def __init__(self, display, clock):
        pygame_windows_size = constant_screensize_x,constant_screensize_y
        self.initialized = False
        self.beginscale = float(pygame_windows_size[1] / (constant_grid_size + 1))
        self.scale = self.beginscale
        self.handler = Handler(display)
        self.saved_larticles = {}
        self.time0 = time.time()
        self.running = True
        self.blits = False
        self.memory = []
        self.fullscreen = False
        self.autoselect = False
        self.previous_handler = None
        self.Pygame_display = display
        self.Pygame_clock = clock
        self.starts = 0

        l = 20
        b = 50
        self.main_button = [pygame_windows_size[0] - b, pygame_windows_size[1] - l, b, l]

    def Simulation_reset(self):
        pygame_windows_size = constant_screensize_x,constant_screensize_y
        self.handler = Handler()
        self.beginscale = float(pygame_windows_size[1] / (constant_grid_size + 1))
        self.scale = self.beginscale

    def Simulation_run(self):
        Pygame_display = self.Pygame_display
        Pygame_clock = self.Pygame_clock
        pygame_windows_size = constant_screensize_x,constant_screensize_y
        self.initialized = True
        x = 0
        y = 0
        gx = 0
        gy = 0

        dxr = 0
        dxl = 0
        dyu = 0
        dyd = 0
        dgxr = 0
        dgxl = 0
        dgyu = 0
        dgyd = 0

        speed = 4 * self.scale
        speed2 = 1
        scrollspeed = 0.5
        stop = False
        checking = False

        while not stop:

            if len(self.handler.larticles) <= 0:
                self.handler = Handler()
                Handler_initialize(Pygame_display, self.handler)
                self.starts += 1

            if len(self.handler.random_larticles) <= handler_random_larticles_amount and not checking:
                checking = True
                print('Appending buffer.')
                p = subprocess.Popen('python create_random_larticles.py', creationflags=0x08000000)

            if checking:
                r = p.poll()
                if r != None:
                    file = open('Random_larticles.pickle', 'rb')
                    l = pickle.load(file)
                    self.handler.random_larticles += l
                    file.close()
                    checking = False
                    p.kill()
                    print('Buffer appended.')

            time0 = time.time()

            mx = None
            my = None

            gx, gy = recalc_grid(gx, gy)

            events = pygame.event.get()
            for event in events:

                if event.type == pygame.QUIT:
                    stop = True
                    pygame.quit()
                    quit()

                if event.type == pygame.KEYDOWN:

                    if event.key == pygame.K_HOME:
                        self.Simulation_reset()
                    elif event.key == pygame.K_k:
                        Handler_kill_selected(self.handler)
                    elif event.key == pygame.K_s:
                        dgyd = speed2
                    elif event.key == pygame.K_w:
                        dgyu = -speed2
                    elif event.key == pygame.K_a:
                        dgxl = -speed2
                    elif event.key == pygame.K_d:
                        dgxr = speed2
                    elif event.key == pygame.K_f:
                        Handler_run(self.handler)
                    elif event.key == pygame.K_r:
                        gx, gy = 0, 0
                    elif event.key == pygame.K_y:
                        self.autoselect = not self.autoselect

                    elif event.key == pygame.K_END:
                        self.scale = self.beginscale
                        x = 0
                        y = 0

                    elif event.key == pygame.K_ESCAPE:
                        stop = True
                        pygame.quit()
                        quit()
                    elif event.key == pygame.K_INSERT:
                        self.running = not self.running

                    elif event.key == pygame.K_PAGEUP:
                        self.blits = not self.blits

                    elif event.key == pygame.K_PAGEDOWN:
                        Handler_set_visual(self.handler)

                    elif event.key == pygame.K_KP_ENTER:
                        stop = True

                    elif event.key == pygame.K_DOWN:
                        dyd = speed
                    elif event.key == pygame.K_UP:
                        dyu = -speed
                    elif event.key == pygame.K_LEFT:
                        dxl = -speed
                    elif event.key == pygame.K_RIGHT:
                        dxr = speed

                    elif event.key == pygame.K_LCTRL:
                        self.fullscreen = not self.fullscreen
                        if self.fullscreen:
                            pygame.display.set_mode(Pygame_display.get_size(), pygame.FULLSCREEN)
                        else:
                            pygame.display.set_mode(Pygame_display.get_size(), pygame.RESIZABLE)

                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_DOWN:
                        dyd = 0
                    elif event.key == pygame.K_UP:
                        dyu = -0
                    elif event.key == pygame.K_LEFT:
                        dxl = -0
                    elif event.key == pygame.K_RIGHT:
                        dxr = 0
                    elif event.key == pygame.K_s:
                        dgyd = 0
                    elif event.key == pygame.K_w:
                        dgyu = 0
                    elif event.key == pygame.K_a:
                        dgxl = 0
                    elif event.key == pygame.K_d:
                        dgxr = 0


                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        mx, my = pygame.mouse.get_pos()
                    elif event.button == 3:
                        Handler_reset_selected(self.handler)
                    elif event.button == 4 and self.scale <= 50:
                        self.scale += scrollspeed
                    elif event.button == 5 and self.scale > 1 + scrollspeed:
                        self.scale -= scrollspeed

            x -= dxl + dxr
            y -= dyd + dyu
            gx -= dgxl + dgxr
            gy -= dgyd + dgyu

            scale = self.scale

            Pygame_display.fill(zwart)

            d = 3
            pygame.draw.rect(Pygame_display, [150, 150, 150],
                             [x, y, int((constant_grid_size + 1) * scale - d),
                              int((constant_grid_size + 1) * scale - d)],
                             d)
            pygame.draw.line(Pygame_display, [150, 150, 150], [pygame_windows_size[1], 0],
                             [pygame_windows_size[1], pygame_windows_size[1]], 3)

            if self.running:
                Handler_run(self.handler, self.autoselect)
            if self.blits:
                Handler_blits_map(Pygame_display, self.handler, self.scale, x, y, gx, gy, mx, my)
                Handler_blits_frame(Pygame_display, self.handler, self.scale, x, y, gx, gy, mx, my)
                if self.handler.selected_larticle != None:
                    Handler_blits_selected_larticle(Pygame_display, self.handler, self.scale, x, y, gx, gy, mx, my)
            else:
                Handler_blits_map(Pygame_display, self.handler, self.scale, x, y, gx, gy, mx, my)
                Handler_blits_frame(Pygame_display, self.handler, self.scale, x, y, gx, gy, mx, my)
                if self.handler.selected_larticle != None:
                    Handler_show_selected_larticle(Pygame_display, self.handler, self.scale, x, y, gx, gy, mx, my)

            time1 = time.time()
            tijd = time1 - time0
            d = 150
            textsurface = myfont12.render('Runtime: ' + str(tijd), False, (250, 250, 250))
            Pygame_display.blit(textsurface, (pygame_windows_size[0] - d, 0))
            textsurface = myfont12.render('Elapsed: ' + str((time.time() - self.time0)), False, (250, 250, 250))
            Pygame_display.blit(textsurface, (pygame_windows_size[0] - d, 15))
            textsurface = myfont12.render('Starts: ' + str(self.starts), False, (250, 250, 250))
            Pygame_display.blit(textsurface, (pygame_windows_size[0] - d, 30))
            textsurface = myfont12.render('Random Brains: ' + str(len(self.handler.random_larticles)), False,
                                          (250, 250, 250))
            Pygame_display.blit(textsurface, (pygame_windows_size[0] - d, 45))
            textsurface = myfont12.render('Scale: ' + str(self.scale), False,
                                          (250, 250, 250))
            Pygame_display.blit(textsurface, (pygame_windows_size[0] - d, 60))
            textsurface = myfont12.render('Autoselect: ' + str(self.autoselect), False,
                                          (250, 250, 250))
            Pygame_display.blit(textsurface, (pygame_windows_size[0] - d, 75))

            pygame.draw.rect(Pygame_display, rood, self.main_button)
            textsurface = myfont12.render('Main', False, (0, 0, 0))
            Pygame_display.blit(textsurface, (self.main_button))
            if mx != None and my != None:
                if self.main_button[0] < mx < self.main_button[0] + self.main_button[2]:
                    if self.main_button[1] < my < self.main_button[1] + self.main_button[3]:
                        stop = True

            pygame.display.update()
            if self.running:
                Pygame_clock.tick()
            else:
                Pygame_clock.tick(30)
