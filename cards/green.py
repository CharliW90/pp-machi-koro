from typing import Union
from .cardTypes import GreenCard

class Bakery(GreenCard):
  cost = 1
  zIndex = 2
  
  def __init__(self):
    super().__init__()
    self.title = "Bakery"
    self.description = "Get 1 coin from the bank.\n(your turn only)"
    self.industry = "store"
    self.triggers = [2, 3]

  def activate(self, game, diceRoll: int) -> None:
    print(self.title + ": triggered on Dice roll: " + str(diceRoll))
    raise NotImplementedError("Not yet implemented the logic here")

class ConvenienceStore(GreenCard):
  cost = 2
  zIndex = 4
  
  def __init__(self):
    super().__init__()
    self.title = "Convenience Store"
    self.description = "Get 3 coins from the bank.\n(your turn only)"
    self.industry = "store"
    self.triggers = [4]

  def activate(self, game, diceRoll: int) -> None:
    print(self.title + ": triggered on Dice roll: " + str(diceRoll))
    raise NotImplementedError("Not yet implemented the logic here")

class CheeseFactory(GreenCard):
  cost = 5
  zIndex = 9
  
  def __init__(self):
    super().__init__()
    self.title = "Cheese Factory"
    self.description = "Get 3 coins from the bank per Ranch you own.\n(your turn only)"
    self.industry = "factory"
    self.triggers = [7]

  def activate(self, game, diceRoll: int) -> None:
    print(self.title + ": triggered on Dice roll: " + str(diceRoll))
    raise NotImplementedError("Not yet implemented the logic here")

class FurnitureFactory(GreenCard):
  cost = 3
  zIndex = 10
  
  def __init__(self):
    super().__init__()
    self.title = "Furniture Factory"
    self.description = "Get 3 coins from the bank per Forest/Mine you own.\n(your turn only)"
    self.industry = "factory"
    self.triggers = [8]

  def activate(self, game, diceRoll: int) -> None:
    print(self.title + ": triggered on Dice roll: " + str(diceRoll))
    raise NotImplementedError("Not yet implemented the logic here")

class FarmersMarket(GreenCard):
  cost = 2
  zIndex = 14
  
  def __init__(self):
    super().__init__()
    self.title = "Farmers Market"
    self.description = "Get 2 coins from the bank per Field/Orchard you own.\n(your turn only)"
    self.industry = "market"
    self.triggers = [11, 12]

  def activate(self, game, diceRoll: int) -> None:
    print(self.title + ": triggered on Dice roll: " + str(diceRoll))
    raise NotImplementedError("Not yet implemented the logic here")

Greens = Union[Bakery, ConvenienceStore, CheeseFactory, FurnitureFactory, FarmersMarket]