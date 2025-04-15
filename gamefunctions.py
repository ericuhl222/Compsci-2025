import random
import pygame
import os
import json
import sys
from wanderingMonster import WanderingMonster

# Constants
GRID_SIZE = 10
SQUARE_SIZE = 32
TOWN_LOCATION = (0, 0)
SCREEN_WIDTH = GRID_SIZE * SQUARE_SIZE
SCREEN_HEIGHT = GRID_SIZE * SQUARE_SIZE
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
SAVE_FILE = "game_save.json"

# ... (Helper functions like get_user_town_choice, print_shop_menu, create_sword, etc. would go here)

# Item creation functions
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

def create_healing_potion(name="Healing Potion", effect="heal", heal_amount=15, price=25):
    """Creates a healing potion item."""
    return {
        "name": name,
        "type": "consumable",
        "effect": effect,
        "heal_amount": heal_amount,
        "price": price,
    }

def create_shop_items():
    """Creates a list of items available in the shop."""
    return [
        create_sword(),
        create_anthrax_dart(),
        create_shield(),
        create_sword(name="Steel Sword", max_durability=20, damage=10, price=30),
        create_shield(name="Iron Shield", max_durability=12, defense=6, price=25),
        create_healing_potion(),  # Add the healing potion to the shop
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
                selected_consumable = consumables[choice - 1]
                if selected_consumable["effect"] == "instant_kill":
                    print(f"You used {selected_consumable['name']}!")
                    print("The monster was instantly killed!")
                    inventory.remove(selected_consumable)
                    return -1000 #indicate monster death
                elif selected_consumable["effect"] == "heal":
                    heal_amount = consumables[choice - 1]["heal_amount"]
                    player_hp = 30 #set player hp to max.
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

def display_inventory(inventory):
    """Displays the items in the user's inventory."""
    if not inventory:
        print("Your inventory is empty.")
    else:
        print("Your inventory contains:")
        for i, item in enumerate(inventory):
            print(f"{i+1}. {item['name']} ({item['type']})") #basic display.  Can be expanded.

def handle_fight(player_hp, player_gold, inventory, equipped_weapon, equipped_shield, monster):
    """Code for handling health and fights within the game."""
    # ... (Implementation of handle_fight as in the older version)
    fight_continues = True
    gold_earned = 0
    while fight_continues:
        display_fight_statistics(player_hp, monster.health)
        player_choice = get_user_fight_options(inventory)

        if player_choice == "1":  # Attack
            player_damage = 0
            if equipped_weapon and equipped_weapon["currentDurability"] > 0:
                player_damage = random.randint(1, equipped_weapon["damage"])
                equipped_weapon["currentDurability"] -= 1
                print(f"Your {equipped_weapon['name']} adds {equipped_weapon['damage']} damage!")
                if equipped_weapon["currentDurability"] <= 0:
                    print(f"Your {equipped_weapon['name']} broke!")
                    equipped_weapon = None
            else:
                player_damage = random.randint(1, 3)  # Unarmed damage

            # Monster's attack is reduced here
            monster_damage = random.randint(1, max(1, monster.attack - 3))  # Reduced monster attack.  Original was 2, changed to 3.

            # Apply defense
            if equipped_shield and equipped_shield["currentDurability"] > 0:
                monster_damage = max(1, monster_damage - equipped_shield["defense"])  # At least 1 damage
                equipped_shield["currentDurability"] -= random.uniform(0.5,1)
                print(f"Your {equipped_shield['name']} reduces damage by {equipped_shield['defense']}!")
                if equipped_shield["currentDurability"] <= 0:
                    print(f"Your {equipped_shield['name']} broke!")
                    equipped_shield = None

            monster.health -= player_damage
            player_hp -= monster_damage

            print(f"You dealt {player_damage} damage!")
            print(f"Monster dealt {monster_damage} damage!")

            if monster.health <= 0 and player_hp <= 0:
                print("You and the monster died at the same time.")
                return 0, player_gold, False  # Game over
            elif monster.health <= 0:
                print("You defeated the monster!")
                gold_earned = monster.gold
                player_gold += monster.gold  # Award gold
                fight_continues = False
                return player_hp, player_gold, True  # Return True for won fight
            elif player_hp <= 0:
                print("You were defeated!")
                fight_continues = False
                return 0, player_gold, False #return false for lost fight
        elif player_choice == "2":  # Use consumable
            if inventory:
                used_consumable = use_consumable(inventory, monster.health)
                if used_consumable == -1000:
                    monster.health = 0  # Monster dies
                    fight_continues = False
                    gold_earned = monster.gold
                    player_gold += monster.gold  # Award gold
                    print(f"You gained {monster.gold} gold!") #added
                    return player_hp, player_gold, True # Monster killed, player wins.
                elif used_consumable:
                    player_hp = used_consumable
                else:
                    print("No consumable used.")
        elif player_choice == "3": #run
            chance = random.randint(0,1)
            if chance == 0:
                print("You successfully ran away!")
                return player_hp, player_gold, True #return true so player doesn't lose hp.
            else:
                # Monster's attack is reduced here
                monster_damage = random.randint(1, max(1, monster.attack - 3)) #reduced from 2 to 3
                player_hp -= monster_damage
                print("Failed to run away")
                print(f"Monster dealt {monster_damage} damage!")
                if player_hp <= 0:
                    print("You were defeated!")
                    return 0, player_gold, False
        elif player_choice == "4":
            display_inventory(inventory)
        elif player_choice == "5": #equip
            if inventory:
                 equipped_weapon = equip_item(inventory, "weapon")
            else:
                 print("No weapons to equip")
            if inventory:
                 equipped_shield = equip_item(inventory, "shield")
            else:
                 print("No shields to equip")
        else:
            print("Invalid choice!")
        if monster.health <= 0:
            fight_continues = False
    if gold_earned > 0:
        print(f"You gained {gold_earned} gold!")
    return player_hp, player_gold, False #this should never be reached.

def display_fight_statistics(player_hp, monster_hp):
    """Displays the current HP of the player and monster."""
    print(f"Your HP: {player_hp}")
    print(f"Monster HP: {monster_hp}")

def get_user_fight_options(inventory):
    """Gets the user's choice during a fight."""
    print("Choose your action:")
    print("1) Attack")
    print("2) Use consumable")
    print("3) Run")
    print("4) Check inventory")
    print("5) Equip Weapon/Shield")
    choice = input("Enter your choice: ")
    return choice

def game_map(player_position, monsters, player_data):
    """Handles the game map screen and movement."""
    pygame.init()
    try:
        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    except pygame.error as e:
        print(f"ERROR: pygame display error: {e}")
        return "quit"

    pygame.display.set_caption("Game Map")

    running = True
    player_rect = pygame.Rect(player_position[0] * SQUARE_SIZE, player_position[1] * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)

    equipped_weapon = None
    equipped_shield = None

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                return "quit"
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player_position = (max(0, player_position[0] - 1), player_position[1])
                elif event.key == pygame.K_RIGHT:
                    player_position = (min(GRID_SIZE - 1, player_position[0] + 1), player_position[1])
                elif event.key == pygame.K_UP:
                    player_position = (player_position[0], max(0, player_position[1] - 1))
                elif event.key == pygame.K_DOWN:
                    player_position = (player_position[0], min(GRID_SIZE - 1, player_position[1] + 1))
                elif event.key == pygame.K_RETURN and player_position == TOWN_LOCATION:
                    return "town"

        # Corrected line:  Creating a new Rect, not assigning to topleft.
        player_rect = pygame.Rect(player_position[0] * SQUARE_SIZE, player_position[1] * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)

        # Collision detection and combat
        monsters_to_remove = []  # Keep track of defeated monsters

        for monster in monsters:
            monster_rect = pygame.Rect(monster.get_location()[0] * SQUARE_SIZE, monster.get_location()[1] * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
            if player_rect.colliderect(monster_rect):
                print(f"You encountered a {monster.name}!")
                # Pass necessary data to handle_fight
                player_hp, player_gold, fight_won = handle_fight(player_data['hp'], player_data['gold'], player_data['inventory'], equipped_weapon, equipped_shield, monster)
                player_data['hp'] = player_hp
                player_data['gold'] = player_gold
                if fight_won:
                    monsters_to_remove.append(monster)  # Add defeated monster to removal list
                else:
                    return "quit" #game over

        # Remove defeated monsters after the loop
        for monster in monsters_to_remove:
            monsters.remove(monster)

        screen.fill(WHITE)

        try:
            pygame.draw.rect(screen, GREEN, pygame.Rect(TOWN_LOCATION[0] * SQUARE_SIZE, TOWN_LOCATION[1] * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
            pygame.draw.circle(screen, GREEN, pygame.Rect(TOWN_LOCATION[0] * SQUARE_SIZE, TOWN_LOCATION[1] * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE).center, SQUARE_SIZE // 4)
        except Exception as e:
            print(f"ERROR: pygame draw town error: {e}")
            return "quit"

        for monster in monsters:
            if not isinstance(monster.get_location(), tuple) or len(monster.get_location()) != 2:
                print(f"DEBUG: ERROR: Monster location is not a tuple: {monster.get_location()}")
                return "quit"
            try:
                monster_rect = pygame.Rect(monster.get_location()[0] * SQUARE_SIZE, monster.get_location()[1] * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
                pygame.draw.rect(screen, monster.color, monster_rect)
            except Exception as e:
                print(f"ERROR: pygame draw monster error: {e}")
                return "quit"

        try:
            pygame.draw.rect(screen, (0, 0, 255), player_rect)
        except Exception as e:
            print(f"ERROR: pygame draw player error: {e}")
            return "quit"

        try:
            pygame.display.flip()
        except Exception as e:
            print(f"ERROR: pygame.display.flip() error: {e}")
            return "quit"
        
        #update player position.
        player_data["x"] = player_position[0]
        player_data["y"] = player_position[1]

def save_game(player_data, monsters, save_name):
    """Saves the current game state to a JSON file."""
    try:
        monster_data = [{"location": monster.get_location(), "name": monster.name, "health": monster.health, "gold": monster.gold, "color": monster.color, "attack": monster.attack, "defense": monster.defense} for monster in monsters]
        data = {"player": player_data, "monsters": monster_data}
        filename = f"{save_name}.json"
        with open(filename, "w") as f:
            json.dump(data, f)
        print(f"Game saved as {filename}.")
    except Exception as e:
        print(f"ERROR: Failed to save game: {e}")

def load_game(save_name):
    """Loads a saved game state from a JSON file."""
    filename = f"{save_name}.json"
    if not os.path.exists(filename):
        print(f"ERROR: Save file {filename} does not exist.")
        return None, None
    try:
        with open(filename, "r") as f:
            data = json.load(f)
        player_data = data["player"]
        monsters = [WanderingMonster(monster["location"], monster["name"], monster["health"], monster["gold"], tuple(monster["color"]), monster["attack"], monster["defense"]) for monster in data["monsters"]]
        print("Game loaded.")
        return player_data, monsters
    except Exception as e:
        print(f"ERROR: Failed to load game: {e}")
        return None, None

def town(player_data, monsters):
    """Handles the town screen and player actions in town."""
    dog_happy = False
    shop_items = create_shop_items() # Create shop items
    dog_speaks = False #added

    while True:
        print("\n--- Town ---")
        print(f"HP: {player_data['hp']}, Gold: {player_data['gold']}")
        print("1) Go to the map")
        print("2) Sleep at the inn (heal 10 HP, cost 20 gold)")
        print("3) Check inventory")
        print("4) Visit the shop")
        print("5) Save Game")
        print("6) Pet the dog")
        print("7) Quit")
        choice = input("Enter your choice: ")

        if choice == "1":
            result = game_map((player_data["x"], player_data["y"]), monsters, player_data)
            if result == "quit":
                return "quit"
            elif result == "town":
                continue
        elif choice == "2":
            if player_data["gold"] >= 20:
                player_data["hp"] += 10
                player_data["gold"] -= 20
                print("You feel rested.")
                # Ensure at least one monster, up to two after sleeping.
                if len(monsters) < 1:
                    monsters.append(WanderingMonster.new_random_monster())
                if len(monsters) < 2:
                    monsters.append(WanderingMonster.new_random_monster())
            else:
                print("Not enough gold.")
        elif choice == "3":
            display_inventory(player_data["inventory"])
            if player_data["inventory"]: # only ask if there are items
                equip_choice = input("Enter the number of the item to equip, or 0 to cancel: ")
                try:
                    equip_choice = int(equip_choice)
                    if equip_choice > 0 and equip_choice <= len(player_data["inventory"]):
                        item_to_equip = player_data["inventory"][equip_choice - 1]
                        if item_to_equip["type"] == "weapon":
                            equipped_weapon = equip_item(player_data["inventory"], "weapon")
                        elif item_to_equip["type"] == "shield":
                            equipped_shield = equip_item(player_data["inventory"], "shield")
                        else:
                            print("You can't equip that item.")
                    elif equip_choice != 0:
                        print("Invalid item number.")
                except ValueError:
                    print("Invalid input.  Please enter a number.")

        elif choice == "4":
            shop(player_data, shop_items) #call shop function and pass shop items
        elif choice == "5":
            save_name = input("Enter a name for your save file: ")
            save_game(player_data, monsters, save_name)
        elif choice == "6":
            print("The dog wags its tail happily!")
            if random.random() < 0.25: # 1/4 chance
                print("The dog says: Woof! You look tired. You should sleep at the inn to feel better and maybe more monsters will appear! Woof!")
                dog_speaks = True #set to true so it doesn't speak again
            dog_happy = True
        elif choice == "7":
            return "quit"
        else:
            print("Invalid choice.")

def shop(player_data, shop_items):
    """Handles the shop screen and player actions in the shop."""
    while True:
        print("\n--- Shop ---")
        print(f"Your Gold: {player_data['gold']}")
        display_shop(shop_items)
        print("Enter the index of the item to purchase (or 0 to cancel): ")
        choice = input()
        if choice == "0":
            print("You leave the shop.")
            return
        try:
            item_index = int(choice)
            # Corrected line: Changed player_gold to player_data["gold"]
            purchase_successful, player_data["gold"] = purchase_item(player_data["inventory"], shop_items, item_index, player_data["gold"])
            if purchase_successful:
                print("Item purchased successfully!")
        except ValueError:
            print("Invalid input. Please enter a number or 0 to cancel.")

def main():
    """Main game function."""
    if os.path.exists(SAVE_FILE):
        os.remove(SAVE_FILE)
        print("DEBUG: Existing save file deleted.")

    print("Welcome to the Town Adventure!")
    print("1) Start New Game")
    print("2) Load Game")
    choice = input("Enter your choice (1 or 2): ")

    if choice == "1":
        player_data = {"hp": 30, "gold": 100, "x": 0, "y": 0, "inventory": [], "attack": 10}
        monsters = [WanderingMonster.new_random_monster() for _ in range(2)]
    elif choice == "2":
        save_name = input("Enter the name of the save file to load: ")
        player_data, monsters = load_game(save_name)
        if player_data is None:
            print("No save game found. Starting new game.")
            player_data = {"hp": 30, "gold": 100, "x": 0, "y": 0, "inventory": [], "attack": 10}
            monsters = [WanderingMonster.new_random_monster() for _ in range(2)]
    else:
        print("Invalid choice. Exiting.")
        return

    town(player_data, monsters)

if __name__ == "__main__":
    main()
