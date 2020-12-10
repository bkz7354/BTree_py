import pygame as pg
import pygame_gui as pgui
import math


def truncate(number, digits):
    stepper = 10.0 ** digits
    return math.trunc(stepper * number) / stepper


class InterfaceManager:
    """
    class that manages the GUI and provides user input to the program
    using get_speed method and is_running variable
    """

    def __init__(self, screen, theme_path):
        self.screen = screen
        # this variable tells whether the simulation is running right now
        self.is_running = False
        self.window_width = screen.get_width()
        self.window_height = screen.get_height()

        self.manager = pgui.UIManager((self.window_width, self.window_height), theme_path)

        self.init_text_entry()
        self.init_buttons()
        self.init_speed_slider([0.0, 3.0])


    def init_text_entry(self):
        textRect = pg.Rect(0, 0, 180, 29)
        textRect.bottomleft = (10, -10)
    
        self.textEntry = pgui.elements.UITextEntryLine(
                                      textRect, self.manager,
                                      anchors={'left': 'left',
                                               'right': 'left',
                                               'top': 'bottom',
                                               'bottom': 'bottom'})
        
        self.textEntry.set_allowed_characters('numbers')
        self.textEntry.set_text_length_limit(4)

    def init_buttons(self):
        buttonRect = pg.Rect(0, 0, 90, 29)

        self.insertButton = self.init_button_bottomleft(buttonRect, (210, -10), 'Insert')
        self.removeButton = self.init_button_bottomleft(buttonRect, (310, -10), 'Remove')
        self.insertRandomButton = self.init_button_bottomleft(buttonRect, (410, -10), 'RNG Insert')
        self.removeRandomButton = self.init_button_bottomleft(buttonRect, (510, -10), 'RNG Remove')

    def init_button_bottomleft(self, rect, pos, text):
        """
        inits button in such a way that it is placed relative to the bottom left corner
        """
        buttonRect = rect.copy()
        buttonRect.bottomleft = pos
        return pgui.elements.UIButton(relative_rect=buttonRect,
                                      text=text, manager=self.manager,
                                      anchors={'left': 'left',
                                               'right': 'left',
                                               'top': 'bottom',
                                               'bottom': 'bottom'})

    
    def init_speed_slider(self, speed_range):
        """
        initiates speed slider and display label
        """
        anchors = {'left': 'right',
                   'right': 'right',
                   'top': 'bottom',
                   'bottom': 'bottom'}


        labelRect = pg.Rect((0, 0, 120, 29))
        labelRect.bottomright = (-10, -10)
        self.speedLabel = pgui.elements.UILabel(labelRect, "speed: 1", 
                                                self.manager, anchors=anchors)
        
        sliderRect = pg.Rect((0, 0, 200, 29))
        sliderRect.bottomright = (-140, -10)
        self.speedSlider = pgui.elements.UIHorizontalSlider(sliderRect, 1, 
                                                            speed_range, self.manager,
                                                            anchors=anchors)

    def process_event(self, event):
        self.manager.process_events(event)

        if event.type == pg.USEREVENT:
            pass

    def get_speed(self):
        return self.speedSlider.get_current_value()

    def update_displayed_speed(self):
        self.speedLabel.set_text("speed: " + str(truncate(self.get_speed(), 1)))
            
    def update(self, time_delta):
        self.update_displayed_speed()
        self.manager.update(time_delta)
        self.manager.draw_ui(self.screen)


