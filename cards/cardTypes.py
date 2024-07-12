import time
from typing import Union
from reference import reference

class BlueCard:
  colour = "blue"
  colorize = reference["ansiColours"]["blue"]
  reset = reference["ansiColours"]["reset"]
  detail = "Blue cards trigger for everyone, on everyone's turn."
  cardType = "Primary"

  def __init__(self):
    self.triggers = []
    self.title = "A Blue card"
    self.description = "A template for cards that are Primary Industries"

  def __str__(self):
    return f"{self.colorize}{self.title}{self.reset}\n{self.colorize}{self.description}{self.reset}"
  
  def trigger(self, player, diceRoll):  # These cards trigger for all players
    if diceRoll in self.triggers:       # so we only need to check that the diceRoll is one that triggers this card
      player.declareAction(f"Triggered {self.title} for {player.name}")
      time.sleep(0.5)
      self.activate(diceRoll)

  def activate(self, diceRoll):
    print(f"This is {'; '.join(str(self).splitlines())}\nit has not been used to build an actual card yet.")

class GreenCard:
  colour = "green"
  colorize = reference["ansiColours"]["green"]
  reset = reference["ansiColours"]["reset"]
  detail = "Green cards trigger for the current player only."
  cardType = "Secondary"

  def __init__(self):
    self.triggers = []
    self.title = "A Green card"
    self.description = "A template for cards that are Secondary Industries"

  def __str__(self):
    return f"{self.colorize}{self.title}\n{self.description}{self.reset}"
  
  def trigger(self, player, diceRoll):                # These cards trigger only for the current player
    if player.current and diceRoll in self.triggers:  # so we check that they are, and that the diceRoll is one that triggers this card
      player.declareAction(f"Triggered {self.title} for {player.name}")
      time.sleep(0.5)
      self.activate(diceRoll)

  def activate(self, diceRoll):
    print(f"This is {self}\nit has not been used to build an actual card yet.")

class RedCard:
  colour = "red"
  colorize = reference["ansiColours"]["red"]
  reset = reference["ansiColours"]["reset"]
  detail = "Red Cards trigger for everyone except the current player."
  cardType = "Restaurant"

  def __init__(self):
    self.triggers = []
    self.title = "A Red card"
    self.description = "A template for cards that are Restaurants"

  def __str__(self):
    return f"{self.colorize}{self.title}\n{self.description}{self.reset}"

  def trigger(self, player, diceRoll):                    # These cards trigger for everyone except the current player
    if not player.current and diceRoll in self.triggers:  # so we check that they aren't, and that the diceRoll is one that triggers this card
      player.declareAction(f"Triggered {self.title} for {player.name}")
      time.sleep(0.5)
      self.activate(diceRoll)

  def activate(self, diceRoll):
    print(f"This is {self}\nit has not been used to build an actual card yet.")

class PurpleCard:
  colour = "purple"
  colorize = reference["ansiColours"]["purple"]
  reset = reference["ansiColours"]["reset"]
  detail = "Purple cards trigger for the current player only."
  cardType = "Major Establishment"

  def __init__(self):
    self.triggers = []
    self.title = "A Purple card"
    self.description = "A template for cards that are Major Establishments"

  def __str__(self):
    return f"{self.colorize}{self.title} + '\n' + {self.description}{self.reset}"

  def trigger(self, player, diceRoll):                # These cards trigger only for the current player
    if player.current and diceRoll in self.triggers:  # so we check that they are, and that the diceRoll is one that triggers this card
      player.declareAction(f"Triggered {self.title} for {player.name}")
      time.sleep(0.5)
      self.activate(diceRoll)

  def activate(self, diceRoll):
    print(f"This is {self}\nit has not been used to build an actual card yet.")

class LandmarkCard:
  colour = "orange"
  colorize = reference["ansiColours"]["orange"]
  reset = reference["ansiColours"]["reset"]
  detail = "Orange cards do not trigger, they grant special abilities.\nBuilding all 4 landmarks achieves victory."
  cardType = "Landmark"

  def __init__(self):
    self.triggers = []
    self.title = "An Orange card"
    self.description = "A template for cards that are Landmarks"
    self.built = False

  def __str__(self):
    if self.built:
      return f"{self.title}\n{self.description}"
    else:
      return f"An unbuilt {self.title} - building this will grant:\n{self.description}"
    
  def ability(self):
    print(f"This is {self}\nit has not been used to build an actual card yet.")

  def build(self, player):
    self.built = True
    player.declareAction(f"{player.name} has built their {self.title}")
    return self.ability()