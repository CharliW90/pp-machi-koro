from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
  from player import Player

from typing import Union
import inquirer
from reference import MyTheme

def choose(player: Player, ask_choices: list[tuple[str, str]], ask_message: str) -> str:
  options = [inquirer.List('choice', message=ask_message, choices=ask_choices,)]
  choice = inquirer.prompt(options, theme=MyTheme(player.colour, player.name))
  return choice['choice'] # type: ignore