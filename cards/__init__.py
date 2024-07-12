from typing import Union
from .cardTypes import BlueCard, GreenCard, RedCard, PurpleCard, LandmarkCard
from .blue import WheatField, Ranch, Forest, Mine, AppleOrchard, Blues
from .green  import Bakery, ConvenienceStore, CheeseFactory, FurnitureFactory, FarmersMarket, Greens
from .red import Cafe, FamilyRestaurant, Reds
from .purple import Stadium, TVStation, BusinessCentre, Purples
from .landmark import TrainStation, ShoppingMall, AmusementPark, RadioTower, Abilities, Landmarks
from .stacks import Deck, Hand

CardTemplate = Union[BlueCard, GreenCard, RedCard, PurpleCard, LandmarkCard]

Card = Union[
  WheatField, Ranch, Bakery, Cafe, ConvenienceStore,
  Forest, Stadium, TVStation, BusinessCentre, CheeseFactory,
  FurnitureFactory, Mine, FamilyRestaurant, AppleOrchard, FarmersMarket,
  TrainStation, ShoppingMall, AmusementPark, RadioTower
  ]