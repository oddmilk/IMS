############## DATA CHECK #################
# Total number of Master_DCR_g__c
A = len(SFDC_DCR[SFDC_DCR.Master_DCR_g__c.isnull()].Id.unique())
A_Master = pd.DataFrame(SFDC_DCR[SFDC_DCR.Master_DCR_g__c.isnull()].Id.unique())
A_Master.columns = ['A_Master']

# Total number into MoveIt for OK to validate
B = len(DataIn.REQUEST_ID_CLIENT.unique())
B_Master = pd.DataFrame(MOVEIT.REQUEST_ID_CLIENT.unique())
B_Master.columns = ['B_Master']

# Date range of incoming client request 
R = [DataIn.REQUEST_DATE.min(), DataIn.REQUEST_DATE.max()]

# For CR that went into MOVEIT/OK for validation, subset SFDC ITEM data frame
SFDC_B = SFDC_DCR_ITEM[SFDC_DCR_ITEM.Change_Request_ref_g__c.isin(B_Master['B_Master'])]

# For the subset of master CR that went into OK for validation, subset rows by: Fields to validate & child ID
	# Field_API_Name_g__c
SFDC_B_In = SFDC_B[SFDC_B.Field_API_Name_g__c.isin(To_be_validated)]

# Reshape MOVEIT data from wide to long
MoveIt_long = pd.melt(DataIn, 
	id_vars = ['REQUEST_ID_CLIENT'],
	value_vars = ['ACT_ROLE_1', # Administrative_Title_cn_g__pc
	'IND_GENDER_COD', # Gender_g__pc
	'FULLNAME', # LastName
	'IND_CLASS_COD', # Professional_Type_g__pc
	'IND_TITLE_COD', # Professional_Subtype_g__pc
	'WKP_ID_CEGEDIM', 
	'IND_SPECIALITY_1']) # Primary_Specialty_g__pc; Specialty_ref_g__c

list_SFDC_MoveIt = [SFDC_B_In, MoveIt_long]
save_xls(list_SFDC_MoveIt, "./SFDC_MOVEIT.xlsx")




SFDC_B_In_Final = SFDC_B_In.groupby('Change_Request_ref_g__c').apply(lambda x: getRightId(x)) # NOTE DCRs creating hospitals are not found here

list_DCR_INTO_OK = [SFDC_B_In, B_Master]
save_xls(list_DCR_INTO_OK, "./DCR_into_OK.xlsx")

# Summary stats
# Courtesy: Chris Albon
def get_stats(data):
	return {'min': group.min(),
	'max': group.max(),
	'count': group.count(),
	'mean': group.mean()}





























