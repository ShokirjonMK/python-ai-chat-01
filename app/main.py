from fastapi import FastAPI, Query
from app.model.similar_qa import get_best_answer

app = FastAPI()


@app.get("/ask")
def ask(
    category: str = Query(..., description="Kategoriya nomi"),
    question: str = Query(..., description="Savolingiz")
):
    answer = get_best_answer(category, question)
    return {
        "success": True,
        "category": category,
        "answer": answer
    }
