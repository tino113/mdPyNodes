

class mdPyNode():

    def __init__(self):
        self.name = 'mdPyNode'
        self.loc = PVector(0,0)
        self.inputDict = {}
        self.outputDict = {}
        self.inputConnections = {}
        self.outputConnections = {}
        self.function = lambda: False

    def __str__(self):
        s = "Inputs: " + str(self.inputDict)
        s += "Outputs: " + str(self.outputDict)
        s += "function: " + str(self.function)
        return s

    def __repr__(self):
        s = "Inputs: " + str(self.inputDict)
        s += " Outputs: " + str(self.outputDict)
        s += " function: " + str(self.function)
        return s

    def __call__(self):
        print(self)
        pass

    def draw(self,layer):
        maxLH = (len(self.inputDict) + len(self.outputDict)) * 14 + 20
        wdth = 100
        layer.noStroke()
        layer.fill(255)
        layer.rect(0,0,wdth,maxLH,10,10,10,10)
        layer.fill(0)
        layer.text(self.name,5,15)
        lineHL = 25
        lineHR = 25
        for i in range(len(self.inputDict)):
            layer.ellipse(8,lineHL,8,8)
            layer.text(self.inputDict.keys()[i],16,lineHL+4)
            lineHL += 14

        for j in range(len(self.outputDict)):
            layer.ellipse(92,lineHL,8,8)
            tw = layer.textWidth(self.outputDict.keys()[j])
            layer.text(self.outputDict.keys()[j],92-8-tw,lineHL+4)
            lineHL += 14
        return (wdth,maxLH)

    def do(self):
        self.outputList = self.function(self.inputList)
        for each in self.outputConnections:
            each.do()