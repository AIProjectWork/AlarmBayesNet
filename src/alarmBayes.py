from nodeUtil import NodeUtil

class AlarmBayes:
    
# -----------------------------------------------------------------------------|
# __init__
# -----------------------------------------------------------------------------|
    def __init__(self):
        
        burglary = NodeUtil("Burglary", "B", None, {'T': 0.001})
        earthquake = NodeUtil("Earthquake", "E", None, {'T': 0.002})
        alarm = NodeUtil("Alarm", "A", [burglary, earthquake], \
                     {'TT': 0.95, 'TF': 0.94, 'FT': 0.29, 'FF': 0.001})
        john = NodeUtil("JohnCalls", "J", [alarm], {'T': 0.9, 'F': 0.05})
        mary = NodeUtil("MaryCalls", "M", [alarm], {'T': 0.7, 'F': 0.01})
        self.all_nodes = [burglary, earthquake, alarm, john, mary]
# ---------------------------- __init__ - ends---------------------------------|
# -----------------------------------------------------------------------------|
# find_node
# -----------------------------------------------------------------------------|
    def find_node(self, name_or_representation):
        """
        match nodeUtil based on name or representation
        """
        for node in self.all_nodes:
            if name_or_representation.lower() in {node.name.lower(), \
                                                  node.representation.lower()}:
                return node
        return None
# ------------------------ find_node - ends------------------------------------|

# -----------------------------------------------------------------------------|
# reset_assignments
# -----------------------------------------------------------------------------|
    def reset_assignments(self):
        """
        Make all nodes' assignment to ASSIGNMENT_NONE
        """
        for node in self.all_nodes:
            node.set_assignment(None)

# ------------------------ reset_assignments - ends----------------------------|

# -----------------------------------------------------------------------------|
# consider_evidence
# -----------------------------------------------------------------------------|
    def consider_evidences(self, evidences):
        """
        this will assign truth value for all nodeUtil from evidence
        """
        for evidence in evidences:
            node = self.find_node(evidence[0])
            node.set_assignment(evidence[1])

# ------------------------ consider_evidence - ends----------------------------|

# -----------------------------------------------------------------------------|
# print_all_nodes
# -----------------------------------------------------------------------------|
    def print_all_nodes(self):
        """
        print all nodeUtil name with truth value assignment
        """
        print ("All nodes status:")
        for node in self.all_nodes:
            print ("nodeUtil: " + node.name + "(" + node.assignment + ")")

# ------------------------ print_all_nodes - ends------------------------------|


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

# -------------------------- normalize - ends----------------------------------|

# -----------------------------------------------------------------------------|
# get_all_evidences
# -----------------------------------------------------------------------------|
    def get_all_evidences(self):
        """
        returns list of nodes with assigned truth values
        """
        evidence_list = []
        for node in self.all_nodes:
            if node.assignment is not NodeUtil.ASSIGNMENT_NONE:
                evidence_list.append(node)
        return evidence_list
# ------------------------ get_all_evidences - ends----------------------------|

# -----------------------------------------------------------------------------|
# generate_samples
# -----------------------------------------------------------------------------|
    def generate_samples(self, required_sample_count):
        """
        this will generate @required_sample_count samples
        and return hashmap
        """
        count_dict = self.generate_dictionary(self.gen_combinations())
        for i in range(0, required_sample_count):
            self.reset_assignments()
            for node in self.all_nodes:
                node.assign_new_random_value_based_on_parent()
                #     now all variables have been assigned values so the sample is ready
            count_dict[self.current_assignment_comb()] = \
                                count_dict[self.current_assignment_comb()] + 1;

        # print count_dict
        return count_dict
# ------------------------ generate_samples - ends-----------------------------|

# -------------------------------------------------------------------------|
# current_assignment_comb
# -------------------------------------------------------------------------|
    def current_assignment_comb(self):
        """
        returns string "TFTFT" based on variables truth values
        """
        comb = ""
        for node in self.all_nodes:
            comb += node.assignment
        return comb

# ------------------------ current_assignment_comb - ends----------------------|

# -----------------------------------------------------------------------------|
# generate_dictoinary
# -----------------------------------------------------------------------------|
    def generate_dictionary(self, combinations):
        """
        creates dictionary using combinations
        """
        dictionary = dict()

        for combination in combinations:
            dictionary[combination] = 0
        return dictionary

# ------------------------ generate_dictoinary - ends--------------------------|

# -----------------------------------------------------------------------------|
# gen_combinations
# -----------------------------------------------------------------------------|
    def gen_combinations(self):
        """
        generates different values
        if total_var = 2
        then it will return TT, TF, FT, FF
        """
        total_vars = len(self.all_nodes)
        all_possible_comb = []
        total_samples = 2 ** total_vars

        for i in range(1, total_vars + 1):
            cycle = 2 ** (total_vars - i)
            for j in range(0, total_samples):
                current_mod = (j / cycle) % 2
                if current_mod is 0:
                    value_to_append = NodeUtil.ASSIGNMENT_TRUE
                else:
                    value_to_append = NodeUtil.ASSIGNMENT_FALSE

                if i is 1:
                    all_possible_comb.append(value_to_append)
                else:
                    all_possible_comb[j] = all_possible_comb[j] + value_to_append

        return all_possible_comb

# -----------------------------------------------------------------------------|
# node_pos_in_list
# -----------------------------------------------------------------------------|
    def node_pos_in_list(self, node):
        """

        """
        for i in range(0, len(self.all_nodes)):
            if self.all_nodes[i] is node:
                return i
        return -1
# ------------------------ node_pos_in_list - ends-----------------------------|
