#To work with environment variables import OS module in to the python program
#	Export the sensitive information
#export password=”srilakshme”-->execute them int the command line
#export apitoken=”abcdefghij”-->execute them in the command line

Import os
Print(os.getenv(“password”))
Print(os.getenv(“apitoken”))
#Python Env_Var.py
