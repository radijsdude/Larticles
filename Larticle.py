from Body import Body
from Brain import Brain

class Larticle():
    def __init__(self,name,gridsize,dna=None):
        self.name = name
        self.body = Body(gridsize)
        self.brain = Brain(self.body.outputs,self.body.inputs,dna)
        self.time_alive = 0
        self.brain_drain = (len(self.brain.dna) + len(self.brain.all_neurons)) / 100
        self.splits = 0

    def set(self,dictionary):
        if 'health' in dictionary:
            self.body.health = dictionary['health']
        if 'x' in dictionary:
            self.body.x = dictionary['x']
        if 'y' in dictionary:
            self.body.y = dictionary['y']
        if 'dna' in dictionary:
            self.brain.set_dna(dictionary['dna'])
        self.brain_drain = (len(self.brain.dna) + len(self.brain.all_neurons)) / 100

    def doe(self,larticles):
        self.time_alive += 1
        forbrain = self.body.tobrain(larticles)
        forbody = self.brain.tobody(forbrain)
        r = self.body.command(forbody,larticles)
        self.body.health -= self.brain_drain
        return r

    def mutate(self):
        self.name = 'mutated_' + self.name
        self.brain.mutate()
