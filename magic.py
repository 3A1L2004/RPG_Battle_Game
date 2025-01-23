"""
Module containing the Spell class for magic spells in the game.

This module defines the properties and behavior of magic spells, including their damage and cost.
"""
import random


class Spell:
    """
    A class representing a magic spell.

    Attributes:
        name (str): The name of the spell.
        cost (int): The MP cost of using the spell.
        dmg (int): The base damage of the spell.
    """

    def __init__(self, name, cost, dmg):
        self.name = name
        self.cost = cost
        self.dmg = dmg

    def generate_damage(self):
        """
        Generate random damage within the spell's damage range.

        Returns:
            int: A random damage value between (dmg - 15) and (dmg + 15).
        """
        low = self.dmg - 15
        high = self.dmg + 15
        return random.randrange(low, high)
