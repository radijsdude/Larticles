import math
import random


class Axon():
    def __init__(self, neuron):
        self.neuron = neuron
        self.weight = random.randrange(-8, 9) / 4

    def set(self, weight):
        self.weight = weight

    def get(self):
        return self.neuron.name, self.weight

    def fire(self):
        return self.weight * self.neuron.calculate()

    def __repr__(self):
        return 'weight: ' + str(self.weight) + ' * potential: ' + str(self.neuron.potential)


class Neuron():
    def __init__(self, name):
        self.name = name
        self.dendrites = {}
        self.potential = 0
        self.error = 0
        self.learningrate = 0.5

    def set(self, potential):
        self.potential = potential

    def get_connections(self):
        con = []
        for name in self.dendrites:
            con.append([self.name,name,self.dendrites[name].weight])
        return con

    def connect(self, neuron, weight=None):
        dendrite = Axon(neuron)
        if weight != None:
            dendrite.set(weight)
        self.dendrites[neuron.name] = dendrite
        t = self.test_connection(4)
        if not t:
            self.dendrites.pop(neuron.name)
        return t


    def test_connection(self,n):
        n -= 1
        r = True
        if n > 0:
            if len(self.dendrites) != 0:
                for dendrite in self.dendrites:
                    t = self.dendrites[dendrite].neuron.test_connection(n)
                    if t == False:
                        r = False
        else:
            r = False
        return r



    def disconnect(self, name):
        if name in self.dendrites:
            self.dendrites.pop(name)

    def sigmoid(self, potential, d=False):
        if not d:
            if potential > -100:
                return 1 / (1 + math.exp(-potential))
            else:
                return 0
        else:
            return potential * (1 - potential)

    def calculate(self):
        if len(self.dendrites) != 0:
            x = 0
            for dendrite in self.dendrites:
                x += self.dendrites[dendrite].fire()
            self.potential = self.sigmoid(x)
        return self.potential

    def add_error(self, error):
        self.error += error

    def correct(self):
        gradient = self.error * self.sigmoid(self.potential, True)
        for dendrite in self.dendrites:
            dw = self.dendrites[dendrite].neuron.learningrate * self.dendrites[dendrite].neuron.potential * gradient
            self.dendrites[dendrite].weight += dw
            self.dendrites[dendrite].neuron.add_error(gradient * self.dendrites[dendrite].weight)
            self.dendrites[dendrite].neuron.correct()
        self.error = 0
        self.calculate()

    def __repr__(self):
        return str(self.name) + ' => ' + str(self.potential) + ' <= ' + str(self.dendrites)


def Test():
    print(' ')
    print(' ')
    print('Test Neuron')
    print(' ')
    print(' ')
    n1 = Neuron(1)
    n2 = Neuron(2)
    n3 = Neuron(3)
    n3.connect(n1, 2)
    n3.connect(n2, 3)

    s = 0.1234567890123456789
    for i in range(5001):
        e = s - n3.calculate()
        n3.add_error(e)
        n3.correct()
        if i % 500 == 0:
            print(i, n3)
    print('get connections')
    print(n3.calculate())
    print(' ')
    print(' ')
    print('End Test Neuron')
    print(' ')
    print(' ')


