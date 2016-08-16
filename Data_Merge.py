# Merging source data
SFDC_DCR = readFile(SFDC_DCR_PATH, '*.CSV', '#Id')
SFDC_DCR_ITEM = readFile(SFDC_ITEM_PATH, '*.CSV', '#Id')
OK_DCR = readFile(OK_DCR_PATH, '*.CSV', '\ufeff"Id"')
OK_DCR_ITEM = readFile(OK_ITEM_PATH, '*.CSV', '\ufeff"Id"')

# Subseting data
SFDC_DCR_SUB = SFDC_DCR[SFDC_DCR_sub_fields]
SFDC_DCR_ITEM_SUB = SFDC_DCR_ITEM[ITEM_sub_fields]
OK_DCR_SUB = OK_DCR[OK_DCR_sub_fields]
OK_DCR_ITEM_SUB = OK_DCR_ITEM[ITEM_sub_fields]

# Loading data from MOVEIT
unzipper(unzipper_source, unzipper_destination)
MOVEIT = readMoveIt(path, pattern_)

# Subseting MOVEIT data
DataIn = MOVEIT[MoveIt_sub_fields]
DataIn["FULLNAME"] = DataIn["IND_LASTNAME"].map(str) + DataIn["IND_FIRSTNAME"].map(str)

# Save and export merged source data
list_MV = [MOVEIT, DataIn]
list_SFDC = [SFDC_DCR, SFDC_DCR_ITEM, SFDC_DCR_SUB, SFDC_DCR_ITEM_SUB]
list_OK = [OK_DCR, OK_DCR_ITEM, OK_DCR_SUB, OK_DCR_ITEM_SUB]
save_xls(list_MV, './MOVEIT.xlsx')
save_xls(list_SFDC, './SFDC.xlsx')
save_xls(list_OK, './OK.xlsx')

