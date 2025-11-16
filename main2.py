# Importa la clases desdes otros archivos  
from ingredient2 import Ingrediente
from inventory2 import Inventario
from menu2 import Menu
from simulation2 import SimulacionVentas

def main():
    """Sistema final"""
    print(" \n---- Bienvendido a HodDog CCS ---- ") 
    
    # Crear instancias persistentes para todo el programa
    gestor_ingrediente = Ingrediente()
    gestor_inventario = Inventario(gestor_ingrediente)
    gestor_menu = Menu(gestor_ingrediente, gestor_inventario)
    simulacion = SimulacionVentas(gestor_menu, gestor_inventario)

    while True:
        print("\n--- Menu Principal ---")
        print("1. Gestion de Ingredientes")
        print("2. Gestion de Menu")
        print("3. Simular dia de Ventas")
        print("4. Salir")
        
        opcion_principal = input("Elige una opción: ")

        if opcion_principal == "1":
            while True:
                print("\nUsted ha ingresado a la gestion de ingredientes")
                print("--- Menú de Ingredientes ---")
                print("1. Listar todos los productos de una categoría")
                print("2. Agregar un ingrediente")
                print("3. Eliminar un ingrediente")
                print("4. Volver al menu principal")

                opcion = input("Elige una opción: ")
                
                if opcion == "1":
                    print("Categorías disponibles: Pan, Salchicha, toppings, Salsa, Acompañante")
                    categoria = input("Ingresa la categoría: ").strip()
                    resultados = gestor_ingrediente.listar_por_categoria(categoria)
                    if resultados:
                        print(f"Productos en la categoria {categoria}:")
                        for item in resultados:
                            print(f"- {item}")
                    else:
                        print(f"No se encontraron productos en la categoría {categoria}.")
                
                elif opcion == "2":
                    nombre = input("Ingresa el nombre del ingrediente: ").strip()
                    categoria = input("Ingresa la categoria: ").strip()
                    tipo = input("Ingresa el tipo: ").strip()
                    gestor_ingrediente.agregar_ingrediente(nombre, categoria, tipo)
                
                elif opcion == "3": 
                    nombre = input("Ingresa el nombre del ingrediente a eliminar: ").strip()
                    gestor_ingrediente.eliminar_ingrediente(nombre)
                
                elif opcion == "4":
                    print("Ustede ha salido de la gestion de ingredientes.")
                    break
                else:
                    print("Opción invalida. Intenta de nuevo.")
        

        elif opcion_principal == "2":
            while True:
                print("\nUsted ha ingresado a la gestion de menu")
                print("--- Menú de Menu ---")
                print("1. Visualizar menu de hot dogs")
                print("2. Verificar inventario para un hotdog especifico")
                print("3. Agregar un nuevo hotdog al menu")
                print("4. Eliminar un hotdog del menu")
                print("5. Volver al menu principal")

                opcion = input("Elige una opción: ")

                if opcion == "1":
                    gestor_menu.ver_lista_hot_dogs()

                elif opcion == "2":
                    nombre_hot_dog = input("Ingresa el nombre del hotdog: ").strip()
                    gestor_menu.verificar_inventario_hot_dog(nombre_hot_dog)

                elif opcion == "3":
                    gestor_menu.agregar_hot_dog()

                elif opcion == "4":
                    nombre_hot_dog = input("Ingresa el nombre del hotdog a eliminar: ").strip()
                    gestor_menu.eliminar_hot_dog(nombre_hot_dog)

                elif opcion == "5":
                    print("Usted ha salido de la gestion de menu.")
                    break
            
        elif opcion_principal == "3":
            print("\nIniciando simulación de día de ventas")
            simulacion.simular_dia()

        elif opcion_principal == "4":
            print("Gracias por usar el sistema de HotDog CCS. Hasta luego!!!")
            break

        else:
            print("Opción invalida. Intenta de nuevo.")

main()