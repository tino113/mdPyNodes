# node based editor for Python

# ask user for a folder to start creating in.
# scan the selected folder for files
# parse each .py file
# look for classes which inherit from the mdPyNode class
# for each function in this class create a 'node'

# draw a list of all options (grouped by class name) on the left
# draw nodes and allow for drag and drop
# allow connections between nodes
# generate python code in the background based on the configuration of nodes
# save these node configurations into a py file.
# allow users to create inputs (parameters) and outputs (return array)
# allow users to re-use all created code as a new node

# clicking on a node allows users to jump into another file and edit the code.
import os
import re
import mdPyNode
import importlib
import thread
from button import button
import time

isTyping = False
strInput = ''
pressedEnter = False


class mdPyNodeRender:

    def __init__(self):
        self.verbosity = 0
        self.optionsDict = {}
        self.tooltips = {}
        self.functions = {}
        self.inputs = {}
        self.outputs = {}
        self.maxWInputs = 15
        self.maxWOutputs = 15
        self.buttons = []
        self.sketchName = ''

    def parseFolders(self, f):
        pyFiles = []
        # walk through all folders and sub folders
        for root, dirs, files in os.walk(f):
            for f in files:
                # if the file is a python file
                if os.path.splitext(f)[1] == '.py':
                    pyFiles.append(f)
        return pyFiles

    def parseFiles(self, fs):
        nodes = {}

        # for each file in the list of files
        for f in fs:
            hasmdPy = False
            # split the file's name by the dot (name and ext)
            mname = re.split('\.', f)[0]
            # module = importlib.import_module(mname)
            # open the file
            c = ''
            func = ''
            with open(f, 'r') as fc:
                isClass = False
                for l in fc:
                    if l.find('class') >= 0 and l.find('(mdPyNode)') >= 0:
                        if not hasmdPy:
                            # add a new dictionary entry for the file
                            nodes.update({mname: {}})
                        hasmdPy = True
                        c = re.split('class |\(|:',l)[1]
                        nodes[mname].update({c: {}})
                        isClass = True
                    if l.find('def') >= 0 and hasmdPy and l.find('__init__') == -1:
                        func = re.split('def |\(|:',l)[1]
                        x = mdPyNode.mdPyNode()
                        nodes[mname][c].update({func:x})
                        #clss = getattr(module,c)
                        #print(module)
                        #print(clss)
                        #function = getattr(clss,func)
                        #self.functions.update({func:function})
                        isClass = False
                    if l.find('"""') >= 0:
                        tt = re.split('"""',l)[1]
                        if isClass:
                            self.tooltips.update({c:tt})   
                        else:
                            self.tooltips.update({func:tt}) 
        return nodes
        
    def parse(self):
        self.optionsDict = self.parseFiles(self.parseFolders(os.getcwd()))

    def doAddNewInput(self):
        global pressedEnter
        global inputs
        global strInput
        while not pressedEnter:
            time.sleep(0.1)
            pass
        pressedEnter = False
        self.inputs.update({strInput: 0})
        if strInput > self.maxWInputs:
            ig.textSize(15)
            self.maxWInputs = ig.textWidth(strInput + " >")
        strInput = ''
        pn.render(bg)
        
    def addNewInput(self):
        global ig
        global isTyping
        isTyping = True
        ig = createGraphics(width, height)
        ig.beginDraw()
        ig.clear()
        ig.background(color(0,0,0,200))
        ig.textSize(30)
        ig.fill(255)
        ig.textAlign(CENTER)
        st = "Please enter a name for your input"
        strInput = ''
        ig.text(st,width/2,height/2)
        ig.endDraw()
        image(ig,0,0)
        thread.start_new_thread( self.doAddNewInput, ())

    def doAddNewOutput(self):
        global pressedEnter
        global outputs
        global strInput
        while not pressedEnter:
            time.sleep(0.1)
            pass
        pressedEnter = False
        self.outputs.update({strInput: 0})
        if strInput > self.maxWOutputs:
            ig.textSize(15)
            self.maxWOutputs = ig.textWidth(strInput + " >")
        strInput = ''
        pn.render(bg)
    
    def addNewOutput(self):
        global ig
        global isTyping
        global strOutput
        isTyping = True
        ig = createGraphics(width, height)
        ig.beginDraw()
        ig.clear()
        ig.background(color(0,0,0,200))
        ig.textSize(30)
        ig.fill(255)
        ig.textAlign(CENTER)
        st = "Please enter a name for your output"
        strOutput = ''
        ig.text(st,width/2,height/2)
        ig.endDraw()
        image(ig,0,0)
        thread.start_new_thread( self.doAddNewOutput, ())

    def doRenameSketch(self):
        global pressedEnter
        while not pressedEnter:
            time.sleep(0.1)
            pass
        pressedEnter = False
        self.sketchName = strInput
        pn.render(bg)
            
    def renameSketch(self):
        global ig
        global isTyping
        global strInput
        isTyping = True
        ig = createGraphics(width, height)
        ig.beginDraw()
        ig.clear()
        ig.background(color(0,0,0,200))
        ig.textSize(30)
        ig.fill(255)
        ig.textAlign(CENTER)
        st = "Please enter a new name"
        if self.sketchName != '':
            st = self.sketchName
            strInput = st
        elif strInput != '':
            st = strInput
            strInput = ''
        ig.text(st,width/2,height/2)
        ig.endDraw()
        image(ig,0,0)
        thread.start_new_thread( self.doRenameSketch, ())
        
    def render(self,bg):
        global scrollOff
        self.buttons = []
        bg.beginDraw()
        bg.clear()
        bg.background(color(80))
        bg.noStroke()
        txth = 15
        bg.textSize(txth)
        
        # setup the library on the left
        bg.fill(color(255,255,255,50))
        bg.rect(0,0,100,height)
        
        # setup the input and output areas
        bg.fill(color(255,255,255,80))
        bg.rect(100,0,self.maxWInputs + 4,height)
        bg.rect(width-self.maxWOutputs - 4,0,self.maxWOutputs + 4 * txth,height)
        bg.fill(color(255))
        bg.text("+",101,txth)
        self.buttons.append(button(self.addNewInput,100,0,txth,txth,'add a new input'))

        lineCount = 0
        for inpt in self.inputs:
            print(inpt)
            bg.fill(color(200))
            bg.text(inpt,102,lineCount + 5 + 15 * 2)
            bg.fill(color(220))
            bg.ellipse(95+self.maxWInputs, lineCount + 1 + 15 * 2, 8, 8)
            lineCount += 16

        lineCount = 0
        for outpt in self.outputs:
            print(outpt)
            bg.fill(color(200))
            bg.text(outpt,width-self.maxWOutputs +10,lineCount + 5 + 15 * 2)
            bg.fill(color(220))
            bg.ellipse(width-self.maxWOutputs + 2, lineCount + 1 + 15 * 2, 8, 8)
            lineCount += 16

        bg.text("+",width-txth+1,txth)
        self.buttons.append(button(self.addNewOutput,width-txth,0,txth,txth,'add a new output'))
        
        # setup the main stage
        bg.fill(color(255,255,255,80))
        wt = 100
        if ig.textWidth(self.sketchName) > 100:
            ig.textSize(15)
            wt = ig.textWidth(self.sketchName) + 4
        bg.rect(100 + self.maxWInputs + 4 + 5,5,wt,txth + 4)
        bg.fill(color(255))
        bg.text(self.sketchName,100 + self.maxWInputs + 4 + 7,txth+5)
        self.buttons.append(button(self.renameSketch,100 + self.maxWInputs + 4 + 5,5,wt,txth,'rename the sketch'))
        
        lineY = 0 + scrollOff
        bg.fill(color(255))
        for x in range(len(self.optionsDict)):
            fl = self.optionsDict.keys()[x]
            bg.text("+ " + self.optionsDict.keys()[x],5,lineY + txth)
            lineY += txth + 3
            for y in range(len(self.optionsDict[fl])):
                cl = self.optionsDict[fl].keys()[y]
                bg.text("+ " + self.optionsDict[fl].keys()[y],20,lineY + txth)
                self.buttons.append(button(lambda: False,20,lineY,textWidth("+ " + cl)+8,txth,self.tooltips[cl]))
                lineY += txth + 3
                for z in range(len(self.optionsDict[fl][cl])):
                    funName = self.optionsDict[fl][cl].keys()[z]
                    bg.text("- " + funName,30,lineY + txth)
                    self.buttons.append(button(lambda: False,30,lineY,textWidth("- " + funName)+8,txth,self.tooltips[funName]))
                    lineY += txth + 1
        bg.endDraw()
        image(bg,0,0)
        
        
pn = ''
pg = '' #Buttons
bg = '' #Background
ig = '' #Input
dragged = ''
mStart = PVector(0,0)
prevW = 0
prevH = 0
scrollOff = 0
tooltipDisplayed = False

def setup():
    global pn
    global nodes
    global pg
    global bg
    global ig
    global prevW
    global prevH
    size(1000,500)
    prevW = width
    prevH = height
    pg = createGraphics(width, height)
    bg = createGraphics(width, height)
    ig = createGraphics(width, height)
    this.surface.setResizable(True)
    pn = mdPyNodeRender()
    pn.parse()
    pn.render(bg)
    
def draw():
    global pg
    global prevW
    global prevH
    global bg
    global ig
    global tooltipDisplayed
    over = False
    for button in pn.buttons:
        button.over(pg)
    clear()
    image(bg,0,0)
    image(pg,0,0)
    image(ig,0,0)
    if prevW != width or prevH != height:
        bg = createGraphics(width, height)
        pn.render(bg)
    prevW = width
    prevH = height

def mouseClicked():
    for button in pn.buttons:
        if button.hover == True:
            button.onClick()
            
def mousePressed():
    global dragged
    global mStart
    mStart = PVector(mouseX,mouseY)
    for button in pn.buttons:
        if button.hover == True:
            dragged = button
    
def mouseReleased():
    if PVector.dist(mStart,PVector(mouseX,mouseY)) < 5:
        #deal with it in click...
        pass
    else:
        print(dragged)

def mouseWheel(event):
    global scrollOff
    e = event.getCount()
    scrollOff += e * 2
    if scrollOff < 0:
        scrollOff = 0
    pn.render(bg)
    
def keyPressed():
    global ig
    global strInput
    global pressedEnter
    if isTyping == True:
        ig.beginDraw()
        ig.clear()
        ig.background(color(0,0,0,200))
        if key == ENTER:
            isTyping == False
            ig.clear()
            ig.endDraw()
            pressedEnter = True
            return
        elif key == BACKSPACE:
            strInput = strInput[:-1]
        else:
            strInput += key
        ig.textSize(30)
        ig.fill(255)
        ig.textAlign(CENTER)
        ig.text(strInput,width/2,height/2)
            
        ig.endDraw()
            
    
            