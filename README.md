## RabiscoPad

A bare-bones SVG sketchpad - Licensed under GPL v3.0

Developed by [Alexandre B A Villares](http://twitter.com/villares) and [Foad S. Farimani](https://twitter.com/fsfarimani)

![image1](docs/assets/readme_animation1.gif)
![image2](docs/assets/readme_animation2.gif)

### Keyboard shortcuts:

- <kbd>s</kbd> save SVG
- <kbd>c</kbd> draw circle
- <kbd>l</kbd> draw line
- <kbd>q</kbd> draw quad/rectangle
- <kbd>space</kbd> free drawing mode
- <kbd>backspace</kbd> or <kbd>delete</kbd> erase last element
- <kbd>r</kbd> erase all
- <kbd>+</kbd> and <kbd>-</kbd> change stroke weight

## change log:

- v2020_12_19 exporting SVG now!
- v2020_12_20 line mode & circle mode
- v2020_12_21 first attempt at GUI Buttons
- v2020_12_22 pe/stroke color buttons

## TODO:

- [X] GUI buttons (can be improved a lot)
    - [X] stroke/pen colors
    - [ ] stroke weight
    - [ ] drawing modes 
	
- [ ] save SVG with timestamp on name
	- [ ] save SVG to user selected file

- [ ] load & save drawing
	- HARDER: load SVG and parse elements to allow editing saved file
	- EASIER: save/load session data in a serialized file
		REALLY EASY: pickle
		I'd have to look: JSON

- [ ] modes & elements
	- [X] line
	- [X] circle
	- [X] "quad"/rectangle
	- [ ] triangle
	- [ ] polygon
	- [ ] select/edit mode
		- erase selected element
		- move
		- transform (**could be with the scroll wheel!**)
		   - rotate
		   - scale

- [ ] snapping
	- to grid / ruler
	- to objects (possibly very hard)

- [ ] other features:
	- import image - maybe hard
	- export raster image (PNG) - easy peasy
	- import / open SVG (hard if you want to edit things, easy otherwise)
	- layers (maybe hard)
	- zoom and pan (maybe hard...)
	- change background
	- resize the window (maybe nasty)
	
- [ ] two-key keyboard shortcuts (a bit of trouble)
	- cmd + s --> save
	- cmd + z --> undo (maybe hard, but I had some ideas...)
	- cmd + r --> redo (see above)
	- cmd + d --> duplicate selected / last drawn 
	


