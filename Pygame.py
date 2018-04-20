import os
import pickle
import subprocess

os.environ['SDL_VIDEO_WINDOW_POS'] = '%i,%i' % (200,30)


import pygame


pygame.font.init()
myfont = pygame.font.SysFont('Comic Sans MS', 12)

from Handler import Handler
import time

wit = (255, 255, 255)
zwart = (0, 0, 0)
rood = (255, 0, 0)
groen = (0, 255, 0)
blauw = (0, 0, 255)
geel = (255, 255, 0)
oranje = (255, 160, 0)
grijs = (190, 200, 200)

display_breedte = 1700
display_lengte = 1000


class game_lus():
    def __init__(self):
        pygame.init()
        self.display = pygame.display.set_mode((display_breedte,display_lengte))
        pygame.display.set_caption('Larticles')
        self.clock = pygame.time.Clock()
        self.size = 100
        self.beginscale = float(display_lengte / self.size)
        self.scale = self.beginscale
        self.handler = Handler(self.display,self.size)
        self.saved_larticles = {}
        self.time0 = time.time()
        self.running = True
        self.blits = True
        self.memory = []

    def get_saved(self):
        file = open('Saved_Larticles.txt','r')
        for larticle in file:
            dna = pickle.load(larticle)
            self.saved_larticles[larticle] = dna
        file.close()

    def reset(self):
        self.handler = Handler(self.display,self.size)

    def run(self):
        x = 0
        y = 0
        dxr = 0
        dxl = 0
        dyu = 0
        dyd = 0
        speed = 2 * self.scale
        scrollspeed = 0.5
        stop = False
        checking = False
        while not stop:

            self.memory.append(len(self.handler.larticles))


            if len(self.memory) > 100:
                self.memory = self.memory[0:100]
            if len(self.memory) > 30:
                s = set(self.memory)
                if len(s) <= 1:
                    self.handler.initialize()



            if len(self.handler.random_larticles) <= self.handler.random_larticles_amount and not checking:
                checking = True
                p = subprocess.Popen('python Create_random_larticles.py ' + str(self.handler.random_larticles_amount))




            if checking:
                r = p.poll()
                if r != None:
                    file = open('Random_Larticles.pickle','rb')
                    l = pickle.load(file)
                    self.handler.random_larticles += l
                    file.close()
                    checking = False
                    p.kill()



            time0 = time.time()


            mx = None
            my = None


            events = pygame.event.get()
            for event in events:


                if event.type == pygame.QUIT:
                    stop = True
                    pygame.quit()
                    quit()


                if event.type == pygame.KEYDOWN:

                    if event.key == pygame.K_HOME:
                        self.reset()
                    if event.key == pygame.K_s:
                        pass
                    if event.key == pygame.K_k:
                        self.handler.kill_selected()
                    if event.key == pygame.K_q:
                        pass
                    if event.key == pygame.K_w:
                        pass

                    if event.key == pygame.K_END:
                        self.scale = self.beginscale
                        x = 0
                        y = 0

                    if event.key == pygame.K_ESCAPE:
                        stop = True
                        pygame.quit()
                        quit()
                    if event.key == pygame.K_INSERT:
                        self.running = not self.running

                    if event.key == pygame.K_PAGEUP:
                        self.blits = not self.blits

                    if event.key == pygame.K_PAGEDOWN:
                        self.handler.set_visual()

                    if event.key == pygame.K_DOWN:
                        dyd = speed
                    if event.key == pygame.K_UP:
                        dyu = -speed
                    if event.key == pygame.K_LEFT:
                        dxl = -speed
                    if event.key == pygame.K_RIGHT:
                        dxr = speed

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_DOWN:
                        dyd = 0
                    if event.key == pygame.K_UP:
                        dyu = -0
                    if event.key == pygame.K_LEFT:
                        dxl = -0
                    if event.key == pygame.K_RIGHT:
                        dxr = 0

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        mx, my = pygame.mouse.get_pos()
                    if event.button == 3:
                        self.handler.reset_selected()
                    if event.button == 4 and self.scale <= 50:
                        self.scale += scrollspeed
                    if event.button == 5 and self.scale > 1 + scrollspeed:
                        self.scale -= scrollspeed

            x -= dxl + dxr
            y -= dyd + dyu
            self.display.fill(zwart)
            pygame.draw.rect(self.display, [150, 150, 150],
                             [x, y, int(self.handler.gridsize * self.scale), int(self.handler.gridsize * self.scale)],
                             3)



            if self.running:
                self.handler.run()
            if self.blits:
                self.handler.blits(self.scale, x, y,mx,my)

            time1 = time.time()
            tijd = time1 - time0

            textsurface = myfont.render('Runtime: ' + str(tijd), False, (250, 250, 250))
            self.display.blit(textsurface, (display_breedte -100, 0))
            textsurface = myfont.render('Elapsed: ' + str((time.time() - self.time0)), False, (250, 250, 250))
            self.display.blit(textsurface, (display_breedte - 100, 15))
            textsurface = myfont.render('Starts: ' + str(self.handler.starts), False, (250, 250, 250))
            self.display.blit(textsurface, (display_breedte - 100, 30))
            textsurface = myfont.render('Buffer: ' + str(len(self.handler.random_larticles)), False, (250, 250, 250))
            self.display.blit(textsurface, (display_breedte - 100, 45))

            pygame.display.update()

            self.clock.tick()


game = game_lus()
game.run()
