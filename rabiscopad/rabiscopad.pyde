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
"""

import interface
import drawing

add_library('svg')

def setup():
    # fullScreen()  # to use this, diable size()
    size(500, 500)  # disable this to use fullScreen()
    interface.setup_gui()
    
def draw():
    background(interface.background_c)
    drawing.draw_elements()

    if interface.export_svg:
        interface.export_svg = False
        endRecord()

    interface.draw_gui(mousePressed)
    interface.treat_multi_keys() # not implemented

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
    
def mouseWheel(e): # not used yet, nothing implemented
    interface.mouse_wheel(e)    
    
# def stop():
#     r = interface.yes_no_pane("Closing!", "Would you like to save session?")
#     if r == 0:
#         # save_session()
#         print("Sorry, save_session() not implemented!")
