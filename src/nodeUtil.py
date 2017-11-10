import random

class NodeUtil:
    ASSIGNMENT_TRUE = "t"
    ASSIGNMENT_NONE = "n"
    ASSIGNMENT_FALSE = "f"

# -----------------------------------------------------------------------------|
# __init__
# -----------------------------------------------------------------------------|
    def __init__(self, name, representation, parent_nodes, cond_distribution):
        self.name = name
        self.representation = representation
        self.parent_nodes = parent_nodes
        self.cond_distribution = cond_distribution
        self.assignment = NodeUtil.ASSIGNMENT_NONE
# ------------------------ __init__ - ends-------------------------------------|

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
            raise Exception("Parent assignment error detected for " + self.name\
                                                                     + "node")
        elif target_self_assignment is NodeUtil.ASSIGNMENT_TRUE:
            # print ("+node:" + self.name)
            return self.cond_distribution[parent_assignment_combination]
        elif target_self_assignment is NodeUtil.ASSIGNMENT_FALSE:
            # print ("-node:" + self.name)
            return 1.0 - self.cond_distribution[parent_assignment_combination]
        else:
            raise Exception('no correct self assignment found for ' + self.name\
                                                                    + " node")
        #if parent_assignment_combination -ends

# ------------------------ get_probability_for_assignment - ends---------------|

# -----------------------------------------------------------------------------|
# set_assignment
# -----------------------------------------------------------------------------|
    def set_assignment(self, assignment):
        """
        if assignment = 'T', 't', "true", "TRUE" will assign ASSIGNMENT_TRUE
        if assignment = 'F', 'f', "false", "FALSE" will assign ASSIGNMENT_FALSE
        """
        if assignment in {'T', 't', NodeUtil.ASSIGNMENT_TRUE, 'true', "TRUE"}:
            self.assignment = NodeUtil.ASSIGNMENT_TRUE
        elif assignment in {'F', 'f', NodeUtil.ASSIGNMENT_FALSE, 'false', "FALSE"}:
            self.assignment = NodeUtil.ASSIGNMENT_FALSE
        else:
            self.assignment = NodeUtil.ASSIGNMENT_NONE
        #if assignment -ends
# ------------------------ set_assignment - ends-------------------------------|

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
        #if self.parent_nodes -ends

        assignment = ""
        for parent in self.parent_nodes:
            if parent.assignment is NodeUtil.ASSIGNMENT_NONE:
                return None
            elif parent.assignment is NodeUtil.ASSIGNMENT_TRUE:
                assignment += 'T'
            elif parent.assignment is NodeUtil.ASSIGNMENT_FALSE:
                assignment += 'F'
            else:
                return None
            #if parent.assignemnt -ends
        #for parent -ends

        return assignment
# ------------------------ get_parent_assignment_combination - ends------------|

# -----------------------------------------------------------------------------|
# assign_new_random_value_based_on_parent
# -----------------------------------------------------------------------------|
    def assign_new_random_value_based_on_parent(self):
        """
        this will generate new random number. and assign a truth value based on
        that number.
        if random number is less or equal to it's probability for assignment 
        true, it will be assigned true else false
        """
        random_value = random.uniform(0, 1)
        # //print random_value
        # print "should be <="
        # print self.cond_distribution[self.get_parent_assignment_combination()]
        if random_value <= self.get_probability_for_assignment(\
                                                        NodeUtil.ASSIGNMENT_TRUE):
            self.assignment = NodeUtil.ASSIGNMENT_TRUE
        else:
            self.assignment = NodeUtil.ASSIGNMENT_FALSE
        #if random_values -ends
# ------------------------ assign_new_random_value_based_on_parent - ends------|