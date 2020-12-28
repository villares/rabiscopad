# -*- coding: utf-8 -*-

B_RADIUS = 0

class Button():

    button_list = []
    display_on = True

    def __init__(self, x, y, w, h,
                 txt,
                 func,
                 txt_color=color(0),
                 fill_color=None,
                 ):
        self.x, self.y = x, y
        self.w, self.h = w, h
        self.txt = txt
        self.txt_color = txt_color
        self.pressed = False
        self.func = func
        self.active = False
        self.fill_color = fill_color or color(200, 200, 240)
        self.fill_color_active = self.darken_color(self.fill_color)
        self.button_list.append(self)

    def mouse_over(self):
        return (self.x < mouseX < self.x + self.w and
                self.y < mouseY < self.y + self.h)

    def display(self, mp):
        mouse_over = self.mouse_over()
        pushStyle()
        strokeWeight(1)
        stroke(0)
        fill(self.calc_fill(mouse_over))
        rectMode(CORNER)
        rect(self.x, self.y, self.w, self.h, B_RADIUS)
        fill(self.txt_color)
        textAlign(CENTER, CENTER)
        text(self.txt,
             self.x + self.w / 2,
             self.y + self.h / 2)
        if self.check(mouse_over, mp):
            self.func(self)
        popStyle()

    def check(self, mouse_over, mp):
        result = False
        if mouse_over and self.pressed and not mp:
            result = True
        if mouse_over and mp:
            self.pressed = True
        else:
            self.pressed = False
        return result

    def toggle(self):
        self.active = not self.active

    def exclusive_on(self):  # no toggle
        for b in self.button_list:
            b.active = False
        self.active = True

    def exclusive_on_and_toggle(self):
        if self.active:
            self.active = False
        else:
            for b in self.button_list:
                b.active = False
            self.active = True

    def calc_fill(self, mouse_over):
        if self.active and mouse_over:
            return self.darken_color(self.fill_color_active)
        elif self.active:
            return self.fill_color_active
        elif mouse_over:
            return self.darken_color(self.fill_color)
        else:
            return self.fill_color

    @staticmethod
    def darken_color(c):
        r, g, b = red(c), green(c), blue(c)
        return color(r * 0.66, g * 0.66, b * 0.66)

    @classmethod
    def display_all(cls, mp):
        if cls.display_on:
            for b in cls.button_list:
                b.display(mp)

class SColorButton(Button):
    button_list = []

    @classmethod
    def set_active(cls, c):
         for b in cls.button_list:
                if b.txt_color == c:
                    b.exclusive_on()                                
                
class ModeButton(Button):
    button_list = []
    
    @classmethod
    def set_active(cls, m):
         for b in cls.button_list:
                if b.txt == m[0]:
                    b.exclusive_on()
                
        
