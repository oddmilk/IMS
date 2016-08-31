# Data monitor report parameters
# reset directory & read in DCR & DCR ITEM data
wd = os.chdir('/Users/mengjichen/Desktop/Roche/201608/BUG')

# reset file directory to load in DCR data
SFDC_DCR_PATH = './SFDC_DCR'
SFDC_ITEM_PATH = './SFDC_ITEM'
OK_DCR_PATH = './OK_DCR'
OK_ITEM_PATH = './OK_ITEM'

# selecting data fields
SFDC_DCR_sub_fields = ['Id', 'Master_DCR_g__c', 'sourceFile', 'Type_g__c']
OK_DCR_sub_fields = ['Id', 'Master_DCR_g__c', 'sourceFile', 'Type_g__c', 'Remarks_g__c', 'Status_g__c']
ITEM_sub_fields = ['Id', 'Change_Request_ref_g__c', 'sourceFile', 'Field_API_Name_g__c', 'Name', 'Old_Field_Value_Text_g__c', 'Field_value_text_g__c']

# Obtaining data from MOVEIT 
unzipper_source = './VR/'
unzipper_destination = './MOVEIT'
path = './MOVEIT'
pattern_ = '*.FLAT'

# Selecting data fields from MOVEIT
MoveIt_sub_fields = ['REQUEST_ID_CLIENT', 'REQUEST_DATE', 'REQUEST_COMMENT', 
'IND_FIRSTNAME', 'IND_LASTNAME', 'IND_GENDER_COD', 
'IND_CLASS_COD', 'ACT_ROLE_1',
'IND_ID_CEGEDIM', 'WKP_ID_CEGEDIM', 
'IND_SPECIALITY_1', 'IND_TITLE_COD', 'WKP_SPECIALITY_1', 
'WKP_PARENT_USUAL_NAME', 'sourceFile']

# To-be-validated data fields in DCR ITEM 
To_be_validated = ['Job_Title_g__c', 
'Gender_g__pc', 
'LastName', 
'Professional_Type_g__pc', 
'Professional_Subtype_g__pc',
'Specialty_ref_g__c',
'Primary_Specialty_g__pc']

