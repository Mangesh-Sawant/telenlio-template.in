from pydantic import BaseModel, Field
from typing import Dict
from uuid import UUID

class TemplateBase(BaseModel):
    title: str
    html: str
    css: str
    example_data: Dict

class TemplateCreate(TemplateBase):
    pass

class TemplateInDB(TemplateBase):
    id: UUID
    user_id: UUID
