from database import *
from notification import * 
from helper import *
from explanation import *


cond_satisfy = 1.0
cond_notsatisfy = 0.0
title = []
db = DB_Object()

def action_posterior():
    exp = explaSet()
    
    for expla in exp.explaset:
        for action in expla._pendingSet:
            action[1]=action[1]*cal_posterior(action)
            print "the probability is", action[0], action[1]
            #####################
    #return explaSet
    

def cal_posterior(action):
    op = db.get_operator(action[0])
    
    beforeS = []
    for x in op["precondition"]:
        beforeS.append(db.get_object_status(x))
    
    for x in beforeS:
        for y in x:
            if y!="ob_name" and y!="ob_type" and y!="_id":
                title.append([x["ob_name"], y])     
                
    #enum: state enumeration       
    enum = myDFS(title, beforeS)
    new_prob=variable_elim(enum, op) 
    return new_prob


##dfs is used to generate the enumeration of all possible
##state combinations    
def myDFS(title, beforeS):
    enum = []
    va = []
    realMyDFS(enum, va, title, beforeS)
    return enum


def realMyDFS(enum, va, title, beforeS):
    if len(va)==len(title):
        enum.append(list(va))
        return enum
        
    key = title[len(va)]
    select_state = [x for x in beforeS if x["ob_name"]==key[0]]
    attr = select_state[0][key[1]]
    for x in attr:
        va.append(x)
        realMyDFS(enum, va, title, beforeS)
        va.remove(x)
        
##impliment the bayesian network calculation for one possible state
#op: the operator in knowlege base, prob: the prior of the action
def variable_elim(enum, op):
    new_prob_1 = 0 #this action happened
    new_prob_2 = 0 #this action does not happend
    for before in enum:
        for after in enum:
            p = bayesian_expand(before, after, op)
            new_prob_1 = new_prob_1 + p[0]
            new_prob_2 = new_prob_2 + p[1]
    return float(new_prob_1)/(new_prob_1+new_prob_2)
    
    
#sv: an concrete state value, op: the operator in knowledge base
#state_c: the notification        
def bayesian_expand(before, after, op):
    #calculate p(s_t-1)
    ps_before = 1
    for i, s in enumerate(before):
        thisp = db.get_attribute_prob(s, title[i][0], title[i][1])
        ps_before = ps_before*float(thisp)
    
    #calculate p(o_t|s_t)
    po_s = 1
    for i, s in enumerate(after):
        thisp = db.get_obs_prob(s, title[i][0], title[i][1])
        po_s = po_s *float(thisp)    
    
    
    ps_actANDs_1 = get_ps_actANDs_1(before, after, op)
    ps_actANDs_2 = get_ps_actANDs_2(before, after)
    
    prob = []
    prob.append(float(ps_before)*po_s*ps_actANDs_1)
    prob.append(float(ps_before)*po_s*ps_actANDs_2)
    
    return prob

#calculate p(s|s_t-1, a_t) happen    
def get_ps_actANDs_1(before, after, op):   
    bef = list(before)
    af = list(after)
    #check precondition
    prob = 1
    precond = op["precondition"]
    for ob in precond:
        for attri in precond[ob]:
            index = title.index([ob, attri])
            if attri=="ability":
                ability_list = bef[index].split(",")
                if compare_ability(ability_list, precond[ob][attri]) is False:
                    return 0
            else:
                if precond[ob][attri]!=bef[index]:
                    return 0
  
    ##check effect
    effect = op["effect"]
    for ob in effect:
        for attri in effect[ob]:
            index=title.index([ob, attri])
            bef[index]=effect[ob][attri]
    if bef!=af:  
        return 0
        
    return 1


#calculate p(s|s_t-1, a_t) not happen
def get_ps_actANDs_2(before, after):
    if before==after: return float(1)
    else: return float(0)    

            
