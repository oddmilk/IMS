"""
This is a module of all visualizations made for IMS

@Author: oddmilk

"""

import matplotlib.pyplot as plt
import seaborn as sns

############################################################
# Load data
############################################################
doctor_profile = pd.read_excel('doctor_profile.xlsx')
doctor_profile.KM_COUNT = doctor_profile.KM_COUNT.astype('category')

# Plot PageView/Visit Ratio against region
p1 = sns.stripplot(x = "PV_Visit_Ratio", y = "REGION", data = doctor_profile, jitter = 0.05, linewidth = 1)
p1.savefig('against_region.png')

p2 = sns.stripplot(x = "PV_Visit_Ratio", y = "KM_COUNT", data = doctor_profile, jitter = 0.05, linewidth = 1)
plt.title('PageView/Visit Ratio against Number of Key Messages Received on iDA')
p2.savefig('against_KM_COUNT.png')

test = doctor_profile.PV_Visit_Ratio.astype(int)
p3 = sns.swarmplot(x = test, y = "Int_Segment", data = doctor_profile, linewidth = 1)
plt.title('PageView/Visit against Doctor National Segment')
plt.xlabel('PageView/Visit')
plt.ylabel('Doctor National Segment')
p3.savefig('against_segment.png')

p4 = sns.stripplot(x = test, y = "EDM_Clicked", data = doctor_profile, jitter = 0.5, linewidth = 1)
plt.title('PageView/Visit against EDM Clicked')
plt.xlabel('PageView/Visit')
plt.ylabel('EDM clicked or not')

