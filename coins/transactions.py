from __future__ import annotations
from typing import TYPE_CHECKING, Union
if TYPE_CHECKING:
  from coins import Coin, CoinPiles, Bank
  from player import Player

def giving(self: Union[Player, Bank], total: int, silent: bool = False) -> list[Coin]:
  given = []
  if total == 0:
    return given
  else:
    remaining = total
    while remaining > 0:
      if remaining >= 10 and len(self.coins.golds) > 0:
        remaining -= 10
        given.append(self.coins.golds.pop())
      elif remaining >= 5 and len(self.coins.silvers) > 0:
        remaining -= 5
        given.append(self.coins.silvers.pop())
      elif remaining >= 1 and len(self.coins.coppers) > 0:
        remaining -= 1
        given.append(self.coins.coppers.pop())
      elif len(self.coins.silvers) > 0: # make overpayment
        remaining -= 5
        given.append(self.coins.silvers.pop())
      elif len(self.coins.golds) > 0:
        remaining -= 5
        given.append(self.coins.golds.pop())
      else:
        remaining = 0

    total_giving = sum([coin.value for coin in given])
    if remaining > 0:
      if not silent: self.declare_action(f"{self.name} is giving {total_giving} coins. {total} requested (payment was short by {remaining}) ==>")
    elif remaining < 0:
      if not silent: self.declare_action(f"{self.name} is giving {total_giving} coins. {total} requested (requires {abs(remaining)} change) ==>")
    else:
      if not silent: self.declare_action(f"{self.name} is giving {total_giving} coins ==>")
    return given

def receiving(self: Union[Player, Bank], coins: list[Coin], silent: bool = False) -> int:
  received = 0
  for coin in coins:
    received += coin.value
    if coin == 1:
      self.coins.coppers.append(coin)   # type: ignore
    elif coin == 5:
      self.coins.silvers.append(coin)   # type: ignore
    elif coin == 10:
      self.coins.golds.append(coin)     # type: ignore
  if received > 0:
    if not silent: self.declare_action(f"==> {self.name} received {sum([coin.value for coin in coins])} coins")
  return received

def calculate_payment(coins: CoinPiles, total: int) -> int:
  payment = 0
  remaining = total
  while remaining > 0:
    if remaining >=10 and len(coins.golds) > 0:
      payment += 10
      remaining -= 10
    elif remaining >=5 and len(coins.silvers) > 0:
      payment += 5
      remaining -= 5
    elif remaining >=1 and len(coins.coppers) > 0:
      payment += 1
      remaining -= 1
    elif len(coins.silvers) > 0:
      payment += 5
      remaining -= 5
    elif len(coins.golds) > 0:
      payment += 10
      remaining -= 10
  return payment