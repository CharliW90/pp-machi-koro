from coins.transactions import *
from coins.coinage import CoinPiles
from cards.stacks import Hand, Abilities

class Player:
  def __init__(self, name):
    self.name = name
    self.current = False
    self.buildActionTaken = False
    self.coins = CoinPiles(3, 0, 0)
    self.cards = Hand()
    self.abilities = Abilities()
  
  def __repr__(self):
    cash = self.coins.total()
    landmarks = 0
    for card in self.cards.landmarks:
      if card.built == True:
        landmarks += 1
    return f"{self.name} has {cash} cash, and has built {landmarks} landmarks"

  def beginTurn(self):
    self.current = True
    print(f"It is {self.name}'s turn!")

  def endTurn(self):
    self.current = False

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
  
  def build(self, card, bank):
    if self.buildActionTaken:
      print(f"You can only take one build action per turn!")
      return
    if(card.type == "Major Establishment"):
      for majorEstablishment in self.cards.majorEstablishments:
        if majorEstablishment.title == card.title:
          print(f"You already have a {card.title} and can only purchase one {card.title} per game.")
          return
    cash = self.coins.total()
    if cash >= card.cost:
      print(f"{self.name} can afford {card.title}")
      payment = calcPayment(self.coins, card.cost)
      self.receive(bank.takePayment(self.give(payment), card.cost))
      if card.type == "Landmark":
        self.abilities.update(card.build())
      else:
        self.cards.add(card)
      self.buildActionTaken = True
      print(f"{self.name} has purchased {card.title} for {card.cost} cash\n{self}")
    else:
      print(f"{self.name} cannot afford {card.title}")
      return card

  def hasWon(self):
    for card in self.cards.landmarks:
      if card.built == False:
        return False
    return True