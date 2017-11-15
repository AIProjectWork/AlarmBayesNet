
class LikelihoodUtil:


#|-----------------------------------------------------------------------------|
# likelihood_weighting
#|-----------------------------------------------------------------------------|
    def likelihood_weighting(self, query,evidences_input,alarmBayes,sample_list):
        """
        
        """
        output_weightList = {}
        for sample_numbers in sample_list:
            weightList = []
            for i in sample_numbers:
                weight = self.weighted_sampling(evidences_input, alarmBayes, sample_numbers)
                #debug
                print ('weight = {} '.format(weight))
                #debug -ends
#                 weightList[x]=weightList[x]+weight
            #for i -ends
            #TODO: check for output style; provide sample values
#             output_weightList.append(weightList)
        #for sample_numbers -ends
        return output_weightList
        
#|------------------------likelihood_weighting -ends---------------------------|    
#|-----------------------------------------------------------------------------|
# weighted_sampling
#|-----------------------------------------------------------------------------|
    def weighted_sampling(self, evidences_input,alarmBayes, sample_numbers):
        """
        
        """
        weight = 1
        node_state = None
        
        alarmBayes.consider_evidences()
        for node in alarmBayes.all_nodes:
            if any(node.representation in sublist for sublist in evidences_input):
                #if node is part of evidence, take its true value
                weight = (weight)*(node.cond_distribution)
            else:
                node.assign_new_random_value_based_on_parent()
            #if -ends
        #for node -ends
            
        
        
        
        
        
        
        #generating samples
#         count_dict = self.generate_dictionary(self.gen_combinations())
#         for i in range(0, sample_numbers):
        alarmBayes.reset_assignments()
        #for all nodes, check whether they are in evidence, or not
        for node in alarmBayes.all_nodes:
            if any(node.representation in sublist for sublist in evidences_input):
                #if node is part of evidence, take its true value
                node_probability = node.cond_distribution
                #if truth_value -ends
                weight = weight*node_probability
            else:
                node.assign_new_random_value_based_on_parent()
        #for node -ends
            
            #now all variables have been assigned values so the sample is ready
#             count_dict[self.current_assignment_comb()] = \
#                                 count_dict[self.current_assignment_comb()] + 1;
        #for i -ends
        
        # print count_dict
        return count_dict, weight
    
#|------------------------weighted_sampling -ends----------------------------------|    