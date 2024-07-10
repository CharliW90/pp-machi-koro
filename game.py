import inquirer
from tabulate import tabulate
import random
from reference import reference
from coins.bank import *
from player import Player
from cards.stacks import Deck

class Game:
  def __init__(self, playernames):
    self.name = "Machi Koro!"
    self.playerCount = len(playernames)
    self.players = []
    for name in playernames:
      self.players.append(Player(name))
    self.bank = Bank()
    self.deck = Deck(self.playerCount)
    self.round = 0

  def __repr__(self):
    players = [player.name for player in self.players]
    return f"This is a game of {self.name}.\nIt has {self.playerCount} players - {', '.join(players)}.\nWe are on round {self.round}"

  def displayCards(self, cash):
    affordableCards = []
    cards = self.deck.contents()
    print(tabulate(cards, ["Name", "Action", "Cost", "Remaining"]))
    for [title, description, cost, qty] in self.deck.contents():
      if cost <= cash:
        affordableCards.append((title, f"Purchase Price: {cost} - BUY?"))
    return affordableCards

  def start(self):
    if self.playerCount > 4 or self.playerCount < 2:
      raise ValueError("This is a game for 2 to 4 players only!")
    else:
      print(f"Let's play ${self.name}")
      self.deck.initialise()
      self.play()
  
  def play(self):
    print(reference)
    playerNum = self.round % self.playerCount
    activePlayer = self.players[playerNum]
    activePlayer.beginTurn()
    takeTurn(self, activePlayer)

    if activePlayer.hasWon():
      print(f"{activePlayer.name} has won!  Congratulations!!\n\nThis game of {self.name} took {self.round} rounds to play.")
      return
    else:
      activePlayer.endTurn()
      self.round += 1
      if self.round < 5:
        return self.play()
      else:
        print("5 rounds completed")

def takeTurn(game, player):
  diceResult = rollDice(player)
  handleDiceResult(game, diceResult)
  building = buildAction(game, player)

def handleDiceResult(game, diceResult):
  for player in game.players:
    player.activate(game, "red", diceResult)
  for player in game.players:
    player.activate(game, "blue", diceResult)
    player.activate(game, "green", diceResult)
  for player in game.players:
    player.activate(game, "purple", diceResult)

def rollDice(player):
  doubleDice = player.abilities.doubleDice
  print(f"What would you like to do?")
  options = [
    inquirer.List('dice',
                  message="How many dice do you want to roll?",
                  choices=[('One', 1)],
                  ignore=lambda x: doubleDice), # if doubleDice is true, ignore this List
    inquirer.List('dice',
                  message="How many dice do you want to roll?",
                  choices=[('One', 1), ('Two', 2)],
                  ignore=lambda x: not doubleDice), # if doubleDice is false, ignore this List
  ]

  action = inquirer.prompt(options)
  print(f"{player.name} rolled {action['dice']} dice")
  rolls = []
  for x in range(action['dice']):
    rolls.append(roll())
  for die in rolls:
    diceFace(die)
  rolled = sum(rolls)
  print(f"> {rolled} <")
  return rolled

def roll():
  return random.randint(1,6)

def diceFace(die):  # credit: https://codegolf.stackexchange.com/a/2603
  r = die-1
  C='o '
  s='-----\n|'+C[r<1]+' '+C[r<3]+'|\n|'+C[r<5]
  print(s+C[r&1]+s[::-1])

def buildAction(game, player):
  cash = player.getBalance()
  print(f"You have {cash} cash - what would you like to do?")
  options = game.displayCards(cash)
  print(options) # inquirer list of options from these