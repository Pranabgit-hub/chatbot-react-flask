import torch
import torch.nn as nn
import pickle
import json
import re
import random
import requests
import wikipedia
from flask import Flask, request, jsonify
from flask_cors import CORS
from transformers import pipeline
from dotenv import load_dotenv
import os

from torch.nn.utils.rnn import pad_sequence

# Load environment variables
load_dotenv()
app = Flask(__name__)
CORS(app)

# === Load artifacts ===
with open("vocab.pkl", "rb") as f:
    vocab = pickle.load(f)

with open("label_encoder.pkl", "rb") as f:
    lbl_encoder = pickle.load(f)

with open("intents.json", encoding='utf-8') as f:
    intents = json.load(f)

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
vocab_size = len(vocab)
num_classes = len(lbl_encoder.classes_)

# === Feedforward PyTorch Model (Matches Colab Training) ===
class IntentModel(nn.Module):
    def __init__(self, vocab_size, embed_dim, hidden_dim, num_classes):
        super(IntentModel, self).__init__()
        self.embedding = nn.Embedding(vocab_size, embed_dim, padding_idx=0)
        self.fc1 = nn.Linear(embed_dim, hidden_dim)
        self.relu = nn.ReLU()
        self.fc2 = nn.Linear(hidden_dim, num_classes)

    def forward(self, x):
        x = self.embedding(x)
        x = x.mean(dim=1)  # mean pooling
        x = self.relu(self.fc1(x))
        return self.fc2(x)

model = IntentModel(vocab_size, embed_dim=64, hidden_dim=64, num_classes=num_classes).to(device)
model.load_state_dict(torch.load("lstm_model.pt", map_location=device))
model.eval()

# === Preprocess user input ===
def preprocess(msg):
    tokens = re.findall(r"\b\w+\b", msg.lower())
    indexed = [vocab.get(tok, 1) for tok in tokens]  # 1 = unknown token
    tensor = pad_sequence([torch.tensor(indexed)], batch_first=True)
    return tensor.to(device)

# === Chat route ===
@app.route("/chat", methods=["POST"])
def chat():
    inp = request.json.get("message", "").strip()
    msg = inp.lower()

    # === 1. Summarization trigger ===
    if msg.startswith("summarize:"):
        text_to_summarize = inp[len("summarize:"):].strip()

        # Lazy-load Pegasus
        summarizer = pipeline(
            "summarization",
            model="google/pegasus-xsum",
            tokenizer="google/pegasus-xsum",
            framework="pt"
        )

        summary = summarizer(
            text_to_summarize, max_length=50, min_length=15, do_sample=False
        )[0]["summary_text"]
        return jsonify({"response": summary})

    # === 2. Generative Q&A with Wikipedia Context ===
    if msg.startswith("question:"):
        question = inp[len("question:"):].strip()

        try:
            topic = question.split()[-1]  # crude heuristic
            context = wikipedia.summary(topic, sentences=3)
        except Exception as e:
            context = "I couldn't retrieve information from Wikipedia."

        prompt = f"question: {question} context: {context}"

        gen_qa_pipeline = pipeline(
            "text2text-generation",
            model="google/flan-t5-base",
            tokenizer="google/flan-t5-base",
            framework="pt"
        )

        result = gen_qa_pipeline(prompt , max_new_tokens=128, do_sample=False)[0]["generated_text"]
        return jsonify({"response": result})
    # === 3. Intent classification ===
    input_tensor = preprocess(msg)
    with torch.no_grad():
        output = model(input_tensor)
        probs = torch.softmax(output, dim=1)
        conf, predicted = torch.max(probs, dim=1)

    predicted_tag = lbl_encoder.inverse_transform([predicted.item()])[0]
    print(f"Input: {msg} | Predicted: {predicted_tag} | Confidence: {conf.item():.2f}")

    if conf.item() >= 0.04:
        for intent in intents["intents"]:
            if intent["tag"] == predicted_tag:
                return jsonify({"response": random.choice(intent["responses"])})

    # === 4. Fallback ===
    return jsonify({"response": "Sorry, I couldn't find an answer for that."})

if __name__ == "__main__":
    print("Starting Flask backend...")
    app.run(debug=True)

