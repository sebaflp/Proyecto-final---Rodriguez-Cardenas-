import requests

class Ingrediente:
    """Clase para cargar datos de ingredientes desde una API."""
    def __init__(self):
        self.ingredientes = []
        self.cargar_ingrediente_desde_api()

    def cargar_ingrediente_desde_api(self):
        url = "https://raw.githubusercontent.com/FernandoSapient/BPTSP05_2526-1/refs/heads/main/ingredientes.json"
        try:
            response = requests.get(url)
            if response.status_code == 200:
                self.ingredientes = response.json()
            else:
                print(f"Error al obtener los datos de la API. Status code: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"Ocurrió un error de conexión: {e}")
    
    def listar_por_categoria(self, categoria):
        """Devuelve una lista de ingredientes que pertenecen a una categoría específica."""
        resultado = []
        for ingrediente in self.ingredientes:
            if ingrediente.get("Categoria") == categoria:
                resultado.append(ingrediente)
        return resultado
    
    def agregar_ingrediente(self, nombre, categoria, tipo):
        """Agrega un nuevo ingrediente a la lista."""
        nuevo_ingrediente = {"Nombre": nombre, "Categoria": categoria, "Tipo": tipo}
        self.ingredientes.append(nuevo_ingrediente)
        print(f"El Ingrediente {nombre} fue agregado exitosamente")

    def eliminar_ingrediente(self, nombre):
        """Elimina un ingrediente de la lista por su nombre."""
        nombre_lower = nombre.strip().lower()
        ingrediente_encontrado = None
        
        # Buscar el ingrediente
        for ingrediente in self.ingredientes:
            if ingrediente.get("Nombre", "").lower() == nombre_lower:
                ingrediente_encontrado = ingrediente
                break
        
        if ingrediente_encontrado:
            self.ingredientes.remove(ingrediente_encontrado)
            print(f"El Ingrediente {nombre} fue eliminado exitosamente.")
        else:
            print(f"El Ingrediente {nombre} no fue encontrado.")
