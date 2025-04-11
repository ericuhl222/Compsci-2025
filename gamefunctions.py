import random
import json
import os
import pygame
import pickle

# Constants for map
GRID_SIZE = 10
SQUARE_SIZE = 32
SCREEN_WIDTH = GRID_SIZE * SQUARE_SIZE
SCREEN_HEIGHT = GRID_SIZE * SQUARE_SIZE
TOWN_LOCATION = (0, 0)
MONSTER_LOCATION = (5, 5)
SAVE_FILE = "game_state.pkl"

# Colors for map
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Town choice / what to do
def get_user_town_choice(player_hp, gold, inventory):
    """Gets the user's choice in town and validates it."""
    while True:
        print("\nYou are in town.")
        print(f"Current HP: {player_hp}, Current Gold: {gold}")
        print("What would you like to do?")
        print("1) Leave town (enter map)")
        print("2) Sleep (Restore HP for 5 Gold)")
        print("3) Check inventory or equip item")
        print("4) Go to the shop")
        print("5) Save and Quit")
        print("6) Quit")

        choice = input("Enter your choice (1, 2, 3, 4, 5, or 6): ")
        if choice in ("1", "2", "3", "4", "5", "6"):
            return choice
        else:
            print("Invalid choice. Please enter 1, 2, 3, 4, 5, or 6.")

# monster code
def new_random_monster():
    """Generates one of several monster types to fight."""
    monsters = ["demon", "ghost", "goblin", "creeper"]
    health = random.randint(10, 30)
    sel_money = random.randint(5, 20)
    power = random.randint(1, 3)
    sel_health = health * power
    sel_monster = random.choice(monsters)
    scenario = [
        f"You come across a {sel_monster} eating a corpse.",
        f"A {sel_monster} jumps out from behind a crate!",
        f"After entering a cave, a {sel_monster} attacks you from a dark corner.",
    ]
    sel_scenario = random.choice(scenario)

    return sel_health, sel_money, sel_monster, sel_scenario

# Fighting code
def handle_fight(player_hp, gold, inventory, equipped_weapon, equipped_shield):
    """Code for handling health and fights within the game."""
    monster_hp, monster_gold, monster_type, scenario = new_random_monster()
    monster_attack = random.randint(5, 12)
    print(scenario)
    print(f"Monster HP: {monster_hp}")

    while player_hp > 0 and monster_hp > 0:
        display_fight_statistics(player_hp, monster_hp)
        choice = get_user_fight_options(inventory)

        if choice == "1":  # Attack
            player_attack = random.randint(5, 15)
            if equipped_weapon and equipped_weapon["currentDurability"] > 0:
                player_attack += equipped_weapon["damage"]
                equipped_weapon["currentDurability"] -= 1
                print(f"Your {equipped_weapon['name']} adds {equipped_weapon['damage']} damage!")
                if equipped_weapon["currentDurability"] == 0:
                    print(f"Your {equipped_weapon['name']} broke!")
                    equipped_weapon = None
            monster_hp -= player_attack
            print(f"You attack the {monster_type} for {player_attack} damage.")

            if monster_hp > 0:
                monster_damage = random.randint(1, monster_attack)
                if equipped_shield and equipped_shield["currentDurability"] > 0:
                    monster_damage -= equipped_shield["defense"]
                    equipped_shield["currentDurability"] -= random.uniform(0.5,1) #shield durability decreased
                    print(f"Your {equipped_shield['name']} reduces damage by {equipped_shield['defense']}!")
                    if equipped_shield["currentDurability"] <= 0:
                      print(f"Your {equipped_shield['name']} broke!")
                      equipped_shield = None
                if monster_damage < 0:
                    monster_damage = 0
                player_hp -= monster_damage
                print(f"The {monster_type} attacks you for {monster_damage} damage.")

        elif choice == "2":
            print("You run away!")
            return player_hp, gold, equipped_weapon, equipped_shield

        elif choice == "3":  # equip
            item_type = input("Enter the type of item to equip (weapon/shield): ").lower()
            if item_type in ("weapon", "shield"):
                if item_type == "weapon":
                    equipped_weapon = equip_item(inventory, item_type)
                    if equipped_weapon:
                        print(f"Equipped {equipped_weapon['name']}.")
                        #review this area...
                elif item_type == "shield":
                    equipped_shield = equip_item(inventory, item_type)
                    if equipped_shield :
                        equipped_shield["currentDurability"] -= 1
                        print(f"Equipped {equipped_shield['name']}.")
                    if equipped_shield and equipped_shield["currentDurability"] == 0:
                        print(f"Your {equipped_shield['name']} broke!")
                        equipped_shield = None
            else:
                print("Invalid item type.")
        elif choice == "4": #consumable
            consumable_used = use_consumable(inventory, monster_hp)
            if consumable_used == -1000:
                monster_hp = 0
            elif consumable_used:
                player_hp = consumable_used
            else:
                print("No consumable used")

    if player_hp <= 0:
        print("You were defeated!")
        return 0, gold, equipped_weapon, equipped_shield
    else:
        print(f"You defeated the {monster_type}!")
        gold += monster_gold
        print(f"You found {monster_gold} gold.")
        return player_hp, gold, equipped_weapon, equipped_shield

# Who is winning
def display_fight_statistics(player_hp, monster_hp):
    """Displays the current HP of the player and monster."""
    print(f"Your HP: {player_hp}, Monster HP: {monster_hp}")

# What to do in fight?
def get_user_fight_options(inventory):
    """Gets the user's choice during a fight."""
    while True:
        print("1) Attack")
        print("2) Run Away")
        print("3) Equip Item")
        print("4) Use Consumable")
        choice = input("Enter your choice (1, 2, 3, or 4): ")
        if choice in ("1", "2", "3", "4"):
            return choice
        else:
            print("Invalid choice. Please enter 1, 2, 3, or 4.")

# Nap time code
def handle_sleep(player_hp, gold):
    """Sleep action restores health after removing 5 gold from your inventory"""
    if gold >= 5:
        player_hp = 30
        gold -= 5
        print("You slept and restored your HP.")
        return player_hp, gold
    else:
        print("You don't have enough gold to sleep.")
        return player_hp, gold

# Visual menu I made for the shop
def print_shop_menu(item1, x: float, item2, y: float):
    """this is to print a small menu for the shop, currently
    it holds only two items in a small box of text
    x and y are prices respectively."""
    print("/" + "-" * 22 + "\\")
    print(f"|{item1:<15}{x:>7}|",)
    print(f"|{item2:<15}{y:>7}|",)
    print("\\" + "-" * 22 + "/")

"""inventory and additional shop stuff will be held below"""

"""Create Item prompts
called with create_"item","""

def create_sword(name="Basic Sword", max_durability=10, damage=5, price=10):
    """Creates a sword item."""
    return {
        "name": name,
        "type": "weapon",
        "maxDurability": max_durability,
        "currentDurability": max_durability,
        "damage": damage,
        "price": price,
    }

def create_anthrax_dart(name="Anthrax Dart", effect="instant_kill", price=20):
    """Creates an item that instantly kills a monster."""
    return {
        "name": name,
        "type": "consumable",
        "effect": effect,
        "price": price,
    }

def create_shield(name="Basic Shield", max_durability=6, defense=3, price=15):
    """Creates a shield item."""
    return {
        "name": name,
        "type": "shield",
        "maxDurability": max_durability,
        "currentDurability": max_durability,
        "defense": defense,
        "price": price,
    }

def create_shop_items():
    """Creates a list of items available in the shop."""
    return [
        create_sword(),
        create_anthrax_dart(),
        create_shield(),
        create_sword(name="Steel Sword", max_durability=20, damage=10, price=30),
        create_anthrax_dart(name="Anthrax Dart", effect="instant_kill", price=40),
        create_shield(name="Iron Shield", max_durability=12, defense=6, price=25),
    ]

def display_shop(shop_items):
    """Displays the items available in the shop."""
    print("/" + "-" * 38 + "\\")
    print(f"|{'Index':<5}{'Item':<15}{'Type':<12}{'Price':>6}|")
    print("|" + "-" * 38 + "|")
    for index, item in enumerate(shop_items):
        print(f"|{index + 1:<5}{item['name']:<15}{item['type']:<12}{item['price']:>6}|")
    print("\\" + "-" * 38 + "/")

def purchase_item(inventory, shop_items, item_index, player_gold):
    """Purchases an item from the shop and adds it to the inventory.
    Also deducts gold."""
    if 1 <= item_index <= len(shop_items):
        purchased_item = shop_items[item_index - 1]
        if player_gold >= purchased_item["price"]:
            inventory.append(purchased_item)
            player_gold -= purchased_item["price"]
            print(f"You purchased {purchased_item['name']}.")
            return True, player_gold
        else:
            print("Not enough gold.")
            return False, player_gold
    else:
        print("Invalid item index.")
        return False, player_gold

#inventory stuff
def equip_item(inventory, item_type):
    """Equips an item of a specific type from inventory."""
    items = [i for i in inventory if i["type"] == item_type]
    if not items:
        print(f"No {item_type} items.")
        return None

    print(f"Select {item_type}:")
    for i, item in enumerate(items):
        print(f"{i + 1}. {item['name']}")
        if "damage" in item:
            print(
                f"  Damage: {item['damage']}, Durability: {item['currentDurability']}/{item['maxDurability']}"
            )
        elif "defense" in item:
            print(
                f"  Defense: {item['defense']}, Durability: {item['currentDurability']}/{item['maxDurability']}"
            )
    print("0. None")

    while True:
        try:
            choice = int(input("Choice: "))
            if 0 <= choice <= len(items):
                return items[choice - 1] if choice else None
            print("Invalid.")
        except ValueError:
            print("Number please.")

def display_inventory(inventory):
    """Displays the items in the user's inventory."""
    if not inventory:
        print("Your inventory is empty.")
        return

    print("\nYour Inventory:")
    for i, item in enumerate(inventory):
        print(f"{i + 1}. {item['name']} ({item['type']})")
        if item["type"] == "weapon":
            print(
                f"    Damage: {item['damage']}, Durability: {item['currentDurability']}/{item['maxDurability']}"
            )
        elif item["type"] == "shield":
            print(
                f"    Defense: {item['defense']}, Durability: {item['currentDurability']}/{item['maxDurability']}"
            )
        elif item["type"] == "consumable":
            print(f"  Effect: {item['effect']}")

def use_consumable(inventory, monster_hp):
    """Allows the player to use a consumable item from their inventory."""
    consumables = [item for item in inventory if item["type"] == "consumable"]
    if not consumables:
        print("You have no consumables.")
        return None

    print("Select a consumable to use:")
    for i, consumable in enumerate(consumables):
        print(f"{i + 1}. {consumable['name']} - Effect: {consumable['effect']}")
    print("0. Cancel")

    while True:
        try:
            choice = int(input("Choice: "))
            if choice == 0:
                return None
            elif 1 <= choice <= len(consumables):
                selected_consumable = consumables[choice - 1]
                if selected_consumable["effect"] == "instant_kill":
                    print(f"You used {selected_consumable['name']}!")
                    print("The monster was instantly killed!")
                    inventory.remove(selected_consumable)
                    return -1000 #indicate monster death
                elif selected_consumable["effect"] == "heal":
                    heal_amount = 10
                    player_hp += heal_amount
                    print(f"You used {selected_consumable['name']} and healed {heal_amount} HP.")
                    inventory.remove(selected_consumable)
                    return player_hp
                else:
                    print("Unknown consumable effect.")
                    return None
            else:
                print("Invalid choice.")
        except ValueError:
            print("Invalid input. Please enter a number.")

def save_game(player_hp, player_gold, inventory, equipped_weapon, equipped_shield, filename):
    """Saves the current game state to a JSON file."""
    game_data = {
        "player_hp": player_hp,
        "player_gold": player_gold,
        "inventory": inventory,
        "equipped_weapon": equipped_weapon,
        "equipped_shield": equipped_shield
    }
    try:
        with open(filename, "w") as f:
            json.dump(game_data, f, indent=4)
        print(f"Game saved to {filename}")
        return True
    except Exception as e:
        print(f"Error saving game: {e}")
        return False

def load_game(filename):
    """Loads a saved game state from a JSON file."""
    if not os.path.exists(filename):
        print(f"Save file not found: {filename}")
        return None, None, None, None, None
    try:
        with open(filename, "r") as f:
            game_data = json.load(f)
        print(f"Game loaded from {filename}")
        player_hp = game_data.get("player_hp", 30)
        player_gold = game_data.get("player_gold", 100)
        inventory = game_data.get("inventory", [])
        equipped_weapon = game_data.get("equipped_weapon", None)
        equipped_shield = game_data.get("equipped_shield", None)
        return player_hp, player_gold, inventory, equipped_weapon, equipped_shield
    except Exception as e:
        print(f"Error loading game: {e}")
        return None, None, None, None, None

def save_map_state(player_position):
    """Saves the player's map position to a file."""
    with open(SAVE_FILE, "wb") as f:
        pickle.dump(player_position, f)

def load_map_state():
    """Loads the player's map position from a file, or returns the starting position."""
    if os.path.exists(SAVE_FILE):
        with open(SAVE_FILE, "rb") as f:
            return pickle.load(f)
    else:
        return (0, 0)

def monster_battle():
    """Simulates a monster battle, using existing handle_fight."""
    global player_hp, player_gold, inventory, equipped_weapon, equipped_shield #access global variables
    player_hp, player_gold, equipped_weapon, equipped_shield = handle_fight(player_hp, player_gold, inventory, equipped_weapon, equipped_shield)
    if player_hp > 0:
        return True
    else:
        return False

def game_map(player_position):
    """Handles the map screen and movement."""
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Game Map")

    running = True
    player_rect = pygame.Rect(player_position[0] * SQUARE_SIZE, player_position[1] * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
    town_rect = pygame.Rect(TOWN_LOCATION[0] * SQUARE_SIZE, TOWN_LOCATION[1] * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
    monster_rect = pygame.Rect(MONSTER_LOCATION[0] * SQUARE_SIZE, MONSTER_LOCATION[1] * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                save_map_state((player_rect.x // SQUARE_SIZE, player_rect.y // SQUARE_SIZE))
                return "quit"

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    player_rect.y = max(0, player_rect.y - SQUARE_SIZE)
                elif event.key == pygame.K_DOWN:
                    player_rect.y = min(SCREEN_HEIGHT - SQUARE_SIZE, player_rect.y + SQUARE_SIZE)
                elif event.key == pygame.K_LEFT:
                    player_rect.x = max(0, player_rect.x - SQUARE_SIZE)
                elif event.key == pygame.K_RIGHT:
                    player_rect.x = min(SCREEN_WIDTH - SQUARE_SIZE, player_rect.x + SQUARE_SIZE)

        screen.fill(WHITE)

        # Draw town
        pygame.draw.rect(screen, GREEN, town_rect)
        pygame.draw.circle(screen, GREEN, town_rect.center, SQUARE_SIZE // 4)

        # Draw monster
        pygame.draw.rect(screen, RED, monster_rect)
        pygame.draw.circle(screen, RED, monster_rect.center, SQUARE_SIZE // 4)

        # Draw player
        pygame.draw.rect(screen, (0, 0, 255), player_rect)

        pygame.display.flip()

        if player_rect.colliderect(town_rect) and (player_rect.x // SQUARE_SIZE, player_rect.y // SQUARE_SIZE) != TOWN_LOCATION:
            running = False
            pygame.quit()
            return "town"

        if player_rect.colliderect(monster_rect):
            running = False
            pygame.quit()
            battle_won = monster_battle()
            if battle_won:
                return "map"
            else:
                return "death"

    save_map_state((player_rect.x // SQUARE_SIZE, player_rect.y // SQUARE_SIZE))
    pygame.quit()
    return "quit"

def main():
    """Main game function."""
    global player_hp, player_gold, inventory, equipped_weapon, equipped_shield
    shop_items = create_shop_items()

    print("Welcome to the Town Adventure!")
    print("1) Start New Game")
    print("2) Load Game")
    choice = input("Enter your choice (1 or 2): ")

    if choice == "2":
        filename = input("Enter filename to load game: ")
        player_hp, player_gold, inventory, equipped_weapon, equipped_shield = load_game(filename)
        if player_hp is None:
            print("Failed to load game, starting a new game.")
            player_hp = 30
            player_gold = 100
            inventory = []
            equipped_weapon = None
            equipped_shield = None
    elif choice == "1":
        player_hp = 30
        player_gold = 100
        inventory = []
        equipped_weapon = None
        equipped_shield = None
    else:
        print("Invalid choice. Exiting.")
        return

    if player_hp is None:
        player_hp = 30
        player_gold = 100
        inventory = []
        equipped_weapon = None
        equipped_shield = None

    player_position = load_map_state() #loads map position

    while True:
        choice = get_user_town_choice(player_hp, player_gold, inventory)

        if choice == "1":
            result = game_map(player_position)
            if result == "town":
                print("Returned to town.")
            elif result == "death":
                print("You died!")
                break
            elif result == "quit":
                break
            player_position = load_map_state() #load the last saved map position.

        elif choice == "2":
            player_hp, player_gold = handle_sleep(player_hp, player_gold)
        elif choice == "3":
            display_inventory(inventory)
            item_type = input("Enter the type of item to equip (weapon/shield/consumable/none): ").lower()
            if item_type in ("weapon", "shield", "consumable"):
                if item_type == "weapon":
                    equipped_weapon = equip_item(inventory, item_type)
                    if equipped_weapon:
                        print(f"Equipped {equipped_weapon['name']}.")
                elif item_type == "shield":
                    equipped_shield = equip_item(inventory, item_type)
                    if equipped_shield:
                        print(f"Equipped {equipped_shield['name']}.")
                elif item_type == "consumable":
                    use_consumable(inventory, 0) #monster hp is not needed when using consumable outside combat.
            elif item_type == "none":
                equipped_weapon = None
                equipped_shield = None
                print("All items unequipped.")
            else:
                print("Invalid item type.")
        elif choice == "4":
            display_shop(shop_items)
            while True:
                try:
                    item_index = int(input("Enter the index of the item to purchase (or 0 to cancel): "))
                except ValueError:
                    print("Invalid input. Please enter a number.")
                    continue
                if item_index == 0:
                    break
                purchase_successful, player_gold = purchase_item(inventory, shop_items, item_index, player_gold)
                if purchase_successful:
                    break
        elif choice == "5":
            filename = input("Enter filename to save game: ")
            if save_game(player_hp, player_gold, inventory, equipped_weapon, equipped_shield, filename):
                break
            else:
                print("Save failed, continuing game.")
        elif choice == "6":
            print("Thank you for playing!")
            break

        if player_hp <= 0:
            print("Game Over!")
            break

