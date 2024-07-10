import inquirer
from tabulate import tabulate
import random
from reference import reference, shortcuts, MyTheme
from coins.bank import *
from player import Player
from cards.stacks import Deck

class Game:
  def __init__(self, playernames):
    self.name = "Machi Koro!"
    self.playerCount = len(playernames)
    self.players = []
    for i, name in enumerate(playernames):
      self.players.append(Player(name, i))
    self.bank = Bank()
    self.deck = Deck(self.playerCount)
    self.round = 0

  def __repr__(self):
    players = [player.name for player in self.players]
    return f"This is a game of {self.name}.\nIt has {self.playerCount} players - {', '.join(players)}.\nWe are on round {self.round}"

  def displayCardsToPlayer(self, player):
    cash = player.getBalance()
    availableCards = self.deck.contents()
    affordableCards = []

    playersLandmarks = player.cards.landmarks
    for landmark in playersLandmarks:
      availableCards.append([
        f"{landmark.colorize}{landmark.title}{landmark.reset}\n{landmark.colorize}- Permanent Ability{landmark.reset}",
        f"{landmark.colorize}{landmark.description.splitlines()[0]}{landmark.reset}\n{landmark.colorize}(your turn only){landmark.reset}",
        f"{landmark.cost} coin",
        f"Qty: {int(not landmark.built)}",
        ])
    
    for [title, description, cost, qty] in availableCards:
      available = int(qty.split(': ')[1])
      price = int(cost.split(' ')[0])
      if price <= cash and available > 0:
        cardTitle = title.splitlines()[0]
        cleanTitle = repr(cardTitle).split("74m")[1].split("\\")[0] # strip away the ANSI colour codes
        affordableCards.append((f"{cardTitle}: Purchase Price: {cost} - BUY?", cleanTitle))
    
    print(tabulate(availableCards, ["Name", "Action", "Cost", "Remaining"]))
    shortcuts['notify'](f"You have {cash} cash - what would you like to do?")
    return affordableCards

  def start(self):
    if self.playerCount > 4 or self.playerCount < 2:
      raise ValueError("This is a game for 2 to 4 players only!")
    else:
      print(f"Let's play ${self.name}")
      self.deck.initialise()
      self.play()
  
  def play(self):
    playerNum = self.round % self.playerCount
    activePlayer = self.players[playerNum]
    activePlayer.beginTurn()
    takeTurn(self, activePlayer)

    if activePlayer.hasWon():
      shortcuts['notify'](f"{activePlayer.name} has won!  Congratulations!!\n\nThis game of {self.name} took {self.round} rounds to play.")
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
  shortcuts['notify']("Time to roll the dice!")
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

  action = inquirer.prompt(options, theme=MyTheme(player))
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
  affordableCards = game.displayCardsToPlayer(player)
  affordableCards.insert(0,("Build Nothing", "Nothing"))
  
  options = [
    inquirer.List('build',
                  message="Build an establishment?",
                  choices=affordableCards)
  ]

  action = inquirer.prompt(options, theme=MyTheme(player))
  print(action['build'])