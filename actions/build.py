from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
  from game import Game
  from player import Player

import time
import inquirer
from reference import MyTheme

def build_action(game: Game, player:Player, settings: dict) -> bool:
  affordable_cards = game.list_affordable_cards(player)
  show_hand = settings.get("offer_to_show_hand")
  show_deck = settings.get("offer_to_show_deck")
  affordable_cards.insert(0,(f"[X] {player.colorize}Build Nothing{player.reset}", "nothing"))
  if show_deck:
    affordable_cards.insert(0,(f"[?] {player.colorize}Look at available cards{player.reset}", "display"))
  if show_hand:
    affordable_cards.insert(0,(f"[?] {player.colorize}Look at your cards{player.reset}", "look"))
  if show_deck and show_hand:
    game.notify(f"Time to build an establishment, {player.name}!  You have {player.get_balance()} coins")
  else:
    game.notify(f"Time to make a decision, {player.name}!  You have {player.get_balance()} coins")
  options = [
    inquirer.List('build',
                  message=f"{player.colorize}Build an establishment?{player.reset}",
                  choices=affordable_cards)
  ]
  action = inquirer.prompt(options, theme=MyTheme(player.colour, player.name))
  choice = action['build'] # type: ignore
  return handle_building(game, player, choice, settings)

def handle_building(game: Game, player: Player, card_title: str, settings: dict) -> bool:
  if card_title == 'nothing':
    cash = player.get_balance()
    statement = f" - holding onto their {cash} coins!" if cash > 1 else "."
    player.declare_action(f"{player.name} built nothing this round{statement}")
    time.sleep(1)
    return False
  elif card_title == 'look':
    settings["offer_to_show_hand"] = False
    player.view_hand()
    time.sleep(1)
    return build_action(game, player, settings)
  elif card_title == 'display':
    settings["offer_to_show_deck"] = False
    game.display_cards_to_player(player)
    time.sleep(1)
    return build_action(game, player, settings)
  else:
    card = game.take_card_from_stack(card_title)
    built = player.build(card, game.bank)
    if not built:
      raise ChildProcessError("Something went wrong when trying to build - sorry!")
    time.sleep(1)
    return built
