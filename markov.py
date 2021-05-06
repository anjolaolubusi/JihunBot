import random

#Possible use: https://stackoverflow.com/questions/8550912/dictionary-of-dictionaries-in-python

class MarkovBrain():
    '''
    MarkovBrain class represents the Markov Chain. It includes a training 
    method and a method to generate text.
    '''
    def __init__(self):
        self.markov_matrix = dict()
        self.states = set()

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
                print("{} -> {}".format(curr_word, next_word))
                if curr_word in self.markov_matrix:
                    if next_word in self.markov_matrix[curr_word]:
                        self.markov_matrix[curr_word][next_word] += 1
                    else:
                        self.markov_matrix[curr_word][next_word] = 1
                else:
                    self.markov_matrix[curr_word] = {next_word: 1}
        print(self.markov_matrix)
        print(len(self.markov_matrix))

    def gen_text():
        '''
        Generates text through the Markov Chain
        '''
        pass
