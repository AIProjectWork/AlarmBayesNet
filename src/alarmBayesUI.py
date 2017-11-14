from alarmBayes import AlarmBayes
import sys
from myIO import MyIO
from nodeUtil import NodeUtil
from enumerationUtil import EnumerationUtil
from __builtin__ import str

class AlarmBayesUI:
#|-----------------------------------------------------------------------------|
# alarmBayesUI
#|-----------------------------------------------------------------------------|
    def createAlarmBayes(self, inputParam, queryParam):
        """
        Given function is a UI function, which takes inputParam and queryParam
        and perform tasks 
        #TODO: complete comment details - which tasks and output if any
        """
        myIO = MyIO()
        evidences_input = myIO.parse_evidence_input(input_value = inputParam)
        query_params = myIO.parse_query_input(input_value = queryParam)

#         #debug
#         print ('evidences_input = {} '.format(evidences_input))
#         print ('query_params = {}'.format(query_params))
#         #debug -ends

        alarmBayes = AlarmBayes()
        # work on each query param turn by turn
        for query in query_params:
            # enum result
            enumerationUtil = EnumerationUtil()
            enumerationUtil.result_for_enumeration(query, evidences_input,\
                                                                     alarmBayes)
    
            # sampling
            for sample_numbers in (10, 50, 100, 200, 500, 1000, 10000, 100000):
                count_dict = alarmBayes.generate_samples(sample_numbers)
                count_of_evidence = enumerationUtil.get_count_from_dict(\
                                        alarmBayes, evidences_input, count_dict)
                count_of_query_evidence = enumerationUtil.get_count_from_dict(\
                                            alarmBayes, evidences_input\
                                            +[(query, NodeUtil.ASSIGNMENT_TRUE)],
                                            count_dict)
                if count_of_evidence is 0:
                    final_value = 0.0
                else:
                    final_value = (count_of_query_evidence / float(\
                                                            count_of_evidence))
                print ("Sampling {}: {} / {} => Distribution<{},{}>".format(\
                                                        sample_numbers,\
                                                        count_of_query_evidence,\
                                                        count_of_evidence,\
                                                        final_value,\
                                                        1 - final_value))
                #if count_of_evidence -ends
            #for sample_numbers -ends
        #for query -ends
#|------------------------alarmBayesUI -ends-----------------------------------|    








if __name__ == '__main__':
    
    if len(sys.argv)>1:
        inputParam = str(sys.argv[1])
        queryParam = str(sys.argv[2])        
    #if len(sys.argv) -ends
    
    alarmBayesUI = AlarmBayesUI()
    
    alarmBayesUI.createAlarmBayes(inputParam, queryParam)
    