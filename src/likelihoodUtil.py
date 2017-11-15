from nodeUtil import NodeUtil

class LikelihoodUtil:


#|-----------------------------------------------------------------------------|
# likelihood_weighting
#|-----------------------------------------------------------------------------|
    def likelihood_weighting(self, query,evidences_input,alarmBayes,sample_list):
        """
        
        """
        weight = self.weighted_sampling(evidences_input, alarmBayes)

        return weight
        
#|------------------------likelihood_weighting -ends---------------------------|    
#|-----------------------------------------------------------------------------|
# weighted_sampling
#|-----------------------------------------------------------------------------|
    def weighted_sampling(self, evidences_input,alarmBayes):
        """
        
        """
        weight = 1
        
        #generating samples
        alarmBayes.reset_assignments()
        alarmBayes.consider_evidences(evidences_input)

        #for all nodes, check whether they are in evidence, or not
        for node in alarmBayes.all_nodes:
            for myNode in alarmBayes.all_nodes:
                #debug
                print ('{} = {}, {} '.format(myNode.representation, myNode.cond_distribution, myNode.assignment))
                #debug -ends
            if any(node.representation in sublist for sublist in evidences_input):
                for index, sublist in enumerate(evidences_input):
                    if sublist[0]==node.representation:
                        nodeIndex = index
                    #if sublist =ends
                #for index, sublist -ends
                truth_val = evidences_input[nodeIndex][1]
                
                #if node is part of evidence, take its true value

                weight = weight*self.find_node_probability(node, truth_val, evidences_input)
                #debug
                print ('weight = {}\n '.format(weight))
                #debug -ends

            else:
                node.assign_new_random_value_based_on_parent()
        #for node -ends

        return weight
     
#|------------------------weighted_sampling -ends------------------------------|

#|-----------------------------------------------------------------------------|
# find_node_probability
#|-----------------------------------------------------------------------------|
    def find_node_probability(self, node, truth_val, evidences_input):
        """
        
        """
        
                
        if node.parent_nodes!=None:
            assignmentStr = ""
            for parent_node in node.parent_nodes: 
                if parent_node.assignment!=NodeUtil.ASSIGNMENT_NONE:
                    assignmentStr+=parent_node.assignment
                else:
                    assignmentStr+=NodeUtil.ASSIGNMENT_TRUE
                #if parent_node -ends
            #for parent_node -ends

            #debug
            print ('assignmentStr = {} '.format(assignmentStr))
            #debug -ends
            if truth_val[0].upper()=='T':
                node_probability = node.cond_distribution[assignmentStr.upper()]
            else:
                node_probability = 1-node.cond_distribution[assignmentStr.upper()]
            #if -ends
        else:
            if truth_val[0].upper()=='T':
                node_probability = node.cond_distribution['T']
            else:
                node_probability = 1-node.cond_distribution['T']
            #if truth_val -ends
        #if node.parent_ndoe -ends
        
#         #assigning value
#         if tr 
#         if node_probability>=0.5:
#             node.assignment=NodeUtil.ASSIGNMENT_TRUE
#         else:
#             node.assignment=NodeUtil.ASSIGNMENT_FALSE
        
        return node_probability
    
#|------------------------find_node_probability -ends----------------------------------|    
