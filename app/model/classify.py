import json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
import joblib
import os

BASE_DIR = os.path.dirname(__file__)

def train_model():
    with open(os.path.join(BASE_DIR, "categories.json"), encoding="utf-8") as f:
        data = json.load(f)

    texts, labels = [], []
    for cat, samples in data.items():
        texts.extend(samples)
        labels.extend([cat] * len(samples))

    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(texts)

    model = MultinomialNB()
    model.fit(X, labels)

    joblib.dump((model, vectorizer), os.path.join(BASE_DIR, "classifier.joblib"))

def load_model():
    return joblib.load(os.path.join(BASE_DIR, "classifier.joblib"))

def predict_category(text: str):
    model, vectorizer = load_model()
    X = vectorizer.transform([text])
    pred = model.predict(X)[0]
    prob = model.predict_proba(X).max()
    return pred, prob
