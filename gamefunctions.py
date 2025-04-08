import random

# Town choice / what to do
def get_user_town_choice(player_hp, gold, inventory):  
    """Gets the user's choice in town and validates it.

    get_user_town_choice(player_hp, gold, inventory)"""
    while True:
        print("\nYou are in town.")
        print(f"Current HP: {player_hp}, Current Gold: {gold}")
        print("What would you like to do?")
        print("1) Leave town (Fight Monster)")
        print("2) Sleep (Restore HP for 5 Gold)")
        print("3) Check your inventory")
        print("4) Go to the shop")
        print("5) Equip item")  
        print("6) Quit")  

        choice = input("Enter your choice (1, 2, 3, 4, 5, or 6): ")  
        if choice in ("1", "2", "3", "4", "5", "6"):  # changed to 6
            return choice
        else:
            print("Invalid choice. Please enter 1, 2, 3, 4, 5, or 6.")  


# monster code
def new_random_monster():
    """Generates one of several monster types to fight.

    returns sel_health, sel_money, sel_monster, sel_scenario
    """
    monsters = ["demon", "ghost", "goblin", "creeper"]
    health = random.randint(10, 30)  
    sel_money = random.randint(5, 20)
    power = random.randint(1, 3)
    sel_health = health * power  # lowered power var
    sel_monster = random.choice(monsters)
    # Scenarios:
    scenario = [
        f"You come across a {sel_monster} eating a corpse.",
        f"A {sel_monster} jumps out from behind a crate!",
        f"After entering a cave, a {sel_monster} attacks you from a dark corner.",
    ]
    sel_scenario = random.choice(scenario)

    return sel_health, sel_money, sel_monster, sel_scenario


# Fighting code
def handle_fight(player_hp, gold, inventory, equipped_weapon, equipped_shield):  
    """Code for handling health and fights within the game.

    called by using handle_fight(player_hp, gold)
    """
    monster_hp, monster_gold, monster_type, scenario = new_random_monster()  # use new random monster
    monster_attack = random.randint(5, 12)  
    print(scenario)  
    print(f"A wild {monster_type} appears!")
    print(f"Monster HP: {monster_hp}")  #

    while player_hp > 0 and monster_hp > 0:
        display_fight_statistics(player_hp, monster_hp)
        choice = get_user_fight_options(inventory)  # inventory

        if choice == "1":
            player_attack = random.randint(5, 15)  
            if equipped_weapon:  
                player_attack += equipped_weapon["damage"]
                print(f"Your {equipped_weapon['name']} adds {equipped_weapon['damage']} damage!")
            monster_hp -= player_attack
            print(f"You attack the {monster_type} for {player_attack} damage.")

            if monster_hp > 0:
                monster_damage = random.randint(1, monster_attack)
                if equipped_shield:
                    monster_damage -= equipped_shield["defense"]  
                    print(f"Your {equipped_shield['name']} reduces damage by {equipped_shield['defense']}!")
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
                elif item_type == "shield":
                    equipped_shield = equip_item(inventory, item_type)
                    if equipped_shield:
                        print(f"Equipped {equipped_shield['name']}.")
            else:
                print("Invalid item type.")
        elif choice == "4": # consumable
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
        gold += monster_gold  # Award gold based on the monster
        print(f"You found {monster_gold} gold.")
        return player_hp, gold, equipped_weapon, equipped_shield


# Who is winning
def display_fight_statistics(player_hp, monster_hp):
    """Displays the current HP of the player and monster."""
    print(f"Your HP: {player_hp}, Monster HP: {monster_hp}")


# What to do in fight?
def get_user_fight_options(inventory):  # inventory
    """Gets the user's choice during a fight.

    called with get_user_fight_options, should be called from gamefunctions
    """
    while True:
        print("1) Continue Fighting")
        print("2) Run Away")
        print("3) Equip Item")  # equip
        print("4) Use Consumable")
        choice = input("Enter your choice (1, 2, 3, or 4): ")  
        if choice in ("1", "2", "3", "4"): 
            return choice
        else:
            print("Invalid choice. Please enter 1, 2, 3, or 4.")  


# Nap time code
def handle_sleep(player_hp, gold):
    """Sleep action restores health after removing 5 gold from your inventory
    called with handle_sleep
    """
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
    x and y are prices respectively.
    called on with print_shop_ menu(item1, x: float, item2, y: float):
    """
    print("/" + "-" * 22 + "\\")
    print(f"|{item1:<15}{x:>7}|",)
    print(f"|{item2:<15}{y:>7}|",)
    print("\\" + "-" * 22 + "/")



"""inventory and additional shop stuff will be held below"""


"""
Create Item prompts
called with create_"item","""


# looks good ?

def create_sword(name="Basic Sword", max_durability=10, damage=5, price=10):
    """Creates a sword item.

    called with create_sword"""
    
    return {
        "name": name,
        "type": "weapon",
        "maxDurability": max_durability,
        "currentDurability": max_durability,
        "damage": damage,  
        "price": price,
    }


def create_anthrax_dart(name="Anthrax Dart", effect="instant_kill", price=20):
    """Creates an item that instantly kills a monster.
    called with create_athrax_dart"""
    return {
        "name": name,
        "type": "consumable",
        "effect": effect,
        "price": price,
    }


def create_shield(name="Basic Shield", max_durability=6, defense=3, price=15):
    """Creates a shield item.
    called with create_shield"""
    
    return {
        "name": name,
        "type": "shield",
        "maxDurability": max_durability,
        "currentDurability": max_durability,
        "defense": defense, 
        "price": price,
    }

#remove?
def create_misc_item(name, note, price=5):
    """Creates a miscellaneous item.
    called with create_misc_item non functional atm"""
    return {
        "name": name,
        "type": "misc",
        "note": note,
        "price": price,
    }

#shop stuff below
def create_shop_items():
    """Creates a list of items available in the shop.
    create_shop_items()"""
    return [
        create_sword(),
        create_anthrax_dart(),
        create_shield(),
        create_sword(name="Steel Sword", max_durability=20, damage=10, price=30),
        create_anthrax_dart(name="Anthrax Dart", effect="instant_kill", price=40),
        create_shield(name="Iron Shield", max_durability=12, defense=6, price=25),
    ]



def display_shop(shop_items):
    """Displays the items available in the shop.
    display_shop"""
    
    print("/" + "-" * 38 + "\\")
    print(f"|{'Index':<5}{'Item':<15}{'Type':<12}{'Price':>6}|")
    print("|" + "-" * 38 + "|")
    for index, item in enumerate(shop_items):
        print(f"|{index + 1:<5}{item['name']:<15}{item['type']:<12}{item['price']:>6}|")
    print("\\" + "-" * 38 + "/")



def purchase_item(inventory, shop_items, item_index, player_gold):
    """Purchases an item from the shop and adds it to the inventory.
    Also deducts gold.
    purchase_item(inventory, shop_items, item_index, player_gold)

    lookin good B)
    """
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
    """Equips an item of a specific type from inventory.
    equip_item(inventory, item_type):"""
    
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
    """Displays the items in the user's inventory.
    display_inventory(inventory)"""
    
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
        elif item["type"] == "misc":
            print(f"    Note: {item['note']}")

def use_consumable(inventory, monster_hp):
    """Allows the player to use a consumable item from their inventory.
    
    use_consumable(inventory, monster_hp)"""
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

def main():
    """Main game function."""
    player_hp = 30
    player_gold = 100
    inventory = []
    shop_items = create_shop_items()
    equipped_weapon = None  # Keep track of equipped weapon
    equipped_shield = None  # Keep track of equipped shield

    print("Welcome to the Town Adventure!")

    while True:
        choice = get_user_town_choice(player_hp, player_gold, inventory)  

        if choice == "1":
            player_hp, player_gold, equipped_weapon, equipped_shield = handle_fight(
                player_hp, player_gold, inventory, equipped_weapon, equipped_shield
            )  
            if player_hp <= 0:
                print("Game Over!")
                break
        elif choice == "2":
            player_hp, player_gold = handle_sleep(player_hp, player_gold)
        elif choice == "3":
            display_inventory(inventory)
        elif choice == "4":
            display_shop(shop_items)
            while True:
                try:
                    item_index = int(
                        input(
                            "Enter the index of the item to purchase (or 0 to cancel): "
                        )
                    )
                    if item_index == 0:
                        break  
                    purchase_successful, player_gold = purchase_item(
                        inventory, shop_items, item_index, player_gold
                    )
                    if purchase_successful:
                        break  # Exit 
                except ValueError:
                    print("Invalid input. Please enter a number.")
        elif choice == "5":  # Equip
            item_type = input("Enter the type of item to equip (weapon/shield): ").lower()
            if item_type in ("weapon", "shield"):
                if item_type == "weapon":
                    equipped_weapon = equip_item(inventory, item_type)
                    if equipped_weapon:
                        print(f"Equipped {equipped_weapon['name']}.")
                elif item_type == "shield":
                    equipped_shield = equip_item(inventory, item_type)
                    if equipped_shield:
                        print(f"Equipped {equipped_shield['name']}.")
            else:
                print("Invalid item type.")
        elif choice == "6":  # Quit
            print("Thank you for playing!")
            break

        # mini main loop simplify main w. this?
        if player_hp <= 0:
            print("Game Over!")
            break


if __name__ == "__main__":
    main()

