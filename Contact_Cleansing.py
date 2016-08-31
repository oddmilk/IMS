# load data
import os
import glob
import pandas as pd 
import numpy as np 
from os import listdir

Contact = pd.read_excel('/Users/mengjichen/Desktop/ID_mapping/Contact/Account_Contact_Location_201608.xls')
Target = pd.read_excel('/Users/mengjichen/Desktop/ID_mapping/Contact/目标医生_0818.xlsx')

# inner join Target table and Contact table
Contact_for_cleansing = pd.merge(Target, Contact, left_on = 'SFDCID', right_on = 'Contact ID', how = 'left')

from pandas import ExcelWriter
writer = ExcelWriter('/Users/mengjichen/Desktop/ID_mapping/Contact/Contact_Pool_Roche.xlsx')
Contact_for_cleansing.to_excel(writer, 'Sheet1')

Contact_OK_ID = Contact['OneKey Individual ID'].unique()

