# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from drawing import drawing_elements
from buttons import Button

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
        svg = createGraphics(width, height, SVG, "sketch.svg")
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
    Button(50, height-50, 50, 50,
                txt="black",
                func=black)
    Button(100, height-50, 50, 50,
                txt="red",
                func=vermelho)

def black():
    global current_stroke_c
    current_stroke_c = color(0)

def vermelho():
    global current_stroke_c
    current_stroke_c = color(255, 0, 0)
    
def draw_gui(mp):
    """
    Draw on-screen buttons 
    """
    pushStyle()
    Button.display_all(mp)
    popStyle()
