class Ingredient:
    def __init__(self, name: str, category: str, type_: str = ""):
        if not name.strip():
            raise ValueError("El nombre del ingrediente no puede estar vacío.")
        valid_categories = ["Pan", "Salchicha", "Topping", "Salsa", "Acompañante"]
        if category not in valid_categories:
            raise ValueError(f"Categoría '{category}' no es válida. Categorías permitidas: {valid_categories}")
        
        self.name = name.strip()
        self.category = category
        self.type_ = type_.strip()
    
    def to_dict(self):
        return {
            "name": self.name,
            "category": self.category,
            "type": self.type_
        }
    
    def load_from_dict(self, data: dict):
        if "name" not in data or "category" not in data:
            raise KeyError("El diccionario debe contener 'name' y 'category'.")
        
        name = data["name"]
        category = data["category"]
        type_ = data.get("type", "")
        
        if not name.strip():
            raise ValueError("El nombre del ingrediente no puede estar vacío.")
        valid_categories = ["Pan", "Salchicha", "Topping", "Salsa", "Acompañante"]
        if category not in valid_categories:
            raise ValueError(f"Categoría '{category}' no es válida. Categorías permitidas: {valid_categories}")
        
        self.name = name.strip()
        self.category = category
        self.type_ = type_.strip()


import requests
import json
from typing import List

class IngredientManager:
    
    def __init__(self):
        self.ingredients: List[Ingredient] = []
    
    def load_from_api(self):
        url = "https://api.github.com/repos/FernandoSapient/BPTSP05_2526-1/contents/"
        try:
            response = requests.get(url)
            response.raise_for_status()
            files = response.json()
            
            for file_info in files:
                if file_info['name'].endswith('.json') and 'ingredient' in file_info['name'].lower():
                    file_url = file_info['download_url']
                    file_response = requests.get(file_url)
                    file_response.raise_for_status()
                    data = file_response.json()
                    
                    for item in data:
                        ingredient = Ingredient("", "", "")
                        ingredient.load_from_dict(item)
                        self.ingredients.append(ingredient)
        except requests.RequestException as e:
            raise requests.RequestException(f"Error al descargar desde API: {e}")
        except json.JSONDecodeError as e:
            raise json.JSONDecodeError(f"Error al parsear JSON: {e}")
    
    def load_from_file(self, filename: str):
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
                for item in data:
                    ingredient = Ingredient("", "", "")
                    ingredient.load_from_dict(item)
                    self.ingredients.append(ingredient)
        except FileNotFoundError:
            raise FileNotFoundError(f"Archivo '{filename}' no encontrado.")
        except json.JSONDecodeError as e:
            raise json.JSONDecodeError(f"Error al parsear JSON en '{filename}': {e}")
    
    def save_to_file(self, filename: str):
        try:
            data = [ing.to_dict() for ing in self.ingredients]
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
        except IOError as e:
            raise IOError(f"Error al guardar en '{filename}': {e}")
    
    def list_by_category(self, category: str) -> List[Ingredient]:
        return [ing for ing in self.ingredients if ing.category == category]
    
    def list_by_type(self, category: str, type_: str) -> List[Ingredient]:
        return [ing for ing in self.ingredients if ing.category == category and ing.type_ == type_]
    
    def add_ingredient(self, ingredient: Ingredient):
        if any(ing.name == ingredient.name for ing in self.ingredients):
            raise ValueError(f"El ingrediente '{ingredient.name}' ya existe.")
        self.ingredients.append(ingredient)
    
    def remove_ingredient(self, name: str, menu_manager) -> bool:
        ingredient = next((ing for ing in self.ingredients if ing.name == name), None)
        if not ingredient:
            raise ValueError(f"Ingrediente '{name}' no encontrado.")
        
        used_in_hotdogs = [hd for hd in menu_manager.hot_dogs if 
                           hd.bread.name == name or hd.sausage.name == name or 
                           any(t.name == name for t in hd.toppings) or 
                           any(s.name == name for s in hd.sauces) or 
                           (hd.side and hd.side.name == name)]
        
        if used_in_hotdogs:
            print(f"El ingrediente '{name}' está en uso en los siguientes hot dogs: {[hd.name for hd in used_in_hotdogs]}")
            confirm = input("¿Deseas eliminar el ingrediente y los hot dogs afectados? (sí/no): ").strip().lower()
            if confirm != 'sí':
                print("Eliminación cancelada.")
                return False
            for hd in used_in_hotdogs:
                menu_manager.hot_dogs.remove(hd)
        
        self.ingredients.remove(ingredient)
        print(f"Ingrediente '{name}' eliminado.")
        return True
