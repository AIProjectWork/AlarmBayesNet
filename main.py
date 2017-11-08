import sys


class Node:
    ASSIGNMENT_TRUE = "t"
    ASSIGNMENT_NONE = "n"
    ASSIGNMENT_FALSE = "f"

    def __init__(self, name, representation, parent_nodes, cond_distribution):
        self.name = name
        self.representation = representation
        self.parent_nodes = parent_nodes
        self.cond_distribution = cond_distribution
        self.assignment = Node.ASSIGNMENT_NONE

    # -----------------------------------------------------------------------------|
    # get_probability_for_assignment
    # -----------------------------------------------------------------------------|
    def get_probability_for_assignment(self, target_self_assignment):
        """
        this will check if all parents are assigned value
        """
        # when no parent is there simply check the assignment and return value
        parent_assignment_combination = self.get_parent_assignment_combination()

        if parent_assignment_combination is None:
            raise Exception("Parent assignment error detected for " + self.name + "node")
        elif target_self_assignment is Node.ASSIGNMENT_TRUE:
            # print ("+node:" + self.name)
            return self.cond_distribution[parent_assignment_combination]
        elif target_self_assignment is Node.ASSIGNMENT_FALSE:
            # print ("-node:" + self.name)
            return 1.0 - self.cond_distribution[parent_assignment_combination]
        else:
            raise Exception('no correct self assignment found for ' + self.name + " node")

    # ------------------------ get_probability_for_assignment - ends----------------------------------|

    # -----------------------------------------------------------------------------|
    # set_assignment
    # -----------------------------------------------------------------------------|
    def set_assignment(self, assignment):
        """
        if assignment = 'T', 't', "true", "TRUE" will assign ASSIGNMENT_TRUE
        if assignment = 'F', 'f', "false", "FALSE" will assign ASSIGNMENT_FALSE
        """
        if assignment in {'T', 't', Node.ASSIGNMENT_TRUE, 'true', "TRUE"}:
            self.assignment = Node.ASSIGNMENT_TRUE
        elif assignment in {'F', 'f', Node.ASSIGNMENT_FALSE, 'false', "FALSE"}:
            self.assignment = Node.ASSIGNMENT_FALSE
        else:
            self.assignment = Node.ASSIGNMENT_NONE

    # ------------------------ set_assignment - ends----------------------------------|

    # -----------------------------------------------------------------------------|
    # get_parent_assignment_combination
    # -----------------------------------------------------------------------------|
    def get_parent_assignment_combination(self):
        """
        if no parent => "T"
        if one parent true => "T"
        if one parent false = "F"
        if 1st parent true, 2nd true = "TT"
        if 1st parent true, 2nd false = "TF"
        ...
        ...
        if any parent if missing assignment => None
        """
        if self.parent_nodes is None:
            return 'T'

        assignment = ""
        for parent in self.parent_nodes:
            if parent.assignment is Node.ASSIGNMENT_NONE:
                return None
            elif parent.assignment is Node.ASSIGNMENT_TRUE:
                assignment += 'T'
            elif parent.assignment is Node.ASSIGNMENT_FALSE:
                assignment += 'F'
            else:
                return None

        return assignment
        # ------------------------ get_parent_assignment_combination - ends----------------------------------|


class AlarmBayes:
    def __init__(self):
        burglary = Node("Burglary", "B", None, {'T': 0.001})
        earthquack = Node("Earthquack", "E", None, {'T': 0.002})
        alarm = Node("Alarm", "A", [burglary, earthquack], {'TT': 0.95, 'TF': 0.94, 'FT': 0.29, 'FF': 0.001})
        john = Node("JohnCalls", "J", [alarm], {'T': 0.9, 'F': 0.05})
        mary = Node("MaryCalls", "M", [alarm], {'T': 0.7, 'F': 0.01})
        self.all_nodes = [burglary, earthquack, alarm, john, mary]

    # -----------------------------------------------------------------------------|
    # find_node
    # -----------------------------------------------------------------------------|
    def find_node(self, name_or_representation):
        """
        match node based on name or representation
        """
        for node in self.all_nodes:
            if name_or_representation.lower() in {node.name.lower(), node.representation.lower()}:
                return node
        return None
        # ------------------------ find_node - ends----------------------------------|

    # -----------------------------------------------------------------------------|
    # reset_assignments
    # -----------------------------------------------------------------------------|
    def reset_assignments(self):
        """
        Make all nodes' assignment to ASSIGNMENT_NONE
        """
        for node in self.all_nodes:
            node.set_assignment(None)

    # ------------------------ reset_assignments - ends----------------------------------|

    # -----------------------------------------------------------------------------|
    # consider_evidence
    # -----------------------------------------------------------------------------|
    def consider_evidences(self, evidences):
        """
        this will assign truth value for all node from evidence
        """
        for evidence in evidences:
            node = self.find_node(evidence[0])
            node.set_assignment(evidence[1])

    # ------------------------ consider_evidence - ends----------------------------------|

    # -----------------------------------------------------------------------------|
    # print_all_nodes
    # -----------------------------------------------------------------------------|
    def print_all_nodes(self):
        """
        print all node name with truth value assignment
        """
        print ("All nodes status:")
        for node in self.all_nodes:
            print ("node: " + node.name + "(" + node.assignment + ")")

    # ------------------------ print_all_nodes - ends----------------------------------|

    # -----------------------------------------------------------------------------|
    # parse_input_evidence
    # -----------------------------------------------------------------------------|
    @staticmethod
    def parse_evidence_input(input_value):
        """
        input is received as [<A,t><B,f>] string. need to convert it into list of tuples
        """
        all_evidence = []
        input_value = input_value.replace("[", "")
        input_value = input_value.replace("]", "")
        while '>' in input_value:
            start_pos = input_value.index("<")
            end_pos = input_value.index(">")
            single_entry = input_value[start_pos:end_pos + 1]
            input_value = input_value[end_pos + 1:]
            single_tuple = single_entry[1:single_entry.index(",")], single_entry[single_entry.index(",") + 1:-1]
            # print(single_tuple[0] + " truthValue: " + single_tuple[1])
            all_evidence.append(single_tuple)
        print(all_evidence)
        return all_evidence
        # ------------------------ parse_input_evidence - ends----------------------------------|

    # -----------------------------------------------------------------------------|
    # parse_query_input
    # -----------------------------------------------------------------------------|
    @staticmethod
    def parse_query_input(input_value):
        """
        sample input will be string [J,M]
        this should return list of nodes representing J and M
        """
        return input_value.replace("[", "").replace("]", "").split(",")
        # ------------------------ parse_query_input - ends----------------------------------|

    # -----------------------------------------------------------------------------|
    # normalize
    # -----------------------------------------------------------------------------|
    @staticmethod
    def normalize(distribution):
        """
        takes distribution and return normalized distribution
        <0.1,0.4> => <0.2,0.8> //this will sum to 1.0
        """
        total = 0
        for value in distribution:
            total += value

        result = []
        for value in distribution:
            result.append(value / total)

        return result

        # ------------------------ normalize - ends----------------------------------|

    # -----------------------------------------------------------------------------|
    # get_all_evidences
    # -----------------------------------------------------------------------------|
    def get_all_evidences(self):
        """
        returns list of nodes with assigned truth values
        """
        evidence_list = []
        for node in self.all_nodes:
            if node.assignment is not Node.ASSIGNMENT_NONE:
                evidence_list.append(node)
        return evidence_list
        # ------------------------ get_all_evidences - ends----------------------------------|


class Enumeration:
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
        for query in queries:
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
        for query_truth in (Node.ASSIGNMENT_TRUE, Node.ASSIGNMENT_FALSE):
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

            # add node to the evidences
            evidences = evidences + [first_node]

            # first assign "true" to the node
            first_node.set_assignment(Node.ASSIGNMENT_TRUE)
            positive_value = first_node.get_probability_for_assignment(first_node.assignment) * Enumeration.enum_all(
                nodes[1:], evidences)

            # now assign "false" to the node
            first_node.set_assignment(Node.ASSIGNMENT_FALSE)
            negative_value = first_node.get_probability_for_assignment(first_node.assignment) * Enumeration.enum_all(
                nodes[1:], evidences)
            # print("after Summing out {}".format(first_node.name))
            # print("returning {}".format(positive_value + negative_value))
            return positive_value + negative_value
            # ------------------------ enum_all - ends----------------------------------|


if __name__ == '__main__':
    bn = AlarmBayes()
    # bn.find_node("B").set_assignment(Node.ASSIGNMENT_TRUE)
    # bn.find_node("E").set_assignment(Node.ASSIGNMENT_TRUE)
    # p_a_true = bn.find_node("a").get_probability_for_assignment(Node.ASSIGNMENT_TRUE)
    # print ("Probability of alarm being true {}".format(p_a_true))

    evidences_input = AlarmBayes.parse_evidence_input(sys.argv[1])
    query_params = AlarmBayes.parse_query_input(sys.argv[2])

    # result by enumeration
    Enumeration.result_for_enumeration(query_params, evidences_input, bn)
