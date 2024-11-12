# Manshoor: Generate Farsi Poems with AI! ✒️

Welcome to **ManshoorAI**, a fun and interactive machine learning project that brings the magic of poetry right to your fingertips! Give us a few words, and our model will craft a beautiful Persian poem inspired by the style of famous Persian poet "Sohrab Sepehri" *(we plan to add more styles in the future)*.

> [!IMPORTANT]  
> Think of this as a fun, hobby project! At this early stage, the results aren't great—I'm fully aware of that. My plan is to gradually improve the model, and hopefully, with your help, we can make it better over time.  
> For now, don't worry too much about the results—it's all part of the process!

## 🗂️ Table of Contents

- [✨ Features](#-features)
- [🚀 Quick Start](#-quick-start)
- [🛠️ How It Works](#️-how-it-works)
- [📚 Methods Explained](#-methods-explained)
- [📝 Example Poem](#-example-poem)
- [🛡️ License](#️-license)
- [💬 Feedback and Contributions](#-feedback-and-contributions)

---

## ✨ Features

- **Input your own words** to inspire the poem.
- **Choose a generation method**:
  - **Greedy**: Always pick the best next word.
  - **Random Sampling**: Add a touch of unpredictability.
  - **Top-k Sampling**: Balance creativity and coherence.
- **Control the length** of the poem.
- **Simple Frontend**: A user-friendly web interface.
- **Flask API Backend**: Powered by [Flask](https://github.com/pallets/flask), running on your local network.

---

## 🚀 Quick Start

### Prerequisites

Make sure you have the following installed:
- Python 3.8+
- `pip` for package management

### 1. Clone the Repository

```bash
git clone https://github.com/Rahiminia/manshoor-ai.git
cd manshoor-ai
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the Backend

Start the Flask API on `localhost:4000`:

```bash
python main.py
```

### 4. Run the Frontend

Once the backend is up and running, open the frontend:
- Navigate to `http://127.0.0.1:4000` in your favorite browser.

> [!Note]
> Ensure that port 4000 is not being used by any other programs.
>

---

## 🛠️ How It Works

### IPython Notebook

I've provided the .ipynb file that defines and trains the model. You can customize the model, use your own data, or make any other modifications as needed.

The model includes an embedding layer and multiple LSTM layers to capture relationships between word vectors.

I also provided the tokenizer used as .json file

*I'm happy to hear your thoughts on my approach/method.*

### Backend API

The Flask backend serves as the engine of ManshoorAI, handling requests to generate poems.

#### API Endpoints

- **`GET /api/generate`**  
  Accepts input words, generation method, and desired length. Returns a freshly generated poem.  
  **Request Body**:
  ```json
  {
    "verse": "در این شب سیاه",
    "method": "top_k",
    "len": 20,
    "k": 5
  }
  ```

### Frontend

A simple web interface to make poetry generation accessible and fun! You can:
- Enter your input words.
- Select a generation method.
- Choose the desired poem length.
- Get your poem instantly!

---

## 📚 Methods Explained

1. **Greedy**: Picks the most probable next word every time.  
   *Pros*: Coherent and structured output.  
   *Cons*: Can feel repetitive or dull.

2. **Random Sampling**: Introduces randomness at each step.  
   *Pros*: Creative and surprising.  
   *Cons*: Can sometimes lack coherence.

3. **Top-k Sampling**: Chooses from the top-k most likely words.  
   *Pros*: Strikes a balance between creativity and structure.  
   *Cons*: Requires tuning of the `k` parameter.

---

## 📝 Example Poem

<img src="https://github.com/user-attachments/assets/7cf68b16-8c9a-4f12-9988-2547ee85b5fe" alt="Example result" width="400px" />

## 🛡️ License

This project is licensed under the MIT License. Feel free to fork, modify, and share!

---

## 💬 Feedback and Contributions

I'd love to hear your thoughts! Found a bug or have an idea for a new feature?  
Open an issue or submit a pull request on [GitHub](https://github.com/Rahiminia/manshoor-ai).

---

Give this project a Star⭐ if you like it :)
