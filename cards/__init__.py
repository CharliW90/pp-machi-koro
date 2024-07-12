from typing import Union
from .cardTypes import BlueCard, GreenCard, RedCard, PurpleCard, LandmarkCard
from .blue import WheatField, Ranch, Forest, Mine, AppleOrchard
from .green  import Bakery, ConvenienceStore, CheeseFactory, FurnitureFactory, FarmersMarket
from .red import Cafe, FamilyRestaurant
from .purple import Stadium, TVStation, BusinessCentre
from .landmark import TrainStation, ShoppingMall, AmusementPark, RadioTower, Abilities
from .stacks import Deck, Hand

CardTemplate = Union[BlueCard, GreenCard, RedCard, PurpleCard, LandmarkCard]

Card = Union[
  WheatField, Ranch, Bakery, Cafe, ConvenienceStore,
  Forest, Stadium, TVStation, BusinessCentre, CheeseFactory,
  FurnitureFactory, Mine, FamilyRestaurant, AppleOrchard, FarmersMarket,
  TrainStation, ShoppingMall, AmusementPark, RadioTower
  ]

Blues = Union[WheatField, Ranch, Forest, Mine, AppleOrchard]
Greens = Union[Bakery, ConvenienceStore, CheeseFactory, FurnitureFactory, FarmersMarket]
Reds = Union[Cafe, FamilyRestaurant]
Purples = Union[Stadium, TVStation, BusinessCentre]
Landmarks = Union[TrainStation, ShoppingMall, AmusementPark, RadioTower]