import onnxruntime as ort
import numpy as np
from tokenizers import Tokenizer


def softmax(x):
    return np.exp(x)/sum(np.exp(x))


DECODING_METHODS = {
    "greedy": 0,
    "sampling": 1,
    "top_k": 2
}


def load_tokenizer(filename):
    return Tokenizer.from_file(filename)


def load_model(filename):
    return ort.InferenceSession(filename)


def pad_and_truncate(tokenizer, input, max_len):
    res = []
    for item in input:
        if len(item) >= max_len:
            res.append(item[:max_len])
        else:
            padding_size = max_len - len(item)
            res.append(
                ([tokenizer.token_to_id('[PAD]')] * padding_size) + item
            )
    return np.array(res)


def to_categorical(input, total):
    res = []
    for item in input:
        if item >= total:
            raise Exception('wrong number of classes')
        cat = np.zeros(total)
        cat[item] = 1
        res.append(cat)
    return np.array(res)


def generate(
        verse,
        seq_len=25,
        k=10,
        decoding_method=DECODING_METHODS['top_k'],
        tokenizer_filename='models/lstm_tokenizer.json',
        model_filename='models/lstm_model.onnx'):
    sentence = verse
    tokenizer = load_tokenizer(tokenizer_filename)
    loaded_model = load_model(model_filename)
    input_shape = loaded_model.get_inputs()[0].shape
    input_shape[0] = 1
    input_name = loaded_model.get_inputs()[0].name
    vocab_size = tokenizer.get_vocab_size()
    max_len = input_shape[-1]
    SEQ_LEN = np.clip(seq_len, 1, 50)
    K = np.clip(k, 1, 1000)
    DECODING_METHOD = np.clip(decoding_method, 0, 2)
    for _ in range(SEQ_LEN):
        s = tokenizer.encode(sentence).ids
        s = pad_and_truncate(tokenizer, [s], max_len)
        p = loaded_model.run(None, {input_name: s.astype(np.float32)})
        if DECODING_METHOD == DECODING_METHODS['greedy']:
            idx = np.argmax(p[0][0])
        elif DECODING_METHOD == DECODING_METHODS['sampling']:
            idx = np.random.choice(range(1, vocab_size + 1), 1, p=p[0][0])
        elif DECODING_METHOD == DECODING_METHODS['top_k']:
            v = list(zip(range(1, vocab_size + 1), p[0][0]))
            v = np.array(sorted(v, key=lambda i: i[1], reverse=True)[:K])
            idx = np.random.choice(v[:, 0], 1, p=softmax(v[:, 1]))
        sentence += " " + tokenizer.decode([int(idx)])
    return sentence
