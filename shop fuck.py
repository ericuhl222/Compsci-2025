def create_sword():
  """Creates a sword item."""
  return {"name": "Sword of Sharpness", "type": "weapon", "maxDurability": 10, "currentDurability": 10, "damage_bonus": 5}

def create_monster_bane():
  """Creates a monster-bane item."""
  return {"name": "Monsterbane Potion", "type": "special", "effect": "instant_monster_defeat"}

def display_inventory(inventory):
  """Displays the player's inventory."""
  if not inventory:
    print("Your inventory is empty.")
    return

  print("Inventory:")
  for i, item in enumerate(inventory):
    print(f"{i + 1}. {item['name']} ({item['type']})")
    if "currentDurability" in item and "maxDurability" in item:
        print(f"   Durability: {item['currentDurability']}/{item['maxDurability']}")
    if 'damage_bonus' in item:
        print(f"   Damage Bonus: {item['damage_bonus']}")
    if 'effect' in item:
        print(f"   Effect: {item['effect']}")

def equip_item(inventory, equipped_items):
  """Allows the player to equip an item."""
  item_type = input("Enter the type of item to equip (weapon, shield, special, etc.): ")
  relevant_items = [item for item in inventory if item["type"] == item_type]

  if not relevant_items:
    print(f"No {item_type}s in your inventory.")
    return

  print("Select an item to equip:")
  for i, item in enumerate(relevant_items):
    print(f"{i + 1}. {item['name']}")
  print("0. None")

  try:
    choice = int(input("Enter your choice: "))
    if choice == 0:
      print("No item equipped.")
      equipped_items[item_type] = None
      return
    elif 1 <= choice <= len(relevant_items):
      selected_item = relevant_items[choice - 1]
      equipped_items[item_type] = selected_item
      print(f"Equipped {selected_item['name']}.")
    else:
      print("Invalid choice.")
  except ValueError:
    print("Invalid input.")

def shop(inventory, gold):
    """Simulates a shop where the player can buy items."""
    print("Welcome to the shop!")
    print(f"Your gold: {gold}")
    print("Available items:")
    print("1. Sword of Sharpness (10 gold)")
    print("2. Monsterbane Potion (15 gold)")
    print("0. Exit shop")

    try:
        choice = int(input("Enter your choice: "))
        if choice == 1:
            if gold >= 10:
                inventory.append(create_sword())
                gold -= 10
                print("Sword purchased!")
            else:
                print("Not enough gold.")
        elif choice == 2:
            if gold >= 15:
                inventory.append(create_monster_bane())
                gold -= 15
                print("Monsterbane Potion purchased!")
            else:
                print("Not enough gold.")
        elif choice == 0:
            print("Exiting shop.")
        else:
            print("Invalid choice.")
    except ValueError:
        print("Invalid input.")
    return inventory, gold

def use_monsterbane(inventory, equipped_items):
    """Removes the monsterbane item from the inventory after use."""
    if equipped_items.get('special') and equipped_items['special']['name'] == "Monsterbane Potion":
        print("The monsterbane potion was used to defeat the monster.")
        inventory.remove(equipped_items['special'])
        equipped_items['special'] = None
    else:
        print("No monsterbane potion equipped.")

# Example usage:
inventory = []
equipped_items = {"weapon": None, "shield": None, "special": None} #dictionary to keep track of equipped items
gold = 25

inventory, gold = shop(inventory, gold)
display_inventory(inventory)
equip_item(inventory, equipped_items)
display_inventory(inventory)
print(equipped_items) #shows equipped items.

if equipped_items.get('special') and equipped_items['special']['name'] == "Monsterbane Potion":
    use_monsterbane(inventory, equipped_items)
    display_inventory(inventory)
    print(equipped_items)
