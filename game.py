from tabulate import tabulate
from reference import shortcuts
from coins.bank import *
from player import Player
from cards.stacks import Deck
from actions.dice import rollDice, handleDiceResult
from actions.build import buildAction, handleBuilding

class Game:
  def __init__(self, playernames, rounds = None):
    self.name = "Machi Koro!"
    self.playerCount = len(playernames)
    self.players = []
    for i, name in enumerate(playernames):
      self.players.append(Player(name, i))
    self.bank = Bank()
    self.deck = Deck(self.playerCount)
    self.round = 0
    self.limitRounds = rounds

  def __str__(self):
    players = [player.name for player in self.players]
    return f"This is a game of {self.name}.\nIt has {self.playerCount} players - {', '.join(players)}.\nWe are on round {self.round}"

  def notify(self, str):
    if "\n" in str:
      lines = str.splitlines()
      for line in lines:
        print(f"{shortcuts['notificationStart']}{line}{shortcuts['notificationEnd']}")
    else:
      print(f"{shortcuts['notificationStart']}{str}{shortcuts['notificationEnd']}")

  def listAffordableCards(self, player):
    availableCards = self.deck.contents()
    affordableCards = []
    playersLandmarks = player.cards.landmarks
    for landmark in playersLandmarks:
      style = "\x1b[9;2m" if landmark.cost > player.getBalance() else "\x1b[3;32m"
      reset = "\x1b[0m"
      availableCards.append([
        f"{landmark.colorize}{landmark.title}{landmark.reset}\n{landmark.colorize}- Permanent Ability{landmark.reset}",
        f"{landmark.colorize}{landmark.description.splitlines()[0]}{landmark.reset}\n{landmark.colorize}(your turn only){landmark.reset}",
        f"{landmark.colorize}{landmark.title}{landmark.reset}\n{style}{landmark.cost} coins{reset}",
        f"Qty: {int(not landmark.built)}",
        ])
    for [title, description, cost, qty] in availableCards:
      available = int(qty.split(': ')[1])
      price = int(repr(cost).split("2m")[1].split(' ')[0])
      if price <= player.getBalance() and available > 0:
        cardTitle = title.splitlines()[0]
        cleanTitle = repr(cardTitle).split("74m")[1].split("\\")[0] # strip away the ANSI colour codes
        affordableCards.append((f"{cardTitle}: Purchase Price: {cost} - BUY?", cleanTitle))
    return affordableCards

  def displayCardsToPlayer(self, player):
    availableCards = self.deck.contents(player.getBalance())
    playersLandmarks = player.cards.landmarks
    for landmark in playersLandmarks:
      style = "\x1b[9;2m" if landmark.cost > player.getBalance() else "\x1b[3;32m"
      reset = "\x1b[0m"
      availableCards.append([
        f"{landmark.colorize}{landmark.title}{landmark.reset}\n{landmark.colorize}- Permanent Ability{landmark.reset}",
        f"{landmark.colorize}{landmark.description.splitlines()[0]}{landmark.reset}\n{landmark.colorize}(your turn only){landmark.reset}",
        f"{style}{landmark.cost} coins{reset}",
        f"Qty: {int(not landmark.built)}",
        ])
    print(tabulate(availableCards, ["Name", "Action", "Cost", "Remaining"]))
    return

  def takeCardFromStack(self, cardTitle):
    card, pile, qty = self.deck.remove(cardTitle)
    self.notify(f"Took a {card.title} from the {pile} pile - there are now {qty} cards remaining in this pile")
    return card

  def start(self):
    if self.playerCount > 4 or self.playerCount < 2:
      raise ValueError("This is a game for 2 to 4 players only!")
    else:
      print(f"Let's play ${self.name}")
      self.deck.initialise()
      self.play()
  
  def play(self):
    self.bank.check(self)
    playerNum = self.round % self.playerCount
    activePlayer = self.players[playerNum]
    self.round += 1
    activePlayer.beginTurn()
    takeTurn(self, activePlayer)

    if activePlayer.hasWon():
      self.notify(f"{activePlayer.name} has won!  Congratulations!!\n\nThis game of {self.name} took {self.round} rounds to play.")
      return
    else:
      activePlayer.endTurn()
      if self.limitRounds:
        if self.round < self.limitRounds:
          self.notify(f"This is round {self.round + 1} of {self.limitRounds}")
          return self.play()
        else:
          self.notify(f"You have reached the limit of {self.limitRounds} rounds.  Game over.")
          return
      else:
        return self.play()

def takeTurn(game, player):
  rollDice(game, player)
  buildAction(game, player, {'offerToShowHand': True, 'offerToShowDeck': True})
  return