

#Function: "dict_same" is used to compare two dict
#DataSource: the two dict come from the mongoDB database
#Caution: do not compare property "_id"
##########?????????????????????????????????????????????
#??????????????????not use now????????????????????????
def dict_same(dict_1, dict_2):
    if len(dict_1)!=len(dict_2):
        return False
    keys = dict_1.keys()
    for x in keys:
        if x!="_id" and dict_1.get(x)!=dict_2.get(x):
            return False     
    return True
    
    
##Function:"compare_ability" is used to check if the patient's
##ability reach the requirement
#to check whether ability constraints satisfied
#we can add additional compare here
def compare_ability(ab1, pre_ab2):
    if pre_ab2[0] == ">=":
        return no_less_than(ab1, pre_ab2)
    return False
    
#############################################################
###################constraint################################
#############################################################
#############################################################
#constraint: no_less_than
def no_less_than(ab1, pre_ab2):
    #print ("inside no less than")
    len_ab1 = len(ab1)
    for i in range(len_ab1):
        if ab1[i] < pre_ab2[i+1]:
           return False
    return True 
