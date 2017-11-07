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
            raise "Parent assignment error detected for" + self.name
        elif target_self_assignment is Node.ASSIGNMENT_TRUE:
            return self.cond_distribution[parent_assignment_combination]
        elif target_self_assignment is Node.ASSIGNMENT_FALSE:
            return 1 - self.cond_distribution[parent_assignment_combination]
        else:
            raise 'no correct self assignment found'

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
            return 'F'

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


if __name__ == '__main__':
    bn = AlarmBayes()
    print ("bayes created {}".format(bn.all_nodes))
    bn.find_node("B").set_assignment(Node.ASSIGNMENT_TRUE)
    bn.find_node("E").set_assignment(Node.ASSIGNMENT_TRUE)
    p_a_true = bn.find_node("a").get_probability_for_assignment(Node.ASSIGNMENT_TRUE)
    print ("Probability of alarm being true {}".format(p_a_true))
