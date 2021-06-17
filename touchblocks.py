"""
insert doc here
"""
__version__ = '1.0'

import kivy
kivy.require('1.0.6')

from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.stencilview import StencilView
from kivy.uix.button import Button
from kivy.uix.image import Image

from kivy.uix.label import Label
from kivy.graphics import Color, Rectangle, Point, GraphicException, Line
from kivy.core.window import Window

from kivy.clock import Clock 

from random import random
from math import sqrt

assetPrefix = "assets/png/"
pathBoxEmpty = assetPrefix+'box_empty.png'
pathBoxBlue = assetPrefix+'box_blue.png'
pathBoxRed = assetPrefix+'box_red.png'
pathPyramidOrange = assetPrefix+'pyramid_orange.png'
pathTriangleGreenLeft = assetPrefix+'triangle_green_left.png'
pathTriangleGreenRight = assetPrefix+'triangle_green_right.png'
pathTriangleYellowLeft = assetPrefix+'triangle_yellow_left.png'
pathTriangleYellowRight = assetPrefix+'triangle_yellow_right.png'

# global variables for control
selectedBlock = None
compareTargetTrigger = None

class TouchableBlock(RelativeLayout):
    def __init__(self, source=pathBoxEmpty, **kwargs):
        super(TouchableBlock, self).__init__(**kwargs)
        gridImage = Image(source=source)
        self.add_widget(gridImage)

        self.displayedBlock = None

    def displayBlock(self, source):
        img = Image(source=source)
        self.add_widget(img)
        self.displayedBlock = source

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
          return True
        return False

    def on_touch_up(self, touch):
        global selectedBlock
        if self.collide_point(*touch.pos):
            if self.displayedBlock is not None:
              selectedBlock = self.displayedBlock

            if self.displayedBlock is None and selectedBlock is not None:
              self.displayBlock(selectedBlock)
              selectedBlock = None

            if compareTargetTrigger:
                compareTargetTrigger()
            return True
        return False

    # def on_touch_move(self, touch):
    #     print("moving")
    #     return True



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
        self.bottomGridLayout.width = Window.height/2 * 1.5 # bottom buttons scaling factor
        self.bottomGridLayout.height = Window.height/3
        self.topGridSourceLayout.height = Window.height/2
        self.topGridSourceLayout.width = self.topGridSourceLayout.height
        self.topGridTargetLayout.height = Window.height/2
        self.topGridTargetLayout.width = self.topGridTargetLayout.height        
        return True

    def setTargetPattern(self, pattern="default"):
        if pattern == "default":
            self.sourceGridTouchableArray[2].displayBlock(pathPyramidOrange)
            self.sourceGridTouchableArray[8].displayBlock(pathBoxBlue)
            self.sourceGridTouchableArray[14].displayBlock(pathBoxRed)
            self.sourceGridTouchableArray[20].displayBlock(pathBoxBlue)
            self.sourceGridTouchableArray[26].displayBlock(pathBoxRed)
            self.sourceGridTouchableArray[27].displayBlock(pathTriangleGreenLeft)
            self.sourceGridTouchableArray[33].displayBlock(pathTriangleYellowRight)
            self.sourceGridTouchableArray[25].displayBlock(pathTriangleGreenRight)
            self.sourceGridTouchableArray[31].displayBlock(pathTriangleYellowLeft)

    def compareTargetPatterns(self, evt):
        theyAreEqual = True
        for i,sourceTouchable in enumerate(self.sourceGridTouchableArray):
            targetTouchable = self.targetGridTouchableArray[i]
            if sourceTouchable.displayedBlock != targetTouchable.displayedBlock:
                theyAreEqual = False

        if theyAreEqual:
            print("TARGET PATTERN")
        return theyAreEqual

    def build(self):

        # return TouchBlocks()
        # create a default grid layout with custom width/height
        self.mainLayout = FloatLayout()

        self.topGridsLayout = GridLayout(cols=2, size_hint=(None,None))
        self.bottomGridLayout = GridLayout(cols=7, size_hint=(None,None))

        self.topGridSourceLayout = GridLayout(cols=6, rows=6, size_hint=(None,None))
        self.topGridTargetLayout = GridLayout(cols=6, rows=6, size_hint=(None,None))

        self.topGridsLayout.width = Window.width
        self.topGridsLayout.height = Window.height/3*2
        self.bottomGridLayout.width = Window.height/2 * 1.5 # bottom buttons scaling factor
        self.bottomGridLayout.height = Window.height/3

        self.topGridSourceLayout.height = Window.height/2
        self.topGridTargetLayout.height = Window.height/2
        self.topGridSourceLayout.width = self.topGridSourceLayout.height
        self.topGridTargetLayout.width = self.topGridTargetLayout.height   

        topGridSourceAnchorLayout = AnchorLayout(anchor_x='center', anchor_y='center')
        topGridTargetAnchorLayout = AnchorLayout(anchor_x='center', anchor_y='center')
        topGridSourceAnchorLayout.add_widget(self.topGridSourceLayout)
        topGridTargetAnchorLayout.add_widget(self.topGridTargetLayout)
        
        self.topGridsLayout.add_widget(topGridSourceAnchorLayout)
        self.topGridsLayout.add_widget(topGridTargetAnchorLayout)

        topGridsAnchorLayout = AnchorLayout(anchor_x='center', anchor_y='top')
        bottomGridAnchorLayout = AnchorLayout(anchor_x='center', anchor_y='bottom')
        topGridsAnchorLayout.add_widget(self.topGridsLayout)
        bottomGridAnchorLayout.add_widget(self.bottomGridLayout)

        self.mainLayout.add_widget(topGridsAnchorLayout)
        self.mainLayout.add_widget(bottomGridAnchorLayout)


        # add buttons into topGridSourceLayout
        self.sourceGridTouchableArray = []
        self.targetGridTouchableArray = []

        for i in range(36):
            wimg = TouchableBlock()
            self.sourceGridTouchableArray.append(wimg)
            self.topGridSourceLayout.add_widget(wimg)
        # add buttons into topGridTargetLayout 
        for i in range(36):
            wimg = TouchableBlock()
            self.targetGridTouchableArray.append(wimg)
            self.topGridTargetLayout.add_widget(wimg)

        # add buttons into bottomGridLayout 
        wimg = TouchableBlock()
        wimg.displayBlock(pathTriangleGreenLeft)
        self.bottomGridLayout.add_widget(wimg)

        wimg = TouchableBlock()
        wimg.displayBlock(pathTriangleGreenRight)
        self.bottomGridLayout.add_widget(wimg)

        wimg = TouchableBlock()
        wimg.displayBlock(pathTriangleYellowLeft)
        self.bottomGridLayout.add_widget(wimg)

        wimg = TouchableBlock()
        wimg.displayBlock(pathTriangleYellowRight)
        self.bottomGridLayout.add_widget(wimg)

        wimg = TouchableBlock()
        wimg.displayBlock(pathBoxRed)
        self.bottomGridLayout.add_widget(wimg)

        wimg = TouchableBlock()
        wimg.displayBlock(pathPyramidOrange)
        self.bottomGridLayout.add_widget(wimg)

        wimg = TouchableBlock()
        wimg.displayBlock(pathBoxBlue)
        self.bottomGridLayout.add_widget(wimg)

        # show target pattern
        self.setTargetPattern(pattern="default")
        global compareTargetTrigger
        compareTargetTrigger = Clock.create_trigger(self.compareTargetPatterns)        

        return self.mainLayout

    def on_pause(self):
        return True

if __name__ == '__main__':
    TouchBlocksApp().run()