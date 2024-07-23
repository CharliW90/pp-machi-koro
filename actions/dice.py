from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
  from game import Game
  from player import Player

import random
import inquirer
from reference import MyTheme

def rollDice(game:Game, player:Player) -> None:
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
  diceFaces = []
  for x in range(action['dice']): # type: ignore
    thisRoll = roll()
    rolls.append(thisRoll)
    diceFaces.append(diceFace(thisRoll))
  
  diceString = "\n".join([f"{line1}  ::  {line2}" for line1, line2 in zip(diceFaces[0].splitlines(), diceFaces[1].splitlines())]) if len(diceFaces) == 2 else diceFaces[0]
  player.declareAction(diceString)
  rolled = sum(rolls)
  player.declareAction(f"> {rolled} <")
  handleDiceResult(game, rolled)
  return

def roll() -> int:
  return random.randint(1,6)

def diceFace(die: int) -> str:  # credit: https://codegolf.stackexchange.com/a/2603
  r = die-1
  C='o '
  s='-----\n|'+C[r<1]+' '+C[r<3]+'|\n|'+C[r<5]
  return(s+C[r&1]+s[::-1])

def handleDiceResult(game: Game, diceResult: int) -> None:
  for player in game.players:
    if not player.current: player.activate(game, "red", diceResult)
  for player in game.players:
    player.activate(game, "blue", diceResult)
    if player.current: player.activate(game, "green", diceResult)
  for player in game.players:
    if player.current: player.activate(game, "purple", diceResult)
  return