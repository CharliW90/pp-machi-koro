from typing import Union
from .card_types import LandmarkCard

class TrainStation(LandmarkCard):
  cost = 4
  z_index = 15

  def __init__(self):
    super().__init__()
    self.title = "Train Station"
    self.description = "You may roll 1 or 2 dice.\n(Ability)"

  def ability(self) -> str:
    return "double_dice"


class ShoppingMall(LandmarkCard):
  cost = 10
  z_index = 16

  def __init__(self):
    super().__init__()
    self.title = "Shopping Mall"
    self.description = "Your Restaurant and Store establishments earn +1 coin each when activated.\n(Ability)"
    
  def ability(self) -> str:
    return "plus_one"


class AmusementPark(LandmarkCard):
  cost = 16
  z_index = 17

  def __init__(self):
    super().__init__()
    self.title = "Amusement Park"
    self.description = "If you roll a double, take another turn after this one.\n(Ability)"
  
  def ability(self) -> str:
    return "double_turn"


class RadioTower(LandmarkCard):
  cost = 22
  z_index = 18

  def __init__(self):
    super().__init__()
    self.title = "Radio Tower"
    self.description = "Once per turn, you may choose to reroll the dice.\n(Ability)"
  
  def ability(self) -> str:
    return "reroll"

class Abilities():
  def __init__(self):
    self.double_dice = False
    self.plus_one = False
    self.double_turn = False
    self.reroll = False

  def update(self, ability_name):
    setattr(self, ability_name, True)
    return getattr(self, ability_name)

Landmarks = Union[TrainStation, ShoppingMall, AmusementPark, RadioTower]