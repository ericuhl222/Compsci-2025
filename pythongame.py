import random

def display_fight_statistics(player_hp, monster_hp):
    """Displays the current HP of the player and monster."""
    print(f"Your HP: {player_hp}, Monster HP: {monster_hp}")

def get_user_fight_options():
    """Gets the user's choice during a fight."""
    while True:
        print("1) Continue Fighting")
        print("2) Run Away")
        choice = input("Enter your choice (1 or 2): ")
        if choice in ("1", "2"):
            return choice
        else:
            print("Invalid choice. Please enter 1 or 2.")

def handle_fight(player_hp, gold):
    """Handles the monster fight."""
    monster_hp = 15
    monster_attack = 5
    monster_type = "Goblin"
    print(f"A wild {monster_type} appears!")

    while player_hp > 0 and monster_hp > 0:
        display_fight_statistics(player_hp, monster_hp)
        choice = get_user_fight_options()

        if choice == "1":
            player_attack = random.randint(3, 8)
            monster_hp -= player_attack
            print(f"You attack the {monster_type} for {player_attack} damage.")

            if monster_hp > 0:
                monster_damage = random.randint(1, monster_attack)
                player_hp -= monster_damage
                print(f"The {monster_type} attacks you for {monster_damage} damage.")

        elif choice == "2":
            print("You run away!")
            return player_hp, gold

    if player_hp <= 0:
        print("You were defeated!")
        return 0, gold
    else:
        print(f"You defeated the {monster_type}!")
        gold += 10
        print("You found 10 gold.")
        return player_hp, gold

def handle_sleep(player_hp, gold):
    """Handles the sleep action."""
    if gold >= 5:
        player_hp = 30
        gold -= 5
        print("You slept and restored your HP.")
        return player_hp, gold
    else:
        print("You don't have enough gold to sleep.")
        return player_hp, gold

def get_user_town_choice():
    """Gets the user's choice in town and validates it."""
    while True:
        print("\nYou are in town.")
        print(f"Current HP: {player_hp}, Current Gold: {gold}")
        print("What would you like to do?")
        print("1) Leave town (Fight Monster)")
        print("2) Sleep (Restore HP for 5 Gold)")
        print("3) Quit")

        choice = input("Enter your choice (1, 2, or 3): ")
        if choice in ("1", "2", "3"):
            return choice
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")

def game_loop():
    """Main game loop."""
    global player_hp, gold #player_hp and gold are needed to be global to be modified in other functions.
    player_hp = 30
    gold = 10

    while True:
        choice = get_user_town_choice()

        if choice == "1":
            if gold >= 0:
                player_hp, gold = handle_fight(player_hp, gold)
                if player_hp <= 0:
                    player_hp = 30 #reset hp on death.
            else:
                print("You are too weak to fight, you run away.")

        elif choice == "2":
            player_hp, gold = handle_sleep(player_hp, gold)

        elif choice == "3":
            print("Quitting the game. Goodbye!")
            break

if __name__ == "__main__":
    game_loop()
  
