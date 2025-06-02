import json
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

BASE_DIR = os.path.dirname(__file__)
qa_path = os.path.join(BASE_DIR, "qa_data.json")


def load_qa():
    with open(qa_path, encoding="utf-8") as f:
        return json.load(f)


def get_best_answer(category, user_question):
    data = load_qa()
    if category not in data:
        return f"Kategoriya topilmadi: {category}"

    qa_pairs = data[category]
    questions = [item['question'] for item in qa_pairs]
    answers = [item['answer'] for item in qa_pairs]

    vectorizer = TfidfVectorizer().fit(questions + [user_question])
    user_vec = vectorizer.transform([user_question])
    question_vecs = vectorizer.transform(questions)

    similarities = cosine_similarity(user_vec, question_vecs).flatten()
    top_score = similarities.max()
    top_index = similarities.argmax()

    if top_score < 0.75:
        return "Savol to‘liq mos kelmadi. Iltimos, savolni boshqacha shaklda yozib ko‘ring."

    return answers[top_index]
