from enum import Enum
from flask import Flask, request, jsonify, render_template
from generate_scripts.generate_lstm_onnx import generate as generate_lstm
from generate_scripts.generate_gpt_onnx import generate as generate_gpt


class MODELS(Enum):
    GPT = 0
    LSTM = 1


class DEFAULT_VALUES(Enum):
    METHOD = 0
    K = 10
    MODEL = MODELS.GPT.value
    SEQ_LEN = 25


def validate(v, c):
    if v < c[0] or v > c[1]:
        return False
    return True


def trim_verse(verse, max_len):
    words = verse.split(' ')
    res = ''
    for word in words:
        if len(res) + len(word) > max_len:
            break
        res += ' ' + word
    return res


app = Flask(__name__)


@app.route('/')
def root():
    print('root')
    return render_template('index.html'), 200


@app.get('/api')
def test():
    return "ManshoorAI", 200


@app.get('/api/generate')
def generate_verse():
    try:
        verse = request.args.get('verse')
        seq_len = int(request.args.get('len') or DEFAULT_VALUES.SEQ_LEN.value)
        method = int(request.args.get('method') or DEFAULT_VALUES.METHOD.value)
        k = int(request.args.get('k') or DEFAULT_VALUES.K.value)
        model = int(request.args.get('model') or DEFAULT_VALUES.MODEL.value)
        verse = trim_verse(verse, 30)
        if not validate(model, [-1, 2]) or \
                not validate(seq_len, [0, 50]) or \
                not validate(method, [-1, 2]) or \
                not validate(k, [1, 1000]):
            raise ValueError('invalid parameters')
        if not verse or len(verse) < 0:
            return jsonify(message="Please provide a sample verse"), 400
        output = ''
        if model == MODELS.GPT.value:
            output = generate_gpt(verse, seq_len)
        else:
            output = generate_lstm(verse, seq_len, k, decoding_method=method)
        return jsonify(verse=output), 200
    except ValueError:
        return jsonify(message="Invalid request format"), 400
    except RuntimeError:
        return jsonify(message="model onnx file not found"), 400


if __name__ == "__main__":
    print("\n\n** ManshoorAI **\n\n")
    app.run(host='127.0.0.1', port=4000)
