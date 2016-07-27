Algorithm Implementation record
-------------------------------
#Summary#
 This document record the progress of implementing the goal recognition algorithm, including details and modifications during each stage.
 
##July 18##

 - **explaSet**=[]: explanations for all the previous observations. Before initialization, this set has a length of 0, at this case, we need to initialize the explaSet according to the knowledge base;
 - *code knowledge base example according to the drawn dia figure*, complete the hand washing part.
 <p align="center">
  <img src="../images/knowledge_base_example.png" width="450"/>
</p>

##July 19##
 - Initialize the explanation set (explaSet)
	 - Step 1: search in "method" collection who has a property of "start_action"
	 - Step 2: for all the returned entries, check if their preconditions are satisfied in the current state
	 - Step 3 : generate the pending set and initialize the explaSet.
 - Initialize the explanation Set (explaSet): didn't finish, only store the updated knowledge base into mongoDB

##July 20##
 - realize explaSet initialization. 

##July 21##
 - create a database class, inside this class, all database related search and operations are included. 
 - calculate action posterior prob based on s(t-1), and o(t), for a given action:
	 - Step 1,  create a list for all it's related object attribute
	 - Step 2, create a list of all possible attribute value combination
	 - Step 3, Bayesian variable elimination to calculate posterior(a)

##July 22##
 - define p(s_t|s_t-1, a_t)
	 - assume that if an action has been implemented, it will ben 100% succeed. 
	 - So **if** precondition(a_t) is satisfied in s_(t-1), and effects(a_t) is satisfied in (s_t), p(s_t|s_t-1, a_t)=1, **else**,  p(s_t|s_t-1, a_t)=0. 
 - calculate p(a_t) give observation
	 - The final p(a_t)[variable elimination] is given by normalizing on (**a_t happened**) and (**a_t not happen**)
	 - for the whole explanation set, calculate **prior(a_t)*posterior(a_t)[variable elimination]**, and then normalize over all the actions in all of the pending set
 - move notification to a class, every time the engine need notification, get it from the class instance.
 - *need to finish belief state update*


##July 26##

 - implement belief state update
	 - when updating, only update those states that occurs in the effect list of the pending sets. Other's remain the same
	 - finished
 - change **explaSet** to a class. 


##July 27##

 - When to trigger the engine?  According to " **no_notif_trigger_prob**"
	 - If **there is** some notification: trigger definitely
	 - If **there is no** notification: 0.9 cases sleep, 0.1 run the activity tracking process. 

 - Update the explanation set, including three steps:
	 - step 1: update the tree structure (not finished)

 - **Revision**:
	 - For each explanation, it has a pending set. Within the pending set, there are one or more than one actions. Because sensor probabilities are considered, we need to consider "**nothing happened**" scenario. 
	 - How to calculate the probability of "**nothing happened**"? If the pending set is [a_1, a_2, a_3, non]:
		 - (1) Calculate the probability of each action "**happened**"
		 - (2) Calculate the probability of "nothing happened", multiply the corresponding not-happen-prob of each action.
		 - (3) Calculate the probability of {one actions happens, two actions happens, three actions happens and so on..}
		 - (4) Step (1)(2)(3) generated the explanations for the current observation. It is something like [a1, p1; a2, p2; a2, p3; a1, a2, p12; a1, a3, p13; a2, a3, p23; a1, a2, a3, p123; non, pn ]  (**example**)
		 - (5) For each case in the action level observation explanation, update and expand the current explanation into new explanations. In this example, the explanation will generate 8 different new explanations. (when calculate the posterior (new) probability for those new explanations, be sure use the parent explanation's prior probability multiply by branch factor nodes. )
		 - (6) finally for all explanations, normalize them.  

 - Tomorrows goal:
	 - finish action level explanation calculating
	 - add a new task and test (expand the knowledge base)
	 - begin the tree structure update (should begin with initialization)

##Remain works
 - Update the explanation set, including three steps
	 - step 1: update the tree structure
	 - step 2: calculate the probability of this explanation
	 - step 3: generate the new pending set, including the prior probability of actions in the pending set


 - Calculate the probability for goals and inner nodes in the tree. Because the desired assistance is hierarchical, only provide the probability of goals is not enough. We also need to calculate the probability of inner nodes in the tree structure.   