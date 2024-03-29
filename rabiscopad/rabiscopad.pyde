"""
A bare-bones SVG SketchBook - Licensed under GPL v3.0

Alexandre B A Villares - http://abav.lugaralgum.com
in collaboration with Foad S. Farimani https://twitter.com/fsfarimani

v2020_12_19 exporting SVG now!
v2020_12_20 line mode & circle mode
v2020_12_21a restructure in modules
v2020_12_21b very crude buttons
v2020_12_22 less crude buttons
v2020_12_24 crude attempt at selection mode
v2020_12_27 mode buttons, multiple key detection (to get SHIFT)
            multiple selection (with SHIFT), moving selected
v2021_01_02 Rotate with mouse wheel, CONTROL to change center of rotation
v2021_01_03 Better selection (for rect, line, circle), highlights are now
            translucent over drawing. Added fill selection buttons.
            Experimental window resize. Changed some shortcuts!
v2021_01_10 Let's try Named tuples!!!
            ctrl+S to save, and with timestamp on filename
v2021_01_11 Choose output location on save
v2021_01_23 First undo ideas
"""

import interface
import drawing

add_library('svg')


def setup():
    # fullScreen()  # to use this, diable size()
    size(800, 600)  # disable this to use fullScreen()
    interface.setup_gui()
    this.surface.setResizable(True)


def draw():
    background(interface.background_c)
    drawing.draw_elements()

    if interface.export_svg_flag:
        interface.export_svg_flag = False
        endRecord()

    interface.draw_gui(mousePressed)


def mousePressed():
    interface.mouse_pressed(mouseButton)


def mouseReleased():
    interface.mouse_released(mouseButton)


def mouseDragged():
    interface.mouse_dragged(mouseButton)


def keyPressed():
    interface.key_pressed(key, keyCode)


def keyReleased():
    interface.key_released(key, keyCode)


def mouseWheel(e):
    interface.mouse_wheel(e)


def export_svg(selection):
    if selection:
        print(selection)
        interface.export_svg_flag = True
        print(interface.export_svg_flag)
        print("Saving file at: " + selection.getAbsolutePath())
        svg = createGraphics(width, height, SVG, selection.getAbsolutePath())
        beginRecord(svg)
    else:
        print("No file was saved")

# def stop():
#     r = interface.yes_no_pane("Closing!", "Would you like to save session?")
#     if r == 0:
#         # save_session()
#         print("Sorry, save_session() not implemented!")
