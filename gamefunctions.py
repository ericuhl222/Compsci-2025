import random


#town choice / what 2 do
"""Gets the user's choice in town and validates it."""
def get_user_town_choice(player_hp, gold):

    while True:
        print("\nYou are in town.")
        print(f"Current HP: {player_hp}, Current Gold: {gold}")
        print("What would you like to do?")
        print("1) Leave town (Fight Monster)")
        print("2) Sleep (Restore HP for 5 Gold)")
        print("3) Check your inventory")
        print("4) Go to the shop")
        print("5) Quit")

        choice = input("Enter your choice (1, 2, 3, 4, or 5): ")
        if choice in ("1", "2", "3", "4", "5"):
            return choice
        else:
            print("Invalid choice. Please enter 1, 2, 3, 4, or 5.")

#new random monster code
     #this will need to be balanced, but could be fun to have OP bad guy
"""generates one of three monster types to fight later
 called with new_random_monster

 returns sel_health, sel_money, sel_monster, sel_scenario"""

def new_random_monster():
    monsters = ["demon", "ghost", "goblin", "creeper"]
    health = random.randint(0,25)
    sel_money = random.randint(0,24)
    power = random.randint(1,3)
    sel_health = health * power
    sel_monster = random.choice(monsters)
    #scenarios:
    scenario = [(f'You come across a {sel_monster} eating a corpse'), (f"A {sel_monster} jumps out from beind a crate"), (f'After entering a cave a {sel_monster} attacks you from a dark corner')]
    sel_scenario = random.choice(scenario)
                                                                   
    return(sel_health, sel_money, sel_monster, sel_scenario)

#tussling 
"""Code for handling health and fights within the game

called by using handle_fight(player_hp, gold):
"""
def handle_fight(player_hp, gold):
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

#who is winning
"""Displays the current HP of the player and monster."""
def display_fight_statistics(player_hp, monster_hp):
    print(f"Your HP: {player_hp}, Monster HP: {monster_hp}")

#what to do in fight?
"""Gets the user's choice during a fight.

called with get_user_fight_options, should be called from gamefunctions"""
    
def get_user_fight_options():
    while True:
        print("1) Continue Fighting")
        print("2) Run Away")
        choice = input("Enter your choice (1 or 2): ")
        if choice in ("1", "2"):
            return choice
        else:
            print("Invalid choice. Please enter 1 or 2.")
#nap time code
"""sleep action restores health after removing 5 gold from your inventory
called with handle_sleep"""

def handle_sleep(player_hp, gold):
    if gold >= 5:
        player_hp = 30
        gold -= 5
        print("You slept and restored your HP.")
        return player_hp, gold
    else:
        print("You don't have enough gold to sleep.")
        return player_hp, gold

#purchasing from the shop
"""this is to be used with a shop code to purchase items within the game
called on with purchase_item(item_price, starting_money, quantity)"""

def purchase_item(item_price, starting_money, quantity):
    total_purchase = (item_price * quantity)
    if starting_money < total_purchase:
        quantity = quantity - 1
        total_purchase = (item_price * quantity)
        if starting_money < total_purchase:
            quantity = quantity - 1
        if starting_money > total_purchase:
            leftover_money = starting_money - (item_price * quantity)
            starting_money
            return(quantity, leftover_money)
            #this portion is to ensure the code doesnt buy more than it can afford.
    if starting_money > total_purchase:
        leftover_money = starting_money - (item_price * quantity)
        starting_money
        return(quantity, leftover_money)

#visual menu I made for the shop
"""this is to print a small menu for the shop, currently
it holds only two items in a small box of text
called on with print_shop_ menu(item1, x: float, item2, y: float):"""

def print_shop_menu(item1, x: float, item2, y: float):
    print('/' + '-' * 22 + '\\' )
    print(f"|{item1:<15}{x:>7}|",)
    print(f"|{item2:<15}{y:>7}|",)
    print('\\' + '-' * 22 + '/' )

"""inventory and shop stuff will be held below"""

