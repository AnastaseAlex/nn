from scipy.io import loadmat
import numpy as np
import os

def load_dataset(datadir = '../data',fname = 'MATRICE_MAREE_11_2015.mat', geofile = 'latlontime.mat',field = 'MATRICE', colnum = [134,135]):
    
