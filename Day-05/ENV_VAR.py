#first you need to export the sensitive information
#export password= "srilakshmi"
#export apitoken= "abcdefghijk"
#In the script import the OS module

import os

print (os.env.password)
print (os.env.apitoken)
