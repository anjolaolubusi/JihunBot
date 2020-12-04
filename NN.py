import sys
import pickle
import tensorflow as tf
import numpy as np

from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.layers import Embedding, LSTM, Dense, Bidirectional
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.models import Sequential
from tensorflow.keras.optimizers import Adam


if(len(sys.argv) == 2):
    file = open(sys.argv[1])
elif(len(sys.argv) == 1):
    file = open('Jihun_Bot_Training_Data.txt')
else:
    print(" Remember python get_data.py <file name>")
    sys.exit()

SourceData = []
try:
    for line in file:
        SourceData.append(line.replace('\n', ''))

    tokenizer = Tokenizer()
    tokenizer.fit_on_texts(SourceData)

    with open('Tokenizer', 'wb') as OutputPath:
        pickle.dump(tokenizer, OutputPath)

    total_words = len(tokenizer.word_index) + 1
    
    input_sequences = []
    for line in SourceData:
        token_list = tokenizer.texts_to_sequences([line])[0]
        for i in range(1, len(token_list)):
            n_gram_sequence = token_list[:i+1]
            input_sequences.append(n_gram_sequence)

    max_sequence_len = max([len(x) for x in input_sequences])
    input_sequences = np.array(pad_sequences(input_sequences, maxlen=max_sequence_len, padding='pre'))

    xs = input_sequences[:, :-1]
    labels = input_sequences[:, -1]

    ys = tf.keras.utils.to_categorical(labels, num_classes=total_words)

    model = Sequential()
    model.add(Embedding(total_words, 240, input_length=max_sequence_len-1))
    model.add(Bidirectional(LSTM(150)))
    model.add(Dense(total_words, activation='softmax'))
    adam = Adam(lr=0.01)
    model.compile(loss='categorical_crossentropy', optimizer=adam, metrics=['accuracy'])
    history = model.fit(xs, ys, epochs=100, verbose=1)

    with open('JBrain.nn', 'wb') as OutputPath:
        pickle.dump(padded, OutputPath)

    print("Data is processed and neural network is trained")
finally:
    file.close()
