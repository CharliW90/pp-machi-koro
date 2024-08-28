from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
  from game import Game
  from player import Player
  from . import Blues, Greens, Reds

from typing import Union
from .card_types import PurpleCard
from actions import choose

class Stadium(PurpleCard):
  cost = 6
  z_index = 6

  def __init__(self):
    super().__init__()
    self.title = "Stadium"
    self.description = "Take 2 coins from each opponent.\n(your turn only)"
    self.industry = "major"
    self.triggers = [6]

  def activate(self, game: Game, player: Player, dice_roll: int) -> None:
    [game.bank.handle_transfer(opponent, 2, player) for opponent in game.players if opponent is not player]

class TVStation(PurpleCard):
  cost = 7
  z_index = 7

  def __init__(self):
    super().__init__()
    self.title = "TV Station"
    self.description = "Take 5 coins from an opponent.\n(your turn only)"
    self.industry = "major"
    self.triggers = [6]

  def activate(self, game: Game, player: Player, dice_roll: int) -> None:
    opponents: list[Player] = list(filter(lambda opponent: opponent is not player, game.players))
    opponent_choices: list[tuple[str, str]] = [(f"{opponent.name} holding {opponent.coins.total} coins", opponent.name) for opponent in opponents]
    chosen_opponent: str = choose(player, opponent_choices, "Choose an opponent to take 5 coins from")
    fetched_chosen_opponent: Player = list(filter(lambda opponent: opponent.name == chosen_opponent, game.players))[0]
    game.bank.handle_transfer(fetched_chosen_opponent, 5, player)

class BusinessCentre(PurpleCard):
  cost = 8
  z_index = 8

  def __init__(self):
    super().__init__()
    self.title = "Business Centre"
    self.description = "Exchange 1 of your non-major establishments for 1 an opponent owns.\n(your turn only)"
    self.industry = "major"
    self.triggers = [6]

  def activate(self, game: Game, player: Player, dice_roll: int) -> None:
    opponents: list[Player] = list(filter(lambda opponent: opponent is not player, game.players))
    # Tell player what cards each opponent has:
    for opponent in opponents:
      unique_cards = set(opponent.cards.blue + opponent.cards.red + opponent.cards.green)
      game.notify(f"Here are the cards that {opponent.name} has")
      print(f"{card.colorize}{card.title} - Qty: {opponent.cards.count(type(card))}{card.reset}" for card in unique_cards)
    opponent_choices: list[tuple[str, str]] = [(f"{opponent.name}", opponent.name) for opponent in opponents]
    opponent_choices.append(('No swap', 'cancel'))

    # Ask player to choose an opponent to take a card from:
    chosen_opponent: str = choose(player, opponent_choices, "Choose an opponent to swap a card with")
    if chosen_opponent == 'cancel':
      game.notify(f"{player.name} has chosen not to swap cards")
      return
    else:
      fetched_chosen_opponent: Player = list(filter(lambda opponent: opponent.name == chosen_opponent, game.players))[0]
      game.notify(f"{player.name} is swapping a card with {fetched_chosen_opponent.name}")
      opponents_cards: list[Union[Blues, Greens, Reds]] = fetched_chosen_opponent.cards.blue + fetched_chosen_opponent.cards.green + fetched_chosen_opponent.cards.red
      opponents_cards.sort
      card_choices: list[tuple[str, str]] = list(map(lambda card: (str(card.title), str(card.title)), opponents_cards))
      card_choices.append(('Cancel swap', 'cancel'))

      # Ask player to choose a card to take from that opponent:
      chosen_card: str = choose(player, card_choices, f"Choose which card to take from {fetched_chosen_opponent.name}")
      if chosen_card == 'cancel':
        game.notify(f"{player.name} has chosen not to swap cards")
        return
      else:
        fetched_chosen_card: Union[Blues, Greens, Reds] = list(filter(lambda card: card.title == chosen_card, opponents_cards))[0]
        game.notify(f"{player.name} has chosen to take a {fetched_chosen_card.title} worth {fetched_chosen_card.cost} coins")
        players_cards: list[Union[Blues, Greens, Reds]] = player.cards.blue + player.cards.green + player.cards.red
        players_cards.sort
        swap_choices: list[tuple[str, str]] = list(map(lambda card: (str(card.title), str(card.title)), players_cards))
        swap_choices.append(('Cancel swap', 'cancel'))

        # Ask player to choose a card to give to that opponent:
        chosen_swap: str = choose(player, swap_choices, f"Choose which card to give to {fetched_chosen_opponent.name} as a swap for their {chosen_card}")
        if chosen_swap == 'cancel':
          game.notify(f"{player.name} has chosen not to swap cards")
          return
        else:
          fetched_chosen_swap: Union[Blues, Greens, Reds] = list(filter(lambda card: card.title == chosen_swap, players_cards))[0]
          game.notify(f"{player.name} has swapped their {chosen_swap} for {fetched_chosen_opponent.name}'s {chosen_card}")

          # Handle swap:
          # From opponent to player:
          opponents_card = fetched_chosen_opponent.cards.remove(fetched_chosen_card.colour, fetched_chosen_card.title)
          player.cards.add(opponents_card)
          # From player to opponent:
          players_card = player.cards.remove(fetched_chosen_swap.colour, fetched_chosen_swap.title)
          fetched_chosen_opponent.cards.add(players_card)

Purples = Union[Stadium, TVStation, BusinessCentre]