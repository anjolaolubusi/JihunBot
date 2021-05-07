import random
import numpy as np
import pickle
import sys

class MarkovBrain():
    '''
    MarkovBrain class represents the Markov Chain. It includes a training 
    method and a method to generate text.
    '''
    def __init__(self):
        self.markov_dict = dict()
        self.states = []
        self.curr_state = None

    def train(self, TData):
        '''
        Trains the Markov Chains
        '''
        curr_word = ""
        next_word = ""
        for line in TData:
            states_line = line.split(" ")
            for i in range(len(states_line)-1):
                curr_word = states_line[i]
                next_word = states_line[i+1]
                if curr_word not in self.states and i == 0:
                    self.states.append(curr_word)
                #if next_word not in self.states:
                    #self.states.append(next_word)
                if curr_word in self.markov_dict:
                    if next_word in self.markov_dict[curr_word]:
                        self.markov_dict[curr_word][next_word] += 1
                    else:
                        self.markov_dict[curr_word][next_word] = 1
                else:
                    self.markov_dict[curr_word] = {next_word: 1}

        for state in self.markov_dict.keys():
            total_sum = sum(self.markov_dict[state].values())
            for path in self.markov_dict[state].keys():
                self.markov_dict[state][path] = self.markov_dict[state][path]/total_sum
        
    def choose_next(self):
        edges = self.markov_dict.get(self.curr_state, 0)
        if(type(edges) is not int):
            prop = 0
            for next_state in edges.keys():
                if (random.random() < edges[next_state] + prop):
                    self.curr_state = next_state
                    return self.curr_state
                else:
                    prop += edges[next_state]
        return True

    def gen_text(self):
        '''
        Generates text through the Markov Chain
        '''
        quote = ""
        prop = 0
        done = False

        a = random.random()
        start_i = int(a * len(self.states))
        self.curr_state = self.states[start_i]
        quote += self.curr_state

        while(done is False):
            next_word = self.choose_next()
            if(type(next_word) is str):
                quote += " {}".format(next_word)
            else:
                done = True
        
        return quote

    def save(self, filename):
        fname = filename + '.mchain'
        file = open(fname, 'wb')
        pickle.dump(self, file)
        file.close()

    def load(self, path):
        file = open(path, 'rb')
        data = pickle.load(file)
        file.close()
        return data

if __name__ == '__main__':
    try:
        if len(sys.argv) != 3:
            raise Exception("Please provide the proper data. \nThe proper command form is python markov.py [Path to Training Data] [Name of saved markov chain]")

        with open(sys.argv[1]) as f:
            content = f.readlines()

        nn = MarkovBrain()
        nn.train(content)
        for i in (range(10)):
            print(nn.gen_text())
        
        nn.save(sys.argv[2])
    except Exception as e:
        print(e)
