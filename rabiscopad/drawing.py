# -*- coding: utf-8 -*-

from collections import namedtuple, deque
import interface

UNDOS = 10
drawing_elements = []
drawing_history = deque(maxlen=UNDOS)
redo_cache = []
Element = namedtuple('Element', 'kind sw sc fc points')

def draw_elements():
    # Drawing actual elements!
    for element in drawing_elements:
        strokeWeight(element.sw)
        stroke(element.sc)
        if element.fc:
            fill(element.fc)
        else:
            noFill()
        draw_plain_element(element)
    # Highlight selected objects
    for i, element in enumerate(drawing_elements):
        if i in interface.current_selection:
            strokeWeight(element.sw + interface.SELEC_DIST)
            stroke(255, 100, 100, 100)
            noFill()
            draw_plain_element(element)
    # Mouse-over highlight on selection mode
    if interface.current_mode == interface.SELECT_MODE:
        for i, element in enumerate(drawing_elements):
            strokeWeight(element.sw + interface.SELEC_DIST)
            stroke(255, 100, 255, 100)
            noFill()
            if i not in interface.current_selection:
                if interface.over_element(element):
                    draw_plain_element(element)
        
def draw_plain_element(element):
        if element.kind == interface.CIRC_MODE and len(element.points) == 2:
            x, y = element.points[0]
            xr, yr = element.points[1]
            circle(x, y, 2 * dist(x, y, xr, yr))
        else:
            # interface.SKETCH_MODE LINE_MODE QUAD_MODE
            beginShape()
            for p in element.points:
                vertex(p[0], p[1])
            if element.fc or element.kind == interface.QUAD_MODE:
                endShape(CLOSE)
            else:
                endShape()
