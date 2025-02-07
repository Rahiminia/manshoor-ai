import numpy as np
import onnxruntime as ort
from tokenizers import Tokenizer

def load_tokenizer(filename):
    return Tokenizer.from_file(filename)

def load_model(filename):
    try:
        return ort.InferenceSession(filename)
    except:
        raise RuntimeError('onnx model file not found')

def generate(verse, seq_len=25, temperature=0.75, tokenizer_filename='models/gpt_tokenizer.json', model_filename='models/model.onnx'):
    sentence = verse
    tokenizer = load_tokenizer(tokenizer_filename)
    loaded_model = load_model(model_filename)
    SEQ_LEN = np.clip(seq_len, 1, 50)
    TEMP = np.clip(temperature, 0, 1)
    input_ids = np.array([tokenizer.encode(sentence).ids])
    attention_mask = np.ones_like(input_ids)
    position_ids = np.cumsum(attention_mask, axis=-1) - 1
    position_ids[position_ids < 0] = 0
    for _ in range(SEQ_LEN):
        ort_inputs = {
            "input_ids": input_ids,
            "attention_mask": attention_mask,
            "position_ids": position_ids
        }
        ort_outputs = loaded_model.run(None, ort_inputs)
        logits = ort_outputs[0]
        next_token_logits = logits[:, -1, :]
        if TEMP == 0:
            next_token = np.argmax(next_token_logits, axis=-1).item()
        else:
            scaled_logits = next_token_logits / TEMP
            scaled_logits = scaled_logits - np.max(scaled_logits, axis=-1, keepdims=True)
            exp_logits = np.exp(scaled_logits)
            probs = exp_logits / np.sum(exp_logits, axis=-1, keepdims=True)
            probs = probs[0]
            next_token = np.random.choice(probs.shape[0], p=probs)
        input_ids = np.concatenate((input_ids, [[next_token]]), axis=1)
        attention_mask = np.concatenate((attention_mask, [[1]]), axis=1)
        position_ids = np.concatenate((position_ids, [[position_ids[0][-1] + 1]]), axis=1)

    generated_text = tokenizer.decode(input_ids[0], skip_special_tokens=True)
    return generated_text

# print(generate('در این شب سیاه'))