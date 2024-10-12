import json
import tensorflow as tf
import numpy as np
from scipy.special import softmax
from tensorflow.keras.preprocessing.text import tokenizer_from_json
from tensorflow.keras.preprocessing.sequence import pad_sequences

DECODING_METHODS = { "greedy": 0, "sampling": 1, "top_k": 2 }

def load_tokenizer(filename='tokenizer.json'):
    try:
        with open(filename) as f:
            data = json.load(f)
            return tokenizer_from_json(data)
    except:
        print('{} not found!'.format(filename))

def load_model(filename='sohrab.keras'):
    try:
        return tf.keras.models.load_model(filename)
    except:
        print('{} not found!'.format(filename))

def generate(verse, seq_len=25, k=10, decoding_method=DECODING_METHODS['top_k'], tokenizer_filename='tokenizer.json', model_filename='sohrab.keras'):
    SEQ_LEN = seq_len
    K = k
    sentence = verse
    decoding_method = decoding_method
    tokenizer = load_tokenizer(tokenizer_filename)
    loaded_model = load_model(model_filename)
    vocab = tokenizer.word_index
    max_len = 17
    seq_len = np.clip(seq_len, 1, 50)
    k = np.clip(k, 1, 1000)
    decoding_method = np.clip(decoding_method, 0, 2)
    for _ in range(SEQ_LEN):
        s = tokenizer.texts_to_sequences([sentence])
        s = pad_sequences(s, maxlen=max_len)
        p = loaded_model.predict(s, verbose=0)
        if decoding_method == DECODING_METHODS['greedy']:
            idx = np.argmax(p[0])
        elif decoding_method == DECODING_METHODS['sampling']:
            idx = np.random.choice(range(1, len(vocab)+1), 1, p=p[0])
        elif decoding_method == DECODING_METHODS['top_k']:
            v = list(zip(range(1, len(vocab)+1), p[0]))
            v = np.array(sorted(v, key=lambda i: i[1], reverse=True)[:K])
            idx = np.random.choice(v[:,0], 1, p=softmax(v[:,1]))
        sentence +=  " " + [w for w in vocab if vocab[w]==idx][0]
    return sentence