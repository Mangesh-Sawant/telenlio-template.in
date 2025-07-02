from typing import List

from app.core.deps import get_current_user, TokenData
from app.db.mongo import db
from app.models.template_model import TemplateCreate
from app.pdf.generator import generate_pdf_from_template
from bson import ObjectId, errors
from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import FileResponse

router = APIRouter(prefix="/templates", tags=["Templates"])


def safe_object_id(id: str):
    try:
        return ObjectId(id)
    except (errors.InvalidId, TypeError):
        return None


@router.post("/", status_code=201)
async def create_template(
        template: TemplateCreate,
        current_user: TokenData = Depends(get_current_user)
):
    new_template = template.dict()
    new_template["user_id"] = str(current_user.user_id)
    result = await db.templates.insert_one(new_template)
    return {"message": "Template created", "template_id": str(result.inserted_id)}


@router.get("/", response_model=List[dict])
async def get_all_templates(current_user: TokenData = Depends(get_current_user)):
    templates = await db.templates.find({"user_id": str(current_user.user_id)}).to_list(length=100)
    for t in templates:
        t["_id"] = str(t["_id"])
    return templates


@router.get("/{template_id}")
async def get_template(template_id: str, current_user: TokenData = Depends(get_current_user)):
    obj_id = safe_object_id(template_id)
    if not obj_id:
        raise HTTPException(status_code=400, detail="Invalid template ID format")

    template = await db.templates.find_one({"_id": obj_id, "user_id": str(current_user.user_id)})
    if not template:
        raise HTTPException(status_code=404, detail="Template not found")

    template["_id"] = str(template["_id"])
    return template


@router.delete("/{template_id}")
async def delete_template(template_id: str, current_user: TokenData = Depends(get_current_user)):
    obj_id = safe_object_id(template_id)
    if not obj_id:
        raise HTTPException(status_code=400, detail="Invalid template ID format")

    result = await db.templates.delete_one({"_id": obj_id, "user_id": str(current_user.user_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Template not found")

    return {"message": "Template deleted"}


@router.patch("/{template_id}")
async def update_template(
        template_id: str,
        updates: dict,  # Accepts partial fields like {"title": "new title"}
        current_user: TokenData = Depends(get_current_user)
):
    obj_id = safe_object_id(template_id)
    if not obj_id:
        raise HTTPException(status_code=400, detail="Invalid template ID format")

    # Ensure the template belongs to the user
    template = await db.templates.find_one({"_id": obj_id, "user_id": str(current_user.user_id)})
    if not template:
        raise HTTPException(status_code=404, detail="Template not found")

    # Clean input fields to avoid overwriting user_id or _id
    disallowed_fields = {"_id", "user_id"}
    for key in disallowed_fields:
        updates.pop(key, None)

    if not updates:
        raise HTTPException(status_code=400, detail="No valid fields to update")

    await db.templates.update_one({"_id": obj_id}, {"$set": updates})
    return {"message": "Template updated"}


@router.post("/{template_id}/render", summary="Render template to PDF")
async def render_template_to_pdf(
        template_id: str,
        data: dict,
        current_user: TokenData = Depends(get_current_user)
):
    obj_id = safe_object_id(template_id)
    if not obj_id:
        raise HTTPException(status_code=400, detail="Invalid template ID format")

    template = await db.templates.find_one({"_id": obj_id, "user_id": str(current_user.user_id)})
    if not template:
        raise HTTPException(status_code=404, detail="Template not found")

    pdf_path = generate_pdf_from_template(
        html=template["html"],
        css=template["css"],
        data=data
    )

    return FileResponse(
        path=pdf_path,
        media_type="application/pdf",
        filename=f"{template['title']}.pdf"
    )
