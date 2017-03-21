################################################################################################
####                        ExecuteSequence class                                           ####
####                        Store execute sequence, effect summary                          ####
################################################################################################
import sys
sys.dont_write_bytecode = True

import copy
from termcolor import colored
from database import *


db = DB_Object()
# 1. sequence: []
# 2. effect_summary = {"obj_name/att_name": {"value": v, "step_name": sn}},}

class ExecuteSequence(object):
    def __init__(self, sequence = [], effect_summary = {}):
        self._sequence = sequence
        self._effect_summary = effect_summary
        
        
    def add_action(self, step_name):
        #if step_name == 'rinse_hand':
         #   print self._sequence
        #print self._sequence
        self._sequence.append(step_name)
        #if step_name == 'rinse_hand':
         #   print "after, ", self._sequence
        #print "after, ", self._sequence
        op = db.get_operator(step_name)
        for obj in op["effect"]:
            for att in op["effect"][obj]:
                new_key = obj + "/" + att
                if (new_key in self._effect_summary) and (self._effect_summary[new_key]["value"] == op["effect"][obj][att]):
                    continue
                    '''
                    print colored('There is two actions has the same result effect', 'red')
                    print "action first", self._effect_summary[new_key]["step_name"]
                    print "action second", step_name
                    exit(0)
                    '''
                else:
                    new_item = {}
                    new_item["value"] = op["effect"][obj][att]
                    new_item["step_name"] = step_name
                    self._effect_summary[new_key] = new_item
                    
                    
                    
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                     
