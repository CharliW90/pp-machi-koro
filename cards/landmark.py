from typing import Union
from .cardTypes import LandmarkCard

class TrainStation(LandmarkCard):
  cost = 4
  zIndex = 15

  def __init__(self):
    super().__init__()
    self.title = "Train Station"
    self.description = "You may roll 1 or 2 dice.\n(Ability)"

  def ability(self) -> str:
    return "doubleDice"


class ShoppingMall(LandmarkCard):
  cost = 10
  zIndex = 16

  def __init__(self):
    super().__init__()
    self.title = "Shopping Mall"
    self.description = "Your Restaurant and Store establishments earn +1 coin each when activated.\n(Ability)"
    
  def ability(self) -> str:
    return "plusOne"


class AmusementPark(LandmarkCard):
  cost = 16
  zIndex = 17

  def __init__(self):
    super().__init__()
    self.title = "Amusement Park"
    self.description = "If you roll a double, take another turn after this one.\n(Ability)"
  
  def ability(self) -> str:
    return "doubleTurns"


class RadioTower(LandmarkCard):
  cost = 22
  zIndex = 18

  def __init__(self):
    super().__init__()
    self.title = "Radio Tower"
    self.description = "Once per turn, you may choose to reroll the dice.\n(Ability)"
  
  def ability(self) -> str:
    return "reRolls"

class Abilities():
  def __init__(self):
    self.doubleDice = False
    self.plusOne = False
    self.doubleTurns = False
    self.reRolls = False

  def update(self, abilityName):
    setattr(self, abilityName, True)
    return getattr(self, abilityName)

Landmarks = Union[TrainStation, ShoppingMall, AmusementPark, RadioTower]