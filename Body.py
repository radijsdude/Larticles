import random


class Body():
    def __init__(self, gridsize):

        self.gridsize = gridsize

        self.x = 0
        self.y = 0

        self.directions = [[1, 0], [0, 1], [-1, 0], [0, -1]]
        self.direction = random.choice(self.directions)

        self.health = 500
        self.previous_health = self.health
        self.health_bar = int(self.health)
        self.regen = 0
        self.regenrate = 5
        self.suffer = -1
        self.body_drain = 0
        self.regenerating = False
        self.happy = 0

        self.eat_damage = self.health_bar / 2

        self.original_color = [0, 1, 0]
        self.color = [1, 1, 1]


        self.memory_1 = 0
        self.memory_2 = 0

        self.voice_1 = 0
        self.voice_2 = 0
        self.sound_1 = 0
        self.sound_2 = 0
        self.talking = False
        self.give_health = False
        self.killer = 0

        self.kills = 0

        self.state = 0

        body_commands = ['command_move', 'command_rotate_left', 'command_rotate_right',
                         'command_regenerate', 'command_split','command_give']
        attack_commands = ['command_eat']
        memory_commands = ['command_memory_1_set','command_memory_1_value','command_memory_1_erase',
                           'command_memory_2_set','command_memory_2_value','command_memory_2_erase']
        speak_commands = ['command_voice_speak','command_voice_1_value','command_voice_2_value','command_voice_set']
        state_commands = ['command_set_state','command_erase_state','command_state_value']

        self.inputs = body_commands + attack_commands + memory_commands + speak_commands + state_commands

        sight = ['sense_see_red', 'sense_see_green', 'sense_see_blue', 'sense_see_health','sense_see_happyness', 'sense_see_distance','sense_see_wall','sense_see_state']
        sense = ['sense_south',
                 'sense_west', 'sense_east',
                 'sense_northwest', 'sense_northeast',
                 'sense_southwest', 'sense_southeast',
                 'sense_memory_1','sense_memory_2','sense_health',
                 'sense_sound_1','sense_sound_2','sense_voice_1','sense_voice_2',
                 'sense_happy','sense_alive','sense_killed','sense_state']
        self.outputs = sight + sense

    def check(self, larticles, x, y):
        t = None
        for larticle in larticles:
            if int(x) == int(larticles[larticle].body.x) and int(y) == int(larticles[larticle].body.y):
                t = larticles[larticle]
        return t

    def check_in(self, x, y):
        t = True
        if not (0 < x < self.gridsize and 0 < y < self.gridsize):
            t = False
        return t

    def get_surounding_pos(self):
        north = int(self.x + self.direction[0]), int(self.y + self.direction[1])
        south = int(self.x - self.direction[0]), int(self.y - self.direction[1])

        if self.direction == [1, 0]:
            left = [0, 1]
        elif self.direction == [0, 1]:
            left = [-1, 0]
        elif self.direction == [-1, 0]:
            left = [0, -1]
        else:
            left = [1, 0]

        west = int(self.x + left[0]), int(self.y + left[1])
        east = int(self.x - left[0]), int(self.y - left[1])

        northwest = int(self.x + left[0] + self.direction[0]), int(self.y + left[1] + self.direction[1])
        northeast = int(self.x - left[0] + self.direction[0]), int(self.y - left[1] + self.direction[1])

        southwest = int(self.x + left[0] - self.direction[0]), int(self.y + left[1] - self.direction[1])
        southeast = int(self.x - left[0] - self.direction[0]), int(self.y - left[1] - self.direction[1])

        return {'north': north, 'south': south,
                'west': west, 'east': east,
                'northwest': northwest, 'northeast': northeast,
                'southwest': southwest, 'southeast': southeast}

    def get_surounding_grid(self, larticles):
        d = self.get_surounding_pos()
        north = self.check(larticles, d['north'][0], d['north'][1])
        south = self.check(larticles, d['south'][0], d['south'][1])
        west = self.check(larticles, d['west'][0], d['west'][1])
        east = self.check(larticles, d['east'][0], d['east'][1])
        northwest = self.check(larticles, d['northwest'][0], d['northwest'][1])
        northeast = self.check(larticles, d['northeast'][0], d['northeast'][1])
        southwest = self.check(larticles, d['southwest'][0], d['southwest'][1])
        southeast = self.check(larticles, d['southeast'][0], d['southeast'][1])
        return {'north': north, 'south': south,
                'west': west, 'east': east,
                'northwest': northwest, 'northeast': northeast,
                'southwest': southwest, 'southeast': southeast}

    def sense(self, larticles):
        grid = self.get_surounding_pos()
        surounding = self.get_surounding_grid(larticles)
        potentials = {}
        for name in surounding:
            if name != 'north':
                n = 'sense_' + name
                if surounding[name] != None:
                    potentials[n] = 1
                else:
                    if self.check_in(grid[name][0],grid[name][1]):
                        potentials[n] = 0
                    else:
                        potentials[n] = 1

        return potentials

    def see(self, larticles):
        x1 = int(self.x + self.direction[0])
        y1 = int(self.y + self.direction[1])
        x2 = int(self.x + 2 * self.direction[0])
        y2 = int(self.y + 2 * self.direction[1])
        see = [0, 0, 0, 0, 0,0, 1,0]
        r11 = self.check_in(x1, y1)
        if r11:
            r12 = self.check(larticles, x1, y1)
            if r12 != None:
                see = r12.body.color + [self.health / (abs(r12.body.health) + 1),r12.body.happy,0, 0,r12.body.state]
            else:
                r21 = self.check_in(x2, y2)
                if r21:
                    r22 = self.check(larticles, x2, y2)
                    if r22 != None:
                        see = r22.body.color + [self.health / (abs(r22.body.health) + 1),r22.body.happy,0, 1,r22.body.state]
                else:
                    see = [0, 0, 0, 0, 0,1, 1,0]
        else:
            see = [0, 0, 0, 0, 0,1, 0,0]
        sight = {'sense_see_red': see[0], 'sense_see_green': see[1], 'sense_see_blue': see[2],
                 'sense_see_health': see[3],'sense_see_happyness':see[4], 'sense_see_wall' : see[5], 'sense_see_distance': see[6],'sense_see_state':see[7]}
        return sight

    def move(self):
        self.x = int(self.direction[0] + self.x)
        self.y = int(self.direction[1] + self.y)

    def rotate_left(self):
        if self.direction == [1, 0]:
            self.direction = [0, 1]
        elif self.direction == [0, 1]:
            self.direction = [-1, 0]
        elif self.direction == [-1, 0]:
            self.direction = [0, -1]
        elif self.direction == [0, -1]:
            self.direction = [1, 0]

    def rotate_right(self):
        if self.direction == [1, 0]:
            self.direction = [0, -1]
        elif self.direction == [0, -1]:
            self.direction = [-1, 0]
        elif self.direction == [-1, 0]:
            self.direction = [0, 1]
        elif self.direction == [0, 1]:
            self.direction = [1, 0]

    def regenerate(self, larticles):
        g = self.get_surounding_grid(larticles)
        t = self.regenrate

        if g['north'] != None:
            if g['north'].body.regenerating:
                t += self.regenrate
        if g['south'] != None:
            if g['south'].body.regenerating:
                t += self.regenrate
        if g['west'] != None:
            if g['west'].body.regenerating:
                t += self.regenrate
        if g['east'] != None:
            if g['east'].body.regenerating:
                t += self.regenrate
        self.health += t

        return t

    def eat(self,larticle):
        h = larticle.body.health
        if h > self.eat_damage:
            self.health += self.eat_damage
        else:
            self.health += h
        larticle.body.health -= self.eat_damage
        if larticle.body.health <= 0:
            self.kills += 1
            self.killer = 1

    def give(self,larticle):
        if self.health > abs(self.eat_damage):
            self.health -= self.eat_damage
            larticle.body.health += self.eat_damage


    def command(self,commands,larticles):
        self.previous_health = self.health
        result = []
        self.body_drain = 0
        self.regen = 0
        t = self.suffer
        self.color = self.original_color




        happy = self.health - self.previous_health
        if happy > 0:
            self.happy = 1
        else:
            self.happy = 0


        if commands['command_regenerate'] > 0.5:
            result.append('regenerate')
            self.regenerating = True
            self.color = [0,0,1]
            self.regen = self.regenerate(larticles)
        else:
            self.regenerating = False








        if commands['command_memory_1_set'] > 0.5:
            self.memory_1 = commands['command_memory_1_value']
        if commands['command_memory_1_erase']:
            self.memory_1 = 0
        if commands['command_memory_2_set'] > 0.5:
            self.memory_1 = commands['command_memory_2_value']
        if commands['command_memory_2_erase']:
            self.memory_1 = 0

        if commands['command_set_state'] > 0.5:
            self.state = commands['command_state_value']
        if commands['command_erase_state'] > 0.5:
            self.state = 0







        if commands['command_rotate_right'] > 0.5:
            self.rotate_right()
        if commands['command_rotate_left'] > 0.5:
            self.rotate_left()

        x, y = int(self.x + self.direction[0]), int(self.y + self.direction[1])
        r1 = self.check_in(x, y)
        r2 = self.check(larticles, x, y)


        if commands['command_eat'] > 0.5:
            if not self.regenerating:
                self.color = [1,0,0]
                if r1:
                    if r2 != None:
                        self.eat(r2)




        if commands['command_split'] > 0.5:
            if self.regenerating:
                if r1:
                    if r2 == None:
                        minh = self.health_bar + self.health_bar / 10
                        if self.health > minh:
                            self.health -= self.health_bar
                            result.append('split')
            else:
                sx, sy = int(self.x - self.direction[0]), int(self.y - self.direction[1])
                rs1 = self.check_in(sx, sy)
                rs2 = self.check(larticles, sx, sy)
                if rs1:
                    if rs2 == None:
                        minh = 1.5 * (self.health_bar + self.health_bar / 5)
                        if self.health > minh:
                            self.health -=    1.5 * self.health_bar
                            result.append('split')


        if commands['command_give'] > 0.5:
            self.give_health = True
            if r1:
                if r2 != None:
                    self.give(r2)
        else:
            self.give_health = False

        if commands['command_voice_set'] > 0.5:
            self.voice_1 = commands['command_voice_1_value']
            self.voice_2 = commands['command_voice_2_value']

        if commands['command_voice_speak'] > 0.5:
            self.talking = True
            if r1:
                if r2 != None:
                    if int(self.x) == int(r2.body.x + r2.body.direction[0]):
                        if int(y) == int(r2.body.y + r2.body.direction[1]):
                            r2.body.sound_1 = self.voice_1
                            r2.body.sound_2 = self.voice_2
        else:
            self.talking = False

        if not self.regenerating and commands['command_move'] > 0.5:
            if r1:
                if r2 == None:
                    self.move()






        self.body_drain = t
        self.health += t
        if self.health > 3 * self.health_bar:
            self.health = 3 * self.health_bar
        return result

    def tobrain(self,larticles):
        see = self.see(larticles)
        sense = self.sense(larticles)
        others = {'sense_health':self.health/self.health_bar,'sense_happy':self.happy,'sense_alive':1,
                  'sense_memory_1':self.memory_1,'sense_memory_2':self.memory_2,
                  'sense_sound_1':float(self.sound_1),'sense_sound_2':float(self.sound_2),
                  'sense_voice_1':self.voice_1,'sense_voice_2':self.voice_2,'sense_killed':self.killer}
        result = {}
        for i in see:
            result[i] = see[i]
        for i in sense:
            result[i] = sense[i]
        for i in others:
            result[i] = others[i]

        self.sound_1 = 0
        self.killer = 0
        return result
































