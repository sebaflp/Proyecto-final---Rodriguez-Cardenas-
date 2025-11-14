class Inventory:

    def __init__(self, initial_inventory=None):
        self.inventory = initial_inventory if initial_inventory else {}

    def add_stock(self, ingredient, quantity):
        if ingredient in self.inventory:
            self.inventory[ingredient] += quantity
        else:
            self.inventory[ingredient] = quantity

    def get_stock(self, ingredient):
        return self.inventory.get(ingredient, 0)

    def list_by_category(self, category):
        return {ing: qty for ing, qty in self.inventory.items() if ing.category == category}

    def update_stock(self, ingredient, new_quantity):
        if ingredient in self.inventory:
            self.inventory[ingredient] = new_quantity
        else:
            raise ValueError("Ingrediente no encontrado en inventario.")

    def __str__(self):
        return "\n".join([f"{ing}: {qty}" for ing, qty in self.inventory.items()])
