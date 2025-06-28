# 🤖 Chatbot with PyTorch + Transformers

A full-stack chatbot project featuring a React frontend and Flask backend. It combines a custom-trained **intent classifier using PyTorch** with **state-of-the-art NLP models** from Hugging Face Transformers — specifically **FLAN-T5** for generative question answering and **Pegasus-XSum** for text summarization. The chatbot is able to classify user intent, answer factual questions using Wikipedia summaries, and summarize text input.

---

## 🚀 Features

### 🧠 1. Intent Classification (PyTorch)
- A feedforward neural network trained in Google Colab using PyTorch.
- Preprocessed user inputs are classified into one of the predefined intent tags.
- Intent labels and training data stored in `intents.json`.
- Artifacts used: `vocab.pkl`, `label_encoder.pkl`, and `lstm_model.pt` (feedforward model).

### 📚 2. Generative Q&A with FLAN-T5
- Uses **Google FLAN-T5** via Hugging Face Transformers to answer factual questions.
- Fetches relevant context from Wikipedia using `wikipedia` Python module.
- Format: `question: What is AI?` → FLAN-T5 answers based on retrieved Wikipedia summary.

### ✂️ 3. Text Summarization with Pegasus
- Triggered with: `summarize: <text>`
- Uses **Google Pegasus-XSum**, a transformer-based summarization model from Hugging Face.
- Produces short, coherent summaries.

### 🛡️ 4. Fallback
- When the model's confidence is too low, it returns a default fallback response.

---

## 📁 Project Structure

```
chatbot-react-flask/
│
├── backend/
│   ├── app.py                  # Flask backend
│   ├── lstm_model.pt          # Trained PyTorch model (feedforward)
│   ├── vocab.pkl              # Vocabulary used in training
│   ├── label_encoder.pkl      # Scikit-learn label encoder
│   ├── intents.json           # Training data for intents
│   └── .env                   # Environment variables (Hugging Face tokens etc.)
│
├── chatbot/                   # React frontend
│   ├── src/                   # React components
│   ├── public/
│   ├── package.json
│   └── ...
│
└── README.md
```

---

## 🔧 Installation & Setup

### Backend (Flask + PyTorch)
```bash
cd backend
python -m venv venv
venv\Scripts\activate  # On Windows
pip install -r requirements.txt
python app.py
```

### Frontend (React)
```bash
cd chatbot
npm install
npm start
```

---

## 🌐 How It Works
- The React frontend sends a POST request to the Flask backend with the user's message.
- Flask:
  - If the message starts with `question:`, it uses FLAN-T5 + Wikipedia.
  - If it starts with `summarize:`, it runs Pegasus-XSum.
  - Otherwise, it classifies the intent using the custom PyTorch model.

---

## 🧪 Example Prompts
```
Hi, how are you?
question: What is Python?
summarize: Artificial Intelligence is a branch of computer science that...
```

---

## 🛠️ Tech Stack
- **Frontend**: React, Axios, HTML/CSS
- **Backend**: Flask, PyTorch, Transformers (Hugging Face)
- **Models**:
  - Custom feedforward neural network for intent classification (PyTorch)
  - FLAN-T5 (generative QA)
  - Pegasus-XSum (summarization)

---

## 🔐 Environment Variables (.env)
Create a `.env` file in the `backend/` folder:
```
HUGGINGFACEHUB_API_TOKEN=your_token_here
```

> ⚠️ **Make sure your `.env` is in `.gitignore`!**

---

## 🙌 Acknowledgements
- [Hugging Face Transformers](https://huggingface.co/transformers/)
- [Google Pegasus](https://huggingface.co/google/pegasus-xsum)
- [Google FLAN-T5](https://huggingface.co/google/flan-t5-base)
- PyTorch + Flask

---

## 📃 License
This project is open-source under the [MIT License](LICENSE).
