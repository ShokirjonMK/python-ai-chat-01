from fastapi import APIRouter
from app.db import category_collection
from app.models import Category
from bson import ObjectId

router = APIRouter(prefix="/categories", tags=["Category"])


@router.get("/")
def list_categories():
    return [{"id": str(c["_id"]), "name": c["name"]} for c in category_collection.find()]


@router.post("/")
def create_category(data: Category):
    # Avval mavjudligini tekshiramiz
    existing = category_collection.find_one({"name": data.name})
    if existing:
        return {
            "success": False,
            "message": f"Kategoriya nomi '{data.name}' allaqachon mavjud."
        }

    result = category_collection.insert_one(data.dict(exclude={"id"}))
    return {
        "success": True,
        "id": str(result.inserted_id),
        "name": data.name
    }


@router.put("/{id}")
def update_category(id: str, data: Category):
    category_collection.update_one(
        {"_id": ObjectId(id)}, {"$set": data.dict()})
    return {"id": id, "name": data.name}


@router.delete("/{id}")
def delete_category(id: str):
    category_collection.delete_one({"_id": ObjectId(id)})
    return {"success": True}
