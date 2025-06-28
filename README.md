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
