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
from kivy.config import Config
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
dragAndDropWidget = None

Config.set('graphics','show_cursor','0')
Config.write()

class TouchableBlock(RelativeLayout):
    def __init__(self, source=pathBoxEmpty, **kwargs):
        super(TouchableBlock, self).__init__(**kwargs)
        gridImage = Image(source=source)
        self.add_widget(gridImage)

        self.pickable = False
        self.immutable = False

        self.displayedBlock = None
        self.displayedWidget = None

    def displayBlock(self, source):
        self.clearBlock()
        img = Image(source=source)
        self.add_widget(img)
        self.displayedBlock = source
        self.displayedWidget = img

    def clearBlock(self):
        if self.displayedWidget is not None:
            self.remove_widget(self.displayedWidget)
        self.displayedBlock = None
        self.displayedWidget = None

    def on_touch_down(self, touch):
        global selectedBlock
        if self.collide_point(*touch.pos):
          if self.displayedBlock is not None and self.pickable is True:
            selectedBlock = self.displayedBlock
          return True
        return False

    def on_touch_up(self, touch):
        global dragAndDropWidget, selectedBlock
        if self.collide_point(*touch.pos):            
            if selectedBlock is not None and self.immutable is False:
              self.displayBlock(selectedBlock)
              selectedBlock = None

            elif selectedBlock is None and self.immutable is False:
              self.clearBlock()
            
            elif self.displayedBlock is not None and self.pickable is True:
              selectedBlock = self.displayedBlock

            if compareTargetTrigger:
                compareTargetTrigger()
            return True
        return False

    def on_touch_move(self, touch):
        global dragAndDropWidget, selectedBlock
        if self.collide_point(*touch.pos):
            if dragAndDropWidget is None and selectedBlock is not None and self.pickable is True:
                dragAndDropWidget = Image(source=selectedBlock, size=(80,80), size_hint=(None,None))
                Window.add_widget(dragAndDropWidget)

            if dragAndDropWidget is not None:
                dragAndDropWidget.pos[0] = touch.pos[0]-40
                dragAndDropWidget.pos[1] = touch.pos[1]-40

            return True
        else:
            if dragAndDropWidget is not None:
                dragAndDropWidget.pos[0] = touch.pos[0]-40
                dragAndDropWidget.pos[1] = touch.pos[1]-40
            return False



class TouchBlocksApp(App):
    title = 'Touch Blocks'

    def __init__(self):
        super(TouchBlocksApp, self).__init__()

        # Window init
        Window.clearcolor = (1, 1, 1, 1)
        Window.bind(on_resize=self.on_resize)
        Window.bind(on_touch_up=self.on_touch_up)

    def on_resize(self, window, width, height):
        self.topGridsLayout.width = Window.width
        self.topGridsLayout.height = Window.height/3*2
        self.bottomGridLayout.width = Window.height/2 * 1.5 # bottom buttons scaling factor
        self.bottomGridLayout.height = Window.height/3
        self.topGridSourceLayout.height = Window.height/1.5
        self.topGridTargetLayout.height = Window.height/1.5
        self.topGridSourceLayout.width = self.topGridSourceLayout.height
        self.topGridTargetLayout.width = self.topGridTargetLayout.height        
        return True

    def on_touch_up(self, touch, window):
        global dragAndDropWidget
        if dragAndDropWidget is not None:
            Window.remove_widget(dragAndDropWidget)
            dragAndDropWidget = None
        return False

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
            print("TARGET PATTERN -- LOCKING ALL")
            for blk in self.targetGridTouchableArray:
                blk.immutable = True

        return theyAreEqual

    def getLabelWidget(self, text, size=28):
        return Label(text='[size='+str(size)+'][font=assets/fonts/computermodern-italic.ttf][color=000000]'+text+'[/color][/font][/size]', markup=True)

    def getHeaderLabelWidget(self, text, size=36):
        return Label(text='[size='+str(size)+'][font=assets/fonts/computermodern-normal.ttf][color=000000]'+text+'[/color][/font][/size]', markup=True)

    def build(self):
        # return TouchBlocks()
        # create a default grid layout with custom width/height
        self.mainLayout = FloatLayout()

        self.topGridsLayout = GridLayout(cols=2, size_hint=(None,None))
        self.bottomGridLayout = GridLayout(cols=8, rows=3, size_hint=(None,None), padding=[-40,40])

        self.topGridsLayout.width = Window.width
        self.topGridsLayout.height = Window.height/3*2
        self.bottomGridLayout.width = Window.height/2 * 1.5 # bottom buttons scaling factor
        self.bottomGridLayout.height = Window.height/3

        self.topGridSourceLayout = GridLayout(cols=8, rows=8, size_hint=(None,None))
        self.topGridTargetLayout = GridLayout(cols=8, rows=8, size_hint=(None,None))

        self.topGridSourceLayout.height = Window.height/1.5
        self.topGridTargetLayout.height = Window.height/1.5
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

        self.sourceGridTouchableArray = []
        self.targetGridTouchableArray = []

        self.topGridSourceLayout.add_widget(self.getLabelWidget('A.'))
        for _ in range(7):
            self.topGridSourceLayout.add_widget(self.getLabelWidget(''))

        self.topGridSourceLayout.add_widget(self.getLabelWidget(''))
        self.topGridSourceLayout.add_widget(self.getLabelWidget('a'))
        self.topGridSourceLayout.add_widget(self.getLabelWidget('b'))
        self.topGridSourceLayout.add_widget(self.getLabelWidget('c'))
        self.topGridSourceLayout.add_widget(self.getLabelWidget('d'))
        self.topGridSourceLayout.add_widget(self.getLabelWidget('e'))
        self.topGridSourceLayout.add_widget(self.getLabelWidget('f'))

        # add buttons into topGridSourceLayout 
        for i in range(6):
            self.topGridSourceLayout.add_widget(self.getLabelWidget(''))
            self.topGridSourceLayout.add_widget(self.getLabelWidget(str(i+1)))
            for _ in range(6):
                wimg = TouchableBlock()
                wimg.immutable = True
                self.sourceGridTouchableArray.append(wimg)
                self.topGridSourceLayout.add_widget(wimg)


        self.topGridTargetLayout.add_widget(self.getLabelWidget('B.'))
        for _ in range(7):
            self.topGridTargetLayout.add_widget(self.getLabelWidget(''))

        self.topGridTargetLayout.add_widget(self.getLabelWidget(''))
        self.topGridTargetLayout.add_widget(self.getLabelWidget('a\''))
        self.topGridTargetLayout.add_widget(self.getLabelWidget('b\''))
        self.topGridTargetLayout.add_widget(self.getLabelWidget('c\''))
        self.topGridTargetLayout.add_widget(self.getLabelWidget('d\''))
        self.topGridTargetLayout.add_widget(self.getLabelWidget('e\''))
        self.topGridTargetLayout.add_widget(self.getLabelWidget('f\''))

        # add buttons into topGridTargetLayout 
        for i in range(6):
            self.topGridTargetLayout.add_widget(self.getLabelWidget(''))
            self.topGridTargetLayout.add_widget(self.getLabelWidget(str(i+1)+'\''))
            for _ in range(6):
                wimg = TouchableBlock()
                self.targetGridTouchableArray.append(wimg)
                self.topGridTargetLayout.add_widget(wimg)



        # add buttons into bottomGridLayout
        self.bottomGridLayout.add_widget(self.getLabelWidget('C.'))
        for _ in range(7):
            self.bottomGridLayout.add_widget(self.getLabelWidget(''))

        self.bottomGridLayout.add_widget(self.getLabelWidget(''))
        self.bottomGridLayout.add_widget(self.getLabelWidget('t'))
        self.bottomGridLayout.add_widget(self.getLabelWidget('u'))
        self.bottomGridLayout.add_widget(self.getLabelWidget('v'))
        self.bottomGridLayout.add_widget(self.getLabelWidget('w'))
        self.bottomGridLayout.add_widget(self.getLabelWidget('x'))
        self.bottomGridLayout.add_widget(self.getLabelWidget('y'))
        self.bottomGridLayout.add_widget(self.getLabelWidget('z'))
        self.bottomGridLayout.add_widget(self.getLabelWidget(''))

        touchableBlocks = [pathTriangleGreenLeft, 
                           pathTriangleGreenRight, 
                           pathTriangleYellowLeft, 
                           pathTriangleYellowRight, 
                           pathBoxRed, 
                           pathPyramidOrange, 
                           pathBoxBlue]

        for touchableBlock in touchableBlocks:
            wimg = TouchableBlock()
            wimg.displayBlock(touchableBlock)
            wimg.immutable = True
            wimg.pickable = True
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