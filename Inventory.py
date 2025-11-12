from typing import Dict
import json 
class Inventory:
    
    def __init__(self, ingredient_manager):
        self.stock: Dict[str, int] = {}
        self.ingredient_manager = ingredient_manager
    
    def load_from_api(self):
        pass 
    
    def load_from_file(self, filename: str):
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                self.stock = json.load(f)
        except FileNotFoundError:
            pass  # Archivo opcional
    
    def save_to_file(self, filename: str):
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.stock, f, indent=4)
    
    def view_all(self):
        for name, qty in self.stock.items():
            print(f"{name}: {qty}")
    
    def search_ingredient(self, name: str) -> int:
        return self.stock.get(name, 0)
    
    def list_by_category(self, category: str):
        ingredients = self.ingredient_manager.list_by_category(category)
        for ing in ingredients:
            qty = self.stock.get(ing.name, 0)
            print(f"{ing.name}: {qty}")
    
    def update_stock(self, name: str, quantity: int):
        if not any(ing.name == name for ing in self.ingredient_manager.ingredients):
            raise ValueError(f"Ingrediente '{name}' no existe en la lista de ingredientes.")
        self.stock[name] = quantity
