from nodeUtil import NodeUtil



class EnumerationUtil:
    def __init__(self):
        pass

    # -----------------------------------------------------------------------------|
    # result_for_enumeration
    # -----------------------------------------------------------------------------|
    @staticmethod
    def result_for_enumeration(queries, evidence_list, input_bayesnet):
        """
        This will take list of queries and perform enum_ask for each
        """
        print("Distribution over " + input_bayesnet.find_node(query).name + ":")
        print (Enumeration.enum_ask(query, evidence_list, input_bayesnet))


    # ------------------------ result_for_enumeration - ends----------------------------------|

    # -----------------------------------------------------------------------------|
    # enum_ask
    # -----------------------------------------------------------------------------|
    @staticmethod
    def enum_ask(query, evidence_list, input_bayesnet):
        """
        this is the function asked for enum. Entry point for each
        """
        result = []
        for query_truth in (NodeUtil.ASSIGNMENT_TRUE, NodeUtil.ASSIGNMENT_FALSE):
            input_bayesnet.reset_assignments()
            input_bayesnet.consider_evidences(evidence_list)
            query_node = input_bayesnet.find_node(query)
            query_node.set_assignment(query_truth)
            result.append(Enumeration.enum_all(input_bayesnet.all_nodes, input_bayesnet.get_all_evidences()))
        return AlarmBayes.normalize(result)


    # ------------------------ enum_ask - ends----------------------------------|

    # -----------------------------------------------------------------------------|
    # enum_all
    # -----------------------------------------------------------------------------|
    @staticmethod
    def enum_all(nodes, evidences):
        """
        this will enum over all nodes in recursive manner
        """
        if nodes is None or len(nodes) is 0:
            return 1.0

        first_node = nodes[0]
        if first_node in evidences:
            # print("starting calculating {}".format(first_node.name))
            result_value = first_node.get_probability_for_assignment(first_node.assignment) * Enumeration.enum_all(
                nodes[1:], evidences)
            # print("after calculating {}".format(first_node.name))
            # print("returning {}".format(result_value))
            return result_value
        else:

            # print("starting summing out {}".format(first_node.name))

            # add nodeUtil to the evidences
            evidences = evidences + [first_node]

            # first assign "true" to the nodeUtil
            first_node.set_assignment(Node.ASSIGNMENT_TRUE)
            positive_value = first_node.get_probability_for_assignment(first_node.assignment) * Enumeration.enum_all(
                nodes[1:], evidences)

            # now assign "false" to the nodeUtil
            first_node.set_assignment(Node.ASSIGNMENT_FALSE)
            negative_value = first_node.get_probability_for_assignment(first_node.assignment) * Enumeration.enum_all(
                nodes[1:], evidences)
            # print("after Summing out {}".format(first_node.name))
            # print("returning {}".format(positive_value + negative_value))
            return positive_value + negative_value
            # ------------------------ enum_all - ends----------------------------------|  # -----------------------------------------------------------------------------|


    # get_count_from_dict
    # -----------------------------------------------------------------------------|
    def get_count_from_dict(bayes_net, fixed_assigned_vars, count_dict):
        """
    
        """
        var_pos_values = []
        for assigned_var in fixed_assigned_vars:
            node = bn.find_node(assigned_var[0])
            pos = bn.node_pos_in_list(node)
            var_pos_values.append((pos, assigned_var[1]))
    
        # print var_pos_values
        count = 0
        for key in bn.gen_combinations():
            is_eligible_assignment = True
            for pos_value in var_pos_values:
                if key[pos_value[0]] is not pos_value[1]:
                    is_eligible_assignment = False
                    break
    
            if is_eligible_assignment:
                count += count_dict[key]
    
        return count
    
    
    # ------------------------ get_count_from_dict - ends----------------------------------|