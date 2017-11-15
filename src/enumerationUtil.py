from alarmBayes import AlarmBayes
from nodeUtil import NodeUtil


class EnumerationUtil:


# -----------------------------------------------------------------------------|
# result_for_enumeration
# -----------------------------------------------------------------------------|
    def result_for_enumeration(self, query, evidence_list, input_bayesnet):
        """
        This will take list of queries and perform enum_ask for each
        """
        print ("\n------------ exact result by enumeration --------------")
        print("Distribution over " + input_bayesnet.find_node(query).name + ":")
        result = self.enum_ask(query, evidence_list, input_bayesnet)
        print ("<{},{}>".format(result[0], result[1]))


# ------------------------ result_for_enumeration - ends-----------------------|
#|-----------------------------------------------------------------------------|
# result_for_sampling
#|-----------------------------------------------------------------------------|
    def result_for_sampling(self,query,evidences_input,alarmBayes,sample_list):
        """
        Input: query, evidence list, bayesnet and sample list 
        it will perform sampling and print the result
        """
        sampling_output = []
        sample_rejection_output = []
        for sample_numbers in sample_list:
            count_dict = alarmBayes.generate_samples(sample_numbers)
            count_of_evidence = self.get_count_from_dict(\
                                    alarmBayes, evidences_input, count_dict)
            count_of_query_evidence = self.get_count_from_dict(\
                                        alarmBayes, evidences_input\
                                        +[(query, NodeUtil.ASSIGNMENT_TRUE)],
                                        count_dict)
            #sampling output
            if count_of_evidence is 0:
                final_value = 0.0
            else:
                final_value = (count_of_query_evidence / float(\
                                                        count_of_evidence))
            #if count_of_evidence -ends
            sampling_output.append([sample_numbers,count_of_query_evidence,\
                                count_of_evidence, final_value,1 - final_value])

            #----------------- performing sample rejection ---------------------
            sample_rejected_dict = self.reject_samples(count_dict,\
                                                     evidences_input, alarmBayes)
#             #debug
#             print ('sample_rejected_dict = {} '.format(sample_rejected_dict))
#             #debug -ends
            count_of_evidence = self.get_count_from_dict(\
                                    alarmBayes, evidences_input, sample_rejected_dict)
            count_of_query_evidence = self.get_count_from_dict(\
                                        alarmBayes, evidences_input\
                                        +[(query, NodeUtil.ASSIGNMENT_TRUE)],
                                        sample_rejected_dict)

            if count_of_evidence is 0:
                final_value = 0.0
            else:
                final_value = (count_of_query_evidence / float(\
                                                        count_of_evidence))
            #if count_of_evidence -ends
            sample_rejection_output.append([sample_numbers,count_of_query_evidence,\
                                count_of_evidence, final_value,1 - final_value])

        #for sample_numbers -ends


        return sampling_output, sample_rejection_output

# |-----------------------------------------------------------------------------|
# result_for_sampling
# |-----------------------------------------------------------------------------|
    def result_for_sampling_rejection(self, query, evidences_input, alarmBayes, sample_list):
        """
        Input: query, evidence list, bayesnet and sample list
        it will perform sampling and print the result
        output will be array of results. rach result is array. result[0] is number of samples and result[1] is distribution
        """
        sample_rejection_output = []
        for sample_numbers in sample_list:
            distribution = self.get_distribution_with_sample_rejection(sample_numbers, alarmBayes, query, evidences_input)
            sample_rejection_output.append([sample_numbers, distribution])

        # for sample_numbers -ends


        return sample_rejection_output


    #|------------------------result_for_sampling -ends----------------------------|


# -----------------------------------------------------------------------------|
# get_distribution_with_sample_rejection
# -----------------------------------------------------------------------------|
    def get_distribution_with_sample_rejection(self, samples_count, alarm_bayes, query, evidences):
        """
        This will generate sample and reject if it is not supported by evidence
        """
        distribution = [0, 0]  # first for supporting with query true sample, other for supporting -ve sample
        for i in range(0, samples_count):
            sample_assignment = alarm_bayes.generate_single_sample()
            if alarm_bayes.is_consistent_with_evidence(sample_assignment, evidences):
                query_index = alarm_bayes.all_nodes.index(alarm_bayes.find_node(query))
                if sample_assignment[query_index] is NodeUtil.ASSIGNMENT_TRUE:
                    distribution[0] = distribution[0] + 1
                else:
                    distribution[1] = distribution[1] + 1
        return distribution

# ------------------------ get_distribution_with_sample_rejection - ends----------------------------------|
#|-----------------------------------------------------------------------------|
# reject_samples
#|-----------------------------------------------------------------------------|
    def reject_samples(self, count_dict,evidences_input, alarmBayes):
        """
        Here we are taking count_dict and matching its key with all evidences.
        key is taken in output_dict if all evidence matches with key in count_dict

        """
        output_dict = {}
        for key in count_dict:
            matchFlag = 0
            total_evidences = len(evidences_input)
            for evidence in evidences_input:
                node = alarmBayes.find_node(evidence[0])
                node_index = alarmBayes.all_nodes.index(node)

                if (key[node_index]==evidence[1]):
                    matchFlag+=1
                #if -ends
            #for evidence -ends
            if total_evidences==matchFlag:
                output_dict[key]=count_dict[key]
            #if total_evidence -ends
        #for key -ends
        return output_dict

#|------------------------reject_samples -ends----------------------------------|

# -----------------------------------------------------------------------------|
# enum_ask
# -----------------------------------------------------------------------------|
    def enum_ask(self, query, evidence_list, input_bayesnet):
        """
        this is the function asked for enum. Entry point for each
        """
        result = []
        for query_truth in (NodeUtil.ASSIGNMENT_TRUE, NodeUtil.ASSIGNMENT_FALSE):
            input_bayesnet.reset_assignments()
            input_bayesnet.consider_evidences(evidence_list)
            query_node = input_bayesnet.find_node(query)
            query_node.set_assignment(query_truth)
            result.append(self.enum_all(input_bayesnet.all_nodes, \
                                        input_bayesnet.get_all_evidences()))
        #for query_truth -ends
        alarmBayes = AlarmBayes()
        return AlarmBayes.normalize(result)


# ------------------------ enum_ask - ends-------------------------------------|

# -----------------------------------------------------------------------------|
# enum_all
# -----------------------------------------------------------------------------|
    def enum_all(self, nodes, evidences):
        """
        this will enum over all nodes in recursive manner
        """
        if nodes is None or len(nodes) is 0:
            return 1.0
        #if nodes -ends

        first_node = nodes[0]
        if first_node in evidences:
            # print("starting calculating {}".format(first_node.name))
            result_value = first_node.get_probability_for_assignment(\
                                                    first_node.assignment)\
                                                    * self.enum_all(nodes[1:],\
                                                                     evidences)
            # print("after calculating {}".format(first_node.name))
            # print("returning {}".format(result_value))
            return result_value
        else:

            # print("starting summing out {}".format(first_node.name))

            # add nodeUtil to the evidences
            evidences = evidences + [first_node]

            # first assign "true" to the nodeUtil
            first_node.set_assignment(NodeUtil.ASSIGNMENT_TRUE)
            positive_value = first_node.get_probability_for_assignment(\
                                                    first_node.assignment)\
                                                     *self.enum_all(nodes[1:],\
                                                                   evidences)

            # now assign "false" to the nodeUtil
            first_node.set_assignment(NodeUtil.ASSIGNMENT_FALSE)
            negative_value = first_node.get_probability_for_assignment(\
                                                    first_node.assignment)\
                                                    * self.enum_all(nodes[1:],\
                                                                     evidences)
            # print("after Summing out {}".format(first_node.name))
            # print("returning {}".format(positive_value + negative_value))
            return positive_value + negative_value
        #if first_node -ends
        # ------------------------ enum_all - ends-------------------------------------|

# -----------------------------------------------------------------------------|
# get_count_from_dict
# -----------------------------------------------------------------------------|
    def get_count_from_dict(self, bayes_net, fixed_assigned_vars, count_dict):
        """

        """
        var_pos_values = []
        for assigned_var in fixed_assigned_vars:
            node = bayes_net.find_node(assigned_var[0])
            pos = bayes_net.node_pos_in_list(node)
            var_pos_values.append((pos, assigned_var[1]))
        #for assigned_var -ends

        # print var_pos_values
        count = 0
        for key in bayes_net.gen_combinations():
            is_eligible_assignment = True
            for pos_value in var_pos_values:
                if key[pos_value[0]] is not pos_value[1]:
                    is_eligible_assignment = False
                    break
                #if key -ends
            #for pos_value -ends
            if is_eligible_assignment:
                count += count_dict[key]
            #if is_eligible_assignment -ends
        #for key -ends
        return count

# ------------------------ get_count_from_dict - ends--------------------------|
