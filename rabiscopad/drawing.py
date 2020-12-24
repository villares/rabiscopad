# -*- coding: utf-8 -*-

import interface

drawing_elements = []

def draw_elements():
    # highlight selected object
    for i, element in enumerate(drawing_elements):
        if i == interface.current_selection:
            strokeWeight(5 + interface.current_stroke_w)
            stroke(255, 100, 100)
            for x, y in element[-1]:
                point(x, y)
    # mouse over on selection mode
    if interface.current_mode == interface.SELECT_MODE:
        for i, element in enumerate(drawing_elements):
            strokeWeight(5 + interface.current_stroke_w)
            stroke(255, 100, 255)
            if i != interface.current_selection:
                for x, y in element[-1]:
                    if dist(x, y, mouseX, mouseY) < 5:
                        for x, y in element[-1]:
                            point(x, y)

    for element in drawing_elements:
        kind, sw, sc, cf, points = element
        strokeWeight(sw)
        stroke(sc)
        if cf:
            fill(cf)
        else:
            noFill()

        if kind in (interface.SKETCH_MODE, interface.LINE_MODE):
            beginShape()
            for p in points:
                vertex(p[0], p[1])
            if not cf:
                endShape()
            else:
                endShape(CLOSE)
        elif kind == interface.CIRC_MODE and len(points) == 2:
            x, y = points[0]
            circle(x, y, 2 * dist(x, y, points[1][0], points[1][1]))
        elif kind == interface.QUAD_MODE and len(points) == 2:
            x, y = points[0]
            rect(x, y, (points[1][0] - x), (points[1][1] - y))
