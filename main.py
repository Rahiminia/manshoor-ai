from flask import Flask, request, jsonify, render_template
from generate import generate

app = Flask(__name__)

@app.route('/')
def root():
    print('root')
    return render_template('index.html'), 200

@app.get('/api')
def test():
    return "SohrabAI", 200

@app.get('/api/generate')
def generate_verse():
    verse = request.args.get('verse')
    if not verse or len(verse) < 0:
        return jsonify(message="Please provide a sample verse"), 400
    output = generate(verse)
    return jsonify(verse=output), 200

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=4000)
