from numpy.random import seed, get_state, set_state, normal
from math import fabs,sqrt

#fixed seed for possibility to cut the noise    

def gaussian_noise(y,add_noise, last_noise_state):
    
    WWW#statistical gaussian noise
    if add_noise:
        last_noise_state = [0 if y[i]==0 else int(fabs(y[i]-normal(y[i],sqrt(y[i])))) for i in range(len(y))]
    else:
        last_noise_state = [-1*last_noise_state[i] for i in range(len(y))]
    
    return last_noise_state