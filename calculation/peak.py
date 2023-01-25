from math import exp, log

#each peak has gaussian profile => has amplitude mean and fwhm = 2*sqrt(2*ln(2))*sigma        
class Peak:
    def __init__(self,amplitude,mean,fwhm):
        self.amplitude = amplitude
        self.mean = mean
        self.fwhm = fwhm
    #method to get value at point for each peak
    def get_value_at_point(self,x):
        try:
            return int(self.amplitude*exp(-(x-self.mean)**2*4*log(2)/self.fwhm/self.fwhm))
        except ZeroDivisionError:
            return int(self.amplitude) if x==self.mean  else 0