import seaborn as sns
import matplotlib.pyplot as plt

with sns.color_palette("RdBu", 5):
	ax = sns.countplot(y = "campaign_type", hue = "region", data = content)

ax.set(xlabel = 'PageView Count', ylabel = 'Campaign Type')

plt.show()
plt.close()

with sns.color_palette("RdBu", 5):
	ax = sns.countplot(y = "campaign_type", hue = "grade", data = content, hue_order = ['A','B','C','D','N'])

ax.set(xlabel = 'PageView Count', ylabel = 'Campaign Type')

plt.show()
plt.close()

with sns.color_palette("RdBu", 9):
	ax = sns.countplot(x = "campaign_type", hue = "department", data = content, orient = "v")
ax.set(xlabel = 'Campaign Type', ylabel = 'PageView Count')

plt.show()
plt.close()


test.loc[test['campaign_type'] == 'g-brand', 'campaign_type'] = 'Other'
test.loc[test['campaign_type'] == 'g-link', 'campaign_type'] = 'Other'
test.loc[test['campaign_type'] == 'g-seminar', 'campaign_type'] = 'Other'
test.loc[test['campaign_type'] == 'g-video', 'campaign_type'] = 'Other'
test.loc[test['campaign_type'] == 'ime', 'campaign_type'] = 'Other'

g = sns.factorplot(x = "region", y = "unique_PV", hue = "grade", col = "campaign_type", data = test, 
	saturation = .5, kind = "bar", ci = None, aspect = .6,
	palette = "RdBu",
	legend = True)
g.set_axis_labels("", "PageView")
g.set_titles("{col_name}")

tag_pv = tp.groupby(['Tag', 'Int_Segment', 'REGION']).apply(lambda x: len(x))
tag_pv = tag_pv.reset_index()
tag_pv.columns = ['Tag','Int_Segment','Region','PV']


g1 = sns.factorplot(x = "Tag", y = "PV", col = "Region", data = tag_pv,
	saturation = .5, kind = "bar", ci = None, aspect = .6,
	palette = "RdBu",
	legend = True)


tag_group = tp.groupby(['Tag', 'Int_Segment', 'REGION'])
tag_dcr = tag_group['Total_PV'].sum()
tag_dcr = tag_dcr.reset_index()

g2 = sns.factorplot(x = "Tag", y = "Total_PV", col = "REGION", data = tag_dcr,
	saturation = .5, kind = "bar", ci = None, aspect = .6,
	palette = "RdBu",
	legend = True)
g2.set_axis_labels("", "PageView")




