import time
from tabulate import tabulate
from reference import shortcuts
from coins.bank import Bank
from player import Player, reset as resetPlayers
from cards.stacks import Deck
from actions.dice import rollDice
from actions.build import buildAction

class Game:
  name = "Machi Koro"

  def __init__(self, playernames, rounds = None):
    self.players = playernames
    self.playerCount = playernames
    self.limitRounds = rounds
    self._initialised = True
    self.bank = Bank()
    self.deck = Deck()
    self.round = 0
    self._initialised = False
    self._inProgress = False

  @property
  def players(self):
    return self.__players
  @players.setter
  def players(self, names):
    if self._initialised: raise Exception("Sorry, but you can't edit games")
    if not isinstance(names, list): raise ValueError(f"Player names must be provided as a List - {names} is a {type(names)}")
    if not 2 <= len(names) <= 4: raise ValueError(f"This is a game for 2 to 4 players only!  You have requested {len(names)} players.")
    generatedPlayers = []
    for i, name in enumerate(names):
      if not isinstance(name, (str, int)): raise ValueError(f"Provided names must be plain strings - {name} is a {type(name)}.")
      generatedPlayers.append(Player(str(name), i))
    self.__players = generatedPlayers
  
  @property
  def playerCount(self):
    return self.__playerCount
  @playerCount.setter
  def playerCount(self, names):
    if self._initialised: raise Exception("Sorry, but you can't edit games")
    if not 2 <= len(names) <= 4: raise ValueError(f"This is a game for 2 to 4 players only!  You have requested {len(names)} players.")
    self.__playerCount = len(names)

  @property
  def rounds(self):
    return self.__rounds
  @rounds.setter
  def rounds(self, value):
    if self._initialised: raise Exception("Sorry, but you can't edit games")
    if value > 100: raise ValueError(f"{value} rounds is too high - if you don't want to limit the number of rounds playable, simply omit this parameter.")
    self.__rounds = value
  
  def __str__(self):
    players = []
    for player in self.players:
      players.append(f"{player.colorize}{player.name}{player.reset}")
    return f"This is a game of {self.name}!\nIt has {self.playerCount} players - {', '.join(players)}.\nWe are on round {self.round}"

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
    self.inProgress = True
    self.deck.generate(self)
    self.notify(f"{self}")
    time.sleep(0.5)
    for player in self.players:
      player.receive(self.bank.givePlayer(3))
      time.sleep(0.2)
    time.sleep(0.5)
    self.play()
  
  def play(self):
    self.bank.check(self)
    playerNum = self.round % self.playerCount
    activePlayer = self.players[playerNum]
    self.round += 1
    activePlayer.beginTurn()
    time.sleep(1)
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

  def endGame(self):
    self.notify("Ending game...")
    self.notify(resetPlayers())

def takeTurn(game, player):
  rollDice(game, player)
  time.sleep(1)
  buildAction(game, player, {'offerToShowHand': True, 'offerToShowDeck': True})
  time.sleep(1)
  return