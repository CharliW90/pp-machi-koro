from collections import Counter
from reference import shortcuts
from .blue import *
from .green import *
from .red import *
from .purple import *
from .landmark import *

class Deck:
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
  
  def contents(self, cash = 100) -> list[tuple]:
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
    pile = lookup(card.title)
    if pile:
      stack = getattr(self, str(pile))
      stack.append(card)
      print(f"Added {card.title} to the {pile} pile - there are now {len(stack)} cards in this pile")
      return len(stack)
    raise ValueError(f"Cannot add a {card.title} card to the Deck")
  
  def remove(self, name: str) -> Blues | Greens | Reds | Purples:
    pile = lookup(name)
    if pile:
      stack = getattr(self, str(pile))
      card = stack.pop()
      print(f"Removed {card.title} from the {pile} pile - there are now {len(stack)} cards in this pile")
      return card
    raise ValueError(f"Cannot remove a {name} card from the Deck")

class Hand():
  def __init__(self):
    self.blue = [WheatField()]
    self.green = [Bakery()]
    self.red = []
    self.purple = []
    self.landmarks = [TrainStation(), ShoppingMall(), AmusementPark(), RadioTower()]
  
  def add(self, card: Blues | Greens | Reds | Purples) -> int:
    stack = getattr(self, card.colour, None)
    if stack:
      stack.append(card)
      return len(stack)
    raise ValueError(f"Cannot add {card.colour} cards to a player's hand")
  
  def remove(self, colour:str, name:str) -> Blues | Greens | Reds | Purples:
    stack = getattr(self, colour, None)
    if stack:
      for i, card in enumerate(stack):
        if card.title == name:
          return stack.pop(i)
      raise ValueError(f"No {name} card")
    raise ValueError(f"Player hands do not include {colour} cards")

  def contents(self) -> list[tuple]:
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
