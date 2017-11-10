
class MyIO:

# -----------------------------------------------------------------------------|
# parse_input_evidence
# -----------------------------------------------------------------------------|
    @staticmethod
    def parse_evidence_input(input_value):
        """
        input is received as [<A,t><B,f>] string. need to convert it into list 
        of tuples
        """
        all_evidence = []
        input_value = input_value.replace("[", "")
        input_value = input_value.replace("]", "")
        while '>' in input_value:
            start_pos = input_value.index("<")
            end_pos = input_value.index(">")
            single_entry = input_value[start_pos:end_pos + 1]
            input_value = input_value[end_pos + 1:]
            single_tuple = single_entry[1:single_entry.index(",")],\
                                    single_entry[single_entry.index(",") + 1:-1]
            # print(single_tuple[0] + " truthValue: " + single_tuple[1])
            all_evidence.append(single_tuple)
        print(all_evidence)
        return all_evidence
# ------------------------ parse_input_evidence - ends-------------------------|

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
# ------------------------ parse_query_input - ends----------------------------|