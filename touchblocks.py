"""
insert doc here
"""
__version__ = '1.0'

import kivy
kivy.require('1.0.6')

from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.stencilview import StencilView
from kivy.uix.button import Button
from kivy.uix.image import Image

from kivy.uix.label import Label
from kivy.graphics import Color, Rectangle, Point, GraphicException, Line
from kivy.core.window import Window
from random import random
from math import sqrt

class TouchBlocks(FloatLayout):
    def __init__(self):
        super(TouchBlocks, self).__init__()

        # subscribe to window resize event
        Window.bind(on_resize=self.on_resize)
        # initialize background color
        Window.clearcolor = (1, 1, 1, 1)
        
        # initialize elements
        self.elements = [Grid(self.canvas)]

        # draw first frame
        self.draw()

    def draw(self):
        with self.canvas:
            self.canvas.clear()

            for element in self.elements:
                element.draw()
                 

    def on_resize(self, window, width, height):
        #self.gridSize = [width, height]
        self.draw()
        return True

    def on_touch_down(self, touch):
        with self.canvas:
            Color(1.0, 0.0, 0.0)
            Rectangle(pos=(touch.x-5, touch.y-5), size=(10, 10))
        return True

    def on_touch_move(self, touch):
        with self.canvas:
            Color(0.0, 1.0, 0.0)
            Rectangle(pos=(touch.x, touch.y), size=(2, 2))
        return True

    def on_touch_up(self, touch):
        with self.canvas:
            Color(0.0, 0.0, 1.0)
            Rectangle(pos=(touch.x-5, touch.y-5), size=(10, 10))
        return True


class TouchBlocksApp(App):
    title = 'Touch Blocks'

    def __init__(self):
        super(TouchBlocksApp, self).__init__()

        # Window init
        Window.clearcolor = (1, 1, 1, 1)
        Window.bind(on_resize=self.on_resize)


    def on_resize(self, window, width, height):
        self.topGridsLayout.width = Window.width
        self.topGridsLayout.height = Window.height/3*2
        self.bottomGridLayout.width = Window.height/2
        self.topGridSourceLayout.height = Window.height/2
        self.topGridSourceLayout.width = self.topGridSourceLayout.height
        self.topGridTargetLayout.height = Window.height/2
        self.topGridTargetLayout.width = self.topGridTargetLayout.height        
        return True

    def build(self):

        # return TouchBlocks()
        # create a default grid layout with custom width/height
        self.mainLayout = GridLayout(cols=1)

        self.topGridsLayout = GridLayout(cols=2, size_hint=(None,None))
        self.bottomGridLayout = GridLayout(cols=6, size_hint=(None,1))

        self.topGridSourceLayout = GridLayout(cols=6, rows=6, size_hint=(None,None))
        self.topGridTargetLayout = GridLayout(cols=6, rows=6, size_hint=(None,None))

        self.topGridsLayout.width = Window.width
        self.topGridsLayout.height = Window.height/3*2
        self.bottomGridLayout.width = Window.height/2 * 1.5 # bottom buttons scaling factor

        self.topGridSourceLayout.height = Window.height/2
        self.topGridTargetLayout.height = Window.height/2
        self.topGridSourceLayout.width = self.topGridSourceLayout.height
        self.topGridTargetLayout.width = self.topGridTargetLayout.height   

        topGridSourceAnchorLayout = AnchorLayout(anchor_x='center', anchor_y='center')
        topGridTargetAnchorLayout = AnchorLayout(anchor_x='center', anchor_y='center')
        bottomGridAnchorLayout = AnchorLayout(anchor_x='center', anchor_y='center')
        topGridSourceAnchorLayout.add_widget(self.topGridSourceLayout)
        topGridTargetAnchorLayout.add_widget(self.topGridTargetLayout)
        bottomGridAnchorLayout.add_widget(self.bottomGridLayout)
        
        self.topGridsLayout.add_widget(topGridSourceAnchorLayout)
        self.topGridsLayout.add_widget(topGridTargetAnchorLayout)

        self.mainLayout.add_widget(self.topGridsLayout)
        self.mainLayout.add_widget(bottomGridAnchorLayout)


        # add buttons into topGridSourceLayout 
        for i in range(36):
            wimg = Image(source='assets/png/box_empty.png')
            self.topGridSourceLayout.add_widget(wimg)
        # add buttons into topGridTargetLayout 
        for i in range(36):
            wimg = Image(source='assets/png/box_empty.png')
            self.topGridTargetLayout.add_widget(wimg)

        # add buttons into bottomGridLayout 
        for i in range(6):
            wimg = Image(source='assets/png/box_empty.png')
            self.bottomGridLayout.add_widget(wimg)


        pyramid = Image(source='assets/png/pyramid_orange.png', pos_hint=(1,1))
        wimg.add_widget(pyramid)

        # create a scroll view, with a size < size of the grid
        # root = ScrollView(size_hint=(None, None), size=(500, 320),
        #         pos_hint={'center_x': .5, 'center_y': .5}, do_scroll_x=True)
        # root.add_widget(layout)

        return self.mainLayout



    def on_pause(self):
        return True

if __name__ == '__main__':
    TouchBlocksApp().run()