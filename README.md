# Living-Particles
An attempt at an artificial life screensaver.https://www.youtube.com/watch?v=eqQlqO-STxM

Version 0.1

How this should be Read:
1) Neuron.py
2) Brain.py
3) Body.py
4) Larticle.py
5) Handler.py
6) Create_random_larticles.py
7) Pygame.py

How this should be Run:
1) Have python 3, (I made this in 3.5).
2) Install pygame and pickle on python with python pip install pygame and python pip install pickle.
3) All files need to be in the same folder.
4) Run Pygame.py.
5) You can set the initial gridsize in the Pygame.py file

Thze Commands:

Escape: stop!!!

Home: Restart the Big Bang

Insert: Pause

left mouse click: select the clicked larticle and or neuron

right mouse click: unselect

scroll: zoom (works better when paused)

End: return to original zoom

arrows: move the grid (works better when paused)

k: kill selected larticle

PageDown: toggle show more (talking = purple mouth, state = colour brightness, giving health = white circle)

PageUp: toggle show nothing


Please tell me if something goes wrong.

Some problems i have in making this a .exe:
in Pygame.py i start a subprocess of Create_random_larticles.py, when using pyinstaller to compile to a .exe, this file will not be converted since the only way i know is to start the subprocess with an os command 'python Create_random_larticles.py' the seperate process is needed to save alot of framerate. so if someone knows how to fix this so i can make it into an exe.

It took madness and time to make this, it will take some madness and time to comment the code.
The Neuron.py file is a gift, it is a script for a feed forward neuron with sigmoid scaling and backwards propagation, tho the backwards propagation is not used in the rest of the program because it kills the framerate, a simple example of it is in the test function.
I made this because the autistic kid in me likes to look at it. Have fun.

