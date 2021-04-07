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












class Grid():
    def __init__(self, canvas, gridDim=[6,6], gridPos=[0,0], gridSize=[100,100]):
        self.gridDim = gridDim
        self.gridPos = gridPos
        self.gridSize = gridSize

        self.canvas = canvas

    def draw(self):
        with self.canvas:
            Color(0,0,0)

            for i in range(self.gridDim[0]):
                for j in range(self.gridDim[1]):
                    distanceX = self.gridSize[0] / self.gridDim[0]
                    distanceY = self.gridSize[1] / self.gridDim[1]
                    x1 = self.gridPos[0] + (distanceX * i)
                    x2 = self.gridPos[0] + (distanceX * i) + self.gridSize[0]
                    y1 = self.gridPos[1] + (distanceY * j)
                    y2 = self.gridPos[1] + (distanceY * j) + self.gridSize[1]
                    Line(points=[x1, y1, x1, y2], width=1)        
                    Line(points=[x1, y1, x2, y1], width=1)






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

    def build(self):
        Window.clearcolor = (1, 1, 1, 1)
        # return TouchBlocks()
        # create a default grid layout with custom width/height
        mainLayout = GridLayout(cols=1, padding=10, spacing=10)

        topGridsLayout = GridLayout(cols=2, padding=10, spacing=10)
        bottomGridLayout = GridLayout(cols=6, padding=10, spacing=10)

        topGridSourceLayout = GridLayout(cols=6, rows=6, padding=10, spacing=0)
        topGridTargetLayout = GridLayout(cols=6, rows=6, padding=10, spacing=0)

        # when we add children to the grid layout, its size doesn't change at
        # all. we need to ensure that the height will be the minimum required
        # to contain all the childs. (otherwise, we'll child outside the
        # bounding box of the childs)
        # mainLayout.bind(minimum_height=mainLayout.setter('height'))
        # topGridsLayout.bind(minimum_height=topGridsLayout.setter('height'))
        # bottomGridLayout.bind(minimum_height=bottomGridLayout.setter('height'))
        # topGridSourceLayout.bind(minimum_height=topGridSourceLayout.setter('height'))
        # topGridTargetLayout.bind(minimum_height=topGridTargetLayout.setter('height'))

        # add layouts to each other
        mainLayout.add_widget(topGridsLayout)
        mainLayout.add_widget(bottomGridLayout)

        topGridsLayout.add_widget(topGridSourceLayout)
        topGridsLayout.add_widget(topGridTargetLayout)

        # add buttons into topGridSourceLayout 
        for i in range(36):
            wimg = Image(source='assets/png/box_empty.png')
            topGridSourceLayout.add_widget(wimg)
        # add buttons into topGridTargetLayout 
        for i in range(36):
            wimg = Image(source='assets/png/box_empty.png')
            topGridTargetLayout.add_widget(wimg)

        # add buttons into bottomGridLayout 
        for i in range(6):
            wimg = Image(source='assets/png/box_empty.png')
            bottomGridLayout.add_widget(wimg)

        # create a scroll view, with a size < size of the grid
        # root = ScrollView(size_hint=(None, None), size=(500, 320),
        #         pos_hint={'center_x': .5, 'center_y': .5}, do_scroll_x=True)
        # root.add_widget(layout)

        return mainLayout

    def on_pause(self):
        return True

if __name__ == '__main__':
    TouchBlocksApp().run()