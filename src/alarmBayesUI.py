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
            sample_list = [10, 50, 100, 200, 500, 1000, 10000, 100000]
            sample_output, sample_rejection_output = \
                    enumerationUtil.result_for_sampling(query, evidences_input,\
                                                        alarmBayes, sample_list)
            
            nSamples = len(sample_list)
            print ("\n------------------- sampling ---------------------------")
            myIO.print_sample_output(sample_output, nSamples)
            
            print("\n------------------ sample - rejection -------------------")
            myIO.print_sample_output(sample_rejection_output, nSamples)
        #for query -ends
#|------------------------alarmBayesUI -ends-----------------------------------|    








if __name__ == '__main__':
    
    if len(sys.argv)>1:
        inputParam = str(sys.argv[1])
        queryParam = str(sys.argv[2])        
    #if len(sys.argv) -ends
    
    alarmBayesUI = AlarmBayesUI()
    
    alarmBayesUI.createAlarmBayes(inputParam, queryParam)
    