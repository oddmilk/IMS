"""
Test for a stressful_life_events/gene interaction in depression
=============================================================================================

Based on the assumption that the onset of depression is related to gene, here 
we investigate how this dependence is related to the episodes of stressful 
life events: not only does gene creates a gap in depression, it also seems
that depression deepens with an increase in stress.

Date: Nov 26, 2016
@author: Oddmilk

"""

#############################################################################################
# Load and massage the data
import pandas as pd 
from scipy import stats

gese = pd.read_csv('gesedata.csv')
gese.head()
gese.columns = ['number', 'depression','gene','stressful_life_events']
# depression: numeric
# gene: dummy (1,0)
# stressful_life_events: I'll treat it as a categorical

#############################################################################################
# Descriptive statistics
desc_depression = gese['depression'].describe()
desc_stress = gese.stressful_life_events.value_counts() 
desc_gene = gese.gene.value_counts() 
print(desc_stress)
print(desc_gene) 
pd.crosstab(gese.stressful_life_events, gese.gene) 

gese['events_cat'] = gese.stressful_life_events
gese.loc[gese.stressful_life_events > 10, 'events_cat'] = 10 # Recode labels

#############################################################################################
# Simple plotting
import matplotlib.pyplot as plt
import seaborn

# Histograms
plt.hist(gese.depression)  # slightly right skewed
plt.hist(gese.gene)	# unequally distributed
plt.hist(gese.stressful_life_events)  # heavily right skewed


#############################################################################################
# Testing for interaction
from statsmodels.graphics.api import interaction_plot
fig = interaction_plot(gese.stressful_life_events, gese.gene, gese.depression)
plt.show() # The plot does indicate an interaction between gene and stressful life events


# Correlation
pearsoncorr = stats.pearsonr(gese.stressful_life_events, gese.depression) # p-value (<.05) indicates a significant correlation between stressful life events and depression outcome


# t test
t_test = stats.ttest_ind(gese.depression[gese.gene == 1], gese.depression[gese.gene == 0])
print(t_test_gene) # p-value (>.05) indicates mean of depression is not significantly different in these two genotypes


#############################################################################################
# statistical analysis

import statsmodels.formula.api as sm

# Model 0: depression against gene
m0 = ols("depression ~ C(gene)", gese).fit()
print(m0.summary())

# Model 1: depression against gene and stressful life events
m1 = ols("depression ~ C(gene) + C(stressful_life_events)", gese).fit() 
print(m1.summary())

# Model 2: depression against gene, stressful life events, and the interaction term
m2 = ols("depression ~ C(gene) + C(events_cat) + C(gene)*C(events_cat)", gese).fit() 
print(m2.summary())


# Outputting summary as table 
ols_output = m2.summary().as_text()
f = open("ols_output.txt", "w")
f.write(ols_output)
f.close()



































