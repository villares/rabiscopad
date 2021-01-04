# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from itertools import chain
from drawing import drawing_elements
from buttons import Button, SColorButton, FColorButton, ModeButton

# Constants for current_mode state, button texts & key shortcuts
SKETCH_MODE = ('sketch', ' ')
LINE_MODE = ('line', 'l')
CIRC_MODE = ('circ', 'c')
QUAD_MODE = ('rect', 'r')
POLY_MODE = ('poly', 'p')  # not implemented
SELECT_MODE = ('select', 'x')

MODES = (SKETCH_MODE, LINE_MODE, CIRC_MODE,
         QUAD_MODE, POLY_MODE, SELECT_MODE)

STROKE_COLOR_SHORTCUTS = "01234567"
COLORS = [             # The main color palette:
    0,                 # black
    50,                # dark grey
    128,               # middle grey
    220,               # light grey
    255,               # white
    color(200, 0, 0),  # red
    color(0, 200, 0),  # green
    color(0, 0, 200),  # blue
]

SELEC_DIST = 5
B_SIZE = 50  # Button size

current_mode = SKETCH_MODE
export_svg = False
current_stroke_w = 2
current_stroke_c = color(0)
current_fill = None
current_element = None
current_selection = []
background_c = color(240, 240, 200)
keys_down = set()

def setup_gui():
    # Stroke color selection show/hide
    global s_menu_button, f_menu_button
    s_menu_button = Button(
        0, -B_SIZE, B_SIZE, B_SIZE,
        txt='stroke\ncolor',
        func=Button.toggle)
    f_menu_button = Button(
        B_SIZE, -B_SIZE, B_SIZE, B_SIZE,
        txt='fill\ncolor',
        func=Button.toggle)
    
    # button function "callback" builders
    def stroke_setter(c):
        def setter(button):
            global current_stroke_c
            button.exclusive_on()
            current_stroke_c = c
        return setter
    
    def fill_setter(c):
        def setter(button):
            global current_fill
            button.exclusive_on()
            current_fill = c
        return setter
    
    def mode_setter(m):
        def setter(button):
            global current_mode
            button.exclusive_on()
            current_mode = m
        return setter    
    
    # Stroke color palette buttons
    x = B_SIZE
    for c in COLORS:
        b = SColorButton(
            x, -B_SIZE, B_SIZE, B_SIZE,
            txt='●',
            txt_color=c,
            func=stroke_setter(c))
        if c == 0:
            b.active = True
        x += B_SIZE
    # Fill color palette buttons
    x = B_SIZE * 2
    for c in COLORS:
        b = FColorButton(
            x, -B_SIZE, B_SIZE, B_SIZE,
            txt='■',
            txt_color=c,
            func=fill_setter(c))
        x += 50
    b = FColorButton(
            x, -B_SIZE, B_SIZE, B_SIZE,
            txt='None',
            txt_color=None,
            func=fill_setter(None))
    b.active = True
    # Mode selection buttons
    x = 100
    for m in MODES:
        b = ModeButton(
            x, -B_SIZE, B_SIZE, B_SIZE,
            txt=m[0],
            txt_color=0,
            func=mode_setter(m))
        if m == SKETCH_MODE:
            b.active = True
        x += B_SIZE

def draw_gui(mp):
    """
    Draw on-screen buttons
    """
    global current_selection
    Button.display_all(mp)
    s_menu_button.txt_color = current_stroke_c
    f_menu_button.txt_color = current_fill

    if s_menu_button.active:
        SColorButton.display_all(mp)
    elif f_menu_button.active:
        FColorButton.display_all(mp)
    else:
        ModeButton.display_all(mp)

    if current_mode != SELECT_MODE:
        current_selection = []

def mouse_released(mb):
    global current_element
    current_element = None

def mouse_pressed(mb):
    global current_element, current_selection
    if not_on_button() and current_mode != SELECT_MODE:
        # Treating SKETCH_MODE, LINE_MODE, CIRC_MODE & etc.
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
        # Treating current_mode == SELECT_MODE
        for i, element in reversed(list(enumerate(drawing_elements))):
            if over_element(element):
                set_selection(i)
                return
        # if no element is picked, and no SHIFT held, desselect all
        if SHIFT not in keys_down:
            current_selection = []

def over_element(element):
    # will have to check differently for circles, lines & quads...
    kind, sw, sc, fc, points = element
    x0, y0 = points[0]
    if kind == CIRC_MODE and len(points) > 1:
        x1, y1 = points[1]
        mouse_center_dist = dist(mouseX, mouseY, x0, y0)
        r = dist(x0, y0, x1, y1)
        if fc:
            return mouse_center_dist < r
        else:
            return r - SELEC_DIST < mouse_center_dist < r + SELEC_DIST
    elif kind == QUAD_MODE and len(points) > 1:
        x2, y2 = points[2]
        if fc:
            return mouse_inside_box(x0, y0, x2, y2)
        else:
            return mouse_over_rect_edges(points)
    elif kind == LINE_MODE and len(points) > 1:
        x1, y1 = points[1]
        return naive_point_over_line(mouseX, mouseY, x0, y0, x1, y1)
    else:
        for x, y in points:
            if dist(mouseX, mouseY, x, y) < SELEC_DIST:
                return True
        return False

def mouse_inside_box(x0, y0, x1, y1):
    return (x0 < mouseX < x1 and
            y0 < mouseY < y1)

def mouse_over_rect_edges(points):
    return any(naive_point_over_line(mouseX, mouseY, lax, lay, lbx, lby)
               for (lax, lay), (lbx, lby) in ((points[0], points[1]),
                                              (points[1], points[2]),
                                              (points[2], points[3]),
                                              (points[3], points[0])))

def naive_point_over_line(px, py, lax, lay, lbx, lby,
                          tolerance=1):
    """
    Check if point is over line using the sum of
    the distances from the point to the line ends
    (the result has to be near equal for True).
    """
    ab = dist(lax, lay, lbx, lby)
    pa = dist(lax, lay, px, py)
    pb = dist(px, py, lbx, lby)
    return (pa + pb) <= ab + tolerance

def set_selection(i):
    global current_selection
    if SHIFT not in keys_down:
        current_selection = [i]
    else:
        if i not in current_selection:
            current_selection.append(i)
        else:
            current_selection.remove(i)

def not_on_button():
    """ Crude first aproach, not on bottom of screen..."""
    return mouseY < height - B_SIZE

def mouse_dragged(mb):
    if current_element:
        points = current_element[-1]
        last_px, last_py = points[-1]
        if current_mode == SKETCH_MODE and good_dist(last_px, last_py):
            points.append((mouseX, mouseY))
        elif current_mode in (LINE_MODE,
                              CIRC_MODE,
                              ):
            x0, y0 = points[0]
            points[:] = (x0, y0), (mouseX, mouseY)
        elif current_mode == QUAD_MODE:
            x0, y0 = points[0]
            points[:] = ((x0, y0), (mouseX, y0),
                         (mouseX, mouseY), (x0, mouseY))

    if current_mode == SELECT_MODE:
        for i in current_selection:
            element = drawing_elements[i]
            points = element[-1]
            dx, dy = mouseX - pmouseX, mouseY - pmouseY
            move_points(points, dx, dy)

def move_points(pts, dx, dy):
    for i, (x, y) in enumerate(pts):
        pts[i] = (x + dx, y + dy)

def good_dist(last_px, last_py):
    return dist(mouseX, mouseY, last_px, last_py) > current_stroke_w

def key_pressed(key, keyCode):
    global export_svg
    global current_stroke_w, current_stroke_c
    global current_fill, background_c
    global current_mode, current_selection
    if key == CODED:
        keys_down.add(keyCode)
    else:
        keys_down.add(key)

    if key in (BACKSPACE, DELETE) and drawing_elements:
        if current_mode != SELECT_MODE:
            drawing_elements.pop()
        elif current_selection:
            to_del = [drawing_elements[i]
                      for i in current_selection]
            for el in to_del:
                drawing_elements.remove(el)
            current_selection = []

    if key == 'e':  # Erase all
        if yes_no_pane("ATENTION", "Erase all elements?") == 0:
            drawing_elements[:] = []
    if key == 's':
        export_svg = True
        svg = createGraphics(width, height, SVG, 'sketch.svg')
        beginRecord(svg)
    if key in ('+', '='):
        current_stroke_w += 1
    if key == '-' and current_stroke_w > 1:
        current_stroke_w -= 1
    # without str() you crash when key is an int code!
    if str(key) in STROKE_COLOR_SHORTCUTS:
        current_stroke_c = COLORS[int(key)]
        SColorButton.set_active(current_stroke_c)

    # treat keyboard shortcuts for modes
    for m in MODES:
        t, k = m  # button text, shortcut key
        if key == k:
            current_mode = m
            # and set gui button according!
            ModeButton.set_active(current_mode)

def key_released(key, keyCode):
    if key == CODED:
        keys_down.discard(keyCode)
    else:
        keys_down.discard(key)

def treat_multi_keys():
    # this will be needed for multi-key shortcuts
    pass


def mouse_wheel(event):
    amt = event.getCount()
    # Rotate or scale all points of selected elements
    if current_selection:
        if CONTROL in keys_down:
            anchor = (mouseX, mouseY)
        else:
            points = (drawing_elements[i][-1] for i in current_selection)
            bb = bounding_box(chain(*points))
            anchor = midpoint(bb)
        for i in current_selection:
            element = drawing_elements[i]
            points = element[-1]
            if SHIFT in keys_down:
                scale_points(points, 1 + amt / 100.0, anchor)
            else:
                rotate_points(points, amt / 10.0, anchor)

def rotate_points(pts, angle, origin):
    x0, y0 = origin
    for i, (xp, yp) in enumerate(pts):
        x, y = xp - x0, yp - y0  # translate to origin
        xr = x * cos(angle) - y * sin(angle)
        yr = y * cos(angle) + x * sin(angle)
        pts[i] = (xr + x0, yr + y0)

def scale_points(pts, factor, origin):
    x0, y0 = origin
    for i, (xp, yp) in enumerate(pts):
        x, y = xp - x0, yp - y0  # translate to origin
        xr = x * factor
        yr = y * factor
        pts[i] = (xr + x0, yr + y0)

def bounding_box(points):
    x_coordinates, y_coordinates = zip(*points)
    return (PVector(min(x_coordinates), min(y_coordinates)),
            PVector(max(x_coordinates), max(y_coordinates)))

def midpoint(t):
    return ((t[0][0] + t[1][0]) / 2.0, (t[0][1] + t[1][1]) / 2.0)

def yes_no_pane(title, message):
    # 0:Yes, 1:No,-1:Canceled/Closed
    from javax.swing import JOptionPane
    return JOptionPane.showConfirmDialog(None,
                                         message,
                                         title,
                                         JOptionPane.YES_NO_OPTION)
