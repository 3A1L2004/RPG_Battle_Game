"""
Module containing the Item class for items in the game.

This module defines the properties of items, such as their type, description, and effect.
"""


class Item:
    """
    A class representing an item in the game.

    Attributes:
        name (str): The name of the item.
        type (str): The type of the item (e.g., potion, elixir, attack).
        description (str): A description of the item's effect.
        prop (int): The property of the item (e.g., healing amount or damage).
    """

    def __init__(self, name, type, description, prop):
        self.name = name
        self.type = type
        self.description = description
        self.prop = prop
