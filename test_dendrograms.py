#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 17 11:15:33 2019

@author: antonio
"""

import numpy as np
from scipy.cluster.hierarchy import dendrogram, linkage
from scipy.spatial.distance  import squareform

X=np.array([[1.0,2.0,3.0,4.0]])
Y=squareform(X)
Z=linkage(Y)
dendrogram(Z)