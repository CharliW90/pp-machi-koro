def giving(self, total):
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
        print(f"{self.name} has no more coins to give.")

    totalGiving = sum([coin.value for coin in given])
    if remaining > 0:
      self.declareAction(f"{self.name} is giving {totalGiving} coins. {total} requested (payment was short by {remaining}) ==>")
    elif remaining < 0:
      self.declareAction(f"{self.name} is giving {totalGiving} coins. {total} requested (requires {abs(remaining)} change) ==>")
    else:
      self.declareAction(f"{self.name} is giving {totalGiving} coins ==>")
    return given

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
    self.declareAction(f"==> {self.name} received {sum([coin.value for coin in coins])} coins")
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