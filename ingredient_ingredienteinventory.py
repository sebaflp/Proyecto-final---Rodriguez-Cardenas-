class Ingredient:
  
    def __init__(self, nombre: str, categoria: str, tipo: str = ""):
        self.nombre = nombre
        self.categoria = categoria
        self.tipo = tipo

        if not nombre:
            print (ValueError("El nombre del ingrediente no puede estar vacío."))
        valid_categorias = ["Pan", "Salchicha", "Topping", "Salsa", "Acompañante"]
        if categoria not in valid_categorias:
            print (ValueError(f"Categoría '{categoria}' no es válida. Categorías permitidas: {valid_categorias}"))
        

    def to_dict(self):
         {
            "Nombre": self.nombre,
            "categoria": self.categoria,
            "tipo": self.tipo
        }
    
    def cargar_data_dict(self, data: dict):
     
        if "nombre" not in data or "categoria" not in data:
            print (KeyError("El diccionario debe contener 'nombre' y 'categoria'."))
        
        nombre = data["nombre"]
        categoria = data["categoria"]
        tipo = data.get("tipo", "")
        
        if not nombre:
            print (ValueError("El nombre del ingrediente no puede estar vacío."))
        valid_categorias = ["Pan", "Salchicha", "Topping", "Salsa", "Acompañante"]
        if categoria not in valid_categorias:
            print (ValueError(f"Categoría '{categoria}' no es válida. Categorías permitidas: {valid_categorias}"))

        self.nombre = nombre
        self.categoria = categoria
        self.tipo = tipo









import requests
import json
from typing import List, Optional

class IngredientManager:
    """
    Clase que gestiona la lista de ingredientes en el sistema de Hot Dog CCS.
    
    Atributos:
        ingredients (List[Ingredient]): Lista de objetos Ingredient.
    
    Métodos:
        __init__: Inicializa la lista vacía.
        load_from_api: Descarga y carga ingredientes desde la API de GitHub.
        load_from_file: Carga ingredientes desde un archivo JSON local.
        save_to_file: Guarda nuevos ingredientes en un archivo JSON local.
        list_by_category: Lista ingredientes por categoría.
        list_by_type: Lista ingredientes por categoría y tipo.
        add_ingredient: Agrega un nuevo ingrediente.
        remove_ingredient: Elimina un ingrediente, verificando uso en menú (requiere MenuManager).
    """
    
    def __init__(self):
        """
        Inicializa el IngredientManager con una lista vacía de ingredientes.
        """
        self.ingredients: List[Ingredient] = []
    
    def load_from_api(self):
        """
        Descarga datos de ingredientes desde la API de GitHub y los carga en la lista.
        Asume que los datos están en archivos JSON en el repositorio.
        
        Raises:
            requests.RequestException: Si falla la descarga desde la API.
            json.JSONDecodeError: Si el JSON descargado es inválido.
        """
        url = "https://api.github.com/repos/FernandoSapient/BPTSP05_2526-1/contents/"
        try:
            response = requests.get(url)
            response.raise_for_status()
            files = response.json()
            
            # Busca archivos JSON relacionados con ingredientes (e.g., "ingredients.json")
            for file_info in files:
                if file_info['name'].endswith('.json') and 'ingredient' in file_info['name'].lower():
                    file_url = file_info['download_url']
                    file_response = requests.get(file_url)
                    file_response.raise_for_status()
                    data = file_response.json()
                    
                    # Asume que data es una lista de diccionarios
                    for item in data:
                        ingredient = Ingredient("", "", "")  # Instancia vacía
                        ingredient.load_from_dict(item)  # Carga desde dict
                        self.ingredients.append(ingredient)
        except requests.RequestException as e:
            raise requests.RequestException(f"Error al descargar desde API: {e}")
        except json.JSONDecodeError as e:
            raise json.JSONDecodeError(f"Error al parsear JSON: {e}")
    
    def load_from_file(self, filename: str):
        """
        Carga ingredientes desde un archivo JSON local (para nuevos ingredientes agregados por el usuario).
        
        Args:
            filename (str): Nombre del archivo JSON.
        
        Raises:
            FileNotFoundError: Si el archivo no existe.
            json.JSONDecodeError: Si el JSON es inválido.
        """
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
        """
        Guarda la lista de ingredientes en un archivo JSON local (solo nuevos, no sobrescribe API).
        
        Args:
            filename (str): Nombre del archivo JSON.
        
        Raises:
            IOError: Si hay error al escribir el archivo.
        """
        try:
            data = [ing.to_dict() for ing in self.ingredients]
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
        except IOError as e:
            raise IOError(f"Error al guardar en '{filename}': {e}")
    
    def list_by_category(self, category: str) -> List[Ingredient]:
        """
        Lista todos los ingredientes de una categoría específica.
        
        Args:
            category (str): Categoría a filtrar (e.g., "Pan").
        
        Returns:
            List[Ingredient]: Lista de ingredientes en la categoría.
        """
        return [ing for ing in self.ingredients if ing.category == category]
    
    def list_by_type(self, category: str, type_: str) -> List[Ingredient]:
        """
        Lista todos los ingredientes de una categoría y tipo específicos.
        
        Args:
            category (str): Categoría a filtrar.
            type_ (str): Tipo a filtrar.
        
        Returns:
            List[Ingredient]: Lista de ingredientes que coinciden.
        """
        return [ing for ing in self.ingredients if ing.category == category and ing.type_ == type_]
    
    def add_ingredient(self, ingredient: Ingredient):
        """
        Agrega un nuevo ingrediente a la lista, verificando que no exista ya.
        
        Args:
            ingredient (Ingredient): Objeto Ingredient a agregar.
        
        Raises:
            ValueError: Si el ingrediente ya existe (por nombre).
        """
        if any(ing.name == ingredient.name for ing in self.ingredients):
            raise ValueError(f"El ingrediente '{ingredient.name}' ya existe.")
        self.ingredients.append(ingredient)
    
    def remove_ingredient(self, name: str, menu_manager) -> bool:
        """
        Elimina un ingrediente por nombre, verificando si está en uso en hot dogs del menú.
        Si está en uso, pide confirmación al usuario y elimina los hot dogs afectados si se confirma.
        
        Args:
            name (str): Nombre del ingrediente a eliminar.
            menu_manager: Instancia de MenuManager para verificar uso en menú.
        
        Returns:
            bool: True si se eliminó, False si no (usuario canceló o no encontrado).
        
        Raises:
            ValueError: Si el ingrediente no existe.
        """
        ingredient = next((ing for ing in self.ingredients if ing.name == name), None)
        if not ingredient:
            raise ValueError(f"Ingrediente '{name}' no encontrado.")
        
        # Verificar si está en uso en hot dogs
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
            # Eliminar hot dogs afectados
            for hd in used_in_hotdogs:
                menu_manager.hot_dogs.remove(hd)
        
        self.ingredients.remove(ingredient)
        print(f"Ingrediente '{name}' eliminado.")
        return True
