import random

class Simulation:
    
    def __init__(self, menu, inventory):
        self.menu = menu
        self.inventory = inventory
        self.sales_data = []

    def simulate_day(self):
        clientes = random.randint(0, 200)
        changed_mind = 0 
        could_not_buy = 0
        total_hotdogs = 0
        hotdog_sales = {}
        failed_hotdogs = set()
        failed_ingredientes = set()
        accompaniments_sold = 0

        for i in range(clientes):
            hotdog_bought = random.randint(0, 5)
            if hotdog_bought == 0:
                print(f"El cliente {i} cambio de opinion")
                changed_mind += 1
                continue

            order = []
            can_buy = True
            for _ in range(hotdog_bought):
                hd = random.choice(self.menu.hotdogs)
                extra_accompaniment = random.choice([True, False])
                if hd.acompanante or extra_accompaniment:
                    accompaniments_sold += 1 
                else:
                    accompaniments_sold += 0

                ok, missing_ingredient = self.menu.check_hotdog_inventory(self.inventory)
                if not ok:
                    print(f"El cliente {i} no pudo comprar el hotdog {hd.name} por falta de {missing_ingredient}")
                    can_buy = False
                    failed_hotdogs.add(hd.name)
                    failed_ingredientes.add(missing_ingredient.name)
                    break
                order.append(hd)
                hotdog_sales[hd.name] = hotdog_sales.get(hd.name, 0) + 1
            if can_buy:
                print(f"El cliente {i} compro {[hd.name for hd in order]}")
                for hd in order:
                    self.inventory.update_stock(hd.pan, self.inventory.get_stock(hd.pan) - 1)
                    self.inventory.update_stock(hd.salchicha, self.inventory.get_stock(hd.salchicha) - 1)
                    for topping in hd.toppings:
                        self.inventory.update_stock(topping, self.inventory.get_stock(topping) - 1)
                    for salsa in hd.salsas:
                        self.inventory.update_stock(salsa, self.inventory.get_stock(salsa) - 1)
                    if hd.acompanante:
                        self.inventory.update_stock(hd.acompanante, self.inventory.get_stock(hd.acompanante) - 1)
                total_hotdogs += len(order)
            else:
                could_not_buy += 1
        
        stats = {"changed_mind": changed_mind,
                    "could_not_buy": could_not_buy,
                    "total_clients": clientes,
                    "avg_hotdogs_per_client": total_hotdogs / max(1, clientes - changed_mind),
                    "top_hotdog": max(hotdog_sales, key=hotdog_sales.get) if hotdog_sales else None,
                    "failed_hotdogs": list(failed_hotdogs),
                    "failed_ingredientes": list(failed_ingredientes),
                    "accompaniments_sold": accompaniments_sold
                }
        self.sales_data.append(stats)