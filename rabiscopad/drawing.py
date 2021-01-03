# -*- coding: utf-8 -*-

import interface

drawing_elements = []

def draw_elements():
    # Drawing actual elements!
    for element in drawing_elements:
        kind, sw, sc, fc, points = element
        strokeWeight(sw)
        stroke(sc)
        if fc:
            fill(fc)
        else:
            noFill()
        draw_plain_element(element)
    # Highlight selected objects
    for i, element in enumerate(drawing_elements):
        if i in interface.current_selection:
            _, sw, _, _, _ = element
            strokeWeight(sw + interface.SELEC_DIST)
            stroke(255, 100, 100, 100)
            noFill()
            draw_plain_element(element)
    # Mouse-over highlight on selection mode
    if interface.current_mode == interface.SELECT_MODE:
        for i, element in enumerate(drawing_elements):
            _, sw, _, _, _ = element
            strokeWeight(sw + interface.SELEC_DIST)
            stroke(255, 100, 255, 100)
            noFill()
            if i not in interface.current_selection:
                if interface.over_element(element):
                    draw_plain_element(element)
        
def draw_plain_element(element):
        kind, _, _, fc, points = element
        if kind == interface.CIRC_MODE and len(points) == 2:
            x, y = points[0]
            circle(x, y, 2 * dist(x, y, points[1][0], points[1][1]))
        else:
            # interface.SKETCH_MODE LINE_MODE QUAD_MODE
            beginShape()
            for p in points:
                vertex(p[0], p[1])
            if fc or kind == interface.QUAD_MODE:
                endShape(CLOSE)
            else:
                endShape()
