import mdPyNode

class types(mdPyNode):
    """data types"""
     
    def int(self,x):
        """whole numbers"""
        return int(x)
    
    def float(self,x):
        """decimal numbers"""
        return float(x)
    
    def string(self,x):
        """letters and words"""
        return str(x)
    
    def bool(self,x):
        """true or false"""
        return boolean(x)
    
class math(mdPyNode):
    """Math Functions"""
    
    def add(self,first,second):
        """add two items"""
        return first + second
    
    def sub(self,first,second):
        """subtract two items"""
        return first - second
    
    def mult(self,first,second):
        """multiply two items"""
        return first * second
    
    def div(self,first,second):
        """divide two items"""
        return first/second