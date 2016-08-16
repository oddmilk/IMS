
# Source Data
	# SFDC: Aug. 1 - Sug. 9
	# MoveIt: Aug. 1 - Aug. 11


# Unzip VR files
zipfilePath_ = '/Users/mengjichen/Desktop/Roche/201608_Names_VR'
destinationfile_path = '/Users/mengjichen/Desktop/Roche/201608_Names_VR'
MOVEIT = readMoveIt('/Users/mengjichen/Desktop/Roche/201608_Names_VR', '*.FLAT')
Num_Names_MOVEIT = MOVEIT.REQUEST_ID_CLIENT.unique()

# Subset DCR ITEM which update client names
Names_CR = SFDC_DCR_ITEM[SFDC_DCR_ITEM.Field_API_Name_g__c == 'LastName']
Num_Names_CR = Names_CR.Change_Request_ref_g__c.unique()

# DCR updating client names that finally landed in MOVEIT
Names_DCR_landed = DataIn[DataIn.REQUEST_ID_CLIENT.isin(Num_Names_CR)]
# DCR departure
len(Num_Names_CR)
# DCR arrival (a number of DCRs departing from SFDC might drop out in Conversion Tool: out-of-scope or)
len(Names_DCR_landed.index)

Names_DCR_In = Names_CR[Names_CR.Change_Request_ref_g__c.isin(Names_DCR_landed.REQUEST_ID_CLIENT.unique())]

Names_DCR_landed_long = pd.melt(Names_DCR_landed, 
	id_vars = ['REQUEST_ID_CLIENT'],
	value_vars = ['ACT_ROLE_1', # Administrative_Title_cn_g__pc
	'IND_GENDER_COD', # Gender_g__pc
	'FULLNAME', # LastName
	'IND_CLASS_COD', # Professional_Type_g__pc
	'IND_TITLE_COD', # Professional_Subtype_g__pc
	'WKP_ID_CEGEDIM', 
	'IND_SPECIALITY_1']) # Primary_Specialty_g__pc; Specialty_ref_g__c

Names_In_Landed = [Names_DCR_In, Names_DCR_landed_long]
save_xls(Names_In_Landed, "./Names_QC.xlsx")
