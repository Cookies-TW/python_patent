# coding= utf-8
import re
import jieba.posseg as pseg
import time
import math
import panding as check
import export as export
import sys 

PYTHONIOENCODING="utf-8"


#version record
""" version record--------------------------------------------------
created on 2016.04.04

author: YUN HAO
version: 13.0-beta
summary: on Ubuntu 14.04 LTS
   

    version record--------------------------------------------------"""
multi_belong_flag_1 = None 
multi_belong_flag_2 = None 
temp_store  = []

independent_item = 0
belong_item = 0
last_belong = 1
termination = False

"""-----------------------------------------------"""
function_detect = 0 #附屬順序除錯功能 0:關閉 1：開啟
"""-----------------------------------------------"""

def clear():
        global multi_belong_flag_1
        global multi_belong_flag_2
        global temp_store
        
        del temp_store[:]
        temp_store  = []
        multi_belong_flag_1 = None 
        multi_belong_flag_2 = None 
        z=0
        
def main():
    global multi_belong_flag_1
    global multi_belong_flag_2
    global temp_store
    global independent_item
    global termination
    global belong_item
    global function_detect
    
    x=0
    file_name = " "
    file =" "
    test_count = 0
    ERROR = False

    
    
    
    #=============================================================================================================
    compare_list_1 = ['或']    
    compare_list_2 = ['至']
    
    message = []
    elements = [] 
    tag = []
    output = []
    
    print("SERVER: WELCOME<br>")    
    f=open("input.txt","r")


    tStart = time.time()
    line = f.readline()


        
    while line:
        if termination is True:
            break
        else:
            #line = (line.decode("BIG5"))
            words = pseg.cut(line)
            for w in words:
                elements.append(w.flag)
            
            if line.find(".")== 1 or line.find(".")== 2 or line.find(".")== 3:    # 僅取得請求項第一行 最好加上位置0為[0-9]
                

                #================================================================================================= Type: Suit
                if elements[2]=='m' or elements[2]=='nr':
                    
                #if line.find("一種") == 3 or line.find("一種") == 4:
                
                    independent_item += 1
                    independent_number = re.search('[0-9]',line) #抓取該請求項編號
                    b = line.find(independent_number.group()) #判斷二位數請求項 ....
                    independent_number = independent_number.group()  
        
                    if (str(line[b+1])).isdigit():  # ●●●● ※修改標記 ●●●●
                        independent_number = (line[b]+line[b+1])  # 已修正為10位數 ●●●● ※修改標記 ●●●●
                        message.append(("{source: "+'"'+independent_number+'"'+", target: "+'"'+independent_number+'"'+', type: "suit"},'))
                        output.append("Claim "+independent_number +" is an independent claim.")
                    else:
                        message.append(("{source: "+'"'+independent_number+'"'+", target: "+'"'+independent_number+'"'+', type: "suit"},'))
                        output.append("Claim "+independent_number +" is an independent claim.")


                #================================================================================================= Type: Licensing processing
                else:
                    
                    belong_item +=1
                    item = re.search('[0-9]',line) #抓取該請求項編號
                    a = line.find(item.group()) #判斷二位數請求項 ....
                    item = item.group()  

                    """print("line: "+line)
                    print("line[a]: "+line[a])
                    print("line[a+1]: "+line[a+1])"""
                    if (str(line[a+1])).isdigit():  
                        item = int(line[a]+line[a+1])  
                    line = line[3:] #移除標記項數字

                    #以上處理項目 以下處理附屬項============================

                    
                    while 1:
                        belong_number = re.search('[0-9]',line) # 尋找附屬值,抓取數字(目前只能抓取一位)
                        """try:
                            
                            #print("item :"+str(item))
                        
                        except :
                            pass"""
                        #print(line)
                        #print("item2 :"+str(item))
                        try:
                            if int(item) > 9: #如果在項的地方已超過10項
                               # print("ACCESS")
                                #print(line)
                                #print(belong_number)
                
                                
                                s = line.find(belong_number.group())
                                #print("line[s+1]: "+line[s+1])
                                #print("belong_number: "+ belong_number.group())
                                #print(s)
                                if(line[s+1].isdigit()):
                                    belong_number = int(line[s]+line[s+1])
                                    #print("belong_number 147: "+str(belong_number))
                                else:
                                    belong_number = belong_number.group()
                    
                            else:
                                s = line.find(belong_number.group()) #尋找數字相對位置,存入s變數中 ◎【需檢視是否其他行也會出現附屬項】
                                belong_number = belong_number.group()
                        except AttributeError:
                            break


                        #------------------------------

                        
                        try:
                            

                            
                            if elements[(str(line.find(belong_number)-1))] is 'x' and elements[(str(line.find(belong_number)+1))] is 'x' :
                                pass
                            else:
                                break
                                
                        except :
                            pass

                        

                        #-----------------------------

                        #print("belong_number 185: "+str(belong_number))
                        if judge_dependent(belong_number,line,function_detect) is "OUT":
                            termination = True
                            break
                        if judge_dependent(belong_number,line,function_detect) is True: #當有偵測到數字；且發現文句中有出現項、第的時候
                            temp_store.append(int(belong_number))

                            try:                
                                if (line[s+2] in compare_list_1 )or (line[s+3]in compare_list_1) or (line[s+4] in compare_list_1):  	#根據s(附屬項之相對位置)往後推移尋找關鍵字,判斷是否多重附屬(或、至) ●●●● ※修改標記 ●●●●
                                   multi_belong_flag_1 = True
                                if (line[s+2] in compare_list_2 )or (line[s+3]in compare_list_2) or (line[s+4] in compare_list_2):
                                   multi_belong_flag_2 = True
                                   
                                   
                            except:
                                pass
                            
                            if int(item) > 9:   #原本值為11   
                                line = line[(s+2):]
                            else:
                                line = line[(s+1):] #刪除目標數字前所有字元 (--> 或許可改成只刪除數字就好)
                            
                            
                            #多重附屬處理=======================================================================
                            if multi_belong_flag_1 is not True and multi_belong_flag_2 is not True:
                                z = len(temp_store)
                                for i in range(0,z,1):
                                    message.append(("{source: "+'"'+str(item)+'"'+", target: "+'"'+str(temp_store[i])+'"'+', type: "licensing"},'))
                                    output.append("Claim "+str(temp_store[i])+" is a preceding claim of claim "+ str(item))
                                clear()
                        else:
                            break

                    #判斷 "或" ================================================================================ 
                    if multi_belong_flag_1 is True:
                    
                        #print("item :"+str(item))
                        record = re.findall("\s[0-9]\s|\s[0-9][0-9]\s",line)
                        z = len(record)
                        for i in range(0,z,1):
                            record = re.findall("[0-9][0-9]|[0-9]",record[i])
                        
                        #test_count +=1
                        z = len(temp_store)
                        #print(temp_store)
                        for i in range(0,z,1):
                            #print(temp_store[i-1])
                            message.append(("{source: "+'"'+str(item)+'"'+", target: "+'"'+str(temp_store[i])+'"'+', type: "licensing"},'))
                            output.append("Claim "+str(temp_store[i])+" is a preceding claim of claim "+ str(item))

                        z = len(record)
                        #print(record)
                        for i in range(0,z,1):
                            #print(temp_store[i-1])
                            message.append(("{source: "+'"'+str(item)+'"'+", target: "+'"'+str(record[i])+'"'+', type: "licensing"},'))
                            output.append("Claim "+str(record[i])+" is a preceding claim of claim "+ str(item))
                        clear()

                    #判斷 "至" ================================================================================
                    if multi_belong_flag_2 is True: #至  此處record 如使用識別所有數字的話 可能發生狀況 需要修正
                        temp_record = []
                        record = re.findall("\s[0-9]\s|\s[0-9][0-9]\s",line)
                        
                        z = len(record)
                        for i in range(0,z,1):
                            temp_record.append(int(record[i]))
                            
                        """after = 0
                         for i in range(0,z,1):
                            print("record: "+record[i])
                            after = after + int(record[i])*math.pow(10,((z-1)-i))
                        print("after: "+str(after))
                        print("temp_store: "+str(temp_store[0]))"""
                        #after = int(record[0])*10 + int(record[1])+1
                        #for i in range(int(temp_store[0]),(int(after)+1),1):
                        for i in range(temp_store[0],(int(temp_record[0])+int(1)),1):
                            message.append(("{source: "+'"'+str(item)+'"'+", target: "+'"'+str(i)+'"'+', type: "licensing"},'))
                            output.append("Claim "+str(i)+" is a preceding claim of claim "+ str(item))
                        clear()
                        #---------------------------------------------------------------->
                        #| Note:
                        #|       belong_number 已為一物件型態,無法以字元型態刪除
                        #|       尚未試過抓取游標,移動游標 指向欲刪除字元(數字)的位置,
                        #|
                        #|       seek()函數用於移動指標,後面接int參數表移動字元數
                        #---------------------------------------------------------------->
                        
            elements = [] 
            line = f.readline()
        
            
        #格式化 輸出單元========================================================================================

    f.close()
    

    #-------- document Error Check
    ERROR = check.Sequence(message)
    #--------
    

    if ERROR is None and termination is False:
        #print("Dependent items: "+independent_item+"<br>")
        #print("Independent items: "+belong_item+"<br>")
        #print("Claim items: ",(independent_item+belong_item)+"<br>")
	        
        fptr = open('result_draw.txt','w')
        c = len(message)
        print("<br>")
        for i in range(0,c,+1):
            print(output[i]+"<br>")
            fptr.writelines(message[i]+"\n")

        fptr.close()
    
    """te = open('test.txt',encoding='unicode')
    line2 = te.readline()
    while line2:
        print(line2)"""   
    tStop = time.time()

    #print(("獨立項： "+"<br>"))
    print("<br>---------------------------------------------------------"+"<br>")
    print("SERVER: Analyze complete."+"<br>")
    print("SERVER: Processing model cost " + str(tStop - tStart) + " seconds."+"<br>")

def judge_dependent(belong_number,line,function_detect):
   """This function is for judging dependent item, if so, this function will return true value """

   default_encoding = 'utf-8'

   # 附屬項判斷資料 (修改成txt 檔案方便之後 plugin 熱插拔)
   dependent_list = ["項", "如", "根據", "依據", "或"]
   if sys.getdefaultencoding() != default_encoding:
        sys.setdefaultencoding(default_encoding) 
   if int(function_detect) is int(0):
        for item in dependent_list: #測試使用，移除附屬順序判斷功能
            if belong_number != None and line.find(item) is not -1:
                return True
                break

   else:
       for item in dependent_list:
            if belong_number != None and line.find(item) is not -1:
                if error_detect(belong_number):
                    print("WRONG DETECTED: ATTACH LOGIC MISTAKE.")
                    return "OUT"
                    break
                else:
                    return True
                    break
    
def test_func(message):
    c = len(message)
    for i in range(0,c,+1):
        print(message[i])

def for_php():
    default_encoding = 'big5'
    if sys.getdefaultencoding() != default_encoding:
         sys.setdefaultencoding(default_encoding)
    global independent_item
    global belong_item
    
    
    ftpr = open('out.txt','w')
    #try:
    ftpr.writelines(("獨立項： "+str(independent_item)+" \n"))
    ftpr.writelines("附屬項： "+str(belong_item)+" \n")
    ftpr.writelines("請求項： "+str(independent_item+belong_item)+" \n")
    ftpr.close()
    #except:
        #ftpr.writelines("ERROR\n") 

if __name__ == "__main__":
    main()
    export.process()
    for_php()
    print("SERVER: Export suuccessful")
     
#---------------------------------------------------------------->
#| Note:
#|       belong_number 已為一物件型態,無法以字元型態刪除
#|       概念：抓取游標,移動游標 指向欲刪除字元(數字)的位置,
#|
#|      ◎此版本尚待修正：
#|                      1. 在107行那邊並沒有辦法解決非請求項之判斷,換言之就是所有阿拉伯數字都會被視為請求項
#|                      2. 「或、至」之判讀,例如：如請求項1至5中任一者...
#|                       
#|      ◎此版本尚需確認：
#|                      1. 需檢視是否其他行也會出現附屬項。目前只讀取每一請求項之第一行,需確認其他行是否會出現請求項之敘述
#|                      2. 第39行(line[s+1] is " ")判斷敘述是否恰當
#---------------------------------------------------------------->   

