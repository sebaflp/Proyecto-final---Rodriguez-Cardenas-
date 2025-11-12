from typing import List, Optional
from ingredient_ingredienteinventory import Ingredient
class HotDog:
    
    def __init__(self, name: str, bread: Ingredient, sausage: Ingredient, toppings: List[Ingredient], sauces: List[Ingredient], side: Optional[Ingredient] = None):
        if bread.category != "Pan" or sausage.category != "Salchicha":
            raise ValueError("Pan y salchicha deben ser de categorías correctas.")
        # Validación de longitud (asumir atributo 'length' en Ingredient si aplica)
        
        self.name = name
        self.bread = bread
        self.sausage = sausage
        self.toppings = toppings
        self.sauces = sauces
        self.side = side
    
    def check_inventory(self, inventory) -> bool:
        # Verificar si hay stock suficiente
        pass  # Implementar lógica
    
    def to_dict(self):
        return {
            "name": self.name,
            "bread": self.bread.to_dict(),
            "sausage": self.sausage.to_dict(),
            "toppings": [t.to_dict() for t in self.toppings],
            "sauces": [s.to_dict() for s in self.sauces],
            "side": self.side.to_dict() if self.side else None
        }
    
    def load_from_dict(self, data: dict, ingredient_manager):
        # Implementar carga
        pass
