import random
import inquirer
from reference import MyTheme

def rollDice(game, player):
  doubleDice = player.abilities.doubleDice
  game.notify(f"Time to roll the dice, {player.name}!")
  options = [
    inquirer.List('dice',
                  message=f"{player.colorize}How many dice do you want to roll?{player.reset}",
                  choices=[('One', 1)],
                  ignore=lambda x: doubleDice), # type: ignore | if doubleDice is true, ignore this List
    inquirer.List('dice',
                  message=f"{player.colorize}How many dice do you want to roll?{player.reset}",
                  choices=[('One', 1), ('Two', 2)],
                  ignore=lambda x: not doubleDice), # type: ignore | if doubleDice is false, ignore this List
  ]

  action = inquirer.prompt(options, theme=MyTheme(player))
  player.declareAction(f"{player.name} rolled {action['dice']} dice") # type: ignore
  rolls = []
  for x in range(action['dice']): # type: ignore
    rolls.append(roll())
  for die in rolls:
    player.declareAction(diceFace(die))
  rolled = sum(rolls)
  player.declareAction(f"> {rolled} <")
  handleDiceResult(game, rolled)
  return

def roll():
  return random.randint(1,6)

def diceFace(die):  # credit: https://codegolf.stackexchange.com/a/2603
  r = die-1
  C='o '
  s='-----\n|'+C[r<1]+' '+C[r<3]+'|\n|'+C[r<5]
  return(s+C[r&1]+s[::-1])

def handleDiceResult(game, diceResult):
  for player in game.players:
    player.activate(game, "red", diceResult)
  for player in game.players:
    player.activate(game, "blue", diceResult)
    player.activate(game, "green", diceResult)
  for player in game.players:
    player.activate(game, "purple", diceResult)
  return