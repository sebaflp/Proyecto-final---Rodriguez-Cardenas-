from ingredient import Ingredient

class HotDog:
    def __init__(self, name, pan, salchicha, toppings, salsas, acompanante=None):
        self.name = name
        self.pan = pan
        self.salchicha = salchicha
        self.toppings = toppings
        self.salsas = salsas
        self.acompanante = acompanante

    def check_inventory(self, inventory):
        required = [self.pan, self.salchicha] + self.toppings + self.salsas
        if self.acompanante:
            required.append(self.acompanante)
        for ing in required:
            if inventory.get_stock(ing) < 1:
                return False, ing
        return True, None

    def __str__(self):
        return f"{self.name}: Pan {self.pan}, Salchicha {self.salchicha}, Toppings {self.toppings}, Salsas {self.salsas}, Acompañante {self.acompanante}"

class Menu:
    def __init__(self, hotdogs=None):
        self.hotdogs = hotdogs if hotdogs else []

    def add_hotdog(self, hotdog):
        self.hotdogs.append(hotdog)

    def remove_hotdog(self, hotdog):
        if hotdog in self.hotdogs:
            self.hotdogs.remove(hotdog)

    def list_hotdogs(self):
        return self.hotdogs

    def check_hotdog_inventory(self, hotdog, inventory):
        return hotdog.check_inventory(inventory)
