"""
Created on Fri Mar 23 09:53:02 2018

@author: mike

Class to compare densities using optimal transport. 
Input is assumed to be a one-dimensional numpy array with length > 1.
"""

import numpy as np


class OptimalTransport():

    """
    Computes the 1D optimal transport distance (L^2) between the signal and a template in domain x \in [0, 1]. 
    Gives a metric to compare signals/distributions. Extends to compare points clouds in bins of interest in the signal.
    
    Assumes signals as numpy arrays.
    """
    
    def __init__(self, source, target):
        self.source = source
        self.target = target
        
    def _normalise(self, density):
        return density / float(np.sum(density))
        
    def _optimaltransport(self):

    # normalise densities to have equal sum. Integers for ease.
    
        f_x, g_y = self._normalise(self.source, self.target), self._normalise(self.target, self.source)
      
        m, n = len(f_x), len(g_y)

        c, i, j = 0, 0, 0

        mapping = np.zeros((m, n)) # Can create heatmap to visualise mapping. Only for small m, n! Or use sparse matrix

        while i < m and j < n:
            if g_y[j] == 0: 
                j += 1
            elif f_x[i] == 0: # if supply/demand if empty, skip. 
                i += 1
            else:
                if f_x[i] - g_y[j] > 0:
                    f_x[i] -= g_y[j]
                    c += (i/(m-1) - j/(n-1)) ** 2 * g_y[j] # density * cost to transport
                    mapping[i,j] = g_y[j]
                    j += 1
                elif f_x[i] - g_y[j] < 0:
                    g_y[j] -= f_x[i]
                    c += (i/(m-1) - j/(n-1)) ** 2 * f_x[i] # density * cost to transport
                    mapping[i,j] = f_x[i]
                    i += 1
                else: 
                    c += (i/(m-1) - j/(n-1)) ** 2 * f_x[i] # density * cost to transport
                    mapping[i,j] = f_x[i]
                    i += 1                
                    j += 1

        return mapping, c
    
    
