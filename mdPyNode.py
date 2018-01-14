

class mdPyNode():

    def __init__(self):
        self.inputDict = {}
        self.outputDict = {}
        self.inputConnections = {}
        self.outputConnections = {}
        self.function = lambda: False

    def do(self):
    	self.outputList = self.function(self.inputList)
    	for each in self.outputConnections:
    		each.do()

