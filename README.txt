# AlarmBayesNet
Given project implements inference algorithm on Alarm Bayes net. 

ReadMe for Bayes Programming Assignment
How to run the code:
•	Open terminal / command prompt
•	Reach to the directory where you extracted the folder
•	Go to “src/” folder
•	And run following command for each question of assignment:
1.	 Alarm is false, infer Burglary and JohnCalls being true. 
	python alarmBayesUI.py "[<A,f>]" "[B,J]"
2.	JohnCalls is true, Earthquake is false, infer Burglary and MaryCalls being true. 
	python alarmBayesUI.py "[<J,t><E,f]" "[B,M]"
3.	MaryCalls is true and JohnCalls is false, infer Burglary and Earthquake being true. 
	python alarmBayesUI.py "[<M,t><J,f]" "[B,E]"


Different number of sampling:
This program is implemented in a way that for each command it will generate different number of samples on its own. So that user does not need to enter sample count every time. Running any of above (or any other valid) command will generate and show results for different number of samples.
Sample Output: 

Input Formats:
python alarmBayesUI.py "[<J,t><E,f]" "[B,M]"  is a valid command. 
1.	Evidence argument:
a.	It is the first argument from command line.
b.	It is array of tuples. Each tuple has variable representative character and truth value for that variable. No space is expected.
c.	As this program is specifically designed for Alarm Bayes net, it will work for only A (Alarm), B (Burglary), E (Earthquake), J (John Calls), M (Mary Calls) variables as evidence, t (true) and f (false) as their valid assignment.
2.	Query argument:
a.	It is the 2nd argument from command line.
b.	It is array of query variable representative character.
c.	As this program is specifically designed for Alarm Bayes net, it will work for only A (Alarm), B (Burglary), E (Earthquake), J (John Calls), M (Mary Calls) variables as query variable.
