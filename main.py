from flask import Flask, request, jsonify
from generate import generate

app = Flask(__name__)

@app.get('/api')
def test():
    return "SohrabAI"

@app.get('/api/generate')
def generate_verse():
    verse = request.args.get('verse')
    if not verse or len(verse) < 0:
        return jsonify(message="Please provide a sample verse")
    output = generate(verse)
    return jsonify(verse=output)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=4000)