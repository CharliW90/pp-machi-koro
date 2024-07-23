from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
  from game import Game
  from coins import Bank

from tabulate import tabulate
from reference import reference
from coins import CoinPiles, Coin, giving, receiving, calcPayment
from cards import Hand, Abilities, Blues, Greens, Reds, Purples, Landmarks

playerColours = ['red','green','blue','purple']
playerNames = []

def reset():
  playerNames.clear()
  return("playerNames reset!")

class Player:
  def __init__(self, name, i):
    self._initialised = False
    self.name = name
    self.colour = i
    self.colorize = self.colour
    self.reset = reference["ansiColours"]["reset"]
    self.current = False
    self.buildActionTaken = False
    self.coins = CoinPiles(0, 0, 0)
    self.cards = Hand()
    self.abilities = Abilities()

  @property
  def name(self):
    return self.__name
  @name.setter
  def name(self, string):
    if self._initialised: raise Exception("Sorry, but you can't edit players")
    if not isinstance(string, (str, int)): raise ValueError(f"Provided names must be plain strings - {string} is a {type(string)}.")
    if len(str(string)) < 1: raise ValueError("Name cannot be blank!")
    if str(string) in playerNames: raise Exception(f"Cannot have duplicate player names - {str(string)} has already been used.\n{playerNames}")
    playerNames.append(str(string))
    self.__name = str(string)

  @property
  def colour(self):
    return self.__colour
  @colour.setter
  def colour(self, i):
    if self._initialised: raise Exception("Sorry, but you can't edit players")
    if i > 3: raise ValueError("Somehow you're trying to generate more players than are allowed in a game - this class should not be called independently of the Game class.")
    self.__colour = playerColours[i]
  
  @property
  def colorize(self):
    return self.__colorize
  @colorize.setter
  def colorize(self, colour):
    if self._initialised: raise Exception("Sorry, but you can't edit players")
    if not colour in playerColours: raise ValueError("Somehow the colour for colorize is not one of the valid player colours")
    self.__colorize = reference["ansiColours"][colour]
  
  def __str__(self) -> str:
    cash = self.coins.total()
    landmarks = 0
    for card in self.cards.landmarks:
      if card.built == True:
        landmarks += 1
    return f"{self.name} has {cash} cash, and has built {landmarks} landmarks"
  
  def declareAction(self, action: str) -> None:
    print(f"{self.colorize}{action}{self.reset}")

  def beginTurn(self) -> None:
    self.current = True
    self.buildActionTaken = False
    self.declareAction(f"It is {self.name}'s turn!")

  def endTurn(self) -> None:
    self.current = False

  def viewHand(self) -> None:
    hand = self.cards.contents()
    print(tabulate(hand, ["Name", "Action", "Owned"]))

  def getBalance(self) -> int:
    return self.coins.total()
  
  def activate(self, game: Game, colour: str, diceRoll) -> None:
    stack = getattr(self.cards, colour)
    for card in stack:
      card.trigger(game, self, diceRoll)

  def receive(self, coins: list[Coin]) -> int:
    return receiving(self, coins)
  
  def give(self, total: int) -> list[Coin]:
    return giving(self, total)
  
  def giveAll(self) -> list[Coin]:
    return giving(self, self.getBalance())
  
  def build(self, card: Blues | Greens | Reds | Purples | Landmarks, bank: Bank) -> bool:
    if self.buildActionTaken:
      print(f"You can only take one build action per turn!")
      return self.buildActionTaken
    else:
      cash = self.coins.total()
      if(card.cardType == "Major Establishment"):
        stack = getattr(self.cards, 'purple')
        for majorEstablishment in stack:
          if majorEstablishment.title == card.title:
            self.declareAction(f"You already have a {card.title} and can only purchase one {card.title} per game.")
            return self.buildActionTaken

      if cash < card.cost:
        print(f"{self.name} cannot afford {card.title}")
        return self.buildActionTaken

      payment = calcPayment(self.coins, card.cost)
      self.receive(bank.takePayment(self.give(payment), card.cost))
      if isinstance(card, Landmarks):
        stack = getattr(self.cards, 'landmarks')
        ability = card.build(self)
        self.abilities.update(ability)
      else:
        self.cards.add(card)

      self.buildActionTaken = True
      self.declareAction(f"{self.name} has purchased {card.title} for {card.cost} cash\n{self}")
      return self.buildActionTaken

  def hasWon(self) -> bool:
    """Checks to see if the player has built all 4 of their landmark cards
    returns False if any are not built, otherwise True"""
    for card in self.cards.landmarks:
      if card.built == False:
        return False
    return True