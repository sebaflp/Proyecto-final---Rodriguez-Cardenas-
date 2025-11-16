import requests
from ingredient2 import Ingrediente
from inventory2 import Inventario

class Menu:
    """ Clase para gestionar el menu de hotdogs """
    def __init__(self, ingrediente_instance, inventario_instance):
        self.ingrediente_instance = ingrediente_instance  # Instancia de Ingrediente para validar
        self.inventario_instance = inventario_instance    # Instancia de Inventario para chequear existencias
        self.hot_dogs = []  # Lista de hot dogs (inicialmente vacía, se carga desde API)
        self.cargar_menu_desde_api()

    def cargar_menu_desde_api(self):
        url = "https://raw.githubusercontent.com/FernandoSapient/BPTSP05_2526-1/refs/heads/main/menu.json"
        try:
            response = requests.get(url)
            if response.status_code == 200:
                self.hot_dogs = response.json()
            else:
                print(f"Error al obtener los datos de la API. Status code: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"Ocurrio un error de conexion: {e}")
        
    def ver_lista_hot_dogs(self):
        """Ver la lista de hot dogs disponibles."""
        if not self.hot_dogs:
            print("No hay hot dogs en el menu.")
            return
        print("\n--- Lista de HotDogs ---")
        for i, hot_dog in enumerate(self.hot_dogs, 1):
            print(f"{i}, {hot_dog}nombre")


    def verificar_inventario_hot_dog(self, nombre_hot_dog):
        """Verifica si hay suficiente inventario para vender un hot dog especifico"""
        hot_dog = None
        nombre_hot_dog_lower = nombre_hot_dog.lower()
        for hd in self.hot_dogs:
            if hd.get("nombre", "").lower() == nombre_hot_dog_lower:
                hot_dog = hd
                break
        if not hot_dog:
            print(f"El hotdog {nombre_hot_dog} no existe en el menú.")
            return False
        
        # Uso de claves en MINÚSCULAS para consistencia con el JSON
        ingredientes_requeridos = [hot_dog.get("pan"), hot_dog.get("salchicha")] + hot_dog.get("toppings", []) + hot_dog.get("salsas", [])
        
        if hot_dog.get("acompanante"):
            ingredientes_requeridos.append(hot_dog.get("acompanante"))
        
        # Limpiar la lista de posibles None/vacíos
        ingredientes_requeridos = [ing for ing in ingredientes_requeridos if ing]
        
        suficiente = True
        for ing in ingredientes_requeridos:
            existencia = self.inventario_instance.buscar_existencia(ing)
            # Se verifica si la existencia es None (no existe en inventario) o es menor a 1
            if existencia is None or existencia < 1:
                print(f"Advertencia: No hay suficiente inventario para {ing} (requerido para {nombre_hot_dog})")
                suficiente = False
        if suficiente:
            print(f"El hot dog {nombre_hot_dog} tiene suficiente inventario para venderse")
        return suficiente
    
    def agregar_hot_dog(self):
        """ Agrega un nuevo hotdog al menu """
        nombre = input("Ingresa el nombre del hot dog: ").strip()
        existe = False
        for hd in self.hot_dogs:
            if hd.get("nombre", "").lower() == nombre.lower():
                existe = True
                break
        if existe:
            print("Ya existe un hot dog con ese nombre")
            return
        
        # Seleccionar pan
        panes = self.ingrediente_instance.listar_por_categoria("Pan")
        if not panes:
            print("No hay panes disponibles")
            return
        print("Panes disponibles: 1. simple, 2. integral, 3. especial, 4. grande, 5. italiano, 6. sin gluten, 7. saludable, 8. gigante, 9. submarino")   
        try:
            idx_pan = int(input("Selecciona el numero del pan: ")) - 1
            pan = panes[idx_pan].get("Nombre")
            pan_info = panes[idx_pan]
        except (ValueError, IndexError):
            print("Seleccion de pan invalida. Cancelando registro.")
            return

        
        # Seleccionar salchicha

        salchichas = self.ingrediente_instance.listar_por_categoria("Salchicha") 
        if not salchichas:
            print("No hay salchichas disponibles.")
            return
        print("Salchichas disponibles: \n1. weiner, 2. breakfast, 3. alemana, 4. francesa, 5. polaca, 6. light, 7. boudin, 8. vienna, 9. Salicce")

        try:
            idx_salchicha = int(input("Selecciona el numero de la salchicha: ")) - 1
            salchicha = salchichas[idx_salchicha].get("Nombre")
            salchicha_info = salchichas[idx_salchicha]
        except (ValueError, IndexError):
            print("Seleccion de salchicha invalida. Cancelando registro.")
            return
        
        # Validar longitud pan y salchicha (usando "Tipo" del JSON como campo de tamaño)
        if pan_info.get("Tipo") != salchicha_info.get("Tipo"):
            print(f"Advertencia: El tipo/tamaño del pan ({pan_info.get('Tipo')}) y la salchicha ({salchicha_info.get('Tipo')}) no coinciden.")
            confirmacion = input("Confirme si desea continuar de todas formas (s/n): ").lower()
            if confirmacion != "s":
                return
        
        # Seleccionar toppings
        toppings = []
        toppings_disp = self.ingrediente_instance.listar_por_categoria("Topping") 
        if toppings_disp:
            print("Toppings disponibles: \n1. tomate, 2. cebolla, 3. repollo, 4. cilantro, 5. papitas, 6. nuez moscada")

            indices = input("Selecciona el numero del topping: ").strip()
            if indices:
                for idx_str in indices.split(","):
                    try:
                        idx = int(idx_str.strip()) - 1
                        if 0 <= idx < len(toppings_disp):
                            toppings.append(toppings_disp[idx].get("Nombre"))
                    except (ValueError, IndexError):
                        pass 
        
        # Seleccionar salsas
        salsas = []
        salsas_disp = self.ingrediente_instance.listar_por_categoria("Salsa")
        if salsas_disp:
            print("Salsas disponibles: \n1. ketchup, 2. mayonesa, 3. BBQ, 4. Mostaza, 5. relish")

            indices = input("Selecciona salsas: ").strip()
            if indices:
                for idx_str in indices.split(","):
                    try:
                        idx = int(idx_str.strip()) - 1
                        if 0 <= idx < len(salsas_disp):
                            salsas.append(salsas_disp[idx].get("Nombre"))
                    except (ValueError, IndexError):
                        pass # Ignorar índices o entradas inválidas

        
        # Seleccionar Acompañante
        acompanantes_disp = self.ingrediente_instance.listar_por_categoria("Acompañante")
        acompanante = None
        if acompanantes_disp:
            opcion = input("¿Incluir acompañante? (s/n): ").lower()
            if opcion == "s":
                print("Acompañantes disponibles: \n1. saladas pequeñas, 2. saladas medianas, 3. saladas grandes, \n4. doradas con queso pequeñas, 5. doradas con queso medianas, 6. doradas con queso grandes, \n7. Super papas, 8. Papas, \n9. Cola Negra, 10. Kolita, 10. Te helado, 11. Naranjada, 12. Limonada, 13. Manzana, 14. Naranaja, 15. Pera")
                
                try:
                    idx = int(input("Selecciona el número del acompañante: ")) - 1
                    acompanante = acompanantes_disp[idx].get("Nombre")
                except (ValueError, IndexError):
                    print("Selección de acompañante invalida. No se incluyo.")
        
        # Agregar el hot dog
        nuevo_hd = {
            "nombre": nombre,
            "pan": pan,
            "salchicha": salchicha,
            "toppings": toppings,
            "salsas": salsas,
            "acompanante": acompanante,
            "precio": 5.0 
        }
        self.hot_dogs.append(nuevo_hd)
        print(f"Hot dog {nombre} agregado exitosamente.")
    
    def eliminar_hot_dog(self, nombre_hot_dog):
        """ Elimina un hotdog del menu. """
        hot_dog = None
        nombre_lower = nombre_hot_dog.lower()
        
        for hd in self.hot_dogs:
            if hd.get("nombre", "").lower() == nombre_lower:
                hot_dog = hd
                break
        
        if not hot_dog:
            print(f"El hotdog {nombre_hot_dog} no existe en el menu.")
            return
        
        if self.verificar_inventario_hot_dog(nombre_hot_dog):
            print("Advertencia: Todavia hay inentario suficiente para vender este hotdog. Confirmas la eliminacion? (s/n)")
            if input().lower() != "s":
                return
        
        # Uso de lista de comprensión para filtrar de forma limpia
        self.hot_dogs = [hd for hd in self.hot_dogs if hd.get("nombre", "").lower() != nombre_lower]
        print(f"Hot dog {nombre_hot_dog} eliminado exitosamente.")