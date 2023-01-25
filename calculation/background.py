from math import exp

#background is uniq for spectrum and it describes by the follow function: a*exp(-b*x)+c*x+d
class Background:
    
    def __init__(self):
        pass
    
    #setters
    def set_background(self,a,b,c,d):
        self.a = a
        self.b = b
        self.c = c
        self.d = d

    #method to get value at point for each peak
    def get_value_at_point(self, x):
        return int(self.a*exp(-self.b*x)+self.c*x+self.d)
