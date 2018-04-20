import pickle
from Larticle import Larticle
import sys
import random

def f(n):
    random_larticles = []
    n = int(n)
    s = str(random.randrange(0,10000))
    for i in range(n):
        l = Larticle('Random' + str(i) + s, 10)
        random_larticles.append(l)
    file = open('Random_Larticles.pickle','wb')
    pickle.dump(random_larticles,file)
    file.close()
    
if __name__ == '__main__':
    a = sys.argv
    f(a[1])
