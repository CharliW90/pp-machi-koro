from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
  from game import Game
  from player import Player

import time
import inquirer
from reference import MyTheme

def buildAction(game: Game, player:Player, settings: dict) -> bool:
  affordableCards = game.listAffordableCards(player)
  showHand = settings.get("offerToShowHand")
  showDeck = settings.get("offerToShowDeck")
  affordableCards.insert(0,(f"[X] {player.colorize}Build Nothing{player.reset}", "nothing"))
  if showDeck:
    affordableCards.insert(0,(f"[?] {player.colorize}Look at available cards{player.reset}", "display"))
  if showHand:
    affordableCards.insert(0,(f"[?] {player.colorize}Look at your cards{player.reset}", "look"))
  if showDeck and showHand:
    game.notify(f"Time to build an establishment, {player.name}!  You have {player.getBalance()} coins")
  else:
    game.notify(f"Time to make a decision, {player.name}!  You have {player.getBalance()} coins")
  options = [
    inquirer.List('build',
                  message=f"{player.colorize}Build an establishment?{player.reset}",
                  choices=affordableCards)
  ]
  action = inquirer.prompt(options, theme=MyTheme(player))
  choice = action['build'] # type: ignore
  return handleBuilding(game, player, choice, settings)

def handleBuilding(game: Game, player: Player, cardTitle: str, settings: dict) -> bool:
  if cardTitle == 'nothing':
    cash = player.getBalance()
    statement = f" - holding onto their {cash} coins!" if cash > 1 else "."
    player.declareAction(f"{player.name} built nothing this round{statement}")
    time.sleep(1)
    return False
  elif cardTitle == 'look':
    settings["offerToShowHand"] = False
    player.viewHand()
    time.sleep(1)
    return buildAction(game, player, settings)
  elif cardTitle == 'display':
    settings["offerToShowDeck"] = False
    game.displayCardsToPlayer(player)
    time.sleep(1)
    return buildAction(game, player, settings)
  else:
    card = game.takeCardFromStack(cardTitle)
    built = player.build(card, game.bank)
    if not built:
      raise ChildProcessError("Something went wrong when trying to build - sorry!")
    time.sleep(1)
    return built
