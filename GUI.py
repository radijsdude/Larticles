
from Simulation import Simulation
from constants import *


class Commands():
    def __init__(self):
        self.helper_button = [0, 0, 70, 30]

        self.keys = {}
        self.keys['j) Escape'] = 'Stop the Program.'
        self.keys['a) Insert'] = 'Run / Pause the simulation.'
        self.keys['i) Home'] = 'Restart the Big Bang.'
        self.keys['g) PageDown'] = 'Show more stuff: white circle = donating health, purple mouth = talking'
        self.keys['h) PageUp'] = 'Show nothing in the simulation.'
        self.keys['f) End'] = 'Return to default zoom.'
        self.keys['d) Arrows'] = 'Move the grid (works better when paused).'
        self.keys['e) Scroll'] = 'Zoom (works better when paused).'
        self.keys['b) Left Click'] = 'Select Larticle or Neuron.'
        self.keys['c) Right Click'] = 'Unselect All.'
        self.keys['k) k'] = 'Kill selected larticle.'
        self.keys['l) a or q'] = 'Stop the program ( a or q depends on keyboard mappings).'


    def run(self):
        stop = False
        while not stop:
            mx, my = None, None
            events = pygame.event.get()
            for event in events:

                if event.type == pygame.QUIT:
                    stop = True
                    pygame.quit()
                    quit()

                if event.type == pygame.KEYDOWN:

                    if event.key == pygame.K_ESCAPE:
                        stop = True
                        pygame.quit()
                        quit()

                    elif event.type == pygame.VIDEORESIZE:
                        screen.x, screen.y = event.w, event.h

                    elif event.key == pygame.K_f:
                        screen.toggle_fullscreen()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        mx, my = pygame.mouse.get_pos()

            if mx != None and my != None:
                if self.helper_button[0] < mx < self.helper_button[0] + self.helper_button[2]:
                    if self.helper_button[1] < my < self.helper_button[1] + self.helper_button[3]:
                        stop = True
                        break

            pygame.draw.rect(screen.display, zwart, [0, 0, 2000, 2000])

            pygame.draw.rect(screen.display, rood, self.helper_button)
            textsurface = myfont10.render('Helper', False, (0, 0, 0))
            screen.display.blit(textsurface, (self.helper_button))

            x0 = 200
            y0 = 200
            t = 30
            i = 0
            for k in list(sorted(self.keys.keys())):
                textsurface = myfont10.render(k + ': ' + self.keys[k], False, (255, 255, 255))
                screen.display.blit(textsurface, [x0, y0 + t * i])
                i += 1

            textsurface = myfont10.render('Thomas Ludo Maarten Arys', False, (255, 255, 255))
            screen.display.blit(textsurface, [100, 100])

            textsurface = myfont10.render('This simulation needs a 1900 * 1080 resolution, otherwise contact:', False,
                                         (255, 255, 255))
            screen.display.blit(textsurface, [100, 70])

            pygame.display.update()
            screen.clock.tick(10)


class Helper():
    def __init__(self):

        self.commands = Commands()
        self.commands_button_pos = [200, 200, 300, 100]
        self.commands_button_tekst = 'Commands'
        self.commands_button_kleur = [255, 0, 0]
        self.commands_tekst_kleur = [0, 0, 0]

        self.options = Options()
        self.options_button_pos = [700, 200, 300, 100]
        self.options_button_tekst = 'Options'
        self.options_button_kleur = [255, 0, 0]
        self.options_tekst_kleur = [0, 0, 0]


        self.main_button = [0, 0, 70, 30]


    def run(self):
        stop = False
        while not stop:
            mx = None
            my = None
            events = pygame.event.get()
            for event in events:

                if event.type == pygame.QUIT:
                    stop = True
                    pygame.quit()
                    quit()


                elif event.type == pygame.VIDEORESIZE:
                    screen.x,screen.y = event.w,event.h

                elif event.type == pygame.KEYDOWN:

                    if event.key == pygame.K_ESCAPE:
                        stop = True
                        pygame.quit()
                        quit()

                    elif event.key == pygame.K_f:
                        screen.toggle_fullscreen()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        mx, my = pygame.mouse.get_pos()

            if mx != None and my != None:
                if self.commands_button_pos[0] < mx < self.commands_button_pos[0] + self.commands_button_pos[2] and \
                                        self.commands_button_pos[
                                            1] < my < self.commands_button_pos[1] + self.commands_button_pos[3]:
                    self.commands.run()

                elif self.options_button_pos[0] < mx < self.options_button_pos[0] + self.options_button_pos[2] and \
                                        self.options_button_pos[
                                            1] < my < self.options_button_pos[1] + self.options_button_pos[3]:
                    self.options.run()

                elif self.main_button[0] < mx < self.main_button[0] + self.main_button[2] and \
                                        self.main_button[
                                            1] < my < self.main_button[1] + self.main_button[3]:
                    stop = True

            screen.display.fill(zwart)

            pygame.draw.rect(screen.display, self.commands_button_kleur, self.commands_button_pos)
            textsurface = myfont10.render(self.commands_button_tekst, False, self.commands_tekst_kleur)
            screen.display.blit(textsurface, self.commands_button_pos)

            pygame.draw.rect(screen.display, self.options_button_kleur, self.options_button_pos)
            textsurface = myfont10.render(self.options_button_tekst, False, self.options_tekst_kleur)
            screen.display.blit(textsurface, self.options_button_pos)

            pygame.draw.rect(screen.display, [255,0,0], self.main_button)
            textsurface = myfont10.render('Main', False, [0,0,0])
            screen.display.blit(textsurface, self.main_button)

            pygame.display.update()
            screen.clock.tick(10)


class Options_File():
    def __init__(self):
        self.breedte = 1900
        self.lengte = 1000
        self.size = 100
        self.suns = 2

class Options():
    def __init__(self):

        self.size = 100
        self.size_button_pos = [400, 300, 700, 100]
        self.size_button_tekst = 'Size: ' + str(self.size)
        self.size_button_kleur = [255, 0, 0]
        self.size_tekst_kleur = [0, 0, 0]

        self.suns = 2
        self.suns_button_pos = [400, 500, 700, 100]
        self.suns_button_tekst = 'Suns: ' + str(self.suns)
        self.suns_button_kleur = [255, 0, 0]
        self.suns_tekst_kleur = [0, 0, 0]

        self.amount_larticles = int(self.size ** 2 / 10)
        self.amount_larticles_button_pos = [400, 700, 700, 100]
        self.amount_larticles_button_tekst = 'amount_larticles: ' + str(self.amount_larticles)
        self.amount_larticles_button_kleur = [255, 0, 0]
        self.amount_larticles_tekst_kleur = [0, 0, 0]

        self.main_button = [0, 0, 70, 30]

        self.default_button_pos = [200,100,300,100]
        self.default_button_tekst = 'Default'
        self.default_button_kleur = [100, 100, 255]
        self.default_tekst_kleur = [0, 0, 0]

        self.default = {}
        self.default['size'] = 100
        self.default['suns'] = 2

    def set_default(self):
        self.size = self.default['size']
        self.suns = self.default['suns']

    def run(self):
        stop = False
        while not stop:
            mx = None
            my = None
            events = pygame.event.get()
            for event in events:

                if event.type == pygame.QUIT:
                    stop = True
                    pygame.quit()
                    quit()

                elif event.type == pygame.VIDEORESIZE:
                    screen.x,screen.y = event.w,event.h

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        stop = True
                        pygame.quit()
                        quit()

                    if event.key == pygame.K_f:
                        screen.toggle_fullscreen()

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        mx, my = pygame.mouse.get_pos()

            if mx != None and my != None:
                if self.size_button_pos[0] < mx < self.size_button_pos[0] + self.size_button_pos[
                    2] and self.size_button_pos[1] < my < self.size_button_pos[1] + self.size_button_pos[3]:
                    user = User_input('Grid size?',1000,100,'all')
                    s = user.run()
                    if s != '':
                        self.size = int(s)
                        
                elif self.suns_button_pos[0] < mx < self.suns_button_pos[0] + self.suns_button_pos[
                    2] and self.suns_button_pos[1] < my < self.suns_button_pos[1] + self.suns_button_pos[3]:
                    user = User_input('Grid suns?',1000,100,'all')
                    s = user.run()
                    if s != '':
                        self.suns = int(s)
                
                elif self.amount_larticles_button_pos[0] < mx < self.amount_larticles_button_pos[0] + self.amount_larticles_button_pos[
                    2] and self.amount_larticles_button_pos[1] < my < self.amount_larticles_button_pos[1] + self.amount_larticles_button_pos[3]:
                    user = User_input('Grid amount_larticles?',1000,100,'all')
                    s = user.run()
                    if s != '':
                        self.amount_larticles = int(s)

                elif self.default_button_pos[0] < mx < self.default_button_pos[0] + self.default_button_pos[2] and \
                                        self.default_button_pos[
                                            1] < my < self.default_button_pos[1] + self.default_button_pos[3]:
                    self.set_default()

                elif self.main_button[0] < mx < self.main_button[0] + self.main_button[2] and \
                                        self.main_button[
                                            1] < my < self.main_button[1] + self.main_button[3]:
                    stop = True

            screen.display.fill(zwart)

            pygame.draw.rect(screen.display, self.size_button_kleur, self.size_button_pos)
            textsurface = myfont10.render('Size: ' + str(self.size), False, self.size_tekst_kleur)
            screen.display.blit(textsurface, self.size_button_pos)

            pygame.draw.rect(screen.display, self.suns_button_kleur, self.suns_button_pos)
            textsurface = myfont10.render('Suns: ' + str(self.suns), False, self.suns_tekst_kleur)
            screen.display.blit(textsurface, self.suns_button_pos)

            pygame.draw.rect(screen.display, self.amount_larticles_button_kleur, self.amount_larticles_button_pos)
            textsurface = myfont10.render('amount_larticles: ' + str(self.amount_larticles), False, self.amount_larticles_tekst_kleur)
            screen.display.blit(textsurface, self.amount_larticles_button_pos)

            pygame.draw.rect(screen.display, self.default_button_kleur, self.default_button_pos)
            textsurface = myfont10.render(self.default_button_tekst, False, self.default_tekst_kleur)
            screen.display.blit(textsurface, self.default_button_pos)

            pygame.draw.rect(screen.display, [255, 0, 0], self.main_button)
            textsurface = myfont10.render('Main', False, [0, 0, 0])
            screen.display.blit(textsurface, self.main_button)

            pygame.display.update()
            screen.clock.tick(10)




class User_input():
    def __init__(self,question,x,y,tipe='all'):
        self.x,self.y,self.b,self.l = x,y,300,200
        self.rect = [self.x,self.y,self.b,self.l]
        self.question = question
        self.tipe = tipe
        self.response= []
        self.alfabet = [chr(i) for i in range(97,122)]
        self.numbers = [str(i) for i in range(10)]

        size = 30
        self.ok_button_pos = [x + self.b - size -10, y + self.l - size -10, size, size]
        self.ok_button_tekst = 'OK'
        self.ok_button_kleur = [0, 255, 0]
        self.ok_tekst_kleur = [0, 0, 0]

    
    def get_number(self,key):
        response = -13
        if key == pygame.K_0:
            response = '0'
        elif key == pygame.K_1:
            response = '1'
        elif key == pygame.K_2:
            response = '2'
        elif key == pygame.K_3:
            response = '3'
        elif key == pygame.K_4:
            response = '4'
        elif key == pygame.K_5:
            response = '5'
        elif key == pygame.K_6:
            response = '6'
        elif key == pygame.K_7:
            response = '7'
        elif key == pygame.K_8:
            response = '8'
        elif key == pygame.K_9:
            response = '9'


        elif key == pygame.K_KP0:
            response = '0'
        elif key == pygame.K_KP1:
            response = '1'
        elif key == pygame.K_KP2:
            response = '2'
        elif key == pygame.K_KP3:
            response = '3'
        elif key == pygame.K_KP4:
            response = '4'
        elif key == pygame.K_KP5:
            response = '5'
        elif key == pygame.K_KP6:
            response = '6'
        elif key == pygame.K_KP7:
            response = '7'
        elif key == pygame.K_KP8:
            response = '8'
        elif key == pygame.K_KP9:
            response = '9'

        return response
    
    def run(self):
        stop = False
        while not stop:
            mx = None
            my = None
            events = pygame.event.get()
            for event in events:

                if event.type == pygame.QUIT:
                    stop = True
                    pygame.quit()
                    quit()



                if event.type == pygame.KEYDOWN:
                    l = pygame.key.name(event.key)

                    if self.tipe == 'all':
                        if l in self.alfabet:
                            self.response.append(l)
                        else:
                            r = self.get_number(event.key)
                            if r in self.numbers:
                                self.response.append(r)

                            
                            
                    if self.tipe == 'int':
                        r = self.get_number(event.key)
                        if r in self.numbers:
                            self.response.append(r)
                            
                            
                            
                    if event.key == pygame.K_BACKSPACE:
                        print('pop')
                        if len(self.response) > 0:
                            self.response.pop(-1)
                    elif event.key == pygame.K_KP_ENTER or event.key == pygame.K_RETURN:
                        stop = True
                    elif event.key == pygame.K_f:
                        screen.toggle_fullscreen()



                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        mx, my = pygame.mouse.get_pos()

            if mx != None and my != None:
                if self.ok_button_pos[0] < mx < self.ok_button_pos[0] + self.ok_button_pos[
                    2] and self.ok_button_pos[1] < my < self.ok_button_pos[1] + self.ok_button_pos[3]:
                    stop = True

            pygame.draw.rect(screen.display, [0, 0, 0], self.rect)
            pygame.draw.rect(screen.display,[255,255,255],self.rect,5)

            pygame.draw.rect(screen.display, self.ok_button_kleur, self.ok_button_pos)
            textsurface = myfont10.render(self.ok_button_tekst, False, self.ok_tekst_kleur)
            screen.display.blit(textsurface, self.ok_button_pos)

            textsurface = myfont10.render(self.question, False, [255, 255, 255])
            screen.display.blit(textsurface, [self.x + 10, self.y])

            print(self.response)
            s = 'User: ' + ''.join(self.response)
            textsurface = myfont10.render(s, False, [255,255,255])
            screen.display.blit(textsurface, [self.x + 10, self.y + 50])

            pygame.display.update()
            screen.clock.tick(10)

        s = ''.join(self.response)
        return s



class Main():
    def __init__(self):
        if os.path.exists('Larticles_Options.pickle'):
            file = open('Larticles_Options.pickle', 'rb')
            self.options_file = pickle.load(file)
            file.close()
        else:
            self.options = Options()

        self.size = self.options.size
        self.suns = self.options.suns

        self.simulation = None
        self.simulation_button_pos = [200, 200, 300, 100]
        self.simulation_button_tekst = 'Simulation'
        self.simulation_button_kleur = [255, 0, 0]
        self.simulation_tekst_kleur = [0, 0, 0]

        self.options = Options()
        self.options_button_pos = [700, 200, 300, 100]
        self.options_button_tekst = 'Options'
        self.options_button_kleur = [100, 255, 100]
        self.options_tekst_kleur = [0, 0, 0]

        self.helper = Helper()
        self.helper_button_pos = [1200, 200, 300, 100]
        self.helper_button_tekst = 'Help'
        self.helper_button_kleur = [100, 100, 255]
        self.helper_tekst_kleur = [0, 0, 0]

        if testing:
            self.simulation = Simulation()
            self.simulation.Simulation_run()

    def run(self):
        stop = False
        while not stop:
            mx = None
            my = None
            events = pygame.event.get()
            for event in events:

                if event.type == pygame.QUIT:
                    stop = True
                    pygame.quit()
                    quit()

                if event.type == pygame.KEYDOWN:

                    if event.key == pygame.K_ESCAPE:
                        stop = True
                        pygame.quit()
                        quit()

                    elif event.key == pygame.K_f:
                        screen.toggle_fullscreen()
                    elif event.key == pygame.K_RETURN:
                        if self.simulation == None:
                            self.simulation = Simulation()

                        self.simulation.Simulation_run()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        mx, my = pygame.mouse.get_pos()


            screen.display.fill(zwart)

            if mx != None and my != None:
                if self.simulation_button_pos[0] < mx < self.simulation_button_pos[0] + self.simulation_button_pos[
                    2] and self.simulation_button_pos[1] < my < self.simulation_button_pos[1] + self.simulation_button_pos[3]:

                    if self.simulation == None:
                        self.simulation = Simulation()

                    self.simulation.Simulation_run()

                elif self.helper_button_pos[0] < mx < self.helper_button_pos[0] + self.helper_button_pos[2] and \
                                        self.helper_button_pos[
                                            1] < my < self.helper_button_pos[1] + self.helper_button_pos[3]:
                    self.helper.run()

                elif self.options_button_pos[0] < mx < self.options_button_pos[0] + self.options_button_pos[2] and \
                                        self.options_button_pos[
                                            1] < my < self.options_button_pos[1] + self.options_button_pos[3]:
                    self.options.run()
                    self.size = self.options.size


            pygame.draw.rect(screen.display, self.simulation_button_kleur, self.simulation_button_pos)
            if self.simulation == None:
                textsurface = myfont10.render(self.simulation_button_tekst, False, self.simulation_tekst_kleur)
                screen.display.blit(textsurface, self.simulation_button_pos)
            else:
                textsurface = myfont10.render('Resume', False, self.simulation_tekst_kleur)
                screen.display.blit(textsurface, self.simulation_button_pos)


            pygame.draw.rect(screen.display, self.helper_button_kleur, self.helper_button_pos)
            textsurface = myfont10.render(self.helper_button_tekst, False, self.helper_tekst_kleur)
            screen.display.blit(textsurface, self.helper_button_pos)

            pygame.draw.rect(screen.display, self.options_button_kleur, self.options_button_pos)
            textsurface = myfont10.render(self.options_button_tekst, False, self.options_tekst_kleur)
            screen.display.blit(textsurface, self.options_button_pos)


            pygame.display.update()
            screen.clock.tick(10)


m = Main()
m.run()
pygame.quit()
quit()
