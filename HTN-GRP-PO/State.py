"""------------------------------------------------------------------------------------------
Hierarchical Task Recognition and Planning in Smart Homes with Partially Observability
Author: Dan Wang danwangkoala@gmail.com (May 2016 - June 2017)
Supervised by Prof. Jesse Hoey (https://cs.uwaterloo.ca/~jhoey/)
Association: Computer Science, University of Waterloo.
Research purposes only. Any commerical uses strictly forbidden.
Code is provided without any guarantees.
Research sponsored by AGEWELL Networks of Centers of Excellence (NCE).
----------------------------------------------------------------------------------------------"""
#######################################################################################################
####                    The State class. Is used to udpate belief state                            ####
####                    Also refer to "Interface specification part II"                            ####
####################################################################################################### 



import sys
import copy
sys.dont_write_bytecode = True
from database import *
from ExplaSet import *



db = DB_Object()
class State(object):
    def __init__(self, cond_satisfy = 1.0, cond_notsatisfy = 0.0):
        self._cond_satisfy = cond_satisfy
        self._cond_notsatisfy = cond_notsatisfy
    
    
    def update_state_belief(self, exp):
        result = self.get_attr_in_effect(exp)
        action_list = result[0]
        title = result[1]
        for i, x in enumerate(title):
            att = db.get_object_attri(x[0], x[1])
            att = self.update_attri_status_belief(att, i, action_list, title)
            
            db.update_state_belief(title[i][0], title[i][1], att)
        
    #get all the state that occur in the effect list
    #of actions in the pending set
    def get_attr_in_effect(self, exp):
        my_set = set()
        action_list = {}
        title = []
        happen_sum = 0
        #for action_candidate in exp._action_posterior_prob:
            #action_list[action_candidate] = exp._action_posterior_prob[action_candidate]
        for action_candidate in exp._prior:
            action_list[action_candidate] = exp._prior[action_candidate]
            happen_sum = happen_sum + action_list[action_candidate]
            op = db.get_operator(action_candidate)
            for x in op["effect"]:
                for y in op["effect"][x]:
                    s = x+"."+y
                    my_set.add(s)
        
        for x in my_set:
            title.append(x.split('.'))
            
        #calculate the prob of nothing happened
        noth_prob = exp._non_happen
        
        #normalize on something happened
        happen_prob = 1-noth_prob
        for k in action_list:
            if happen_sum !=0:
                action_list[k] = (action_list[k]/happen_sum)*happen_prob   
        action_list["nothing"] = noth_prob
        
        return [action_list, title]


    #update the attribute status belief for a specific attribute
    def update_attri_status_belief(self, att, index, action_list, title):
        newp = copy.deepcopy(att)
        sump=0
        for x in newp:
            
            p = 0
            for y in att:
                
                for k, v in action_list.items():

                    ##p(a)
                    pa = float(v)

                    ##p(s_1)
                    ps_1 = float(att[y])
                    
                    #calculate p(o_t|s_t)
                    po_s = db.get_obs_prob(x, title[index][0], title[index][1])
                    
                    #calculate p(s|s_t-1, a_t) happen
                    ps_actANDs = self.get_ps_actANDs(x, y, [k, v], index, title)

                    p = p+pa * ps_1 * po_s * ps_actANDs
                         
            newp[x] = p
            sump = sump +p            

        for x in newp:
            newp[x] = newp[x]/sump
        return newp        




    def get_ps_actANDs(self, after, before, action, index, title):
        #case 1: nothing happened
        if action[0]=="nothing":
            if after==before:
                return self._cond_satisfy
            else:
                return self._cond_notsatisfy
        
        #get the action;   
        op = db.get_operator(action[0])
       
        
        #check effect 
        #the whether target attribute status change
        #exist in the effect list 
        #if exist, continue, else return 0   
        effect = op["effect"]
        
        if (title[index][0] not in effect) or (title[index][1] not in effect[title[index][0]]):
            if before == after:
                return self._cond_satisfy
            else:
                return self._cond_notsatisfy
        
        elif effect[title[index][0]][title[index][1]] != after:
            return self._cond_notsatisfy
        
        ##check precondition
        #check if the precondition of the action is satisfied
        #in the previous state
        precond = op["precondition"]
        if (title[index][1] in precond[title[index][0]]) and (precond[title[index][0]][title[index][1]] != before):
            return self._cond_notsatisfy
            
        #return value
        return self._cond_satisfy  
        
