from sentence_transformers import SentenceTransformer, util
import json
import os

BASE_DIR = os.path.dirname(__file__)
qa_path = os.path.join(BASE_DIR, "qa_data.json")

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

    embeddings = model.encode(
        questions + [user_question], convert_to_tensor=True)
    user_emb = embeddings[-1]
    sims = util.pytorch_cos_sim(user_emb, embeddings[:-1]).squeeze()

    top_score = sims.max().item()
    top_index = sims.argmax().item()

    if top_score < 0.5:
        return "Mazmunga mos savol topilmadi. Iltimos, aniqroq savol bering."

    return answers[top_index]
