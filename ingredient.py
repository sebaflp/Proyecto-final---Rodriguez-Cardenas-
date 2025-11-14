class Ingredient:
    def __init__(self, name, category, type_):
        self.name = name
        self.category = category
        self.type = type_

    def __str__(self):
        return f"{self.name} ({self.category}, {self.type})"