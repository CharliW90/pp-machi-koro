from inquirer.themes import Default, term

rgb_colours = {
  'red': [208,0,0],
  'green': [0,208,0],
  'blue': [0,0,208]
}

rgb_colours['cyan'] = [b+g for b, g in zip(rgb_colours['blue'], rgb_colours['green'])]
rgb_colours['yellow'] = [r+g for r, g in zip(rgb_colours['red'], rgb_colours['green'])]
rgb_colours['magenta'] = [r+b for r, b in zip(rgb_colours['red'], rgb_colours['blue'])]

rgb_colours['crashmat_blue'] = [b+int(g/2) for b, g in zip(rgb_colours['blue'], rgb_colours['green'])]
rgb_colours['orange'] = [r+int(g/2) for r, g in zip(rgb_colours['red'], rgb_colours['green'])]
rgb_colours['pink'] = [r+int(b/2) for r, b in zip(rgb_colours['red'], rgb_colours['blue'])]

rgb_colours['teal'] = [g+int(b/2) for g, b in zip(rgb_colours['green'], rgb_colours['blue'])]
rgb_colours['lime'] = [g+int(r/2) for g, r in zip(rgb_colours['green'], rgb_colours['red'])]
rgb_colours['purple'] = [b+int(r/2) for b, r in zip(rgb_colours['blue'], rgb_colours['red'])]

rgb_colours['crashmat_blue_faded'] = [b+int(g/2.5)+int(r/3) for b, g, r in zip(rgb_colours['blue'], rgb_colours['green'], rgb_colours['red'])]
rgb_colours['orange_faded'] = [r+int(g/2.5)+int(b/3) for r, g, b in zip(rgb_colours['red'], rgb_colours['green'], rgb_colours['blue'])]
rgb_colours['pink_faded'] = [r+int(b/2.5)+int(g/3) for r, b, g in zip(rgb_colours['red'], rgb_colours['blue'], rgb_colours['green'])]

rgb_colours['teal_faded'] = [int(g/2)+int(b/2) for g, b in zip(rgb_colours['green'], rgb_colours['blue'])]
rgb_colours['lime_faded'] = [int(g/2)+int(r/2) for g, r in zip(rgb_colours['green'], rgb_colours['red'])]
rgb_colours['purple_faded'] = [int(b/2)+int(r/2) for b, r in zip(rgb_colours['blue'], rgb_colours['red'])]

ansi_colours = {colour: f"\033[38;2;{';'.join(str(x) for x in rgb_colours[colour])};74m" for colour in rgb_colours}
ansi_colours['reset'] = f"\033[39m"

hex_colours = {colour: '#%02x%02x%02x' % (*rgb_colours[colour],) for colour in rgb_colours}

def colorize(text: str, colour: str | None = None) -> str:
  if not colour:
    colour = text.lower()
  if colour in ansi_colours:
    return f"{ansi_colours[colour]}{text}{ansi_colours['reset']}"
  return f"COLORIZE_ERROR: {colour} not a colour"

shortcuts = {
  'notification_start': f"{ansi_colours['yellow']}==> ",
  'notification_end': f"{ansi_colours['reset']}\n",
  'unaffordable': "\x1b[9;2m",
  'affordable': "\x1b[3;32m",
  'reset': "\x1b[0m",
  'blink_start': "\033[5m",
  'blink_end': "\033[0m"
}

reference: dict[str, dict[str, str]] = {"ansi_colours": ansi_colours, "hex_colours": hex_colours, "shortcuts": shortcuts}

class MyTheme(Default):
  def __init__(self, colour: str, name: str):
    super().__init__()
    self.Question.mark_color = term.color_rgb(*rgb_colours[colour]) # type: ignore
    self.Question.brackets_color = term.color_rgb(*rgb_colours[colour]) # type: ignore
    self.Question.default_color = term.on_color_rgb(*rgb_colours[colour]) # type: ignore
    self.List.selection_color = term.on_color_rgb(*rgb_colours[colour]) # type: ignore
    self.List.selection_cursor = f"{name} =>" # type: ignore

welcome = (
  "WELCOME TO THE CITY OF MACHI KORO!\nCongratulations!  You've just been elected Mayor.\n"
  "\nBut don't get too comfortable - the citizens have some pretty big demands: \n"
  "jobs, a new stadium, a couple of cheese factories, maybe even an amusement park."
)

full_description = (
  "It's going to be a tough proposition, since the city currently consists of a wheat field, a bakery, "
  "blueprints for a few landmarks, and a single die.\n\nArmed only with your trusty die and a dream "
  "you must grow Machi Koro into the largest city in the region.  You will need to earn income from "
  "establishments, build landmarks, and take your neighbours' business.\n\nThey say Rome wasn't built "
  "in a day, but Machi Koro will rise in less than 30 minutes!"
)

help_text_card_activation = (
  "\nIn Machi Koro each roll of the die has a chance for establishments to earn income for all players, "
  f"regardless of whose turn it is.  {colorize('Blue')} cards trigger for everyone, for example any time "
  f"a player rolls a '1' all players earn income from their Wheat Fields.  {colorize('Green')} cards "
  "trigger only for the active player, for example any time a player rolls a '2' they earn income from "
  f"their Bakery cards but no one else does.  {colorize('Red')} cards trigger only for other players, and "
  "act against the player who rolled, for example any time a player rolls a '3' the player must pay any "
  f"other players who own Cafe cards.  {colorize('Purple')} cards trigger only for the active player - "
  "these Major Establishments take coins/cards from other players and trigger on a roll of a '6', but "
  "each player may only own one of each of these cards."
)

help_text_game_start = (
  "\nEach player starts with 3 coins, a Wheat Field and a Bakery.  The Wheat Field will trigger on a roll of "
  "'1' when any player rolls, whereas the Bakery will trigger on a roll of '2' only for the player who rolled."
  "\nEach player also starts with 4 Landmark cards - Train Station, Shopping Mall, Amusement Park, Radio Tower "
  "- which are 'unbuilt'.  Players must build these landmarks to get the abilities they grant, but also to win "
  "the game by building all 4.  The first player to build all 4 of their Landmark cards wins"
)

help_text_cards = (
  "\nThere are 15 types of establishment card (ignoring the 4 Landmark cards players need to build from their hand). "
  f"These cards are {colorize('Blue')}, {colorize('Green')}, {colorize('Red')}, or {colorize('Purple')}.  There are "
  f"6 of each card to be bought, except for {colorize('Purple')} which players may only own one of each.  Most cards "
  f"{colorize('Blue')} and {colorize('Green')} cards earn income from the Bank, whereas {colorize('Red')}, and "
  f"{colorize('Purple')} cards take from other players.  Some {colorize('Green')} cards earn income based on how many "
  f"of another type of card the player has, for example the '{colorize('Cheese Factory', 'green')}' card earns 3 coins "
  f"for each '{colorize('Ranch', 'blue')}' card that the player owns."
)

help_text_turn_taking = (
  "\nOn a player's turn, the first thing they must do is roll the dice.  Once the dice roll is known, cards that are "
  f"triggered by that number must be handled.  Multiple cards may trigger - if {colorize('Red')} cards trigger (i.e. "
  "on a roll of 3, 9 or 10) then these must be handled before anything else.  If the player does not have enough money "
  f"to pay the players with {colorize('Red')} cards then they stop paying - they are then allowed to earn income on "
  "their other establishments without having to pay this to those players that they had failed to pay previously.\n"
  "Once the player has rolled the dice, and handled the outcome of that, they may spend any remaining coins they have "
  "purchasing new establishments from the Deck."
)

help_text = [help_text_card_activation, help_text_game_start, help_text_cards, help_text_turn_taking]

credits = [
  "This python-plays game is based on the Pandasaurus board game Machi Koro (5th Anniversary Edition)",
  "Pandasaurus Machi Koro (5th Anniversary Edition) Credits:",
  "Game Design: Masao Suganuma",
  "Development: Nathan McNair and Molly Wardlow",
  "Illustration: Noboru Hotta",
  "Graphic Design: Taro Hino and Jason D. Kingsley",
  "Editing: Dustin Schwartz",
  "Special Thanks: Nobuaki Takerube, Simon Lundström, and the tens of thousands of fans who have made Machi Koro a smash hit over the past five years!",
  "This python-plays game was written by Charli Williams as a challenge to learn the python programming language",
  "Charli came from a javascript background, and this may be reflected in the coding here, but they tried their best to be pythonic",
  "https://github.com/CharliW90"
]