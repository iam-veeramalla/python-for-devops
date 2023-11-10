import sys as sys                          #importing sys module for command line arguments
import os as os                            #importing os module for environment variables


def add (num1 , num2):
  num3= num1+ num2
  return num3                             #using this function we can pass two values it will return sum of 2 numbers as return


def mul (num1 , num2):                   #using this function we can pass two values it will return multiplication of 2 numbers as return
  num3= num1 * num2                      #Remember we just defined the function we didn't call this function as of now
  return num3         


num1= int(sys.argv[1])                   #reading the argument from command line interface and storing first variable in num1.
operation= (sys.argv[1])                 #reading the argument from command line interface and storing second variable in operation variable.
num2= int(sys.argv[1])                   #reading the argument from command line interface and storing third variable in num2 variable.
                                        #Eg: if calculator.py 2 add 3 entered by user
                                        # 2 will store in num1 
                                        # add will store in operation
                                        # 3 will store in num3

if operation=="add":
   print(add(num1, num2)
##this is all about sys module and command line arguments


##########################################ENVIRONMENT VARIABLES####################################################################################

#export password="abhishek"
print (os.getenv("password"))

## enviroment variables used to pass the sensitive information as a variable

                                
