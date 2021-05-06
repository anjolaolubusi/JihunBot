import pickle
from markov import *

def train_NN():
    nn = MarkovBrain()
    TData = ["A B C D", "A B B A C C C C D D A A A C C CA J D A AS S JSAJAS", "ASJKASJJAS IASI A A A D D DK JJ D D D DK D"]
    print(TData)
    print("\n")
    nn.train(TData)

def save_NN():
    pass

if __name__ == '__main__':
    train_NN()
