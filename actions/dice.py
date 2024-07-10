import inquirer
import random
from reference import shortcuts, MyTheme

def rollDice(player):
  doubleDice = player.abilities.doubleDice
  shortcuts['notify'](f"Time to roll the dice, {player.name}!")
  options = [
    inquirer.List('dice',
                  message=f"{player.colorize}How many dice do you want to roll?{player.reset}",
                  choices=[('One', 1)],
                  ignore=lambda x: doubleDice), # if doubleDice is true, ignore this List
    inquirer.List('dice',
                  message=f"{player.colorize}How many dice do you want to roll?{player.reset}",
                  choices=[('One', 1), ('Two', 2)],
                  ignore=lambda x: not doubleDice), # if doubleDice is false, ignore this List
  ]

  action = inquirer.prompt(options, theme=MyTheme(player))
  player.declareAction(f"{player.name} rolled {action['dice']} dice")
  rolls = []
  for x in range(action['dice']):
    rolls.append(roll())
  for die in rolls:
    player.declareAction(diceFace(die))
  rolled = sum(rolls)
  player.declareAction(f"> {rolled} <")
  return rolled

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