import gamefunctions
import random

def game_loop():
    """Main game loop."""
    global player_hp, gold #player_hp and gold are needed to be global to be modified in other functions.
    player_hp = 30
    gold = 10
    inventory = []

    while True:
        choice = gamefunctions.get_user_town_choice(player_hp, gold)

        if choice == "1":
            if gold >= 0:
                player_hp, gold = gamefunctions.handle_fight(player_hp, gold)
                if player_hp <= 0:
                    player_hp = 30 #reset hp on death.
            else:
                print("You are too weak to fight, you run away.")

        elif choice == "2":
            player_hp, gold = gamefunctions.handle_sleep(player_hp, gold)

        elif choice == "3":
            pass
            #gamefunctions.display_inventory(inventory)
        elif choice == "4":
            pass
            #shop
        elif choice == "5":
            print("Quitting the game. Goodbye!")
            break

if __name__ == "__main__":
    game_loop()
  
