## RabiscoPad

A bare-bones SVG sketchpad - Licensed under GPL v3.0

Developed by [Alexandre B A Villares](http://twitter.com/villares) and [Foad S. Farimani](https://twitter.com/fsfarimani)

![image1](docs/assets/readme_animation1.gif)
![image2](docs/assets/readme_animation2.gif)

### Keyboard shortcuts:

- <kbd>s</kbd> save SVG
- <kbd>c</kbd> draw circle
- <kbd>l</kbd> draw line
- <kbd>Space</kbd> fre hand draw mode

## change log:

- v2020_12_19 exporting SVG now!
- v2020_12_20 line mode & circle mode

## TODO:

- [ ] GUI buttons
	- [ ] pen colors 
        - [ ] weight and mode buttons
- [ ] selection mode
- [ ] save SVG with timestamp on name
	- [ ] save SVG to user selected file

- [ ] load & save drawing
	- HARDER: load SVG and parse elements to allow editing saved file
	- EASIER: save/load session data in a serialized file
		REALLY EASY: pickle
		I'd have to look: JSON

- [ ] elements
	- rectangle
	- triangle
	- polygon

- [ ] snapping
	- ruler
	- ? objects (possibly very hard)

- [ ] features:
	- import image - maybe hard
	- export raster image (PNG) - easy peasy
	- import / open SVG (HARD)
	- layers (maybe hard)
	- zoom and pan (maybe hard...)
	- change background
	- resize the window (maybe hard)
	- selection
		- erase selected element
		- move
		- transform / rotate

- [ ] keyboard shortcuts
	- cmd + s --> save
	- cmd + z --> undo
	- cmd + r --> redo
	- cmd + d --> duplicate selected / last drawn
	- 


