#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep 22 21:49:10 2018
/*
 * Thanks to ImportanceOfBeingErnest for the idea/implementation for this class.
 * https://stackoverflow.com/questions/46131572/making-a-non-overlapping-bubble-chart-in-matplotlib-circle-packing
 */ and some changes in the plotting:
     https://stackoverflow.com/questions/4700614/how-to-put-the-legend-out-of-the-plot
     
Modifications by booort. 
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# Read CSV with the data
df = pd.read_csv('YOURFILE.csv')

# Select data from a column
data = df['YOUR_COLUM_that_sizes_the_circles']


np.interp(data, (data.min(), data.max()), (0, 10)) #scale the data

class C():
    def __init__(self,r):
        self.N = len(r)
        self.x = np.ones((self.N,3))
        self.x[:,2] = r
        maxstep = 2*self.x[:,2].max()
        length = np.ceil(np.sqrt(self.N))
        grid = np.arange(0,length*maxstep,maxstep)
        gx,gy = np.meshgrid(grid,grid)
        self.x[:,0] = gx.flatten()[:self.N]
        self.x[:,1] = gy.flatten()[:self.N]
        self.x[:,:2] = self.x[:,:2] - np.mean(self.x[:,:2], axis=0)

        self.step = self.x[:,2].min()
        self.p = lambda x,y: np.sum((x**2+y**2)**2)
        self.E = self.energy()
        self.iter = 1.

    def minimize(self):
        while self.iter < 1000*self.N:
            for i in range(self.N):
                rand = np.random.randn(2)*self.step/self.iter
                self.x[i,:2] += rand
                e = self.energy()
                if (e < self.E and self.isvalid(i)):
                    self.E = e
                    self.iter = 1.
                else:
                    self.x[i,:2] -= rand
                    self.iter += 1.

    def energy(self):
        return self.p(self.x[:,0], self.x[:,1])

    def distance(self,x1,x2):
        return np.sqrt((x1[0]-x2[0])**2+(x1[1]-x2[1])**2)-x1[2]-x2[2]

    def isvalid(self, i):
        for j in range(self.N):
            if i!=j: 
                if self.distance(self.x[i,:], self.x[j,:]) < 0:
                    return False
        return True

    def plot(self, ax):
        for i in range(self.N):
            circ = plt.Circle(self.x[i,:2],self.x[i,2],label=df['risk'][i]+': '+df['value'][i],color=np.random.rand(3,))
            ax.add_patch(circ)
            circ = plt.Circle(self.x[i,:2],self.x[i,2],color='black',fill=False) #this plot the border
            ax.add_patch(circ)

c = C(data)

fig, ax = plt.subplots(subplot_kw=dict(aspect="equal"))
ax.axis("off")

c.minimize()

c.plot(ax)
ax.relim()
ax.autoscale_view()

# Shrink current axis by 20%
box = ax.get_position()
ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])

# Put a legend to the right of the current axis
ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))

plt.show()