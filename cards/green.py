from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
  from game import Game
  from player import Player

from typing import Union
from .card_types import GreenCard
from .blue import WheatField, Ranch, Forest, Mine, AppleOrchard

class Bakery(GreenCard):
  cost = 1
  z_index = 2
  
  def __init__(self):
    super().__init__()
    self.title = "Bakery"
    self.description = "Get 1 coin from the bank.\n(your turn only)"
    self.industry = "store"
    self.triggers = [2, 3]

  def activate(self, game: Game, player: Player, dice_roll: int) -> None:
    player.receive(game.bank.give_player(2 if player.abilities.plus_one else 1))

class ConvenienceStore(GreenCard):
  cost = 2
  z_index = 4
  
  def __init__(self):
    super().__init__()
    self.title = "Convenience Store"
    self.description = "Get 3 coins from the bank.\n(your turn only)"
    self.industry = "store"
    self.triggers = [4]

  def activate(self, game: Game, player: Player, dice_roll: int) -> None:
    player.receive(game.bank.give_player(4 if player.abilities.plus_one else 3))

class CheeseFactory(GreenCard):
  cost = 5
  z_index = 9
  
  def __init__(self):
    super().__init__()
    self.title = "Cheese Factory"
    self.description = "Get 3 coins from the bank per Ranch you own.\n(your turn only)"
    self.industry = "factory"
    self.triggers = [7]

  def activate(self, game: Game, player: Player, dice_roll: int) -> None:
    players_ranches = player.cards.count(Ranch)
    if players_ranches > 0:
      player.receive(game.bank.give_player(3 * players_ranches))
    else:
      print(f"{player.name} has no Ranches - no income received.")

class FurnitureFactory(GreenCard):
  cost = 3
  z_index = 10
  
  def __init__(self):
    super().__init__()
    self.title = "Furniture Factory"
    self.description = "Get 3 coins from the bank per Forest/Mine you own.\n(your turn only)"
    self.industry = "factory"
    self.triggers = [8]

  def activate(self, game: Game, player: Player, dice_roll: int) -> None:
    players_forests = player.cards.count(Forest)
    players_mines = player.cards.count(Mine)
    if players_forests > 0 or players_mines > 0:
      player.receive(game.bank.give_player(3 * (players_forests + players_mines)))
    else:
      print(f"{player.name} has no Forests or Mines - no income received.")


class FarmersMarket(GreenCard):
  cost = 2
  z_index = 14
  
  def __init__(self):
    super().__init__()
    self.title = "Farmers Market"
    self.description = "Get 2 coins from the bank per Field/Orchard you own.\n(your turn only)"
    self.industry = "market"
    self.triggers = [11, 12]

  def activate(self, game: Game, player: Player, dice_roll: int) -> None:
    players_wheat_fields = player.cards.count(WheatField)
    players_apple_orchards = player.cards.count(AppleOrchard)
    if players_wheat_fields > 0 or players_apple_orchards > 0:
      player.receive(game.bank.give_player(3 * (players_wheat_fields + players_apple_orchards)))
    else:
      print(f"{player.name} has no Wheat Fields or Apple Orchards - no income received.")

Greens = Union[Bakery, ConvenienceStore, CheeseFactory, FurnitureFactory, FarmersMarket]