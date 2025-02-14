from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
  from game import Game
  from player import Player
  from coins import Coin

from typing import Union
from .card_types import BlueCard

class WheatField(BlueCard):
  cost = 1
  z_index = 0

  def __init__(self):
    super().__init__()
    self.title = "Wheat Field"
    self.description = "Get 1 coin from the bank.\n(anyone's turn)"
    self.industry = "field"
    self.triggers = [1]

  def activate(self, game: Game, player: Player, dice_roll: int) -> None:
    player.receive(game.bank.give_player(1))

class Ranch(BlueCard):
  cost = 1
  z_index = 1

  def __init__(self):
    super().__init__()
    self.title = "Ranch"
    self.description = "Get 1 coin from the bank.\n(anyone's turn)"
    self.industry = "farm"
    self.triggers = [2]

  def activate(self, game: Game, player: Player, dice_roll: int) -> None:
    player.receive(game.bank.give_player(1))

class Forest(BlueCard):
  cost = 3
  z_index = 5
  
  def __init__(self):
    super().__init__()
    self.title = "Forest"
    self.description = "Get 1 coin from the bank.\n(anyone's turn)"
    self.industry = "industrial"
    self.triggers = [5]

  def activate(self, game: Game, player: Player, dice_roll: int) -> None:
    player.receive(game.bank.give_player(1))

class Mine(BlueCard):
  cost = 6
  z_index = 11

  def __init__(self):
    super().__init__()
    self.title = "Mine"
    self.description = "Get 5 coins from the bank.\n(anyone's turn)"
    self.industry = "industrial"
    self.triggers = [9]

  def activate(self, game: Game, player: Player, dice_roll: int) -> None:
    player.receive(game.bank.give_player(5))

class AppleOrchard(BlueCard):
  cost = 3
  z_index = 13
  
  def __init__(self):
    super().__init__()
    self.title = "Apple Orchard"
    self.description = "Get 3 coins from the bank.\n(anyone's turn)"
    self.industry = "field"
    self.triggers = [10]

  def activate(self, game: Game, player: Player, dice_roll: int) -> None:
    player.receive(game.bank.give_player(1))

Blues = Union[WheatField, Ranch, Forest, Mine, AppleOrchard]