import sys
from __builtin__ import str

from alarmBayes import AlarmBayes
from enumerationUtil import EnumerationUtil
from myIO import MyIO
from likelihoodUtil import LikelihoodUtil


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
        print ('query_params = {}'.format(query_params))
#         #debug -ends

        alarmBayes = AlarmBayes()
        # work on each query param turn by turn
        for query in query_params:
            # result for query
           
            print ("\n###################################################")
            print ("\t RESULT FOR QUERY: {}".format(alarmBayes.find_node(\
                                                         query).name.upper()))
            print ("###################################################")

            # enum result
            enumerationUtil = EnumerationUtil()
            
            enumerationUtil.result_for_enumeration(query, evidences_input,\
                                                                     alarmBayes)
    
            # sampling
            sample_list = [10, 50, 100, 200, 500, 1000, 10000, 100000]
            sample_output = \
                    enumerationUtil.result_for_sampling(query, evidences_input,\
                                                        alarmBayes, sample_list)
            # sampling rejection
            result_with_sample_rejection = \
                enumerationUtil.result_for_sampling_rejection(query, evidences_input, \
                                                              alarmBayes, sample_list)

            nSamples = len(sample_list)
            print ("\n------------------- sampling (positive samples / total samples) ---------------------------")
            myIO.print_sample_output(sample_output, nSamples)

            print("\n------------------ sample - rejection (positive samples / total samples)-------------------")
            # myIO.print_sample_output(sample_rejection_output, nSamples)
            myIO.print_sample_rejection_output(result_with_sample_rejection)

            #finding likelihood
            likelihoodUtil = LikelihoodUtil()
            likelihood_result = enumerationUtil.result_for_likelihood_weight(query, evidences_input, alarmBayes, sample_list)
            
            print ("\n------------- likelihood (query sample weight / total weight) ----------------------------")
            myIO.print_likelihood_output(likelihood_result, nSamples)
        #for query -ends
#|------------------------alarmBayesUI -ends-----------------------------------|    








if __name__ == '__main__':
    
    if len(sys.argv)>1:
        inputParam = str(sys.argv[1])
        queryParam = str(sys.argv[2])        
    #if len(sys.argv) -ends
    
    alarmBayesUI = AlarmBayesUI()
    
    alarmBayesUI.createAlarmBayes(inputParam, queryParam)
    