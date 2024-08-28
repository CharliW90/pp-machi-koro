from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
  from player import Player
  from game import Game

import time
from actions.dice import roll, dice_face

def determine_player_one(players: list[Player], game: Game) -> Player:
  player_dict: dict[str, Player] = {player.name: player for player in players}
  player_rolls: list[dict] = []
  for player in players:
    first_roll = roll()
    player.declare_action(dice_face(first_roll))
    print() # Insert blank line to console
    time.sleep(0.2)
    player.declare_action(f"{player.name} rolled {first_roll}")
    print() # Insert blank line to console
    player_rolls.append({"name": player.name, "roll": first_roll})
    time.sleep(0.5)

  sorted_players = sorted(player_rolls, key=lambda player_roll: player_roll['roll'], reverse=True)
  highest_roll = sorted_players[0]['roll']
  if sorted_players[0]['roll'] > sorted_players[1]['roll']:
    player_one = sorted_players[0]['name']
    game.notify(f"{player_one} rolled a {highest_roll} and will go first!")
    time.sleep(0.5)
    return player_dict[player_one]
  else:
    roll_again = []
    for player_roll in sorted_players:
      if player_roll['roll'] == highest_roll:
        for player in players:
          if player.name == player_roll['name']:
            roll_again.append(player)
    names = [player.name for player in roll_again]
    print(f"Players {' and '.join(names)} rolled a {highest_roll} and need to roll again!")
    time.sleep(0.5)
    return determine_player_one(roll_again, game)
  
def set_turn_orders(all_players: list[Player], player_one: Player) -> None:
  if player_one not in all_players:
    raise ValueError("Cannot set the turn orders based on a player who is not in the group of players.")
  
  index = all_players.index(player_one)
  for i, player in enumerate(all_players):
    player.turn_order = (i + len(all_players) - index) % len(all_players)