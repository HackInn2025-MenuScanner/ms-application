from pydantic import BaseModel, Field


class Nutrients(BaseModel):
    calories: float = 0.0
    protein_g: float = Field(0.0, description="Protein in grams")
    fat_g: float = Field(0.0, description="Fat in grams")
    carbs_g: float = Field(0.0, description="Carbohydrates in grams")
    fiber_g: float = Field(0.0, description="Fiber in grams")


class FoodNutrition(BaseModel):
    dish_name: str
    food_name: str
    food_id: str = ""
    nutrients: Nutrients
    food_description: str = ""
    food_url: str = ""