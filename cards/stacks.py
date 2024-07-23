from collections import Counter
from reference import shortcuts
from .blue import *
from .green import *
from .red import *
from .purple import *
from .landmark import *

class Deck:
  """
  This is a class to hold lists representing stacks of cards.
  These stacks of cards represent the deck of cards in the game, and are organised into stacks of same cards.
  The game starts with 6 of each Establishment card, and one of each Major Establishment per player in the game. The deck does not hold any Landmark cards.
  The stacks can be added to and removed from, or their contents can be described.
  """
  def __init__(self, playerCount:int):
    self.wheatFields = [WheatField() for _ in range(6)]
    self.ranches = [Ranch() for _ in range(6)]
    self.bakeries = [Bakery() for _ in range(6)]
    self.cafes = [Cafe() for _ in range(6)]
    self.convenienceStores = [ConvenienceStore() for _ in range(6)]
    self.forests = [Forest() for _ in range(6)]
    self.majorEstablishments = [card for card in [Stadium(), TVStation(), BusinessCentre()] for _ in range(playerCount)]
    self.cheeseFactories = [CheeseFactory() for _ in range(6)]
    self.furnitureFactories = [FurnitureFactory() for _ in range(6)]
    self.mines = [Mine() for _ in range(6)]
    self.familyRestaurants = [FamilyRestaurant() for _ in range(6)]
    self.appleOrchards = [AppleOrchard() for _ in range(6)]
    self.farmersMarkets = [FarmersMarket() for _ in range(6)]
  
  def contents(self, cash: int = 100) -> list:
    """
    Returns a list of descriptions of the cards in the Deck, incl. the name, dice rolls that trigger it, description, cost and the quantity left in the pile.
    When printed to the console, the strings are colour coded depending on card colour and affordability.
    """
    cardStacks = [stack for stack in [getattr(self, attribute) for attribute in dir(self)] if isinstance(stack, list)]
    cardCounts = [[title, count] for stack in cardStacks for title, count in Counter(card.title for card in stack).items()]
    
    allCards = ()       # here we will store a multiline f-string per card - tuple because immutable and indexable
    allCardIndexes = [] # here we will store the zIndex per card
    mapOfCards = {}     # here we will map the zIndex of a card to its position in allCards tuple

    for title, qty in cardCounts:
      card = [card for stack in cardStacks for card in stack if card.title == title][0]

      mapOfCards[str(card.zIndex)] = len(allCards)
      allCardIndexes.append(card.zIndex)

      style = shortcuts['affordable'] if card.cost <= cash else shortcuts['unaffordable']
      styleReset = shortcuts['reset']

      allCards += ([
        f"{card.colorize}{card.title}{card.reset}\n{card.colorize}> ({'-'.join(map(str, card.triggers))}) <{card.reset}",
        f"{card.colorize}{card.description.splitlines()[0]}{card.reset}\n{card.colorize}{card.description.splitlines()[1]}{card.reset}",
        f"{style}{card.cost} coin{'s' if card.cost > 1 else ''}{styleReset}",
        f"Qty: {qty}",
        ],)   # <= that comma makes this a tuple, and you can add a tuple to a tuple
      
    allCardIndexes.sort()
    sortedCards = [allCards[mapOfCards[str(index)]] for index in allCardIndexes]
    return sortedCards

  def add(self, card: Blues | Greens | Reds | Purples) -> int:
    """
    Adds an establishment card to the Deck - returns the number of cards now in that pile.
    """
    pile = lookup(card.title)
    if pile:
      stack = getattr(self, str(pile))
      stack.append(card)
      print(f"Added {card.title} to the {pile} pile - there are now {len(stack)} cards in this pile")
      return len(stack)
    raise ValueError(f"Cannot add a {card.title} card to the Deck")
  
  def remove(self, name: str) -> tuple[Blues | Greens | Reds | Purples, str, int]:
    """
    Removes an establishment card from the Deck - finds the card by name, removes it, and returns it along with the name of the pile it was taken from, and the number of cards now in that pile.
    """
    pile = lookup(name)
    if pile:
      stack = getattr(self, str(pile))
      if len(stack) == 0:
        raise ValueError(f"Cannot remove a {name} card from the {pile} pile - there are none left!")
      card = stack.pop()
      print(f"Removed {card.title} from the {pile} pile - there are now {len(stack)} cards in this pile")
      return card, pile, len(stack)
    raise AttributeError(f"Cannot remove a {name} card from the Deck - no pile exists for these cards.")

class Hand():
  """
  This is a class to hold lists representing stacks of cards.
  These stacks of cards represent a player's hand of cards, and are organised into stacks based of each colour.
  Players start with a Wheat Field card, a Bakery card. Players also have a stack containing one of each Landmark card (unbuilt).
  The stacks can be added to and removed from, or their contents can be described.
  """
  def __init__(self):
    self.blue = [WheatField()]  # this card is not drawn from the Deck, it is in addition to the 6 in the Deck
    self.green = [Bakery()]     # this card is not drawn from the Deck, it is in addition to the 6 in the Deck
    self.red = []
    self.purple = []
    self.landmarks = [TrainStation(), ShoppingMall(), AmusementPark(), RadioTower()]
  
  def add(self, card: Blues | Greens | Reds | Purples) -> int:
    """
    Adds an establishment card to the Deck - returns the number of cards now in that pile.
    """
    stack = getattr(self, card.colour, None)
    if stack:
      stack.append(card)
      return len(stack)
    raise ValueError(f"Cannot add {card.colour} cards to a player's hand")
  
  def remove(self, colour:str, name:str) -> Blues | Greens | Reds | Purples:
    """
    Removes an establishment card from the Hand - finds the card by name, removes it, and returns it.
    """
    stack = getattr(self, colour, None)
    if stack:
      for i, card in enumerate(stack):
        if card.title == name:
          return stack.pop(i)
      raise ValueError(f"No {name} card")
    raise ValueError(f"Player hands do not include {colour} cards")

  def contents(self) -> list:
    """
    Returns a list of descriptions of the cards in the Deck, incl. the name, dice rolls that trigger it, description, cost and the quantity left in the pile.
    When printed to the console, the strings are colour coded depending on card colour and affordability.
    """
    cardStacks = [stack for stack in [getattr(self, attribute) for attribute in dir(self)] if isinstance(stack, list)]
    cardCounts = [[title, count] for stack in cardStacks for title, count in Counter(card.title for card in stack).items()]
    
    allCards = ()       # here we will store a multiline f-string per card - tuple because immutable and indexable
    allCardIndexes = [] # here we will store the zIndex per card
    mapOfCards = {}     # here we will map the zIndex of a card to its position in allCards tuple

    for title, qty in cardCounts:
      card = [card for stack in cardStacks for card in stack if card.title == title][0]

      mapOfCards[str(card.zIndex)] = len(allCards)
      allCardIndexes.append(card.zIndex)

      if card.cardType == "Landmark":
        if card.built:
          allCards += ([
            f"{card.colorize}{card.title}{card.reset}\n{card.colorize}> Landmark Card <{card.reset}",
            f"{card.colorize}{card.description.splitlines()[0]}{card.reset}\n{card.colorize}{card.description.splitlines()[1]}{card.reset}",
            f"{card.colorize}Built!{card.reset}",
            ],)   # <= that comma makes this a tuple, and you can add a tuple to a tuple
        else:
          allCards += ([
            f"\x1b[9;2m{card.colorize}{card.title}{card.reset}\x1b[0m\n{card.colorize}> Unbuilt Landmark <{card.reset}",
            f"\x1b[9;2m{card.colorize}{card.description.splitlines()[0]}{card.reset}\x1b[0m\n{card.colorize}{card.description.splitlines()[1]}{card.reset}",
            f"{card.colorize}Not yet built...{card.reset}",
            ],)   # <= that comma makes this a tuple, and you can add a tuple to a tuple
      else:
        allCards += ([
          f"{card.colorize}{card.title}{card.reset}\n{card.colorize}> ({'-'.join(map(str, card.triggers))}) <{card.reset}",
          f"{card.colorize}{card.description.splitlines()[0]}{card.reset}\n{card.colorize}{card.description.splitlines()[1]}{card.reset}",
          f"{card.colorize}Qty: {qty}{card.reset}",
          ],)     # <= that comma makes this a tuple, and you can add a tuple to a tuple
    
    allCardIndexes.sort()
    sortedCards = [allCards[mapOfCards[str(index)]] for index in allCardIndexes]
    return sortedCards

def lookup(name: str) -> str | None:
  """
  This function provides a simple translation from 'card title' to 'stack name' for finding a card in the Deck.
  It is mostly converting a string of words to a single camelCase word, but also handles the fact that majorEstablishments containing three different cards
  """
  match name:
    case "Wheat Field":
      return "wheatFields"
    case "Ranch":
      return "ranches"
    case "Bakery":
      return "bakeries"
    case "Cafe":
      return "cafes"
    case "Convenience Store":
      return "convenienceStores"
    case "Forest":
      return "forests"
    case "Stadium" | "TV Station" | "Business Centre": 
      return "majorEstablishments"
    case "Cheese Factory":
      return "cheeseFactories"
    case "Furniture Factory":
      return "furnitureFactories"
    case "Mine":
      return "mines"
    case "Family Restaurant":
      return "familyRestaurants"
    case "Apple Orchard":
      return "appleOrchards"
    case "Farmers Market":
      return "farmersMarkets"
    case _:
      print(f"Error: {name} is not one of the expected names")
      return
