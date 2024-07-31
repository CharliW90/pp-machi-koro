from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
  from game import Game
  from player import Player

import random
import inquirer
from reference import MyTheme

def roll_dice(game:Game, player:Player) -> None:
  double_dice = player.abilities.double_dice
  game.notify(f"Time to roll the dice, {player.name}!")
  options = [
    inquirer.List('dice',
                  message=f"{player.colorize}How many dice do you want to roll?{player.reset}",
                  choices=[('One', 1)],
                  ignore=lambda x: double_dice), # type: ignore | if double_dice is true, ignore this List
    inquirer.List('dice',
                  message=f"{player.colorize}How many dice do you want to roll?{player.reset}",
                  choices=[('One', 1), ('Two', 2)],
                  ignore=lambda x: not double_dice), # type: ignore | if double_dice is false, ignore this List
  ]

  action = inquirer.prompt(options, theme=MyTheme(player))
  player.declare_action(f"{player.name} rolled {action['dice']} dice") # type: ignore

  rolls = []
  dice_faces = []
  for _ in range(action['dice']): # type: ignore
    thisRoll = roll()
    rolls.append(thisRoll)
    dice_faces.append(dice_face(thisRoll))
  
  dice_string = "\n".join([f"{line1}  ::  {line2}" for line1, line2 in zip(dice_faces[0].splitlines(), dice_faces[1].splitlines())]) if len(dice_faces) == 2 else dice_faces[0]
  player.declare_action(dice_string)
  rolled = sum(rolls)
  player.declare_action(f"> {rolled} <")
  handle_dice_result(game, rolled)
  return

def roll() -> int:
  return random.randint(1,6)

def dice_face(die: int) -> str:  # credit: https://codegolf.stackexchange.com/a/2603
  r = die-1
  C='o '
  s='-----\n|'+C[r<1]+' '+C[r<3]+'|\n|'+C[r<5]
  return(s+C[r&1]+s[::-1])

def handle_dice_result(game: Game, dice_result: int) -> None:
  for player in game.players:
    if not player.current: player.activate(game, "red", dice_result)
  for player in game.players:
    player.activate(game, "blue", dice_result)
    if player.current: player.activate(game, "green", dice_result)
  for player in game.players:
    if player.current: player.activate(game, "purple", dice_result)
  return