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
                if curr_word not in self.states:
                    self.states.append(curr_word)
                if next_word not in self.states:
                    self.states.append(next_word)
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

        self.markov_matrix = np.zeros((len(self.states), len(self.states)))
        for i in range(self.markov_matrix.shape[0]):
            for j in range(self.markov_matrix.shape[1]):
                prop_dict = self.markov_dict.get(self.states[i], 0)
                if(type(prop_dict) is not int):
                    self.markov_matrix[i][j] = prop_dict.get(self.states[j], 0) 
                else: 
                    self.markov_matrix[i][j] = prop_dict
        np.set_printoptions(precision=10)
        M = self.markov_matrix - np.identity(len(self.states))
        M = np.transpose(M)
        M[0] = np.ones(M.shape[0])
        b = np.zeros(M.shape[0])
        b[0] = 1
        self.vector_state = np.linalg.solve(M, b)

    def choose_next(self):
        edges = self.markov_dict.get(self.curr_state, 0)
        if(type(edges) is not int):
            for next_state in edges.keys():
                if (random.random() < edges[next_state]):
                    self.curr_state = next_state
                    return self.curr_state
        return True

    def gen_text(self):
        '''
        Generates text through the Markov Chain
        '''
        quote = ""
        prop = 0
        done = False

        for i in range(len(self.vector_state)):
            if (random.random() < self.vector_state[i] + prop):
                self.curr_state = self.states[i]
                quote += self.curr_state
                break
            else:
                prop += self.vector_state[i]

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
        nn.save(sys.argv[2])
    except Exception as e:
        print(e)
