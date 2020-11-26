
import pygame as pg
pg.init()
pg.font.init()
screen=pg.display.set_mode((500, 500))

font=pg.font.SysFont("Times new roman", 25)
clock = pg.time.Clock()

class Box():
        def __init__(self, pos_, size_=None):
            if size_ is None:
                size_ = [100, 100]
            self.size = size_
            self.pos=pos_
            self.color=(100, 100, 100)
        def draw(self):
            pg.draw.rect(screen, self.color, (self.pos, (50, 50)))
class Box_value():
        def __init__(self, pos_, size_=None, value_=None):
            if value_==None:
                self.value = value_=0.
            self.pos=pos_
            self.size=size_
            self.value=value_
        def draw(self, t=None):
            value_text=font.render(str(self.value), False, (255, 0, 0))
            screen.blit(value_text, self.pos)
class Node():
    def __init__(self, pos_, size_, value_):
        self.box=Box(pos_, size_)
        self.box_value=Box_value(pos_, size_, value_)
    def draw(self):
        self.box.draw()
        self.box_value.draw()

