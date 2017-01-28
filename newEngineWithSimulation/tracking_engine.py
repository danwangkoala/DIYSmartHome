from notification import *
from ExplaSet import *
from State import *



class Tracking_Engine(object):
    def __init__(self, no_trigger = 0, sleep_interval = 1, cond_satisfy=1.0, cond_notsatisfy = 0.0, delete_trigger = 0.001):
        self._no_trigger = no_trigger
        self._sleep_interval = sleep_interval
        self._cond_satisfy = cond_satisfy
        self._cond_notsatisfy = cond_notsatisfy
        self._delete_trigger = delete_trigger

            
    def start(self):
        print "the engine has been started"
        while(True):
            notif = notification()   ##check the current notification
            
            #if no notification, and the random prob is less than no_notif_trigger_prob
    #sleep the engine
            if notif._notif.qsize() == 0 and random.random()<self._no_trigger:
                time.sleep(self._sleep_interval)
                
            #go through the engine logic to update    
            else:
                exp = explaSet(cond_satisfy = self._cond_satisfy, cond_notsatisfy = self._cond_notsatisfy, delete_trigger = self._delete_trigger)
                exp.explaInitialize()
                  
                ##calcuate the posterior prob of each action in pending set
                exp.action_posterior()
                
                
                ##update the belief state
                state = State()
                state.update_state_belief()
                
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
                
    
                
                exp.pendingset_generate()

                exp.task_prob_calculate()
                
                
                
                '''
                for x in exp.explaset:
                    print "the probability is", x._prob
                    
                    print "the pdngin set is", x._pendingSet
                '''
                print "the exlalength is", len(exp.explaset)
                exp.print_explaSet()
                exp.task_prob_calculate()
                print "go into the next loop"
                print 
                print 
                '''
                for x in exp.explaset:
                    print x._prob
                    print x._forest
                    print x._pendingSet    
                '''
                ##calculate the probability of goals and innner nodes in the tree
                ##this kind of information is used for promp decision making. 
                ##unlike the paper, my algorithm needs to calculate the probability of
                ##each node. So as to realize hierarchical prompt.                
            ##break                    
            
            
       
            
        
    
    