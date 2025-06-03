from sentence_transformers import SentenceTransformer, util
from app.db import qa_collection
from bson import ObjectId
from app.services.llm import generate_llm_response


model = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")


# def get_best_answer(category_id: str, user_question: str) -> str:
#     qa_items = list(qa_collection.find({"category_id": category_id}))
#     if not qa_items:
#         return "Bu kategoriya bo‘yicha savollar mavjud emas."

#     questions = [q["question"] for q in qa_items]
#     answers = [q["answer"] for q in qa_items]

#     question_embeddings = model.encode(questions, convert_to_tensor=True)
#     user_embedding = model.encode(user_question, convert_to_tensor=True)

#     similarities = util.cos_sim(user_embedding, question_embeddings)[0]
#     best_score = similarities.max().item()
#     best_index = similarities.argmax().item()

#     if best_score < 0.5:
#         return "Savolingiz tushunarsiz. Iltimos, aniqroq yozing."

#     return answers[best_index]


def get_best_answer(category_id: str, user_question: str):
    qa_items = list(qa_collection.find({"category_id": category_id}))
    if not qa_items:
        return generate_llm_response(user_question)

    questions = [q["question"] for q in qa_items]
    answers = [q["answer"] for q in qa_items]

    question_embeddings = model.encode(questions, convert_to_tensor=True)
    user_embedding = model.encode(user_question, convert_to_tensor=True)

    similarities = util.cos_sim(user_embedding, question_embeddings)[0]
    best_score = similarities.max().item()
    best_index = similarities.argmax().item()

    if best_score < 0.5:
        return generate_llm_response(user_question)

    return answers[best_index]
