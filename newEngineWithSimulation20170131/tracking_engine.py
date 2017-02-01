import random
import time
from notification import *
from ExplaSet import *
from State import *
from Simulator import *



class Tracking_Engine(object):
    def __init__(self, no_trigger = 0, sleep_interval = 1, cond_satisfy=1.0, cond_notsatisfy = 0.0, delete_trigger = 0.001, non_happen = 0.00001):
        self._no_trigger = no_trigger
        self._sleep_interval = sleep_interval
        self._cond_satisfy = cond_satisfy
        self._cond_notsatisfy = cond_notsatisfy
        self._delete_trigger = delete_trigger
        self._non_happen = non_happen

            
    def start(self):
        print "the engine has been started"
        notif = notification()   ##check the current notification
        exp = explaSet(cond_satisfy = self._cond_satisfy, cond_notsatisfy = self._cond_notsatisfy, delete_trigger = self._delete_trigger, non_happen = self._non_happen)
        exp.explaInitialize()
        exp.print_explaSet()
        
        
        while(notif._notif.qsize()>0):
            step = notif.get_one_notif()
            notif.delete_one_notif()
            
            #if no notification, and the random prob is less than no_notif_trigger_prob
    #sleep the engine
            
            if step == "none" and random.random()<self._no_trigger:
                time.sleep(self._sleep_interval)
                
            #go through the engine logic to update    
            else:
                if step != "none":
                    realStateANDSensorUpdate(step)
                      
                ##calcuate the posterior prob of each action in pending set
                exp.action_posterior()
                
                
                ##update the belief state
                state = State()
                state.update_state_belief(exp)
                
                
                ##update the explanation         
                ##for each existing explanation, includes three steps:
                    ##step1: decide which actions has happended and its distribution
                            ##(obtain the action level explanation for the current obs)
                    ##step2: for each action level explanation, generate new explanation and
                            ##update the corresponding tree structure, and calculate the
                            ##probability of the explanation
                    ##step3: calculate the probability of this explanation
                    ##step4: update the pending set
                            ##(including the prior probability of actions in the pending set)
                exp.explaSet_expand()
                
                '''
                
                exp.pendingset_generate()

                exp.task_prob_calculate()
                
                
                
                
                print "the exlalength is", len(exp.explaset)
                exp.print_explaSet()
                
                exp.task_prob_calculate()
                '''
                #exp.print_explaSet()
                print "go into the next loop"
                print 
                print 
               
         
                ##calculate the probability of goals and innner nodes in the tree
                ##this kind of information is used for promp decision making. 
                ##unlike the paper, my algorithm needs to calculate the probability of
                ##each node. So as to realize hierarchical prompt.                
            ##break   
            
                          
            
            
       
            
        
    
    