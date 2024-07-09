def giving(self, total):
  giving = []
  if total == 0:
    return giving
  else:
    remaining = total
    while remaining > 0:
      if remaining >= 10 and len(self.coins.golds) > 0:
        remaining -= 10
        giving.append(self.coins.golds.pop())
      elif remaining >= 5 and len(self.coins.silvers) > 0:
        remaining -= 5
        giving.append(self.coins.silvers.pop())
      elif remaining >= 1 and len(self.coins.coppers) > 0:
        remaining -= 1
        giving.append(self.coins.coppers.pop())
      elif len(self.coins.silvers) > 0: # make overpayment
        remaining -= 5
        giving.append(self.coins.silvers.pop())
      elif len(self.coins.golds) > 0:
        remaining -= 5
        giving.append(self.coins.golds.pop())
      else:
        remaining = 0
        print(f"{self.name} has no more coins to give.")

    totalGiving = sum([coin.value for coin in giving])
    if remaining > 0:
      print(f"{self.name} is giving {totalGiving}. {total} requested - payment was short by {remaining}!")
    elif remaining < 0:
      print(f"{self.name} is giving {totalGiving}. {total} requested - requires {abs(remaining)} change!")
    else:
      print(f"{self.name} is giving {totalGiving}.")
    return giving

def receiving(self, coins):
  received = 0
  for coin in coins:
    received += coin.value
    if coin.colour == "Copper":
      self.coins.coppers.append(coin)
    elif coin.colour ==  "Silver":
      self.coins.silvers.append(coin)
    elif coin.colour == "Gold":
      self.coins.golds.append(coin)
  if received > 0:
    print(f"{self.name} received {sum([coin.value for coin in coins])} cash")
  return received

def calcPayment(coins, total):
  payment = 0
  remaining = total
  while remaining > 0:
    if remaining >=10 and len(coins.gold) > 0:
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