import os 
import pandas as pd 
import numpy as np 

CODE = pd.read_table('/Users/mengjichen/Desktop/UAT_1008/CN/CEGEDIM_SPHCN_2163_OK_CN_CODE_0000000015_20161008080329.flat', header = True)
QUAL = pd.read_table('/Users/mengjichen/Desktop/UAT_1008/CN/CEGEDIM_SPHCN_2163_OK_CN_QUALIFYING_DATA_0000000015_20161008080329.flat', header = True, sep = '|')