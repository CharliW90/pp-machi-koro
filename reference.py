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

reference = {"rgbColours": rgbColours, "ansiColours": ansiColours, "hexColours": hexColours}