import calculator_new as basic_cal # as works as alis and we are giving alis name to calculator_new as basic_cal

#calculator_new  is already devloped program so we are calling it i here as module to call module in here keyword is import
#module is nothing but group of functions

num = 4 
num = 2

basic_cal.adition()

#now we are importing module from different location here it how to do

import sys
sys.path.append('/workspaces/python-for-devops/Day-03/')  #this is path to module to call in this script
import float as floatc #creating alias name
#while giving path to module just give file  name dont provide extension 

floatc

from calculator_new import abbstraction #this is used fro calling only specific funtion from module 

abbstraction()