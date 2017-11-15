from alarmBayes import AlarmBayes


class MyIO:

# -----------------------------------------------------------------------------|
# parse_input_evidence
# -----------------------------------------------------------------------------|
    def parse_evidence_input(self, input_value):
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
        #while '>' -ends
        print(all_evidence)
        return all_evidence
# ------------------------ parse_input_evidence - ends-------------------------|

# -----------------------------------------------------------------------------|
# parse_query_input
# -----------------------------------------------------------------------------|
    def parse_query_input(self, input_value):
        """
        sample input will be string [J,M]
        this should return list of nodes representing J and M
        """
        
        return input_value.replace("[", "").replace("]", "").split(",")
# ------------------------ parse_query_input - ends----------------------------|

# -----------------------------------------------------------------------------|
# print_all_nodes
# -----------------------------------------------------------------------------|
    def print_all_nodes(self, all_nodes):
        """
        print all nodeUtil name with truth value assignment
        """
        print ("All nodes status:")
        for node in all_nodes:
            print ("nodeUtil: " + node.name + "(" + node.assignment + ")")
        #for node -ends

# ------------------------ print_all_nodes - ends------------------------------|
#|-----------------------------------------------------------------------------|
# print_sample_output
#|-----------------------------------------------------------------------------|
    def print_sample_output(self, output_list, nSamples):
        """
        input : output_list[0] = sample_numbers
                output_list[1] = count_of_query_evidence
                output_list[2] = count_of_evidence
                output_list[3] = final_value
                output_list[4] = 1 - final_value
        """
        for i in range(nSamples):
            print ("nSamples {}: {} / {} => <{},{}>".format( \
                output_list[i][0], output_list[i][1],\
                                        output_list[i][2],output_list[i][3],\
                                        output_list[i][4]))
        #for i -ends



            # |------------------------print_sample_output -ends----------------------------------|    #|-----------------------------------------------------------------------------|
        # print_sample_rejection_output
        # |-----------------------------------------------------------------------------|

    def print_sample_rejection_output(self, result):
        """
        result: [[10,[3,4],[100,[20,30]]
        """
        for result_entry in result:
            distribution = result_entry[1]
            normal_distribution = AlarmBayes.normalize(distribution)
            print ("nSamples {}: {} / {} => <{},{}>".format(result_entry[0], distribution[0], distribution[1],
                                                            normal_distribution[0], normal_distribution[1]))


            # |------------------------print_sample_output -ends----------------------------------|

    def print_likelihood_output(self, output_list, nSamples):
        """
        input : output_list[0] = sample_numbers
                output_list[1] = weight of query
                output_list[2] = total weight
                output_list[3] = calculated weight
                output_list[4] = 1 - calculated weight
        """
        for i in range(0,nSamples):
            print ("nSamples {}: {} / {} => <{},{}>".format( \
                output_list[i][0], output_list[i][1], \
                output_list[i][2],output_list[i][3], \
                output_list[i][4]))
            #for i -ends



            # |------------------------print_sample_output -ends----------------------------------|    #|-----------------------------------------------------------------------------|
            # print_sample_rejection_output
            # |-----------------------------------------------------------------------------|