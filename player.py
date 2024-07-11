import time
from tabulate import tabulate
from reference import reference
from coins.transactions import *
from coins.coinage import CoinPiles
from cards.stacks import Hand, Abilities

playerColours = ['red','green','blue','purple']
playerNames = []

def reset():
  print("Resetting playerNames...")
  playerNames.clear()
  return("playerNames reset!")

class Player:
  def __init__(self, name, i):
    self.name = name
    self.colour = i
    self.colorize = self.colour
    self.reset = reference["ansiColours"]["reset"]
    self.current = False
    self.buildActionTaken = False
    self.coins = CoinPiles(0, 0, 0)
    self.cards = Hand()
    self.abilities = Abilities()
    self._initialised = False

  @property
  def name(self):
    return self.__name
  @name.setter
  def name(self, string):
    if self._initialised: raise Exception("Sorry, but you can't edit players")
    if not isinstance(string, (str, int)): raise ValueError(f"Provided names must be plain strings - {string} is a {type(string)}.")
    if len(str(string)) < 1: raise ValueError("Name cannot be blank!")
    if str(string) in playerNames: raise Exception(f"Cannot have duplicate player names - {str(string)} has already been used.")
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
  
  def __str__(self):
    cash = self.coins.total()
    landmarks = 0
    for card in self.cards.landmarks:
      if card.built == True:
        landmarks += 1
    return f"{self.name} has {cash} cash, and has built {landmarks} landmarks"
  
  def declareAction(self, str):
    time.sleep(0.2)
    print(f"{self.colorize}{str}{self.reset}")

  def beginTurn(self):
    self.current = True
    self.buildActionTaken = False
    self.declareAction(f"It is {self.name}'s turn!")

  def endTurn(self):
    self.current = False

  def viewHand(self):
    hand = self.cards.contents()
    print(tabulate(hand, ["Name", "Action", "Owned"]))

  def getBalance(self):
    return self.coins.total()
  
  def activate(self, game, colour, diceRoll):
    stack = getattr(self.cards, colour)
    for card in stack:
      card.trigger(self, diceRoll)

  def receive(self, coins):
    return receiving(self, coins)
  
  def give(self, total):
    return giving(self, total)
  
  def giveAll(self):
    return giving(self, self.getBalance())
  
  def build(self, card, bank):
    if self.buildActionTaken:
      print(f"You can only take one build action per turn!")
    else:
      cash = self.coins.total()
      if(card.type == "Major Establishment"):
        stack = getattr(self.cards, 'purple')
        for majorEstablishment in stack:
          if majorEstablishment.title == card.title:
            self.declareAction(f"You already have a {card.title} and can only purchase one {card.title} per game.")
      elif cash >= card.cost:
        payment = calcPayment(self.coins, card.cost)
        self.receive(bank.takePayment(self.give(payment), card.cost))
        if card.type == "Landmark":
          stack = getattr(self.cards, 'landmarks')
          ability = card.build()
          self.abilities.update(ability)
        else:
          self.cards.add(card)
        self.buildActionTaken = True
        self.declareAction(f"{self.name} has purchased {card.title} for {card.cost} cash\n{self}")
      else:
        print(f"{self.name} cannot afford {card.title}")

    return self.buildActionTaken

  def hasWon(self):
    for card in self.cards.landmarks:
      if card.built == False:
        return False
    return True