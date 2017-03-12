import re
from colorama import init
from colorama import Fore, Back, Style


def Sequence(message):
    """For sure the independent item is bigger than dependent"""
    ERROR = False
    item = 0
    
    c = len(message)
    for i in range(0,c,+1):
        temp = re.findall("[0-9]",message[i])
        if len(temp) is 3:
            temp[0] = temp[0]+temp[1]
            temp[1] = temp[2]
        elif len(temp) is 4:
            temp[0] = temp[0]+temp[1]
            temp[1] = temp[2]+temp[3]


        if int(item) > int(temp[0]):
            print("Traceback:")
            print("        "+message[i])
            print("SequenceError: "+"Item sequence is not correct.")
            print()
            ERROR = True

        
        if int(temp[0]) < int(temp[1]):
            
            print("Traceback:")
            print("        "+message[i])
            print("SequenceError: "+"Dependent is bigger than independent item.")
            print()
            ERROR = True

        item = temp[0]

    if ERROR is True:
        return ERROR
        
#def Syntax(line):    
    
    

