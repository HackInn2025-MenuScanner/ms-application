from pydantic import BaseModel
from typing import List

class MenuItem(BaseModel):
    original_name: str
    translated_name: str

class MenuItems(BaseModel):
    items: List[MenuItem] = []