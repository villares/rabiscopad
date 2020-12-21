"""
A bare-bones SVG SketchBook - Licensed under GPL v3.0

Alexandre B A Villares - http://abav.lugaralgum.com
in collaboration with Foad S. Farimani https://twitter.com/fsfarimani

v2020_12_19 exporting SVG now!
v2020_12_20 line mode & circle mode
"""
add_library('svg')

drawing_elements = []
export_svg = False
current_stroke_w = 2
current_stroke_c = color(0)
current_fill = None
current_element = None
background_c = color(240, 240, 200)

SKETCH_MODE, LINE_MODE, CIRC_MODE, QUAD_MODE, TRI_MODE, SELECT_MODE = range(6)
current_mode = SKETCH_MODE

def setup():
    # fullScreen()  # to use this, disable size()
    size(500, 500)  # disable this to use fullScreen()

def draw():
    global export_svg

    background(background_c)
    draw_elements()

    if export_svg:
        export_svg = False
        endRecord()

    draw_gui()

def draw_elements():
    for element in drawing_elements:
        kind, sw, sc, cf, points = element
        strokeWeight(sw)
        stroke(sc)
        if cf:
            fill(cf)
        else:
            noFill()
            
        if kind in (SKETCH_MODE, LINE_MODE):
            beginShape()
            for p in points:
                vertex(p[0], p[1])
            if not cf:
                endShape()
            else:
                endShape(CLOSE)
        elif kind == CIRC_MODE and len(points) == 2:
            x, y = points[0]
            circle(x, y, 2 * dist(x, y, points[1][0], points[1][1]))
        elif kind == QUAD_MODE and len(points) == 2:
            x, y = points[0]
            rect(x, y, (points[1][0] - x), (points[1][1] - y))
    
def mousePressed():
    global current_element

    # SKETCH_MODE, LINE_MODE, CIRC_MODE, QUAD_MODE, TRI_MODE
    points = [(mouseX, mouseY)]
    current_element = (current_mode,      # kind
                       current_stroke_w,  # stroke weight
                       current_stroke_c,  # stroke color
                       current_fill,
                       points)
    drawing_elements.append(current_element)

def mouseReleased():
    global current_element
    current_element = None

def mouseDragged():
    if current_element:
        points = current_element[-1]
        last_px, last_py = points[-1]
        if current_mode == SKETCH_MODE and good_dist(last_px, last_py):
            points.append((mouseX, mouseY))
        
        if current_mode in (LINE_MODE, CIRC_MODE, QUAD_MODE):
            if len(points) == 1:
                points.append((mouseX, mouseY))
            else:
                points[-1] = (mouseX, mouseY)


def good_dist(last_px, last_py):
    return dist(mouseX, mouseY, last_px, last_py) > current_stroke_w


def keyPressed():
    global export_svg
    global current_stroke_w, current_stroke_c
    global current_fill, background_c
    global current_mode
    # print(key, keyCode, CODED)
    
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
    if key == 'q':
        current_mode = QUAD_MODE
    if key == ' ':
        current_mode = SKETCH_MODE


def draw_gui():
    """
    Draw on-screen buttons 
    """
    pushStyle()
    popStyle()
