# For each Field_API, find DCR that have data failed to be transported to MoveIt

	# Function
def FieldCompare(df1, df2, key1, key2, meth):
	df = pd.merge(df1, df2, left_on = key1, right_on = key2, how = meth)
	return(df)


	# LastName
Name_In = SFDC_B_In_Final[SFDC_B_In_Final.Field_API_Name_g__c == 'LastName'][['Change_Request_ref_g__c', 'Field_value_text_g__c', 'sourceFile']] # returning all DCR from SFDC updating/refreshing client name
Name_MoveIt = MoveIt_long[MoveIt_long.variable == 'FULLNAME'][['REQUEST_ID_CLIENT', 'value']] # all DCR updating/refreshing client name after into MoveIt

	# Match & identify the set of all DCRs in Name_In and Name_MoveIt
t1 = pd.merge(Name_In, Name_MoveIt, left_on = 'Change_Request_ref_g__c', right_on = 'REQUEST_ID_CLIENT', how = 'outer')

	# Produces the set of DCRs that match in both Name_In and Name_MoveIt
Comp_Name = pd.merge(Name_In, Name_MoveIt, left_on = 'Change_Request_ref_g__c', right_on = 'REQUEST_ID_CLIENT', how = 'inner')
Name_diff_DCR = t2[t2['value'] != t2['Field_value_text_g__c']].REQUEST_ID_CLIENT # this returns all DCRs that have disagreeing names
Name_diff_DCR = pd.DataFrame(Name_diff_DCR)
list_Name = [Comp_Name, Name_diff_DCR]
save_xls(list_Name, './Name_QC.xlsx')

	# Gender
Gender_In = SFDC_B_In_Final[SFDC_B_In_Final.Field_API_Name_g__c == 'Gender_g__pc'][['Change_Request_ref_g__c', 'Field_value_text_g__c', 'sourceFile']] # returning all DCR from SFDC updating/refreshing client name
Gender_MoveIt = MoveIt_long[MoveIt_long.variable == 'IND_GENDER_COD'][['REQUEST_ID_CLIENT', 'value']] # all DCR updating/refreshing client name after into MoveIt
Comp_Gender = FieldCompare(Gender_In, Gender_MoveIt, 'Change_Request_ref_g__c', 'REQUEST_ID_CLIENT', 'inner')
	# Recode
Comp_Gender['SFDC_Value'] = np.where(np.equal(Comp_Gender['Field_value_text_g__c'], "男性") | np.equal(Comp_Gender['Field_value_text_g__c'], "Male"), "GEN.M", "GEN.F")
Comp_Gender['SFDC_Value'] = np.where(np.equal(Comp_Gender['Field_value_text_g__c'], "女性") | np.equal(Comp_Gender['Field_value_text_g__c'], "Female"), "GEN.F", "GEN.M")
Comp_Gender['SFDC_Value'] = np.where(np.equal(Comp_Gender['Field_value_text_g__c'], "未知"), "GEN.U", Comp_Gender['SFDC_Value'])
Gender_diff_DCR = Comp_Gender[Comp_Gender['SFDC_Value'] != Comp_Gender['value']].REQUEST_ID_CLIENT # returning DCRs disagreeing in gender value
Gender_diff_DCR = pd.DataFrame(Gender_diff_DCR)
list_Gender = [Comp_Gender, Gender_diff_DCR]
save_xls(list_Gender, './Gender_QC.xlsx')

	# Primary_Specialty_g__pc -> IND_SPECIALITY_1
SP_In = SFDC_B_In_Final[SFDC_B_In_Final.Field_API_Name_g__c == 'Primary_Specialty_g__pc'][['Change_Request_ref_g__c', 'Field_value_text_g__c', 'sourceFile']] # returning all DCR from SFDC updating/refreshing client name
SP_MoveIt = MoveIt_long[MoveIt_long.variable == 'IND_SPECIALITY_1'][['REQUEST_ID_CLIENT', 'value']] # all DCR updating/refreshing client name after into MoveIt
Comp_SP = FieldCompare(SP_In, SP_MoveIt, 'Change_Request_ref_g__c', 'REQUEST_ID_CLIENT', 'inner')

	# Need to reference Master data
SP_Transformer = pd.read_excel('./master_data.xlsx', sheetname = '专长')
Comp_SP = pd.merge(Comp_SP, SP_Transformer, left_on = 'Field_value_text_g__c', right_on = 'CODE_LOCAL_LONG_LABEL', how = 'left') # 
Comp_SP['SFDC_Value'] = 'SP.WCN.' + Comp_SP['CODE_EID'].astype(str)
SP_diff_DCR = Comp_SP[Comp_SP['SFDC_Value'] != Comp_SP['value']].REQUEST_ID_CLIENT
SP_diff_DCR = pd.DataFrame(SP_diff_DCR)
list_SP = [Comp_SP, SP_diff_DCR]
save_xls(list_SP, './SP_QC.xlsx')
	# Note: special attention needs to be paid to NaN incurred in the joining process: '药剂学' vs. '药剂'

	# Professional_Type_g__pc -> IND_CLASS_COD
Type_Transformer = pd.read_excel('./master_data.xlsx', sheetname = '职业类别')
Type_In = SFDC_B_In_Final[SFDC_B_In_Final.Field_API_Name_g__c == 'Professional_Type_g__pc'][['Change_Request_ref_g__c', 'Field_value_text_g__c', 'sourceFile']] # returning all DCR from SFDC updating/refreshing client name
Type_MoveIt = MoveIt_long[MoveIt_long.variable == 'IND_CLASS_COD'][['REQUEST_ID_CLIENT', 'value']] # all DCR updating/refreshing client name after into MoveIt
Comp_Type = FieldCompare(Type_In, Type_MoveIt, 'Change_Request_ref_g__c', 'REQUEST_ID_CLIENT', 'inner')
Comp_Type = pd.merge(Comp_Type, Type_Transformer, left_on = 'Field_value_text_g__c', right_on = 'CODE_LOCAL_SHORT_LABEL', how = 'left') # '其他' was automatically mapped to NaN
Comp_Type['SFDC_Value'] = 'TYP.' + Comp_Type['CODE_EID'].astype(str)
Type_diff_DCR = Comp_Type[Comp_Type['CODE_EID'] != Comp_Type['value']].REQUEST_ID_CLIENT
Type_diff_DCR = pd.DataFrame(Type_diff_DCR)
list_Type = [Comp_Type, Type_diff_DCR]
save_xls(list_Type, './Type_QC.xlsx')

	# Professional_Subtype_g__pc -> IND_TITLE_COD
Subtype_Transformer = pd.read_excel('./master_data.xlsx', sheetname = '职称')
Subtype_In = SFDC_B_In_Final[SFDC_B_In_Final.Field_API_Name_g__c == 'Professional_Subtype_g__pc'][['Change_Request_ref_g__c', 'Field_value_text_g__c', 'sourceFile']] # returning all DCR from SFDC updating/refreshing client name
Subtype_MoveIt = MoveIt_long[MoveIt_long.variable == 'IND_TITLE_COD'][['REQUEST_ID_CLIENT', 'value']] # all DCR updating/refreshing client name after into MoveIt
Comp_Subtype = FieldCompare(Subtype_In, Subtype_MoveIt, 'Change_Request_ref_g__c', 'REQUEST_ID_CLIENT', 'inner')
Comp_Subtype = pd.merge(Comp_Subtype, Subtype_Transformer, left_on = 'Field_value_text_g__c', right_on = 'CODE_LOCAL_SHORT_LABEL', how = 'left')
Subtype_diff_DCR = Comp_Subtype[Comp_Subtype['CODE_EID'] != Comp_Subtype['value']].REQUEST_ID_CLIENT
Subtype_diff_DCR = pd.DataFrame(Subtype_diff_DCR)
list_Subtype = [Comp_Subtype, Subtype_diff_DCR]
save_xls(list_Subtype, './Subtype_QC.xlsx')


	# Administrative_Title_cn_g__pc -> ACT_ROLE_1
Role_Transformer = pd.read_excel('./master_data.xlsx', sheetname = '职务')
Role_In = SFDC_B_In_Final[SFDC_B_In_Final.Field_API_Name_g__c == 'Administrative_Title_cn_g__pc'][['Change_Request_ref_g__c', 'Field_value_text_g__c', 'sourceFile']] # returning all DCR from SFDC updating/refreshing client name
Role_MoveIt = MoveIt_long[MoveIt_long.variable == 'ACT_ROLE_1'][['REQUEST_ID_CLIENT', 'value']] # all DCR updating/refreshing client name after into MoveIt
Comp_Role = FieldCompare(Role_In, Role_MoveIt, 'Change_Request_ref_g__c', 'REQUEST_ID_CLIENT', 'inner')
Comp_Role = pd.merge(Comp_Role, Role_Transformer, left_on = 'Field_value_text_g__c', right_on = 'CODE_LOCAL_SHORT_LABEL', how = 'left')
Comp_Role['SFDC_Value'] = 'TIH.WCN.' + Comp_Role['CODE_EID'].astype(str)
Role_diff_DCR = Comp_Role[Comp_Role['CODE_EID'] != Comp_Role['value']].REQUEST_ID_CLIENT
Role_diff_DCR = pd.DataFrame(Role_diff_DCR)
list_Role = [Comp_Role, Role_diff_DCR]
save_xls(list_Role, './Type_QC.xlsx')
