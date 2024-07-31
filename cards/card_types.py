from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
  from player import Player
  from game import Game

from reference import reference


class BlueCard:
  colour = "blue"
  colorize = reference["ansi_colours"]["blue"]
  reset = reference["ansi_colours"]["reset"]
  detail = "Blue cards trigger for everyone, on everyone's turn."
  card_type = "Primary"

  def __init__(self) -> None:
    self.triggers = []
    self.title = "A Blue card"
    self.description = "A template for cards that are Primary Industries"

  def __str__(self) -> str:
    return f"{self.colorize}{self.title}{self.reset}\n{self.colorize}{self.description}{self.reset}"

  def trigger(self, game: Game, player: Player, dice_roll: int) -> None:   # These cards trigger for all players
    if dice_roll in self.triggers:   # so we only need to check that the dice_roll is one that triggers this card
      player.declare_action(f"Triggered {self.title} for {player.name}")
      self.activate(game, dice_roll)

  def activate(self, game: Game, dice_roll: int) -> None:
    print(f"This is {'; '.join(str(self).splitlines())}\nit has not been used to create an actual card yet.")
    raise NotImplementedError("This is a template for cards to be built from - the activate function should be implemented on the child Class")

class GreenCard:
  colour = "green"
  colorize = reference["ansi_colours"]["green"]
  reset = reference["ansi_colours"]["reset"]
  detail = "Green cards trigger for the current player only."
  card_type = "Secondary"

  def __init__(self) -> None:
    self.triggers = []
    self.title = "A Green card"
    self.description = "A template for cards that are Secondary Industries"

  def __str__(self) -> str:
    return f"{self.colorize}{self.title}{self.reset}\n{self.colorize}{self.description}{self.reset}"

  def trigger(self, game: Game, player: Player, dice_roll: int) -> None:   # These cards trigger only for the current player
    if player.current and dice_roll in self.triggers:  # so we check that they are, and that the dice_roll is one that triggers this card
      player.declare_action(f"Triggered {self.title} for {player.name}")
      self.activate(game, dice_roll)

  def activate(self, game: Game, dice_roll: int) -> None:
    print(f"This is {'; '.join(str(self).splitlines())}\nit has not been used to create an actual card yet.")
    raise NotImplementedError("This is a template for cards to be built from - the activate function should be implemented on the child Class")

class RedCard:
  colour = "red"
  colorize = reference["ansi_colours"]["red"]
  reset = reference["ansi_colours"]["reset"]
  detail = "Red cards trigger for everyone except the current player."
  card_type = "Restaurant"

  def __init__(self) -> None:
    self.triggers = []
    self.title = "A Red card"
    self.description = "A template for cards that are Restaurants"

  def __str__(self) -> str:
    return f"{self.colorize}{self.title}{self.reset}\n{self.colorize}{self.description}{self.reset}"

  def trigger(self, game: Game, player: Player, dice_roll: int) -> None:   # These cards trigger for everyone except the current player
    if not player.current and dice_roll in self.triggers:  # so we check that they aren't, and that the dice_roll is one that triggers this card
      player.declare_action(f"Triggered {self.title} for {player.name}")
      self.activate(game, dice_roll)

  def activate(self, game: Game, dice_roll: int) -> None:
    print(f"This is {'; '.join(str(self).splitlines())}\nit has not been used to create an actual card yet.")
    raise NotImplementedError("This is a template for cards to be built from - the activate function should be implemented on the child Class")

class PurpleCard:
  colour = "purple"
  colorize = reference["ansi_colours"]["purple"]
  reset = reference["ansi_colours"]["reset"]
  detail = "Purple cards trigger for the current player only."
  card_type = "Major Establishment"

  def __init__(self) -> None:
    self.triggers = []
    self.title = "A Purple card"
    self.description = "A template for cards that are Major Establishments"

  def __str__(self) -> str:
    return f"{self.colorize}{self.title}{self.reset}\n{self.colorize}{self.description}{self.reset}"

  def trigger(self, game: Game, player: Player, dice_roll: int) -> None:   # These cards trigger only for the current player
    if player.current and dice_roll in self.triggers:  # so we check that they are, and that the dice_roll is one that triggers this card
      player.declare_action(f"Triggered {self.title} for {player.name}")
      self.activate(game, dice_roll)

  def activate(self, game: Game, dice_roll: int) -> None:
    print(f"This is {'; '.join(str(self).splitlines())}\nit has not been used to create an actual card yet.")
    raise NotImplementedError("This is a template for cards to be built from - the activate function should be implemented on the child Class")

class LandmarkCard:
  colour = "orange"
  colorize = reference["ansi_colours"]["orange"]
  reset = reference["ansi_colours"]["reset"]
  detail = "Orange cards do not trigger, they grant special abilities.\nBuilding all 4 landmarks achieves victory."
  card_type = "Landmark"

  def __init__(self) -> None:
    self.triggers = []
    self.title = "An Orange card"
    self.description = "A template for cards that are Landmarks"
    self.built = False

  def __str__(self) -> str:
    if self.built:
      return f"{self.colorize}{self.title}{self.reset}\n{self.colorize}{self.description}{self.reset}"
    else:
      return f"{self.colorize}{self.title} (unbuilt) - building this will grant:{self.reset}\n{self.colorize}{self.description}{self.reset}"

  def build(self, player: Player) -> str:
    self.built = True
    player.declare_action(f"{player.name} has built their {self.title}")
    return self.ability()

  def ability(self) -> str:
    return f"This is {self.title} - it has not been used to create an actual card yet."