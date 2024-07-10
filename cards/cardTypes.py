from reference import reference

class BlueCard:
  def __init__(self):
    self.colour = "blue"
    self.colorize = reference["ansiColours"][self.colour]
    self.reset = reference["ansiColours"]["reset"]
    self.detail = "Blue cards trigger for everyone, on everyone's turn.\nThey are the second card type to be processed."
    self.type = "Primary"
    self.order = 1
    self.triggers = []
    self.title = f"A {self.colour} card"
    self.description = f"A template for {self.type} cards"

  def __repr__(self):
    return f"{self.colorize}{self.title} + '\n\n' + {self.description}{self.reset}"

  def activate(self, diceRoll):
    print(f"This is {self}\n\nit has not been used to build an actual card yet.")
  
  def trigger(self, player, diceRoll):
    if diceRoll in self.triggers:
      print(f"Triggered {self.title} for {player.name}")
      self.activate(diceRoll)

class GreenCard:
  def __init__(self):
    self.colour = "green"
    self.colorize = reference["ansiColours"][self.colour]
    self.reset = reference["ansiColours"]["reset"]
    self.detail = "Green cards trigger for the current player only.\nThey are the third card type to be processed."
    self.type = "Secondary"
    self.order = 2
    self.triggers = []
    self.title = f"A {self.colour} card"
    self.description = f"A template for {self.type} cards"

  def __repr__(self):
    return f"{self.colorize}{self.title} + '\n\n' + {self.description}{self.reset}"

  def activate(self, diceRoll):
    print(f"This is {self}\n\nit has not been used to build an actual card yet.")
  
  def trigger(self, player, diceRoll):
    if player.current and diceRoll in self.triggers:
      print(f"Triggered {self.title} for {player.name}")
      self.activate(diceRoll)

class RedCard:
  def __init__(self):
    self.colour = "red"
    self.colorize = reference["ansiColours"][self.colour]
    self.reset = reference["ansiColours"]["reset"]
    self.detail = "Red Cards trigger for everyone except the current player.\nThey are the first card type to be processed."
    self.type = "Restaurant"
    self.order = 0
    self.triggers = []
    self.title = f"A {self.colour} card"
    self.description = f"A template for {self.type} cards"

  def __repr__(self):
    return f"{self.colorize}{self.title} + '\n\n' + {self.description}{self.reset}"

  def activate(self, diceRoll):
    print(f"This is {self}\n\nit has not been used to build an actual card yet.")

  def trigger(self, player, diceRoll):
    if not player.current and diceRoll in self.triggers:
      print(f"Triggered {self.title} for {player.name}")
      self.activate(diceRoll)

class PurpleCard:
  def __init__(self):
    self.colour = "purple"
    self.colorize = reference["ansiColours"][self.colour]
    self.reset = reference["ansiColours"]["reset"]
    self.detail = "Purple cards trigger for the current player only.\nThey are the last card type to be processed."
    self.type = "Major Establishment"
    self.order = 3
    self.triggers = [6]
    self.title = f"A {self.colour} card"
    self.description = f"A template for {self.type} cards"

  def __repr__(self):
    return f"{self.colorize}{self.title} + '\n\n' + {self.description}{self.reset}"

  def activate(self, diceRoll):
    print(f"This is {self}\n\nit has not been used to build an actual card yet.")

  def trigger(self, player, diceRoll):
    if player.current and diceRoll in self.triggers:
      print(f"Triggered {self.title} for {player.name}")
      self.activate(diceRoll)

class LandmarkCard:
  def __init__(self):
    self.colour = "orange"
    self.colorize = reference["ansiColours"][self.colour]
    self.reset = reference["ansiColours"]["reset"]
    self.detail = "Orange cards do not trigger, they grant special abilities.\nBuilding all 4 landmarks achieves victory."
    self.type = "Landmark"
    self.triggers = []
    self.title = f"A {self.colour} card"
    self.description = f"A template for {self.type} cards"
    self.built = False

  def __repr__(self):
    if self.built:
      return f"{self.title}\n\n{self.description}"
    else:
      return f"An unbuilt {self.title} - building this will grant:\n{self.description}"
    
  def ability(self):
    print(f"This is {self}\n\nit has not been used to build an actual card yet.")

  def build(self):
    self.built = True
    print("Built " + self.title)
    return self.ability()