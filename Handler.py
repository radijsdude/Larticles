import random
from Larticle import Larticle
import pygame
import math

pygame.font.init()
myfont = pygame.font.SysFont('Comic Sans MS', 12)


class Handler():
    def __init__(self, display, size):
        print(' ')
        print(' ')
        print('Initializing Handler.')
        print(' ')
        print(' ')
        self.display = display
        self.count = 0
        self.died = 0
        self.solardeaths = 0
        self.epoch = 0
        self.splits = 0
        self.larticles = {}
        self.random_larticles = []
        self.gridsize = size
        self.mutationrate = 90

        self.min_larticles = 0
        self.previous_amount_kills = 0
        self.amount_larticles = int(1000 / 10000 * self.gridsize ** 2)
        self.amount_suns = int(2 / 10000 * self.gridsize ** 2)

        self.eaters = 0
        self.stupids = 0
        self.regenerators = 0
        self.newbies = 0

        self.click_error = 0.8

        if self.amount_suns < 2:
            self.amount_suns = 2

        self.suns = []
        self.positions = {}

        self.visual = False

        self.selected_larticle = None
        self.selected_neuron = None

        self.starts = 0

        self.random_larticles_amount = 500

        self.initialize()

        print(' ')
        print(' ')
        print('Creating random Larticles')
        print(' ')
        print(' ')

        self.random_larticles = self.create_random_larticles(self.random_larticles_amount)

        print(' ')
        print(' ')
        print('Creating random Larticles done.')
        print(' ')
        print(' ')


        print(' ')
        print('Handler Initializing Succesfull.')
        print(' ')


    def create_random_larticles(self,n):
        random_larticles = []
        for i in range(int(n)):
            l = Larticle('Random' + str(i), self.gridsize)
            random_larticles.append(l)
        return random_larticles



    def initialize(self):
        print(' ')
        print('Placing Larticles.')
        print(' ')
        self.starts += 1
        perc = 0
        for i in range(self.amount_larticles):
            l = Larticle('Begin_' + str(i), self.gridsize)
            self.place_larticle(l)
            if i % int(self.amount_larticles / 10) == 0:
                print(str(perc), '%')
                perc += 10

        self.get_all_positions()
        print(' ')
        print('Placing Larticles Done.')
        print(' ')

    def get_all_positions(self):
        pos = {}
        doubles = []
        for name in self.larticles:
            x, y = int(self.larticles[name].body.x), int(self.larticles[name].body.y)
            s = str(x) + '_' + str(y)
            if s not in pos:
                pos[s] = name
            else:
                print('Double: ', name)
                doubles.append(name)
        for name in doubles:
            if name in self.larticles:
                self.larticles.pop(name)
        self.positions = pos

    def get_positions(self, larticle):
        xs, ys = int(larticle.body.x + 2 * larticle.body.direction[0]), int(
            larticle.body.y + 2 * larticle.body.direction[1])
        pos = larticle.body.get_surounding_pos()
        ss = [str(xs) + '_' + str(ys)]
        for p in pos:
            s = str(pos[p][0]) + '_' + str(pos[p][1])
            ss.append(s)
        l = {}
        for s in ss:
            if s in self.positions:
                if self.positions[s] in self.larticles:
                    l[self.larticles[self.positions[s]].name] = self.larticles[self.positions[s]]
        return l

    def check_in(self, x, y):
        t = True
        if not (0 < int(x) < self.gridsize and 0 < int(y) < self.gridsize):
            t = False
        return t

    def check_pos(self, x, y):

        t = True
        s = str(int(x)) + '_' + str(int(y))
        if s in self.positions:
            t = False
        return t

    def check_around(self, x, y):
        p1x, p1y = x + 1, y
        p2x, p2y = x - 1, y
        p3x, p3y = x, y + 1
        p4x, p4y = x, y - 1
        r = [[int(x), int(y)], [int(p1x), int(p1y)], [int(p2x), int(p2y)], [int(p3x), int(p3y)], [int(p4x), int(p4y)]]
        for pos in r:
            s = str(int(pos[0])) + '_' + str(int(pos[1]))
            if s in self.positions:
                return False
        return True

    def place_larticle(self, larticle):
        t = True
        tt = 0
        ranx = None
        rany = None
        while t:
            tt += 1
            ranx = random.randrange(0, int(self.gridsize))
            rany = random.randrange(0, int(self.gridsize))
            r1 = self.check_around(ranx, rany)
            r2 = self.check_in(ranx, rany)
            if r1 and r2:
                self.count += 1
                larticle.body.x = int(ranx)
                larticle.body.y = int(rany)
                self.positions[str(ranx) + '_' + str(rany)] = larticle.name
                self.larticles[larticle.name] = larticle
                t = False
            if tt > 50:
                print('larticle handler place larticle while break')
                break
        return ranx, rany

    def run(self):
        print(self.epoch)
        self.eaters = 0
        self.stupids = 0
        self.regenerators = 0
        self.newbies = 0
        self.epoch += 1
        died = []
        for name in list(self.larticles.keys()):

            larticle = self.larticles[name]

            x0 = int(larticle.body.x)
            y0 = int(larticle.body.y)
            s0 = str(x0) + '_' + str(y0)

            if [x0, y0] not in self.suns:

                if larticle.body.health > 0:

                    if larticle.body.color == [1, 0, 0]:
                        self.eaters += 1
                    elif larticle.body.color == [0, 1, 0]:
                        self.stupids += 1
                    elif larticle.body.color == [0, 0, 1]:
                        self.regenerators += 1
                    elif larticle.body.color == [1, 1, 1]:
                        self.newbies += 1

                    larticles = self.get_positions(larticle)

                    r = larticle.doe(larticles)

                    x = int(larticle.body.x)
                    y = int(larticle.body.y)
                    s = str(x) + '_' + str(y)

                    if x0 != x or y0 != y:
                        self.positions.pop(s0)
                        self.positions[s] = larticle.name

                    if 'split' in r:

                        if larticle.body.regenerating:
                            dx, dy = int(x + larticle.body.direction[0]), int(y + larticle.body.direction[1])
                        else:
                            dx, dy = int(x - larticle.body.direction[0]), int(y - larticle.body.direction[1])

                        if self.check_in(dx, dy) and self.check_pos(dx, dy):
                            self.count += 1
                            self.splits += 1
                            larticle.splits += 1
                            name = 'split_' + str(larticle.splits) + '_' + str(self.epoch) + '_' + str(self.count)

                            r = random.randrange(0, 100)
                            if r <= self.mutationrate:
                                r2 = random.randrange(0,100)
                                if r2 <= 90:
                                    l = Larticle(name, self.gridsize, larticle.brain.dna)
                                    l.mutate()
                                else:
                                    n = 'Random_' + name
                                    l = self.random_larticles[0]
                                    l.name = n
                                    l.body.gridsize = self.gridsize
                                    self.random_larticles.pop(0)
                            else:
                                l = Larticle(name, self.gridsize, larticle.brain.dna)
                            l.body.x = dx
                            l.body.y = dy
                            self.larticles[l.name] = l
                            self.positions[str(dx) + '_' + str(dy)] = l.name

                else:
                    died.append(name)
            else:
                died.append(name)
                self.solardeaths += 1

        self.suns = []
        for i in range(self.amount_suns):
            self.suns.append([random.randrange(0, self.gridsize), random.randrange(0, self.gridsize)])

        for name in died:
            self.died += 1
            self.larticles.pop(name)
        if len(self.larticles) <= 0:
            self.initialize()

    def set_visual(self):
        self.visual = not self.visual

    def reset_selected(self):
        self.selected_larticle = None
        self.selected_neuron = None

    def kill_selected(self):
        if self.selected_larticle.name in self.larticles:
            self.larticles.pop(self.selected_larticle.name)

    def map_color(self, color):
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

    def state_color(self,larticle):
        c = larticle.body.state * 150
        colour = list(larticle.body.color)
        colour = self.map_color(colour)
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


    def blits(self, scale, x, y, mx=None, my=None):

        pos = {}
        doubles = []

        wx, wy = self.display.get_size()

        pygame.draw.rect(self.display, [0, 0, 0], [wy, - 10, wx + 10, wy + 10])
        pygame.draw.rect(self.display, [150, 150, 150], [wy, - 10, wx + 10, wy + 10], 3)

        textsurface = myfont.render('Epoch: ' + str(self.epoch), False, (250, 250, 250))
        self.display.blit(textsurface, (wy + 10, 0))

        textsurface = myfont.render('Larticles: ' + str(len(self.larticles)), False, (250, 250, 250))
        self.display.blit(textsurface, (wy + 10, 15))

        textsurface = myfont.render('Died: ' + str(self.died), False, (250, 250, 250))
        self.display.blit(textsurface, (wy + 10, 30))

        textsurface = myfont.render('Solar Deaths: ' + str(self.solardeaths), False, (250, 250, 250))
        self.display.blit(textsurface, (wy + 10, 45))

        textsurface = myfont.render('Splits: ' + str(self.splits), False, (250, 250, 250))
        self.display.blit(textsurface, (wy + 10, 60))

        textsurface = myfont.render('Deaths: ' + str(self.died - self.previous_amount_kills), False, (255, 255, 255))
        self.display.blit(textsurface, (wy + 170, 0))
        self.previous_amount_kills = self.died

        textsurface = myfont.render('Newbies: ' + str(self.newbies), False, (250, 250, 250))
        self.display.blit(textsurface, (wy + 170, 15))

        textsurface = myfont.render('Eaters: ' + str(self.eaters), False, (250, 100, 100))
        self.display.blit(textsurface, (wy + 170, 30))

        textsurface = myfont.render('Stupids: ' + str(self.stupids), False, (100, 250, 100))
        self.display.blit(textsurface, (wy + 170, 45))

        textsurface = myfont.render('Regenerators: ' + str(self.regenerators), False, (100, 100, 250))
        self.display.blit(textsurface, (wy + 170, 60))

        textsurface = myfont.render('Surface Area: ' + str(self.gridsize ** 2), False, (250, 250, 250))
        self.display.blit(textsurface, (wy + 340, 0))

        for sun in self.suns:
            if int(sun[0] * scale + x) < wy:
                pygame.draw.circle(self.display, [255, 227, 15],
                                   [int(sun[0] * scale + x), int(sun[1] * scale + y)],
                                   int(scale), int(scale / 2))

        for name in self.larticles:
            larticle = self.larticles[name]
            lx = int(larticle.body.x)
            ly = int(larticle.body.y)
            ls = str(lx) + '_' + str(ly)
            if ls not in pos:
                pos[ls] = name
            else:
                doubles.append(name)

            if mx != None and my != None:
                if mx < wy:
                    if abs(lx * scale - self.click_error * scale) <= mx - x <= abs(
                                            lx * scale + self.click_error * scale) and abs(
                                        ly * scale - self.click_error * scale) <= my - y <= abs(
                                        ly * scale + self.click_error * scale):
                        self.selected_larticle = larticle
            if - 50 < lx * scale + x < wy and - 50 < ly * scale + y < wy:
                if not self.visual:
                    k = self.map_color(larticle.body.color)
                else:
                    k = self.state_color(larticle)
                pygame.draw.circle(self.display, k,
                                   [int(lx * scale + x), int(ly * scale + y)],
                                   int(scale / 2))
                if self.visual:
                    if larticle.body.talking:
                        kleur = [250,100,250]
                    else:
                        kleur = [0,0,0]

                    if larticle.body.give_health:
                        pygame.draw.circle(self.display, [250, 250, 250],
                                           [int(lx * scale + x), int(ly * scale + y)],
                                           int(scale/2),1)
                    pygame.draw.line(self.display, kleur,
                                     [int((lx + larticle.body.direction[0] / 2) * scale + x),
                                      int((ly + larticle.body.direction[1] / 2) * scale + y)],
                                     [int(lx * scale + x), int(ly * scale + y)], int(scale/5))
                else:
                    pygame.draw.line(self.display, [0,0,0],
                                     [int((lx + larticle.body.direction[0] / 2) * scale + x),
                                      int((ly + larticle.body.direction[1] / 2) * scale + y)],
                                     [int(lx * scale + x), int(ly * scale + y)], int(scale/5))









        for name in doubles:
            print('Double: ', name)
            if name in self.larticles:
                print('Deleted.')
                self.larticles.pop(name)
                self.died += 1
            else:
                print('Not found.')

        self.positions = pos

        dy = 100
        if self.selected_larticle != None:
            if 0 <= int(self.selected_larticle.body.x * scale + x) <= wy:
                pygame.draw.circle(self.display, [211, 14, 237], [int(self.selected_larticle.body.x * scale + x),
                                                                  int(self.selected_larticle.body.y * scale + y)],
                                   int(scale * 3), int(scale))
            textsurface = myfont.render('Name: ' + str(self.selected_larticle.name), False, (250, 250, 250))
            self.display.blit(textsurface, (wy + 10, dy))
            textsurface = myfont.render('Splits: ' + str(self.selected_larticle.splits), False, (250, 250, 250))
            self.display.blit(textsurface, (wy + 10, dy + 15))
            textsurface = myfont.render('Health: ' + str(int(self.selected_larticle.body.health)), False,
                                        (250, 250, 250))
            self.display.blit(textsurface, (wy + 10, dy + 30))
            textsurface = myfont.render('Age: ' + str(self.selected_larticle.time_alive), False, (250, 250, 250))
            self.display.blit(textsurface, (wy + 10, dy + 45))
            textsurface = myfont.render(
                'Pos: ' + str(self.selected_larticle.body.x) + ' ' + str(self.selected_larticle.body.y), False,
                (250, 250, 250))
            self.display.blit(textsurface, (wy + 10, dy + 60))
            textsurface = myfont.render('Drain Body: ' + str(abs(self.selected_larticle.body.body_drain)), False,
                                        (250, 250, 250))
            self.display.blit(textsurface, (wy + 10, dy + 75))
            textsurface = myfont.render('Drain Brain: ' + str(self.selected_larticle.brain_drain), False,
                                        (250, 250, 250))
            self.display.blit(textsurface, (wy + 10, dy + 90))
            drain = abs(self.selected_larticle.brain_drain) + abs(self.selected_larticle.body.body_drain)
            textsurface = myfont.render('Drain Total: ' + str(drain)[:6], False,
                                        (250, 250, 250))
            self.display.blit(textsurface, (wy + 10, dy + 105))
            textsurface = myfont.render(
                'Regen: ' + str(self.selected_larticle.body.regen),
                False,
                (250, 250, 250))
            self.display.blit(textsurface, (wy + 10, dy + 120))
            textsurface = myfont.render(
                'Kills: ' + str(self.selected_larticle.body.kills),
                False,
                (250, 250, 250))
            self.display.blit(textsurface, (wy + 10, dy + 135))
            textsurface = myfont.render(
                'Direction: ' + str(self.selected_larticle.body.direction),
                False,
                (250, 250, 250))
            self.display.blit(textsurface, (wy + 10, dy + 150))
            textsurface = myfont.render(
                'Dna length: ' + str(len(self.selected_larticle.brain.dna)),
                False,
                (250, 250, 250))
            self.display.blit(textsurface, (wy + 10, dy + 165))
            textsurface = myfont.render(
                'Neurons amount: ' + str(len(self.selected_larticle.brain.all_neurons)),
                False,
                (250, 250, 250))
            self.display.blit(textsurface, (wy + 10, dy + 180))
            textsurface = myfont.render(
                'Talking: ' + str(self.selected_larticle.body.talking),
                False,
                (250, 250, 250))
            self.display.blit(textsurface, (wy + 10, dy + 195))
            textsurface = myfont.render(
                'State: ' + str(self.selected_larticle.body.state),
                False,
                (250, 250, 250))
            self.display.blit(textsurface, (wy + 10, dy + 210))

            r = 225
            t = len(self.selected_larticle.brain.all_neurons)
            tt = 0
            tttt = 0
            tttttt = 0
            pos = {}
            dx = 220
            for neuron in sorted(self.selected_larticle.brain.all_neurons.keys()):

                pos[neuron] = [r * math.cos(2 * math.pi * tt / t) + wx - r - 150,
                               r * math.sin(2 * math.pi * tt / t) + wy - r - 100]
                tt += 1
                n = self.selected_larticle.brain.all_neurons[neuron].name
                if n.split('_')[0] != 'hidden':
                    p = self.selected_larticle.brain.all_neurons[neuron].potential
                    if p > 0.5:
                        kleur = [100,250,100]
                    else:
                        kleur = [250,100,100]
                    textsurface = myfont.render(
                        n + ' = ' + str(p)[0:6],
                        False,
                        kleur)
                    if n in self.selected_larticle.brain.input_names:
                        self.display.blit(textsurface, (wy + dx, dy + 12 * tttt))
                        tttt += 1
                    else:
                        self.display.blit(textsurface, (wy + 2 * dx - 20, dy + 12 * tttttt))
                        tttttt += 1

            for name1, name2, weight in self.selected_larticle.brain.dna:
                kleur = [0, 250, 0]
                if weight < 0:
                    kleur = [250, 0, 0]
                if name1 in pos and name2 in pos:
                    pygame.draw.line(self.display, kleur, pos[name1], pos[name2], int(abs(weight) + 1))
                else:
                    print(name1, name2, weight)

            size = 5
            for name in pos:
                if mx != None and my != None:
                    if pos[name][0] - size < mx < pos[name][0] + size and pos[name][1] - size < my < pos[name][
                        1] + size:
                        self.selected_neuron = self.selected_larticle.brain.all_neurons[name]
                kleur = [100, 100, 250]
                if name in self.selected_larticle.brain.input_names:
                    kleur = [100, 250, 100]
                elif name in self.selected_larticle.brain.output_names:
                    kleur = [250, 100, 100]
                pygame.draw.circle(self.display, kleur,
                                   [int(pos[name][0]), int(pos[name][1])],
                                   int(size))

            if self.selected_neuron != None:

                if self.selected_neuron.name in self.selected_larticle.brain.input_names:
                    kleur = [100, 250, 100]
                elif self.selected_neuron.name in self.selected_larticle.brain.output_names:
                    kleur = [250, 100, 100]
                else:
                    kleur = [100, 100, 250]
                textsurface = myfont.render(str(self.selected_neuron.name) + ': ' + str(
                    self.selected_larticle.brain.all_neurons[self.selected_neuron.name].potential), False,
                                            kleur)
                self.display.blit(textsurface, (wy + 10, wy - 30))

                if self.selected_neuron.name in pos:
                    pygame.draw.circle(self.display, [250, 250, 250],
                                       [int(pos[self.selected_neuron.name][0]), int(pos[self.selected_neuron.name][1])],
                                       int(size * 3), 4)
                connections = self.selected_larticle.brain.all_neurons[self.selected_neuron.name].get_connections()
                names = []
                for name1, name2, weight in connections:
                    names.append(name2)
                    pygame.draw.line(self.display, [250, 0, 250], pos[name1], pos[name2], 3)
                names2 = []
                for name in names:
                    conn = self.selected_larticle.brain.all_neurons[name].get_connections()
                    for name1, name2, weight in conn:
                        names2.append(name2)
                        pygame.draw.line(self.display, [250, 0, 250], pos[name1], pos[name2], 3)
                names3 = []
                for name in names2:
                    conn = self.selected_larticle.brain.all_neurons[name].get_connections()
                    for name1, name2, weight in conn:
                        names3.append(name2)
                        pygame.draw.line(self.display, [250, 0, 250], pos[name1], pos[name2], 3)
                for name in names3:
                    conn = self.selected_larticle.brain.all_neurons[name].get_connections()
                    for name1, name2, weight in conn:
                        pygame.draw.line(self.display, [250, 0, 250], pos[name1], pos[name2], 3)
