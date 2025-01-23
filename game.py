"""
Module containing the core game logic, including the Person class and bcolors class.

This module defines the characters (players and enemies) and their actions, such as attacking, using magic, and managing items.
"""

import random
from magic import Spell


class bcolors:
    """
    A class for colored text output in the terminal.

    Attributes:
        HEADER (str): Purple-colored text.
        OKBLUE (str): Blue-colored text.
        OKGREEN (str): Green-colored text.
        WARNING (str): Yellow-colored text.
        FAIL (str): Red-colored text.
        ENDC (str): Resets the color to default.
        BOLD (str): Bold text.
        UNDERLINE (str): Underlined text.
    """

    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class Person:
    """
    A class representing a character in the game (player or enemy).

    Attributes:
        name (str): The name of the character.
        maxhp (int): The maximum health points (HP) of the character.
        hp (int): The current health points (HP) of the character.
        maxmp (int): The maximum magic points (MP) of the character.
        mp (int): The current magic points (MP) of the character.
        atkl (int): The lower bound of the character's attack damage.
        atkh (int): The upper bound of the character's attack damage.
        magic (list): A list of magic spells the character can use.
        items (list): A list of items the character can use.
        actions (list): A list of available actions (Attack, Magic, Items).
    """

    def __init__(self, name, hp, mp, atk, magic, items):
        self.maxhp = hp
        self.hp = hp
        self.maxmp = mp
        self.mp = mp
        self.atkl = atk - 10
        self.atkh = atk + 10
        self.magic = magic
        self.items = items
        self.actions = ["Attack", "Magic", "Items"]
        self.name = name

    def generate_damage(self):
        """
        Generate random damage within the character's attack range.

        Returns:
            int: A random damage value between atkl and atkh.
        """
        return random.randrange(self.atkl, self.atkh)

    def take_damage(self, dmg):
        """Reduce HP by the given damage amount.

        Reduce the character's HP by the given damage amount.

        Args:
            dmg (int): The amount of damage to be taken.

        Returns:
            int: The updated HP after taking damage.
        """
        self.hp -= dmg
        if self.hp < 0:
            self.hp = 0
        return self.hp

    def heal(self, dmg):
        """Heal HP by the given amount.

        Heal the character's HP by the given amount.

        Args:
            dmg (int): The amount of HP to heal.
        """
        self.hp += dmg
        if self.hp > self.maxhp:
            self.hp = self.maxhp

    def get_hp(self):
        """Get current HP.

        Get the current HP of the character.

        Returns:
            int: The current HP.
        """
        return self.hp

    def get_max_hp(self):
        """Get maximum HP.

        Get the maximum HP of the character.

        Returns:
            int: The maximum HP.
        """
        return self.maxhp

    def get_mp(self):
        """Get current MP.

        Get the current MP of the character.

        Returns:
            int: The current MP.
        """
        return self.mp

    def get_max_mp(self):
        """Get maximum MP.

        Get the maximum MP of the character.

        Returns:
            int: The maximum MP.
        """
        return self.maxmp

    def reduce_mp(self, cost):
        """Reduce MP by the given cost.

        Reduce the character's MP by the given cost.

        Args:
            cost (int): The amount of MP to reduce.
        """
        self.mp -= cost

    def choose_action(self):
        """Display the available actions for the character."""
        i = 1
        print("\n" + "    " + bcolors.BOLD + self.name + bcolors.ENDC)
        print("\n" + bcolors.OKBLUE + bcolors.BOLD + "    ACTIONS" + bcolors.ENDC)
        for item in self.actions:
            print("        " + str(i) + ".", item)
            i += 1

    def choose_magic(self):
        """Display the available magic spells for the character."""
        i = 1

        print("\n" + bcolors.OKBLUE + bcolors.BOLD + "    MAGIC" + bcolors.ENDC)
        for spell in self.magic:
            print("        " + str(i) + ".", spell.name, "(cost: ", str(spell.cost) + ")")
            i += 1

    def choose_item(self):
        """Display the available items for the character."""
        i = 1

        print("\n" + bcolors.OKGREEN + bcolors.BOLD + "    ITEMS:" + bcolors.ENDC)
        for item in self.items:
            print("        " + str(i) + "." + item["item"].name + ":", item["item"].description,
                  " (x" + str(item["quantity"]) + ")")
            i += 1

    def choose_target(self, enemies):
        """Choose a target from the list of enemies.

        Choose a target from the list of enemies.

        Args:
            enemies (list): A list of enemy objects.

        Returns:
            int: The index of the chosen enemy.
        """
        i = 1
        print("\n", bcolors.FAIL + bcolors.BOLD + "    TARGET:" + bcolors.ENDC)
        for enemy in enemies:
            if enemy.get_hp() != 0:
                print("        " + str(i) + ".", enemy.name)
                i += 1
        choice = int(input("    Choose target: ")) - 1
        return choice

    def get_enemy_stats(self):
        """Display the stats of an enemy."""
        hp_bar = ""
        bar_ticks = (self.hp / self.maxhp) * 100 / 2

        while bar_ticks > 0:
            hp_bar += "█"
            bar_ticks -= 1

        while len(hp_bar) < 50:
            hp_bar += " "

        hp_string = str(self.hp) + "/" + str(self.maxhp)
        current_hp = ""

        if len(hp_string) < 11:
            decreased = 11 - len(hp_string)

            while decreased > 0:
                current_hp += " "
                decreased -= 1

            current_hp += hp_string

        else:
            current_hp = hp_string

        print("                         __________________________________________________ ")
        print(bcolors.BOLD + self.name + "     " +
              current_hp + " |" + bcolors.FAIL + hp_bar + bcolors.ENDC + "| ")

    def get_stats(self):
        """Display the stats of a player."""
        hp_bar = ""
        bar_ticks = (self.hp / self.maxhp) * 100 / 4

        mp_bar = ""
        mp_ticks = (self.mp / self.maxmp) * 100 / 10

        while bar_ticks > 0:
            hp_bar += "█"
            bar_ticks -= 1

        while len(hp_bar) < 25:
            hp_bar += " "

        while mp_ticks > 0:
            mp_bar += "█"
            mp_ticks -= 1

        while len(mp_bar) < 10:
            mp_bar += " "

        hp_string = str(self.hp) + "/" + str(self.maxhp)
        current_hp = ""

        if len(hp_string) < 9:
            decreased = 9 - len(hp_string)

            while decreased > 0:
                current_hp += " "
                decreased -= 1

            current_hp += hp_string

        else:
            current_hp = hp_string

        mp_string = str(self.mp) + "/" + str(self.maxmp)
        current_mp = ""

        if len(mp_string) < 7:
            decreased = 7 - len(mp_string)

            while decreased > 0:
                current_mp += " "
                decreased -= 1

            current_mp += mp_string
        else:
            current_mp = mp_string

        print("                         _________________________               __________ ")
        print(bcolors.BOLD + self.name + "       " +
              current_hp + " |" + bcolors.OKGREEN + hp_bar + bcolors.ENDC + "|     " +
              current_mp + " |" + bcolors.OKBLUE + mp_bar + bcolors.ENDC + "| ")
