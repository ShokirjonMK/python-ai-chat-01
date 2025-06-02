import json
import os
from sentence_transformers import SentenceTransformer, util

BASE_DIR = os.path.dirname(__file__)
qa_path = os.path.join(BASE_DIR, "qa_data.json")

# Sentence-BERT modeli (multilingual va yengil)
model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')


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

    question_embeddings = model.encode(questions, convert_to_tensor=True)
    user_embedding = model.encode(user_question, convert_to_tensor=True)

    similarities = util.cos_sim(user_embedding, question_embeddings)[0]
    best_score = similarities.max().item()
    best_index = similarities.argmax().item()

    if best_score < 0.5:
        return "Savol ma’nosi aniq topilmadi. Iltimos, savolni yanada aniqroq shaklda yozing."

    return answers[best_index]
