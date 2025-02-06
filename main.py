from flask import Flask, request, jsonify, render_template
from generate_scripts.generate_lstm_onnx import generate

def validate(v, c):
    if v < c[0] or v > c[1]:
        return False
    return True

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
        seq_len = int(request.args.get('len'))
        method = int(request.args.get('method'))
        k = int(request.args.get('k'))
        if not validate(seq_len, [0, 50]) or not validate(method, [-1, 2]) or not validate(k, [1, 1000]):
            raise ValueError('invalid parameters')
        if not verse or len(verse) < 0:
            return jsonify(message="Please provide a sample verse"), 400
        output = generate(verse, seq_len, k, decoding_method=method)
        return jsonify(verse=output), 200
    except:
        return jsonify(message="Invalid request format"), 400

if __name__ == "__main__":
    print("\n\n** ManshoorAI **\n\n")
    app.run(host='127.0.0.1', port=4000)
