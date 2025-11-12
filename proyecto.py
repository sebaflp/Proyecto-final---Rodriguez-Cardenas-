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
        """
        Convierte el objeto Ingredient a un diccionario para facilitar la serialización JSON.
        
        Returns:
            dict: Diccionario con las claves 'name', 'category' y 'type'.
        """
        return {
            "name": self.name,
            "category": self.category,
            "type": self.type_
        }
    
    @classmethod
    def from_dict(cls, data: dict):
        """
        Crea un objeto Ingredient desde un diccionario (deserialización desde JSON).
        
        Args:
            data (dict): Diccionario con las claves 'name', 'category' y opcionalmente 'type'.
        
        Returns:
            Ingredient: Un nuevo objeto Ingredient.
        
        Raises:
            KeyError: Si faltan claves requeridas en el diccionario.
        """
        if "name" not in data or "category" not in data:
            raise KeyError("El diccionario debe contener 'name' y 'category'.")
        type_ = data.get("type", "")
        return cls(data["name"], data["category"], type_)
