import datetime


class button():
    
    def __init__(self,function=lambda: False,x=0,y=0,w=0,h=0,tooltip='',tooltipTime=0.5,btype = 'button'):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.tooltip = tooltip
        self.hover = False
        self.hoverStart = 0
        self.tooltipTime = tooltipTime
        self.tooltipDisplayed = False
        self.function = function
        self.type = btype
        self.drawn = False
        
    def debugDraw(self):
        pg.beginDraw()
        pg.rect(self.x,self.y,self.w,self.h)
        pg.endDraw()
        
    def over(self,pg):
        if (mouseX >= self.x and mouseX <= self.x+self.w and mouseY >= self.y and mouseY <= self.y+self.h):
            if self.hover == False:
                self.tooltipDisplayed = False
                self.hoverStart = datetime.datetime.now()
            elif datetime.datetime.now() - self.hoverStart >= datetime.timedelta(seconds=self.tooltipTime):
                if self.tooltipDisplayed == False:
                    pg.beginDraw()
                    pg.textSize(15)
                    x1=self.x+self.w
                    y1=self.y+self.h
                    w1=pg.textWidth(self.tooltip)+4
                    h1=15+4
                    if(x1 + w1 > width):
                        x1 -= w1 + 15
                       
                    pg.fill(color(0,0,0,100))
                    pg.rect(x1,y1,w1,h1)
                    pg.fill(color(255,255,255,200))
                    pg.text(self.tooltip,x1+2,y1+15)
                    pg.endDraw()
                    self.drawn = True
                    self.tooltipDisplayed = True
            self.hover = True
            image(pg,0,0)
            return True
        else:
            self.hover = False
            if self.drawn == True:
                pg.beginDraw()
                pg.clear()
                pg.endDraw()
                self.drawn = False
        return False

    def onClick(self):
        self.function()
        
            