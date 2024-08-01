from __future__ import annotations

from typing import Union

class Coinage:
  value = 0

  def __eq__(self, value: int | Coinage) -> bool:
    if not isinstance(value, int | Coinage):
      raise TypeError(f"Cannot compare Coinage with {type(value).__name__} - can only compare with int or other Coinage")
    if isinstance(value, int):
      return self.value == value
    else:
      return self.value == value.value
  
  def __ne__(self, value: int | Coinage) -> bool:
    if not isinstance(value, int | Coinage):
      raise TypeError(f"Cannot compare Coinage with {type(value).__name__} - can only compare with int or other Coinage")
    if isinstance(value, int):
      return self.value != value
    else:
      return self.value != value.value
  
  def __lt__(self, value: int | Coinage) -> bool:
    if not isinstance(value, int | Coinage):
      raise TypeError(f"Cannot compare Coinage with {type(value).__name__} - can only compare with int or other Coinage")
    if isinstance(value, int):
      return self.value < value
    else:
      return self.value < value.value
  
  def __gt__(self, value: int | Coinage) -> bool:
    if not isinstance(value, int | Coinage):
      raise TypeError(f"Cannot compare Coinage with {type(value).__name__} - can only compare with int or other Coinage")
    if isinstance(value, int):
      return self.value > value
    else:
      return self.value > value.value
  
  def __le__(self, value: int | Coinage) -> bool:
    if not isinstance(value, int | Coinage):
      raise TypeError(f"Cannot compare Coinage with {type(value).__name__} - can only compare with int or other Coinage")
    if isinstance(value, int):
      return self.value <= value
    else:
      return self.value <= value.value
  
  def __ge__(self, value: int | Coinage) -> bool:
    if not isinstance(value, int | Coinage):
      raise TypeError(f"Cannot compare Coinage with {type(value).__name__} - can only compare with int or other Coinage")
    if isinstance(value, int):
      return self.value >= value
    else:
      return self.value >= value.value

class One(Coinage):
  def __init__(self):
    self.value = 1
    self.colour = "Copper"

  def __str__(self) -> str:
    return f"A single {self.colour} coin, with a value of {self.value}"

class Five(Coinage):
  def __init__(self):
    self.value = 5
    self.colour = "Silver"

  def __str__(self) -> str:
    return f"A single {self.colour} coin, with a value of {self.value}"

class Ten(Coinage):
  def __init__(self):
    self.value = 10
    self.colour = "Gold"

  def __str__(self) -> str:
    return f"A single {self.colour} coin, with a value of {self.value}"

Coin = Union[One, Five, Ten]

class CoinPiles:
  def __init__(self, coppers: int, silvers: int, golds: int):
    self.coppers = [One() for _ in range(coppers)]
    self.silvers = [Five() for _ in range(silvers)]
    self.golds = [Ten() for _ in range(golds)]
    self._iterator = 0
    self._sequence = [self.coppers, self.silvers, self.golds]

  def __str__(self) -> str:
    return f"3 piles of coins (Coppers, Silvers and Golds) with a total value of {self.total()}."
  
  def __len__(self) -> int:
    return len(self._sequence)
  
  def __iter__(self):
    return self
  
  def __next__(self) -> list[Coin]:
    if self._iterator < len(self._sequence):
      iteration = self._sequence[self._iterator]
      self._iterator += 1
      return iteration
    else:
      self._iterator = 0
      raise StopIteration

  def total(self) -> int:
    total = 0
    for stack in self:
      for coin in stack:
        total += coin.value
    return total