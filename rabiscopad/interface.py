# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from drawing import drawing_elements
from buttons import Button

COLORS = {'BLACK': 0,
          'WHITE': 255,
          'LIGHT_GREY': 240,
          'DARK_GREY': 50,
          'MIDDLE_GREY': 128,
          'RED': color(200, 0, 0),
          'GREEN': color(0, 200, 0),
          'BLUE': color(0, 0, 200),
          }
SKETCH_MODE, LINE_MODE, CIRC_MODE, SELECT_MODE = range(4)

current_mode = SKETCH_MODE
export_svg = False
current_stroke_w = 2
current_stroke_c = color(0)
current_fill = None
current_element = None
background_c = color(240, 240, 200)

def mouse_pressed(mb):
    global current_element

    # SKETCH_MODE, LINE_MODE, CIRC_MODE
    points = [(mouseX, mouseY)]
    current_element = (current_mode,      # kind
                       current_stroke_w,  # stroke weight
                       current_stroke_c,  # stroke color
                       current_fill,
                       points)
    drawing_elements.append(current_element)

def mouse_released(mb):
    global current_element
    current_element = None

def mouse_dragged(mb):
    if current_element:
        points = current_element[-1]
        last_px, last_py = points[-1]
        if current_mode == SKETCH_MODE and good_dist(last_px, last_py):
            points.append((mouseX, mouseY))

        if current_mode in (LINE_MODE, CIRC_MODE):
            if len(points) == 1:
                points.append((mouseX, mouseY))
            else:
                points[-1] = (mouseX, mouseY)


def good_dist(last_px, last_py):
    return dist(mouseX, mouseY, last_px, last_py) > current_stroke_w


def key_pressed(key, keyCode):
    global export_svg
    global current_stroke_w, current_stroke_c
    global current_fill, background_c
    global current_mode

    if key in (BACKSPACE, DELETE) and drawing_elements:
        drawing_elements.pop()
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
    if key == ' ':
        current_mode = SKETCH_MODE

def key_released(key, keyCode):
    # this will be needed for multi-key shortcuts
    pass

def treat_multi_keys():
    # this will be needed for multi-key shortcuts
    pass

def setup_gui():
    Button(50, height - 50, 50, 50,
           txt='black',
           func=color_setter(COLORS['BLACK']))
    Button(100, height - 50, 50, 50,
           txt='red',
           func=color_setter(COLORS['RED']))

def color_setter(c):
    def setter(button):
        global current_stroke_c
        button.exclusive_on()
        current_stroke_c = c
    return setter


def draw_gui(mp):
    """
    Draw on-screen buttons 
    """
    Button.display_all(mp)

def mouse_wheel(e):
    pass

def yes_no_pane(title, message):
    # Sim é 0, Não é 1, fechar a janela é -1
    from javax.swing import JOptionPane
    return JOptionPane.showConfirmDialog(None,
                                         message,
                                         title,
                                         JOptionPane.YES_NO_OPTION)
