# Actelion reshaper
# load data
import os
import glob
import pandas as pd 
import numpy as np 
from os import listdir

# stack tables by index
df = pd.read_excel('/Users/mengjichen/Desktop/Actelion_Reshape_1.xlsx', index = 'TARGET')
df_Hosp = df[['TARGET', 'OK1', 'OK2', 'OK3', 'OK4', 'OK5', 'OK6', 'OK7', 'OK8', 'OK9']]
df_Hosp_Long = pd.DataFrame(df_Hosp.stack())

df_Adr = df[['Address', 'ADR1', 'ADR2', 'ADR3', 'ADR4', 'ADR5', 'ADR6', 'ADR7', 'ADR8', 'ADR9']]
df_Adr_Long = pd.DataFrame(df_Adr.stack())

df_branch_hosp = [df_Hosp_Long, df_Adr_Long]
save_xls(df_branch_hosp, '/Users/mengjichen/Desktop/Actelion_Branch.xlsx')

#####
df2 = pd.read_excel('/Users/mengjichen/Desktop/Actelion_Reshape_2.xlsx', index = 'TARGET')
df2_Hosp = df2[['TARGET', 'OK1', 'OK2', 'OK3', 'OK4', 'OK5', 'OK6', 'OK7']]
df2_Hosp_Long = pd.DataFrame(df2_Hosp.stack())

df2_Adr = df2[['Address', 'ADR1', 'ADR2', 'ADR3', 'ADR4', 'ADR5', 'ADR6', 'ADR7']]
df2_Adr_Long = pd.DataFrame(df2_Adr.stack())

df2_branch_hosp = [df2_Hosp_Long, df2_Adr_Long]
save_xls(df2_branch_hosp, '/Users/mengjichen/Desktop/Actelion_Peer_Branch.xlsx')
