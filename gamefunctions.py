#Eric Uhl
#2.17.25
#computer science
#i usually dont win

"""This is a module for game.py, it has a purchase item function, name prompt, a monster generator, and it prints a shop menu.

recently replaced print commands with return, everything appears to be functional.
"""



""" this is a program for purchasing an item, it takes starting money and subtracts item(s)value from your total.

purchase_item ((random.random()), random.randint(1,6), random.randint(0,4))
This is how you call the function"""

import random

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
        




#monster code.
"""monster generator, asigns health, power level, mulitiplies health by the power level, and picks one of three scenerios where you are interacting with the monster.

 new_random_monster()
 is the function call, seems to be working great."""

def new_random_monster():
    monsters = ["demon", "ghost", "goblin", "creeper"]
    health = random.randint(0,185)
    money = random.randint(0,185)
    power = random.randint(1,5)
    sel_health = health * power
    sel_monster = random.choice(monsters)
    #scenarios:
    scenario = [(f'You come across a {sel_monster} eating a corpse'), (f"A {sel_monster} jumps out from beind a crate"), (f'After entering a cave a {sel_monster} attacks you from a dark corner')]
    sel_scenario = random.choice(scenario)
                                                                   
    return(sel_health, money, sel_monster, sel_scenario)




"""takes name as arg returns "hello name!" centered.

name = input()
print_welcome(name)"""

def print_welcome(name):
    text = (f"Hello {name}")
    centered_text = text.center(15)
    print(centered_text)

"""shop menu, prints nicely formatted shop menu. Items can be changed as the function is called.

print_shop_menu('milk', 14.99, 'pie', 18.48)"""

def print_shop_menu(item1, x: float, item2, y: float):
    print('/' + '-' * 22 + '\\' )
    print(f"|{item1:<15}{x:>7}|",)
    print(f"|{item2:<15}{y:>7}|",)
    print('\\' + '-' * 22 + '/' )





""" testing functions held in this file, but only if called from this file
"""
def test_functions():
        #fuction for shop =D
    print_shop_menu('milk', 14.99, 'pie', 18.48)
    #welcome "name"
    name = input()
    print_welcome(name)
    #fuction for monster
    new_random_monster()
    #purchase item
    purchase_item ((random.random()), random.randint(1,6), random.randint(0,4))
if __name__ == "__main__":
    test_functions()
