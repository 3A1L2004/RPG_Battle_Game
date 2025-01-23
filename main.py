"""
Main module for running the RPG battle game.

This module initializes the game, including players, enemies, spells, and items.
It also handles the main game loop where players and enemies take turns to attack, use magic, or items.
"""

from game import Person, bcolors
from magic import Spell
from inventory import Item
import random

# Create Magic
fire = Spell("Fire", 25, 600)
thunder = Spell("Thunder", 25, 600)
blizzard = Spell("Blizzard", 25, 600)
meteor = Spell("Meteor", 40, 1200)

# Create Items
potion = Item("Potion", "potion", "Heals 50 HP", 50)
elixer = Item("Elixer", "elixer", "Fully restores HP/MP of player", 9999)
grenade = Item("Grenade", "attack", "Deals 500 damage", 500)

player_spells = [fire, thunder, blizzard, meteor]
player_items = [{"item": potion, "quantity": 15},
                {"item": elixer, "quantity": 5}, {"item": grenade, "quantity": 5}]

# Instantiate Players and Enemies
player1 = Person("Homayun", 3260, 132, 300, player_spells, player_items)
player2 = Person("AmirAli", 3260, 132, 300, player_spells, player_items)
player3 = Person("Hossein", 3260, 132, 300, player_spells, player_items)

enemy1 = Person("Enemy_1", 1250, 130, 560, [], [])
enemy2 = Person("Enemy_2", 1250, 130, 560, [], [])
enemy3 = Person("Enemy_3", 1250, 130, 560, [], [])

players = [player1, player2, player3]
enemies = [enemy1, enemy2, enemy3]

running = True

print(bcolors.FAIL + bcolors.BOLD + "AN ENEMY ATTACKS!" + bcolors.ENDC)

while running:
    print("=============================")

    # Show stats of all players and enemies
    print("\n\n")
    print("NAME                     HP                                      MP")

    for player in players:
        player.get_stats()

    print("\n")

    for enemy in enemies:
        enemy.get_enemy_stats()

    # Players' turn
    for player in players:
        if player.get_hp() == 0:
            continue  # Skip if player is defeated

        player.choose_action()
        choice = input("    Choose action: ")
        index = int(choice) - 1

        if index > 2 or index < 0:
            raise ValueError("Invalid action! Choose a correct value for action (from 1 to 3).")

        if index == 0:  # Attack
            dmg = player.generate_damage()
            target = player.choose_target(enemies)
            enemies[target].take_damage(dmg)
            print("You attacked " + enemies[target].name + " for", dmg, "points of damage.")

        elif index == 1:  # Magic
            player.choose_magic()
            magic_choice = int(input("    Choose magic: ")) - 1

            if magic_choice > 3 or magic_choice < 0:
                raise ValueError("Invalid magic! Choose a correct value for magic (from 1 to 4).")

            spell = player.magic[magic_choice]
            magic_dmg = spell.generate_damage()

            current_mp = player.get_mp()

            if spell.cost > current_mp:
                print(bcolors.FAIL + "\nNot enough MP\n" + bcolors.ENDC)
                continue

            player.reduce_mp(spell.cost)

            target = player.choose_target(enemies)
            enemies[target].take_damage(magic_dmg)
            print(bcolors.OKBLUE + "\n" + spell.name + " deals", str(magic_dmg),
                  "points of damage to " + enemies[target].name + bcolors.ENDC)

        elif index == 2:  # Items
            player.choose_item()
            item_choice = int(input("    Choose item: ")) - 1

            if item_choice > 2 or index < 0:
                raise ValueError("Invalid item! Choose a correct value for item (from 1 to 3).")

            item = player.items[item_choice]["item"]

            if player.items[item_choice]["quantity"] == 0:
                print(bcolors.FAIL + "\n" + "None left..." + bcolors.ENDC)
                continue

            player.items[item_choice]["quantity"] -= 1

            if item.type == "potion":
                player.heal(item.prop)
                print(bcolors.OKGREEN + "\n" + item.name + " heals for", str(item.prop), "HP" + bcolors.ENDC)

            elif item.type == "elixer":
                player.hp = player.maxhp
                player.mp = player.maxmp
                print(bcolors.OKGREEN + "\n" + item.name + " fully restores HP/MP" + bcolors.ENDC)

            elif item.type == "attack":
                target = player.choose_target(enemies)
                enemies[target].take_damage(item.prop)
                print(bcolors.FAIL + "\n" + item.name + " deals", str(item.prop),
                      "points of damage to " + enemies[target].name + bcolors.ENDC)

    # Check if all enemies are defeated
    defeated_enemies = 0
    for enemy in enemies:
        if enemy.get_hp() == 0:
            defeated_enemies += 1

    if defeated_enemies >= 2:
        print(bcolors.OKGREEN + "You win!" + bcolors.ENDC)
        running = False
        break

    # Enemies' turn
    for enemy in enemies:
        if enemy.get_hp() == 0:
            continue  # Skip if enemy is defeated

        target = random.randrange(0, len(players))
        enemy_dmg = enemy.generate_damage()
        players[target].take_damage(enemy_dmg)
        print(bcolors.FAIL + enemy.name + " attacks " + players[target].name + " for", enemy_dmg,
              "points of damage." + bcolors.ENDC)

    # Check if all players are defeated
    defeated_players = 0
    for player in players:
        if player.get_hp() == 0:
            defeated_players += 1

    if defeated_players >= 2:
        print(bcolors.FAIL + "Your enemies have defeated you!" + bcolors.ENDC)
        running = False
        break
