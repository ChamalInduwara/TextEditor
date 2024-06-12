width = int(open('Assets/Data/width.txt', 'r').read())
height = int(open('Assets/Data/height.txt', 'r').read())

font = open('Assets/Data/font_fam.txt', 'r').read()
font_size = int(open('Assets/Data/font_size.txt', 'r').read())
font_clr = open('Assets/Data/font_clr.txt', 'r').read()

sizes = ['10', '12', '14', '16', '18', '20', '22', '24', '26', '28', '30', '32', '34', '36', '38', '40']

bg_clr = open('Assets/Data/bg_clr.txt', 'r').read()
txt_clr = open('Assets/Data/txt_clr.txt', 'r').read()
txt_panel_clr = open('Assets/Data/txt_panel_clr.txt', 'r').read()
widget_clr = open('Assets/Data/widget_clr.txt', 'r').read()
widget_hover_clr = open('Assets/Data/widget_hover_clr.txt', 'r').read()
themes = open('Assets/Data/theme.txt', 'r').read()

settings = False
word_count = 0
line_count = 1

font_clrs = ['red', 'black', 'yellow', 'white', 'gray', '#F8F8F8']

text = ''

status = f'Words: {word_count}      Lines: {line_count}      Font family: {font}      Font size: {font_size}'
