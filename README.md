# Machi Koro (the first of my 'Python Play' series)

To practice my python skills, I didn't want to just do a load of traditional katas, so I decided instead to turn my hand to trying to implement some of my favourite board games as Terminal games, in a series I'm calling 'Python Plays' (PP).

Machi Koro is a small and simple card game where players compete to build their town into the largest city in the region.  Starting with just a Wheat Field and a Bakery, and the plans to build 4 landmarks, players take it in turns to add to their town.  The first player to buld all 4 of their landmark cards, wins.  Each turn the player rolls one or two dice, and the sum then 'activates' cards with that number 
- blue cards (Primary Industries) trigger for everyone when their number is rolled, and earn money from the the Bank;
- green cards (Secondary Industries) trigger only for the active player, and earn money from the the Bank;
- red cards (Restaurants) trigger for everyone except the active player, and earn money from the active player;
- purple cards (Major Establishments) trigger only for the active player, and allow for special actions to be taken.

Card effects stack, so having multiple of the same card can win big!  Similarly, a throw that triggers your rivals red cards can cast big if they've stacked their hand that way.

Cash flows fast between players, and with the most expensive landmark requiring 22 cash in hand it can be a really tricky game to get right.

Players begin only with one dice to roll - building the Train Station allows a player to choose to roll one or two dice - a Wheat Field (triggered on a roll of 1) and a Bakery (triggered on a roll of 2 or 3).

## Cards

| Card | Roll | Trigger | Build Cost | Activation |
| ---- | :--: | ------- | :--------: | ---------- |
| $\color{#0d0dd0}{\textsf{Wheat Field}}$ | 1 | Everyone | 1 | Get 1 from the Bank |
| $\color{#0d0dd0}{\textsf{Ranch}}$ | 2 | Everyone | 1 | Get 1 from the Bank |
| $\color{#0d9c0d}{\textsf{Bakery}}$ | 2 or 3 | Active Player | 1 | Get 1 from the Bank |
| $\color{#d00d0d}{\textsf{Cafe}}$ | 3 | Opponents | 2 | Take 1 from Active Player |
| $\color{#0d9c0d}{\textsf{Convenience Store}}$ | 4 | Active Player | 2 | Get 3 from the Bank |
| $\color{#0d0dd0}{\textsf{Forest}}$ | 5 | Everyone | 3 | Get 1 from the Bank |
| $\color{#680dd0}{\textsf{Stadium}}$ | 6 | Active Player | 6 | Take 2 from each opponent |
| $\color{#680dd0}{\textsf{TV Station}}$ | 6 | Active Player | 7 | Take 5 from one opponent |
| $\color{#680dd0}{\textsf{Business Centre}}$ | 6 | Active Player | 8 | Swap one establishment with one opponent  |
| $\color{#0d9c0d}{\textsf{Cheese Factory}}$ | 7 | Active Player | 5 | Get 3 from Bank per Ranch owned |
| $\color{#0d9c0d}{\textsf{Furniture Factory}}$ | 8 | Active Player | 3 | Get 3 from Bank per Forest/Mine owned |
| $\color{#0d0dd0}{\textsf{Mine}}$ | 9 | Everyone | 6 | Get 5 coins from the Bank |
| $\color{#d00d0d}{\textsf{Family Restaurant}}$ | 9 or 10 | Opponents | 3 | Take 2 from Active Player |
| $\color{#0d0dd0}{\textsf{Apple Orchard}}$ | 10 | Everyone | 3 | Get 3 from the Bank |
| $\color{#0d9c0d}{\textsf{Farmers Market}}$ | 11 or 12 | Active Player | 2 | Get 2 from Bank per Field/Orchard owned |

## Landmarks

Players who have built a more expensive landmark, the Amusement Park (16 cash), are allowed to take another turn if they roll a double.  And players who have built the most expensive landmark, the Radio Tower (22 cash) can reroll the dice once per turn.

## Miscellaneous Code

### Colours

I wanted to use colours, to match the cards in the original game, so played around with ANSI escape code.  I ended up with a 'reference' module, that held a List of RGB values, and also a List of ANSI codes and hex-codes based on that list of RGB values.

```python
rgbColours = {
  'red': [208,13,13],
  'green': [13,156,13],
  'blue': [13,13,208],
  'purple': [104,13,208],
  'orange': [208,104,13]
}

ansiColours = {
  'red': f"\033[38;2;{rgbColours['red'][0]};{rgbColours['red'][1]};{rgbColours['red'][2]};74m",
  'green': f"\033[38;2;{rgbColours['green'][0]};{rgbColours['green'][1]};{rgbColours['green'][2]};74m",
  'blue': f"\033[38;2;{rgbColours['blue'][0]};{rgbColours['blue'][1]};{rgbColours['blue'][2]};74m",
  'purple': f"\033[38;2;{rgbColours['purple'][0]};{rgbColours['purple'][1]};{rgbColours['purple'][2]};74m",
  'orange': f"\033[38;2;{rgbColours['orange'][0]};{rgbColours['orange'][1]};{rgbColours['orange'][2]};74m",
  'reset': f"\033[39m"
}

hexColours = {
  'red': '#%02x%02x%02x' % (rgbColours['red'][0], rgbColours['red'][1], rgbColours['red'][2]),
  'green': '#%02x%02x%02x' % (rgbColours['green'][0], rgbColours['green'][1], rgbColours['green'][2]),
  'blue': '#%02x%02x%02x' % (rgbColours['blue'][0], rgbColours['blue'][1], rgbColours['blue'][2]),
  'purple': '#%02x%02x%02x' % (rgbColours['purple'][0], rgbColours['purple'][1], rgbColours['purple'][2]),
  'orange': '#%02x%02x%02x' % (rgbColours['orange'][0], rgbColours['orange'][1], rgbColours['orange'][2]),
}
```

adding one of these 'ansiColours' to the start of an f-string for terminal output will colour the text that colour - for example:

```python
print(f"{reference["ansiColours"]["red"]}Cafe{reference["ansiColours"]["reset"]}")
print(f"{reference["ansiColours"]["green"]}Bakery{reference["ansiColours"]["reset"]}")
print(f"{reference["ansiColours"]["blue"]}Wheat Field{reference["ansiColours"]["reset"]}")
```
will output:

> $\color{#d00d0d}{\textsf{Cafe}}$
>
> $\color{#0d9c0d}{\textsf{Bakery}}$
>
> $\color{#0d0dd0}{\textsf{Wheat Field}}$

I then stored these values against the card types that want them - so all 'Red Cards' have a property of colorize that will output the relevant f-string ANSI code, meaning that the above can become:

```python
print(f"{card.colorize}{card.title}{card.reset}")
```

> $\color{#d00d0d}{\textsf{Cafe}}$