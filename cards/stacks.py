from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
  from .blue import Blues
  from .green import Greens
  from .red import Reds
  from .purple import Purples
  from .landmark import Landmarks

from typing import Union
from collections import Counter
from reference import reference
from .blue import WheatField, Ranch, Forest, Mine, AppleOrchard
from .green import Bakery, ConvenienceStore, CheeseFactory, FurnitureFactory, FarmersMarket
from .red import Cafe, FamilyRestaurant
from .purple import Stadium, TVStation, BusinessCentre
from .landmark import TrainStation, ShoppingMall, AmusementPark, RadioTower

cardTypes = Union[WheatField, Ranch, Forest, Mine, AppleOrchard, Bakery, ConvenienceStore, CheeseFactory, FurnitureFactory, FarmersMarket, Cafe, FamilyRestaurant, Stadium, TVStation, BusinessCentre]

class Deck:
  """
  This is a class to hold lists representing stacks of cards.
  These stacks of cards represent the deck of cards in the game, and are organised into stacks of same cards.
  The game starts with 6 of each Establishment card, and one of each Major Establishment per player in the game. The deck does not hold any Landmark cards.
  The stacks can be added to and removed from, or their contents can be described.
  """
  def __init__(self, playerCount: int):
    self.wheat_fields = [WheatField() for _ in range(6)]
    self.ranches = [Ranch() for _ in range(6)]
    self.bakeries = [Bakery() for _ in range(6)]
    self.cafes = [Cafe() for _ in range(6)]
    self.convenience_stores = [ConvenienceStore() for _ in range(6)]
    self.forests = [Forest() for _ in range(6)]
    self.major_establishments = [card for card in [Stadium(), TVStation(), BusinessCentre()] for _ in range(playerCount)]
    self.cheese_factories = [CheeseFactory() for _ in range(6)]
    self.furniture_factories = [FurnitureFactory() for _ in range(6)]
    self.mines = [Mine() for _ in range(6)]
    self.family_restaurants = [FamilyRestaurant() for _ in range(6)]
    self.apple_orchards = [AppleOrchard() for _ in range(6)]
    self.farmers_markets = [FarmersMarket() for _ in range(6)]

  def __len__(self) -> int:
    stacks = [
      self.wheat_fields, self.ranches, self.bakeries, self.cafes, self.convenience_stores,
      self.forests, self.major_establishments, self.cheese_factories, self.furniture_factories,
      self.mines,self.family_restaurants, self.apple_orchards, self.farmers_markets
    ]
    return sum(len(stack) for stack in stacks)
  
  def contents(self, cash: int = 100) -> list:
    """
    Returns a list of descriptions of the cards in the Deck, incl. the name, dice rolls that trigger it, description, cost and the quantity left in the pile.
    When printed to the console, the strings are colour coded depending on card colour and affordability.
    """
    card_stacks = [stack for stack in [getattr(self, attribute) for attribute in dir(self)] if isinstance(stack, list)]
    card_counts = [[title, count] for stack in card_stacks for title, count in Counter(card.title for card in stack).items()]
    
    all_cards = ()       # here we will store a multiline f-string per card - tuple because immutable and indexable
    all_card_indexes = [] # here we will store the z_index per card
    map_of_cards = {}     # here we will map the z_index of a card to its position in allCards tuple

    for title, qty in card_counts:
      card = [card for stack in card_stacks for card in stack if card.title == title][0]

      map_of_cards[str(card.z_index)] = len(all_cards)
      all_card_indexes.append(card.z_index)

      style = reference['shortcuts']['affordable'] if card.cost <= cash else reference['shortcuts']['unaffordable']
      styleReset = reference['shortcuts']['reset']

      all_cards += ([
        f"{card.colorize}{card.title}{card.reset}\n{card.colorize}> ({'-'.join(map(str, card.triggers))}) <{card.reset}",
        f"{card.colorize}{card.description.splitlines()[0]}{card.reset}\n{card.colorize}{card.description.splitlines()[1]}{card.reset}",
        f"{style}{card.cost} coin{'s' if card.cost > 1 else ''}{styleReset}",
        f"Qty: {qty}",
        ],)   # <= that comma makes this a tuple, and you can add a tuple to a tuple
      
    all_card_indexes.sort()
    sorted_cards = [all_cards[map_of_cards[str(index)]] for index in all_card_indexes]
    return sorted_cards

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

class Hand:
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

  def __len__(self) -> int:
    return sum(card.built for card in self.landmarks) + sum(len(stack) for stack in [self.blue, self.green, self.red, self.purple])
  
  def count(self, card_type: type[cardTypes]) -> int:
    """
    Returns the number of cards of a given card type in the players hand, as an int
    """
    stack = getattr(self, card_type.colour, [])
    count = 0
    for card in stack:
      if isinstance(card, card_type):
        count += 1
    return count
  
  def add(self, card: Blues | Greens | Reds | Purples) -> int:
    """
    Adds an establishment card to the Hand - returns the number of cards now in that pile.
    """
    stack = getattr(self, card.colour, None)
    if stack is not None:
      stack.append(card)
      return len(stack)
    raise ValueError(f"Cannot add {card.colour} cards to a player's hand")
  
  def remove(self, colour:str, name:str) -> Blues | Greens | Reds | Purples:
    """
    Removes an establishment card from the Hand - finds the card by name, removes it, and returns it.
    """
    stack = getattr(self, colour, None)
    if stack is not None:
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
    card_stacks = [stack for stack in [getattr(self, attribute) for attribute in dir(self)] if isinstance(stack, list)]
    card_counts = [[title, count] for stack in card_stacks for title, count in Counter(card.title for card in stack).items()]
    
    all_cards = ()       # here we will store a multiline f-string per card - tuple because immutable and indexable
    all_card_indexes = [] # here we will store the z_index per card
    map_of_cards = {}     # here we will map the z_index of a card to its position in allCards tuple

    for title, qty in card_counts:
      card = [card for stack in card_stacks for card in stack if card.title == title][0]

      map_of_cards[str(card.z_index)] = len(all_cards)
      all_card_indexes.append(card.z_index)

      if card.card_type == "Landmark":
        if card.built:
          all_cards += ([
            f"{card.colorize}{card.title}{card.reset}\n{card.colorize}> Landmark Card <{card.reset}",
            f"{card.colorize}{card.description.splitlines()[0]}{card.reset}\n{card.colorize}{card.description.splitlines()[1]}{card.reset}",
            f"{card.colorize}Built!{card.reset}",
            ],)   # <= that comma makes this a tuple, and you can add a tuple to a tuple
        else:
          all_cards += ([
            f"\x1b[9;2m{card.colorize}{card.title}{card.reset}\x1b[0m\n{card.colorize}> Unbuilt Landmark <{card.reset}",
            f"\x1b[9;2m{card.colorize}{card.description.splitlines()[0]}{card.reset}\x1b[0m\n{card.colorize}{card.description.splitlines()[1]}{card.reset}",
            f"{card.colorize}Not yet built...{card.reset}",
            ],)   # <= that comma makes this a tuple, and you can add a tuple to a tuple
      else:
        all_cards += ([
          f"{card.colorize}{card.title}{card.reset}\n{card.colorize}> ({'-'.join(map(str, card.triggers))}) <{card.reset}",
          f"{card.colorize}{card.description.splitlines()[0]}{card.reset}\n{card.colorize}{card.description.splitlines()[1]}{card.reset}",
          f"{card.colorize}Qty: {qty}{card.reset}",
          ],)     # <= that comma makes this a tuple, and you can add a tuple to a tuple
    
    all_card_indexes.sort()
    sorted_cards = [all_cards[map_of_cards[str(index)]] for index in all_card_indexes]
    return sorted_cards

def lookup(name: str) -> str | None:
  """
  This function provides a simple translation from 'card title' to 'stack name' for finding a card in the Deck.
  It is mostly converting a string of words to a single snake_case word, but also handles the fact that major_establishments contains three different cards
  """
  match name:
    case "Wheat Field":
      return "wheat_fields"
    case "Ranch":
      return "ranches"
    case "Bakery":
      return "bakeries"
    case "Cafe":
      return "cafes"
    case "Convenience Store":
      return "convenience_stores"
    case "Forest":
      return "forests"
    case "Stadium" | "TV Station" | "Business Centre": 
      return "major_establishments"
    case "Cheese Factory":
      return "cheese_factories"
    case "Furniture Factory":
      return "furniture_factories"
    case "Mine":
      return "mines"
    case "Family Restaurant":
      return "family_restaurants"
    case "Apple Orchard":
      return "apple_orchards"
    case "Farmers Market":
      return "farmers_markets"
    case _:
      print(f"Error: {name} is not one of the expected names")
      return
