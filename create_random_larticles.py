from Simulation import Larticle
import random
import pickle
def Handler_create_random_larticles(n):
    random_larticles = []
    for i in range(int(n)):
        r = random.randrange(0,1000000)
        l = Larticle('Random' + str(i))
        random_larticles.append(l)
    file = open('Random_Larticles.pickle','wb')
    pickle.dump(random_larticles,file)
    file.close()
Handler_create_random_larticles(1000)