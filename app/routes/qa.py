from fastapi import APIRouter
from fastapi import Request
from app.db import qa_collection
from app.models import QAItem
from bson import ObjectId
from typing import List
from fastapi import HTTPException
from typing import Optional

router = APIRouter(prefix="/qa", tags=["QA"])


@router.get("/")
def list_qa(category_id: Optional[str] = None, search: Optional[str] = None):
    filter_query = {}

    if category_id:
        filter_query["category_id"] = category_id

    if search:
        filter_query["question"] = {"$regex": search, "$options": "i"}

    items = qa_collection.find(filter_query)

    return [
        {
            "id": str(item["_id"]),
            "category_id": item["category_id"],
            "question": item["question"],
            "answer": item["answer"]
        }
        for item in items
    ]



@router.post("/")
def create_qa(data: QAItem):
    # Unikal savolni tekshiramiz (shu kategoriya ichida)
    existing = qa_collection.find_one({
        "category_id": data.category_id,
        "question": data.question
    })
    if existing:
        return {
            "success": False,
            "message": f"Ushbu savol '{data.question}' allaqachon mavjud."
        }

    result = qa_collection.insert_one(data.dict(exclude={"id"}))
    return {
        "success": True,
        "id": str(result.inserted_id),
        **data.dict()
    }


@router.post("/bulk")
def create_qa_bulk(items: List[QAItem]):
    inserted = []
    skipped = []

    for item in items:
        exists = qa_collection.find_one({
            "category_id": item.category_id,
            "question": item.question
        })
        if exists:
            skipped.append(item.question)
            continue

        qa_collection.insert_one(item.dict(exclude={"id"}))
        inserted.append(item.question)

    return {
        "success": True,
        "inserted": inserted,
        "skipped": skipped
    }


@router.put("/{id}")
def update_qa(id: str, data: QAItem):
    qa_collection.update_one({"_id": ObjectId(id)}, {"$set": data.dict()})
    return {"id": id, **data.dict()}


@router.delete("/{id}")
def delete_qa(id: str):
    qa_collection.delete_one({"_id": ObjectId(id)})
    return {"success": True}
