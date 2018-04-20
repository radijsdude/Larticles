from Neuron import Neuron
import random
import itertools

class Brain():
    def __init__(self,input_names,output_names,dna=None):

        self.input_names = input_names
        self.output_names = output_names
        self.all_names = []
        self.all_neurons = {}
        i = 0
        for name in self.input_names:
            self.all_names.append(name)
            self.all_neurons[name] = Neuron(name)
            n = 'hidden_' + str(i)
            self.all_names.append(n)
            self.all_neurons[n] = Neuron(n)
            i += 1

        for name in self.output_names:
            self.all_names.append(name)
            self.all_neurons[name] = Neuron(name)
            n = 'hidden_' + str(i)
            self.all_names.append(n)
            self.all_neurons[n] = Neuron(n)
            i += 1

        if dna != None:
            self.set_dna(dna)
        else:
            self.create_random_dna()





    def set_dna(self,dna):
        self.dna = dna
        for i, dna in enumerate(self.dna):
            name1, name2, weight = dna
            if name1 not in self.all_neurons:
                self.all_neurons[name1] = Neuron(name1)
            if name2 not in self.all_neurons:
                self.all_neurons[name2] = Neuron(name2)
            if name1 not in self.input_names:
                self.all_neurons[name1].connect(self.all_neurons[name2], weight)

        self.get_dna()

    def get_dna(self):
        con = []
        for name in self.all_neurons:
            con += self.all_neurons[name].get_connections()
        self.dna = con




    def create_random_dna(self):

        p = list(itertools.permutations(self.all_names, 2))
        length = random.randrange(int(len(self.all_names) / 2),int(len(self.all_names) * 2))
        dna = []

        for i in range(length):
            t = True
            while t:

                n1, n2 = random.choice(p)
                if n1 != n2 and n1 not in self.input_names:
                    r2 = random.randrange(-8, 9) / 4
                    dna.append([n1, n2, r2])
                    t = False
        self.get_dna()
        self.set_dna(dna)

    def mutate(self):
        r1 = random.randrange(0, 100)
        if 0 <= r1 < 33:
            if len(self.dna) != 0:
                r2 = random.randrange(0, len(self.dna))
                self.all_neurons[self.dna[r2][0]].disconnect(self.dna[r2][1])
                self.dna.pop(r2)

        elif 33 <= r1 < 66:
            n1 = random.choice(list(self.all_names))
            n2 = random.choice(list(self.all_names))
            if n1 != n2 and n1 not in self.input_names:
                r2 = random.randrange(-4, 5) / 4
                self.dna.append([n1, n2, r2])
                if n1 not in self.all_neurons:
                    self.all_neurons[n1] = Neuron(n1)
                if n2 not in self.all_neurons:
                    self.all_neurons[n2] = Neuron(n2)
                tt = self.all_neurons[n1].connect(self.all_neurons[n2],r2)
                if tt:
                    self.dna.append([n1,n2,r2])

        elif 66 <= r1 <= 99:
            if len(self.dna) != 0:
                r2 = random.randrange(0, len(self.dna))
                r3 = random.randrange(-4, 5) / 4
                self.dna[r2][-1] = r3
                self.all_neurons[self.dna[r2][0]].connect(self.all_neurons[self.dna[r2][0]],r3)
        self.get_dna()
        self.set_dna(self.dna)


    def tobody(self,inputs):

        result = {}

        for name in inputs:
            self.all_neurons[name].set(inputs[name])
        for name in self.output_names:
            result[name] = self.all_neurons[name].calculate()

        return result



































