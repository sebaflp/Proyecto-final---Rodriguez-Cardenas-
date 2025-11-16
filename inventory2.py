# Importa la clase Ingrediente desde el archivo ingredient2.py
from ingredient2 import Ingrediente  

class Inventario:
    """Clase para gestionar el inventario de ingredientes"""
    
    def __init__(self, ingrediente_instance):
        """ Inicializa el inventario con todos los ingredientes existentes en 100 unidades."""
        self.ingrediente_instance = ingrediente_instance
        self.existencias = {}
        for ing in self.ingrediente_instance.ingredientes:
            nombre = ing.get("Nombre")
            if nombre:
                self.existencias[nombre] = 100  # Se inicializan las existencias con 100 unidades
    
    def buscar_existencia(self, nombre):
        """ Busca la existencia de un ingrediente específico"""
        return self.existencias.get(nombre)
    
    def listar_por_categoria(self, categoria):
        """ Lista las existencias de todos los ingredientes de una categoría específica"""
        ingredientes_categoria = self.ingrediente_instance.listar_por_categoria(categoria)
        if not ingredientes_categoria:
            print(f"No hay ingredientes en la categoría {categoria}.")
            return
        
        print(f"Existencias en la categoría {categoria}:")
        for ingrediente in ingredientes_categoria:
            nombre = ingrediente.get("Nombre")
            cantidad = self.existencias.get(nombre, 100)
            print(f"- {cantidad}")
    
    def actualizar_existencia(self, nombre, cantidad_comprada):
        """ Actualiza la existencia de un ingrediente específico sumando la cantidad comprada """
        if nombre in self.existencias:
            self.existencias[nombre] += cantidad_comprada
            print(f"Existencia de {nombre} actualizada. Nueva cantidad: {self.existencias[nombre]}")
        else:
            print(f"No se puede actualizar: el ingrediente {nombre} no existe en la lista de ingredientes.")