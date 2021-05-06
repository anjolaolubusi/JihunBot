import pickle
from markov import *

def train_NN():
    nn = MarkovBrain()
    TData = ["A B C D", "A B B A"]
    print(TData)
    print("\n")
    nn.train(TData)

def save_NN():
    pass

if __name__ == '__main__':
    train_NN()
