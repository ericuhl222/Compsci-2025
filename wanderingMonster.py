import random

# Constants (assuming these are defined elsewhere)
GRID_SIZE = 10
TOWN_LOCATION = (0, 0)


class WanderingMonster:
    """A class to represent a wandering monster in the game."""

    def __init__(self, location, name, health, gold, color, attack, defense):
        self._location = tuple(location)  # Private location
        self.name = name
        self.health = health
        self.gold = gold
        self.color = color
        self.attack = attack
        self.defense = defense

    def get_location(self):
        return self._location

    def set_location(self, new_location):
        self._location = new_location

    def move(self, direction, occupied_locations):
        x, y = self._location
        new_x, new_y = x, y

        if direction == "up" and y > 0:
            new_y -= 1
        elif direction == "down" and y < GRID_SIZE - 1:
            new_y += 1
        elif direction == "left" and x > 0:
            new_x -= 1
        elif direction == "right" and x < GRID_SIZE - 1:
            new_y += 1

        new_location = (new_x, new_y)

        if new_location != TOWN_LOCATION and new_location not in occupied_locations:
            self._location = new_location

    @staticmethod
    def new_random_monster(exclude_locations=()):
        monsters = ["demon", "ghost", "goblin", "creeper"]
        health = random.randint(10, 30)
        gold = random.randint(5, 20)
        name = random.choice(monsters)
        attack = random.randint(5, 15)
        defense = random.randint(0, 10)

        if name == "demon":
            color = (255, 0, 0)
        elif name == "ghost":
            color = (200, 200, 200)
        elif name == "goblin":
            color = (0, 255, 0)
        else:
            color = (0, 0, 255)

        while True:
            x = random.randint(0, GRID_SIZE - 1)
            y = random.randint(0, GRID_SIZE - 1)
            location = (x, y)
            if location not in exclude_locations and location != TOWN_LOCATION:
                break

        return WanderingMonster(location, name, health, gold, color, attack, defense)

    @staticmethod
    def new_random_strong_monster():
        strong_monsters = [
            {"name": "Dire Wolf", "health": 40, "attack": 10, "gold": 25, "defense": 5, "color": (160, 82, 45)},  # Brown
            {"name": "Stone Golem", "health": 60, "attack": 12, "gold": 30, "defense": 10, "color": (128, 128, 128)}, # Gray
            {"name": "Shadow Imp", "health": 35, "attack": 9, "gold": 20, "defense": 3, "color": (64, 64, 64)},   # Dark Gray
        ]
        strong_monster_data = random.choice(strong_monsters)
    
        # Generate a random location (you might want to pass in 'exclude_locations' here as well)
        x = random.randint(0, GRID_SIZE - 1)
        y = random.randint(0, GRID_SIZE - 1)
        location = (x, y)
    
        strong_monster_data["location"] = location
    
        return WanderingMonster(**strong_monster_data)
