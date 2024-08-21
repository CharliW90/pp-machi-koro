from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
  from game import Game
  from coins import Bank

from tabulate import tabulate
from reference import reference
from coins import CoinPiles, Coin, giving, receiving, calculate_payment
from cards import Hand, Abilities, Blues, Greens, Reds, Purples, Landmarks

player_colours = ['red','green','blue','purple']
player_names = []

def reset():
  player_names.clear()
  return("playerNames reset!")

class Player:
  def __init__(self, name: str, i: int):
    self.initialised = False
    self.name = name
    self.colour = i
    self.colorize = self.colour
    self.turn_order = 0
    self.reset: str = reference["ansi_colours"]["reset"]
    self.current: bool = False
    self.build_action_taken: bool = False
    self.coins: CoinPiles = CoinPiles(0, 0, 0)
    self.cards: Hand = Hand()
    self.abilities: Abilities = Abilities()

  @property
  def initialised(self) -> bool:
    return self.__initialised
  @initialised.setter
  def initialised(self, trigger: bool):
    if hasattr(self, "initialised"):
      if self.initialised: raise Exception("Player already initialised - cannot initialise again.")
    self.__initialised = trigger

  @property
  def name(self) -> str:
    return self.__name
  @name.setter
  def name(self, string: str):
    if self.initialised: raise Exception("Sorry, but you can't edit players")
    if not isinstance(string, str): raise ValueError(f"Provided names must be plain strings - {string} is a {type(string).__name__}.")
    string = string.strip()
    if len(string) < 1: raise ValueError("Name cannot be blank!")
    if len(string) > 48: raise ValueError("Name too long - max length 48 characters!")
    if '\\' in repr(string): raise ValueError("Name cannot contain escape characters!")
    if string in player_names: raise Exception(f"Cannot have duplicate player names - '{string}' has already been used.\n{player_names}")
    player_names.append(string)
    self.__name = string

  @property
  def colour(self) -> str:
    return self.__colour
  @colour.setter
  def colour(self, i: int):
    if self.initialised: raise Exception("Sorry, but you can't edit players")
    if not isinstance(i, int) or isinstance(i, bool): raise ValueError(f"Provided number must be integer - {i} is a {type(i).__name__}.")
    if 0 > i or i > 3: raise ValueError(f"Attempting to set colour based on int {i} is not possible - int must be between 0 and {len(player_colours)-1}")
    self.__colour = player_colours[i]
  
  @property
  def colorize(self) -> str:
    return self.__colorize
  @colorize.setter
  def colorize(self, colour: str):
    if self.initialised: raise Exception("Sorry, but you can't edit players")
    if not isinstance(colour, str): raise ValueError(f"Provided colour must be plain string - {colour} is a {type(colour).__name__}.")
    if not colour in player_colours: raise ValueError("Somehow the colour for colorize is not one of the valid player colours")
    self.__colorize = reference["ansi_colours"][colour]

  @property
  def turn_order(self):
    return self.__turn_order
  @turn_order.setter
  def turn_order(self, order: int):
    if self.initialised: raise Exception("Sorry, but you can't edit players")
    if not isinstance(order, int) or isinstance(order, bool): raise ValueError(f"Provided number must be integer - {order} is a {type(order).__name__}.")
    if 0 <= order < len(player_names):
      self.__turn_order = order
    else:
      raise ValueError(f"Cannot assign {order} as a turn order - in a game of {len(player_names)} players possible turn orders are {' / '.join([str(num) for num in range(len(player_names))])}.")
  
  def __str__(self) -> str:
    return f"Player {self.turn_order + 1}: {self.name}"

  def __repr__(self) -> str:
    cash = self.coins.total()
    landmarks = sum(card.built for card in self.cards.landmarks)
    return f"{self.name} has {cash} cash remaining and has built {landmarks} landmarks"
  
  def __eq__(self, other: Player) -> bool:
    if not isinstance(other, Player): raise TypeError(f"Cannot compare Player with {type(other).__name__}.  Player class objects may only be compared with other Player class objects.")
    return self.name == other.name
  
  def __ne__(self, other: Player) -> bool:
    if not isinstance(other, Player): raise TypeError(f"Cannot compare Player with {type(other).__name__}.  Player class objects may only be compared with other Player class objects.")
    return self.name != other.name

  # The below are defined as what may be considered as the opposite of expected,
  # however a 'less than' turn order should be considered a 'greater than' player
  # i.e. player 1 should be greater than player 2, so 1 > 2 is our logic
  def __lt__(self, other: Player) -> bool:
    if not isinstance(other, Player): raise TypeError(f"Cannot compare Player with {type(other).__name__}.  Player class objects may only be compared with other Player class objects.")
    return self.turn_order > other.turn_order
  
  def __gt__(self, other: Player) -> bool:
    if not isinstance(other, Player): raise TypeError(f"Cannot compare Player with {type(other).__name__}.  Player class objects may only be compared with other Player class objects.")
    return self.turn_order < other.turn_order
  
  def __le__(self, other: Player) -> bool:
    if not isinstance(other, Player): raise TypeError(f"Cannot compare Player with {type(other).__name__}.  Player class objects may only be compared with other Player class objects.")
    return self.turn_order >= other.turn_order
  
  def __ge__(self, other: Player) -> bool:
    if not isinstance(other, Player): raise TypeError(f"Cannot compare Player with {type(other).__name__}.  Player class objects may only be compared with other Player class objects.")
    return self.turn_order <= other.turn_order
  
  def declare_action(self, action: str) -> None:
    for line in action.splitlines():
      print(f"{self.colorize}{line}{self.reset}")

  def begin_turn(self) -> None:
    self.current = True
    self.build_action_taken = False
    self.declare_action(f"It is {self.name}'s turn!")

  def end_turn(self) -> None:
    self.current = False

  def view_hand(self) -> None:
    hand = self.cards.contents()
    print(tabulate(hand, ["Name", "Action", "Owned"]))

  def get_balance(self) -> int:
    return self.coins.total()
  
  def activate(self, game: Game, colour: str, dice_roll) -> None:
    stack = getattr(self.cards, colour)
    for card in stack:
      card.trigger(game, self, dice_roll)

  def receive(self, coins: list[Coin], silent=False) -> int:
    return receiving(self, coins, silent)
  
  def give(self, total: int, silent=False) -> list[Coin]:
    return giving(self, total, silent)
  
  def give_all(self, silent=False) -> list[Coin]:
    return giving(self, self.get_balance(), silent)
  
  def build(self, card: Blues | Greens | Reds | Purples | Landmarks, bank: Bank) -> bool:
    if self.build_action_taken:
      print(f"You can only take one build action per turn!")
      return self.build_action_taken
    else:
      cash = self.coins.total()
      if(card.card_type == "Major Establishment"):
        stack = getattr(self.cards, 'purple')
        for major_establishment in stack:
          if major_establishment.title == card.title:
            self.declare_action(f"You already have a {card.title} and can only purchase one {card.title} per game.")
            return self.build_action_taken

      if cash < card.cost:
        print(f"{self.name} cannot afford {card.title}")
        return self.build_action_taken
      payment = calculate_payment(self.coins, card.cost)
      self.receive(bank.take_payment(self.give(payment), card.cost))
      if isinstance(card, Landmarks):
        stack = getattr(self.cards, 'landmarks')
        ability = card.build(self)
        self.abilities.update(ability)
      else:
        self.cards.add(card)

      self.build_action_taken = True
      self.declare_action(f"{self.name} has purchased {card.title} for {card.cost} cash\n{repr(self)}")
      return self.build_action_taken

  def has_won(self) -> bool:
    """Checks to see if the player has built all 4 of their landmark cards
    returns False if any are not built, otherwise True"""
    for card in self.cards.landmarks:
      if card.built == False:
        return False
    return True