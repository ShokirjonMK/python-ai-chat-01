from fastapi import FastAPI, Query
from app.routes import category, qa
from app.services.ai import get_best_answer

app = FastAPI()

app.include_router(category.router)
app.include_router(qa.router)


@app.get("/ask")
def ask(category_id: str = Query(...), question: str = Query(...)):
    answer = get_best_answer(category_id, question)
    return {
        "category_id": category_id,
        "question": question,
        "answer": answer
    }
