# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from drawing import drawing_elements
from buttons import Button, SColorButton, ModeButton

SKETCH_MODE = 'sketch'
LINE_MODE = 'line'
CIRC_MODE = 'circ'
QUAD_MODE = 'rect'
POLY_MODE = 'triang'
SELECT_MODE = 'select'
MODES = (SKETCH_MODE, LINE_MODE, CIRC_MODE,
         QUAD_MODE, POLY_MODE, SELECT_MODE)

COLORS = [
    0,  # black
    50,  # dark grey
    128,  # middle grey
    220,  # light grey
    255,  # white
    color(200, 0, 0),  # red
    color(0, 200, 0),  # green
    color(0, 0, 200),  # blue
]

current_mode = SKETCH_MODE
export_svg = False
current_stroke_w = 2
current_stroke_c = color(0)
current_fill = None
current_element = None
current_selection = None
background_c = color(240, 240, 200)
keys_down = set()

def setup_gui():
    global s_menu_button
    s_menu_button = Button(
        0, height - 50, 50, 50,
        txt='stroke\ncolor',
        func=Button.toggle)
    x = 50
    for c in COLORS:
        b = SColorButton(
            x, height - 50, 50, 50,
            txt='•',
            txt_color=c,
            func=color_setter(c))
        if c == 0:
            b.active = True
        x += 50
        
    x = 100
    for m in MODES:
        b = ModeButton(
            x, height - 50, 50, 50,
            txt=m,
            txt_color=0,
            func=mode_setter(m))
        if m == SKETCH_MODE:
            b.active = True
        x += 50


def draw_gui(mp):
    """
    Draw on-screen buttons 
    """
    global current_selection
    Button.display_all(mp)
    if s_menu_button.active:
        SColorButton.display_all(mp)
    else:
        ModeButton.display_all(mp)
    if current_mode != SELECT_MODE:
        current_selection = None

def color_setter(c):
    def setter(button):
        global current_stroke_c
        button.exclusive_on()
        current_stroke_c = c
    return setter

def mode_setter(m):
    def setter(button):
        global current_mode
        button.exclusive_on()
        current_mode = m
    return setter

def mouse_released(mb):
    global current_element
    current_element = None

def mouse_pressed(mb):
    global current_element, current_selection
    if not_on_button() and current_mode != SELECT_MODE:
        # SKETCH_MODE, LINE_MODE, CIRC_MODE & etc.
        points = [(mouseX, mouseY)]
        current_element = (
            current_mode,      # kind
            current_stroke_w,  # stroke weight
            current_stroke_c,  # stroke color
            current_fill,
            points
        )
        drawing_elements.append(current_element)
    elif not_on_button():
        for i, element in reversed(list(enumerate(drawing_elements))):
            # will have to check differently for circles...
            points = element[-1]
            for j, pt in enumerate(points):
                if dist(mouseX, mouseY, pt[0], pt[1]) < 5:
                    current_selection = i
                    return
        current_selection = None

def not_on_button():
        return mouseY < height - 50

def mouse_dragged(mb):
    if current_element:
        points = current_element[-1]
        last_px, last_py = points[-1]
        if current_mode == SKETCH_MODE and good_dist(last_px, last_py):
            points.append((mouseX, mouseY))
        if current_mode in (LINE_MODE,
                            CIRC_MODE,
                            QUAD_MODE):
            if len(points) == 1:
                points.append((mouseX, mouseY))
            else:
                points[-1] = (mouseX, mouseY)

def good_dist(last_px, last_py):
    return dist(mouseX, mouseY, last_px, last_py) > current_stroke_w


def key_pressed(key, keyCode):
    if key == CODED:
        keys_down.add(keyCode)
    else:
        keys_down.add(key)
    
    global export_svg
    global current_stroke_w, current_stroke_c
    global current_fill, background_c
    global current_mode, current_selection

    if key in (BACKSPACE, DELETE) and drawing_elements:
        if current_mode != SELECT_MODE:
            drawing_elements.pop()
        elif current_selection is not None:
            drawing_elements.pop(current_selection)
            current_selection = None

    if key == 'r':  # Reset
        drawing_elements[:] = []
    if key == 's':
        export_svg = True
        svg = createGraphics(width, height, SVG, 'sketch.svg')
        beginRecord(svg)
    if key in ('+', '='):
        current_stroke_w += 1
    if key == '-' and current_stroke_w > 1:
        current_stroke_w -= 1
    if key == 'l':
        current_mode = LINE_MODE
    if key == 'c':
        current_mode = CIRC_MODE
    if key == 'q':
        current_mode = QUAD_MODE
    if key == ' ':
        current_mode = SKETCH_MODE
    if key == 'x':
        current_mode = SELECT_MODE
    if str(key) in "01234567":   # without str() you crash when key is an int code!
        current_stroke_c = COLORS[int(key)]


def key_released(key, keyCode):
    if key == CODED:
        keys_down.discard(keyCode)
    else:
        keys_down.discard(key)

def treat_multi_keys():
    # this will be needed for multi-key shortcuts
    pass


def mouse_wheel(e):
    pass

def yes_no_pane(title, message):
    # 0:Yes, 1:No,-1:Canceled/Closed
    from javax.swing import JOptionPane
    return JOptionPane.showConfirmDialog(None,
                                         message,
                                         title,
                                         JOptionPane.YES_NO_OPTION)
