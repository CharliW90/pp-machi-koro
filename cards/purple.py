from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
  from game import Game

from typing import Union
from .card_types import PurpleCard

class Stadium(PurpleCard):
  cost = 6
  zIndex = 6

  def __init__(self):
    super().__init__()
    self.title = "Stadium"
    self.description = "Take 2 coins from each opponent.\n(your turn only)"
    self.industry = "major"
    self.triggers = [6]

  def activate(self, game: Game, dice_roll: int) -> None:
    print(f"{self.title}: triggered on Dice roll: {dice_roll}")
    raise NotImplementedError("Not yet implemented the logic here")

class TVStation(PurpleCard):
  cost = 7
  zIndex = 7

  def __init__(self):
    super().__init__()
    self.title = "TV Station"
    self.description = "Take 5 coins from an opponent.\n(your turn only)"
    self.industry = "major"
    self.triggers = [6]

  def activate(self, game: Game, dice_roll: int) -> None:
    print(f"{self.title}: triggered on Dice roll: {dice_roll}")
    raise NotImplementedError("Not yet implemented the logic here")

class BusinessCentre(PurpleCard):
  cost = 8
  zIndex = 8

  def __init__(self):
    super().__init__()
    self.title = "Business Centre"
    self.description = "Exchange 1 of your non-major establishments for 1 an opponent owns.\n(your turn only)"
    self.industry = "major"
    self.triggers = [6]

  def activate(self, game: Game, dice_roll: int) -> None:
    print(f"{self.title}: triggered on Dice roll: {dice_roll}")
    raise NotImplementedError("Not yet implemented the logic here")

Purples = Union[Stadium, TVStation, BusinessCentre]