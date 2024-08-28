from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
  from game import Game
  from player import Player

from typing import Union
from .card_types import RedCard

class Cafe(RedCard):
  cost = 2
  z_index = 3

  def __init__(self):
    super().__init__()
    self.title = "Cafe"
    self.description = "Take 1 coin from the active player.\n(opponent's turn)"
    self.industry = "restaurant"
    self.triggers = [3]

  def activate(self, game: Game, player: Player, dice_roll: int) -> None:
    current_player: Player = game.current_player()
    game.bank.handle_transfer(current_player, 2 if player.abilities.plus_one else 1, player)

class FamilyRestaurant(RedCard):
  cost = 3
  z_index = 12

  def __init__(self):
    super().__init__()
    self.title = "Family Restaurant"
    self.description = "Take 2 coins from the active player.\n(opponent's turn)"
    self.industry = "restaurant"
    self.triggers = [9, 10]

  def activate(self, game: Game, player: Player, dice_roll: int) -> None:
    current_player: Player = game.current_player()
    game.bank.handle_transfer(current_player, 3 if player.abilities.plus_one else 2, player)

Reds = Union[Cafe, FamilyRestaurant]