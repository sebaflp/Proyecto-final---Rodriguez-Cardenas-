import random
from menu2 import Menu
from inventory2 import Inventario

class SimulacionVentas:
    """ Clase para simular un dia de ventas de hotdogs """
    
    def __init__(self, menu_instance, inventario_instance):
        self.menu_instance = menu_instance  # Instancia de Menu
        self.inventario_instance = inventario_instance  # Instancia de Inventario
    
    def simular_dia(self):
        """Simula un dia de ventas con clientes aleatorios."""
        
        # Verificar que hay hotdogs disponibles antes de simular
        if not self.menu_instance.hot_dogs:
            print("El menu esta vacio. No se puede realizar la simulacion.")
            return
        
        num_clientes = random.randint(0, 200)
        cambiaron_opinion = 0
        no_pudieron_comprar = 0
        total_hot_dogs_vendidos = 0
        acompanantes_vendidos = 0
        hot_dogs_vendidos = {}  # Diccionario para contar ventas por hot dog
        hot_dogs_causa_marcha = set()
        ingredientes_causa_marcha = set()  
        
        for i in range(num_clientes):
            num_hot_dogs = random.randint(0, 5)
            if num_hot_dogs == 0:
                print(f"El cliente {i} cambio de opinion")
                cambiaron_opinion += 1
                continue
            
            orden = []  # Lista de hotdogs que el cliente intenta comprar
            pudo_comprar = True
            ingredientes_totales = []  # Lista de todos los ingredientes para esta orden
            
            for _ in range(num_hot_dogs):
                
                # Selecciona hotdog aleatoriamente
                hot_dog = random.choice(self.menu_instance.hot_dogs)
                hot_dog_nombre = hot_dog.get("nombre", "Hotdog Desconocido") 
                
                # Ingredientes base del hotdog
                ings_hd = [hot_dog.get("pan"), hot_dog.get("salchicha")] + hot_dog.get("toppings", []) + hot_dog.get("salsas", [])
                
                if hot_dog.get("acompanante"):
                    ings_hd.append(hot_dog.get("acompanante"))
                
                # Selecciona aleatoriamente si compra acompañante adicional
                acompanante_adicional = random.choice([True, False])
                if acompanante_adicional:
                    acompanantes_disp = self.menu_instance.ingrediente_instance.listar_por_categoria("Acompañante")
                    if acompanantes_disp:
                        acomp_extra = random.choice(acompanantes_disp).get("Nombre")
                        ings_hd.append(acomp_extra)
                
                # Limpiar lista de ingredientes de posibles None o vacíos
                ings_hd = [ing for ing in ings_hd if ing]
                
                # Verifica inventario para este hot dog
                ingredientes_faltantes = []
                for ing in ings_hd:
                    existencia = self.inventario_instance.buscar_existencia(ing)
                    
                    if existencia is None or existencia < 1:
                        ingredientes_faltantes.append(ing)
                        pudo_comprar = False
                        
                if not pudo_comprar:
                    # El cliente se marcha si falta al menos un ingrediente
                    print(f"El cliente {i} no pudo comprar el hotdog '{hot_dog_nombre}' por falta de: {', '.join(ingredientes_faltantes)}")
                    hot_dogs_causa_marcha.add(hot_dog_nombre)
                    ingredientes_causa_marcha.update(ingredientes_faltantes)
                    break # El cliente no compra nada de su orden
                
                # Si llega hasta esta parte, significa que el hot dog se puede comprar
                orden.append(hot_dog_nombre)
                ingredientes_totales.extend(ings_hd)
            
            if pudo_comprar and orden:
                # Resta del inventario
                for ing in ingredientes_totales:
                    if ing in self.inventario_instance.existencias:
                        self.inventario_instance.existencias[ing] -= 1
                
                # Cuenta las ventas
                for hd_nombre in orden:
                    hot_dogs_vendidos[hd_nombre] = hot_dogs_vendidos.get(hd_nombre, 0) + 1
                    total_hot_dogs_vendidos += 1
                
                # Cuenta los acompañantes vendidos
                acompanantes = self.menu_instance.ingrediente_instance.listar_por_categoria("Acompañante")

                # Extrae los nombres de los acompañantes
                nombres_acompanantes = []
                for a in acompanantes:
                    nombres_acompanantes.append(a.get("Nombre"))

                # Ahora filtramos y contamos
                ingredientes_acompanantes = []
                for ing in ingredientes_totales:
                    # Solo si hay acompañantes y el ingrediente está en la lista
                    if acompanantes and ing in nombres_acompanantes:
                        ingredientes_acompanantes.append(ing)

                # Aumenta el contador
                acompanantes_vendidos += len(ingredientes_acompanantes)

            else:
                if num_hot_dogs > 0 and not pudo_comprar:
                    no_pudieron_comprar += 1
                
        # Reporte final
        print("\n--- Reporte del Día de Ventas ---")
        print(f"Total de clientes que intentaron comprar: {num_clientes}")
        print(f"Clientes que cambiaron de opinión (orden de 0): {cambiaron_opinion}")
        print(f"Clientes que no pudieron comprar por falta de inventario: {no_pudieron_comprar}")
        
        clientes_efectivos = num_clientes - cambiaron_opinion
        if total_hot_dogs_vendidos == 0:
            print("No se vendieron hot dogs.")
            promedio_hot_dogs = 0
        else:
            promedio_hot_dogs = total_hot_dogs_vendidos / clientes_efectivos if clientes_efectivos > 0 else 0
            
            # Calcula el mas vendido
            mas_vendido = max(hot_dogs_vendidos, key=hot_dogs_vendidos.get)
            max_ventas = hot_dogs_vendidos[mas_vendido]
            
            print(f"Total de hot dogs vendidos: {total_hot_dogs_vendidos}")
            print(f"Promedio de hotdogs por cliente (efectivo): {promedio_hot_dogs:.2f}")
            print(f"Hotdog más vendido: {mas_vendido} con {max_ventas} ventas")
            
        print(f"\n--- Problemas ---")
        print(f"Hot dogs que causaron que el cliente se marchara: {list(hot_dogs_causa_marcha)}")
        print(f"Ingredientes que causaron que el cliente se marchara: {list(ingredientes_causa_marcha)}")
        print(f"Acompañantes vendidos (aproximado): {acompanantes_vendidos}")