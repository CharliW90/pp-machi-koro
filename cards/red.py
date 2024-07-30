from typing import Union
from .cardTypes import RedCard

class Cafe(RedCard):
  cost = 2
  zIndex = 3

  def __init__(self):
    super().__init__()
    self.title = "Cafe"
    self.description = "Take 1 coin from the active player.\n(opponent's turn)"
    self.industry = "restaurant"
    self.triggers = [3]

  def activate(self, game, diceRoll) -> None:
    print(f"{self.title}: triggered on Dice roll: {diceRoll}")
    raise NotImplementedError("Not yet implemented the logic here")

class FamilyRestaurant(RedCard):
  cost = 3
  zIndex = 12

  def __init__(self):
    super().__init__()
    self.title = "Family Restaurant"
    self.description = "Take 2 coins from the active player.\n(opponent's turn)"
    self.industry = "restaurant"
    self.triggers = [9, 10]

  def activate(self, game, diceRoll) -> None:
    print(f"{self.title}: triggered on Dice roll: {diceRoll}")
    raise NotImplementedError("Not yet implemented the logic here")

Reds = Union[Cafe, FamilyRestaurant]