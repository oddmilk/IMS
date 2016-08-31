# DCR matching

############ Total number of Master_DCR_g__c ################
# SFDC > MOVEIT >= ONEKEY WEEKLY REPORT
# SFDC
A = len(SFDC_DCR[SFDC_DCR.Master_DCR_g__c.isnull()].Id.unique())
A_Master = pd.DataFrame(SFDC_DCR[SFDC_DCR.Master_DCR_g__c.isnull()].Id.unique())
A_Master.columns = ['A_Master']

# Data into MOVEIT
B = len(DataIn.REQUEST_ID_CLIENT.unique())
B_Master = pd.DataFrame(MOVEIT.REQUEST_ID_CLIENT.unique())
B_Master.columns = ['B_Master']

# Subsetting SFDC DCR ITEM files that landed in MOVEIT
SFDC_B = SFDC_DCR_ITEM[SFDC_DCR_ITEM.Change_Request_ref_g__c.isin(B_Master['B_Master'])]
SFDC_B_In = SFDC_B[SFDC_B.Field_API_Name_g__c.isin(To_be_validated)]
Departure = SFDC_B_In[['Id', 'Field_API_Name_g__c', 'Name', 'Old_Field_Value_Text_g__c', 'Field_value_text_g__c', 'Change_Request_ref_g__c', 'sourceFile']]

# Revalidation #
Reval = Departure.groupby(['Change_Request_ref_g__c', 'Field_API_Name_g__c']).apply(lambda x: getRightId(x))
Reval_Fields = Reval[Reval.Field_API_Name_g__c.isin(['Professional_Subtype_g__pc','LastName', 'Job_Title_g__c'])]
Reval_Fields_Export = Reval_Fields[Reval_Fields.Field_value_text_g__c.notnull()]

# Adding requestor remarks from SFDC_DCR #
SFDC_Remarks = SFDC_DCR[['Id', 'Requestor_Remarks_g__c', 'Master_DCR_g__c']]
SFDC_Remarks = SFDC_Remarks[SFDC_Remarks.Requestor_Remarks_g__c.notnull()]
SFDC_Remarks = SFDC_Remarks[SFDC_Remarks.Master_DCR_g__c.isnull()]

Reval_Fields_Remarks = Reval_Fields_Export.merge(SFDC_Remarks, left_on = 'Change_Request_ref_g__c', right_on = 'Id', how = 'left')

writer = ExcelWriter('/Users/mengjichen/Desktop/Roche/201607/Revalidation_July.xlsx')
Reval_Fields_Remarks.to_excel(writer, 'Sheet1')
writer.save()
































# Strip unwanted list name from DataIn columns #
# IND_GENDER_COD: [GEN.M] -> [M]
DataIn['IND_GENDER_COD'] = DataIn['IND_GENDER_COD'].map(lambda x: str(x).strip('GEN.')) # IND_GENDER_COD was a float object. Need to convert it to str format explicitly
DataIn['IND_CLASS_COD'] = DataIn['IND_CLASS_COD'].map(lambda x: str(x).strip('TYP.'))
DataIn['ACT_ROLE_1'] = DataIn['ACT_ROLE_1'].map(lambda x: str(x).strip('TIH.WCN.'))
DataIn['IND_SPECIALITY_1'] = DataIn['IND_SPECIALITY_1'].map(lambda x: str(x).strip('SP.WCN.'))
DataIn['IND_TITLE_COD'] = DataIn['IND_TITLE_COD'].map(lambda x: str(x).strip('TIH.WCN.'))
DataIn['WKP_SPECIALITY_1'] = DataIn['WKP_SPECIALITY_1'].map(lambda x: str(x).strip('SP.WCN.')) # NOTE: WKP_* and IND_* are using the same mapping sheet
# Convert ACT_ROLE_1 & IND_TITLE_COD to numeric values
DataIn[['ACT_ROLE_1', 'IND_TITLE_COD']] = DataIn[['ACT_ROLE_1', 'IND_TITLE_COD']].apply(pd.to_numeric())
DataIn['ACT_ROLE_1'] = pd.to_numeric(DataIn['ACT_ROLE_1'])


############################## Label-Code Conversion ####################################
LOV = pd.ExcelFile('/Users/mengjichen/Desktop/Roche/Onekey LOV 2016.xlsx')
##### Department specialty ######
DEPT_MAPPING = pd.read_excel('/Users/mengjichen/Desktop/Roche/Client_DEPT_SP_Mapping.xlsx')

##### Administrative title ###### '职务'
ADMIN_MAPPING = LOV.parse('Aff_Position')
ADMIN_MAPPING = ADMIN_MAPPING[['Code ', 'CN Short Label']]
ADMIN_MAPPING.columns = ['ACT_ROLE', 'Administrative_Label']
ADMIN_MAPPING['ACT_ROLE'] = ADMIN_MAPPING['ACT_ROLE'].astype(float)

##### Gender ##### '性别'
GENDER_MAPPING = LOV.parse('Prof_Gender')
GENDER_MAPPING = GENDER_MAPPING[['Code ', 'CN Short Label']] # Note there's a whitespace in the header... lol
GENDER_MAPPING.columns = ['IND_GENDER_COD', 'Gender_Label']

##### Professional type ##### '职业类别'
TYPE_MAPPING = LOV.parse('Prof_Type')
TYPE_MAPPING = TYPE_MAPPING[['Code ', 'CN Short Label']]
TYPE_MAPPING.columns = ['IND_CLASS_COD', 'Type_Label']

##### Individual specialty ##### '专长'
SP_MAPPING = LOV.parse('Prof-Hosp Specialties')
SP_MAPPING = SP_MAPPING[['Code ', 'CN Short Label', 'CN Long Label']]
SP_MAPPING.columns = ['IND_SPECIALITY_1', 'SP_Short', 'SP_Long']

##### Professional subtype ##### '职称'
SUBTYPE_MAPPING = LOV.parse('Prof_Title')
SUBTYPE_MAPPING = SUBTYPE_MAPPING[['Code ', 'CN Short Label']]
SUBTYPE_MAPPING.columns = ['IND_TITLE_COD', 'Title_Label']

# Map OK Code to Label
Converted_DataIn1 = pd.merge(DataIn[pd.notnull(DataIn.IND_GENDER_COD)], GENDER_MAPPING, how = 'left', on = 'IND_GENDER_COD') 
Converted_DataIn2 = pd.merge(Converted_DataIn[pd.notnull(Converted_DataIn1.IND_CLASS_COD)], TYPE_MAPPING, how = 'left', on = 'IND_CLASS_COD')
Converted_DataIn2['ACT_ROLE'] = Converted_DataIn2['ACT_ROLE_1'].convert_objects(convert_numeric = True)
Converted_DataIn3 = pd.merge(Converted_DataIn2, ADMIN_MAPPING, how = 'left', on = 'ACT_ROLE')
Converted_DataIn4 = pd.merge(Converted_DataIn3, SP_MAPPING, how = 'left', on = 'IND_SPECIALITY_1')
Converted_DataIn5 = pd.merge(Converted_DataIn4, SUBTYPE_MAPPING, how = 'left', on = 'IND_TITLE_COD')

# MOVEIT reshaper
MoveIt_long = pd.melt(Converted_DataIn5, 
	id_vars = ['REQUEST_ID_CLIENT'],
	value_vars = ['Administrative_Label', # Administrative_Title_cn_g__pc
	'Gender_Label', # Gender_g__pc
	'FULLNAME', # LastName
	'Type_Label', # Professional_Type_g__pc
	'Title_Label', # Professional_Subtype_g__pc
	'WKP_ID_CEGEDIM', 
	'SP_Long']) # Primary_Specialty_g__pc; Specialty_ref_g__c

list_SFDC_MoveIt = [Departure, Depature_Stamped, MoveIt_long]
save_xls(list_SFDC_MoveIt, "./Departure_Stamped_Arrival.xlsx")




################################# Phase 2 ########################################
# Detect DCRs that get lost in the transportation from MOVEIT to OneKey Tool
# DCR as validated by call center 
# Data source: Onekey Tools UR extract 
# Time range: Jul.1 - Jul.31
