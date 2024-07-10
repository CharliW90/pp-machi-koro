from inquirer.themes import Default, term

rgbColours = {
  'red': [208,13,13],
  'green': [13,156,13],
  'blue': [13,13,208],
  'purple': [104,13,208],
  'orange': [208,104,13],
  'yellow': [208, 208, 13]
}

ansiColours = {
  'red': f"\033[38;2;{';'.join(str(x) for x in rgbColours['red'])};74m",
  'green': f"\033[38;2;{';'.join(str(x) for x in rgbColours['green'])};74m",
  'blue': f"\033[38;2;{';'.join(str(x) for x in rgbColours['blue'])};74m",
  'purple': f"\033[38;2;{';'.join(str(x) for x in rgbColours['purple'])};74m",
  'orange': f"\033[38;2;{';'.join(str(x) for x in rgbColours['orange'])};74m",
  'yellow': f"\033[38;2;{';'.join(str(x) for x in rgbColours['yellow'])};74m",
  'reset': f"\033[39m"
}

hexColours = {
  'red': '#%02x%02x%02x' % (*rgbColours['red'],),
  'green': '#%02x%02x%02x' % (*rgbColours['green'],),
  'blue': '#%02x%02x%02x' % (*rgbColours['blue'],),
  'purple': '#%02x%02x%02x' % (*rgbColours['purple'],),
  'orange': '#%02x%02x%02x' % (*rgbColours['orange'],),
  'yellow': '#%02x%02x%02x' % (*rgbColours['yellow'],)
}

shortcuts = {
  'notificationStart': f"\n{ansiColours['yellow']}==> ",
  'notificationEnd': f"{ansiColours['reset']}\n",
  'notify': lambda str: print(f"\n{ansiColours['yellow']}==> {str}{ansiColours['reset']}\n")
}

reference = {"rgbColours": rgbColours, "ansiColours": ansiColours, "hexColours": hexColours}

class MyTheme(Default):
  def __init__(self, player):
    super().__init__()
    self.Question.mark_color = term.color_rgb(*rgbColours[player.colour])
    self.Question.brackets_color = term.color_rgb(*rgbColours[player.colour])
    self.Question.default_color = term.on_color_rgb(*rgbColours[player.colour])
    self.List.selection_color = term.on_color_rgb(*rgbColours[player.colour])
    self.List.selection_cursor = f"{player.name} =>"