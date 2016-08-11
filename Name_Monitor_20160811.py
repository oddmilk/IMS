
# Source Data
	# SFDC: Aug. 1 - Sug. 9
	# MoveIt: Aug. 1 - Aug. 11


# Unzip VR files
zipfilePath_ = '/Users/mengjichen/Desktop/Roche/201608_Names_VR'
destinationfile_path = '/Users/mengjichen/Desktop/Roche/201608_Names_VR'
MOVEIT = readMoveIt('/Users/mengjichen/Desktop/Roche/201608_Names_VR', '*.FLAT')
Num_Names_MOVEIT = MOVEIT.REQUEST_ID_CLIENT.unique()

# Subset DCR ITEM which update client names
Names_CR = SFDC_DCR_ITEM[SFDC_DCR_ITEM.Field_API_Name_g__c == 'Gender_g__pc']
Num_Names_CR = Names_CR.Change_Request_ref_g__c.unique()

# DCR updating client names that finally landed in MOVEIT
Names_DCR_landed = MOVEIT[MOVEIT.REQUEST_ID_CLIENT.isin(Num_Names_CR)]
# DCR departure
len(Num_Names_CR)
# DCR arrival (a number of DCRs departing from SFDC might drop out in Conversion Tool: out-of-scope or)
len(Names_DCR_landed.index)

Names_DCR_In = Names_CR[Names_CR.Change_Request_ref_g__c.isin(Names_DCR_landed.REQUEST_ID_CLIENT.unique())]
