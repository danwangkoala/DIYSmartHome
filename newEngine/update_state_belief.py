from database import *
from notification import * 
from helper import *
from explanation import *


cond_not_satisfy = 0.001
cond_satisfy = 0.999
title = [] #all possible state in the effect list of pending set actions 
db = DB_Object()
exp=explaSet()
update_state = []
action_list = []

def update_state_belief():    
    get_attr_in_effect()
    for i, x in enumerate(title):
        att = db.get_object_attri(x[0], x[1])
        att = update_attri_status_belief(att, i)
        db.update_state_belief(title[i][0], title[i][1], att)

#get all the state that occur in the effect list
#of actions in the pending set
def get_attr_in_effect():
    my_set = set()
    for expla in exp.explaset:
        for action in expla._pendingSet:
            action_list.append(action)
            op = db.get_operator(action[0])
            for x in op["effect"]:
                for y in op["effect"][x]:
                    s = x+"."+y
                    my_set.add(s)
    for x in my_set:
        title.append(x.split('.'))
    return 

#update the attribute status belief for a specific attribute
def update_attri_status_belief(att, index):
    newp = att
    sump=0
    for x in newp:
        p = 0
        for y in att:
            for a in action_list:
                ##p(a)
                pa = float(a[1])
                ##p(s_1)
                ps_1 = float(att[y])
                #calculate p(o_t|s_t)
                po_s = db.get_obs_prob(x, title[index][0], title[index][1])
                #calculate p(s|s_t-1, a_t) happen
                ps_actANDs = get_ps_actANDs(x, y, a, index)
                
                p = p+pa * ps_1 * po_s * ps_actANDs 
                
        newp[x] = p
        sump = sump +p            
    
    
    #normalize
    for x in newp:
        newp[x] = newp[x]/sump
    return newp
    

def get_ps_actANDs(after, before, action, index):
    #get the action;   
    op = db.get_operator(action[0])
    
    #check effect 
    #the whether target attribute status change
    #exist in the effect list 
    #if exist, continue, else return 0   
    effect = op["effect"]
    if effect[title[index][0]][title[index][1]] != after:
        return cond_not_satisfy
    
    ##check precondition
    #check if the precondition of the action is satisfied
    #in the previous state
    precond = op["precondition"]
    if precond[title[index][0]][title[index][1]] != before:
        return cond_not_satisfy
        
    #return value
    return cond_satisfy


