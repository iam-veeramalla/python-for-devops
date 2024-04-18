import sys

def add(a, b):
    add=a+b
    return add

def sub(a, b):
    subtraction=a-b
    return subtraction

def mul(a,b):
    mul=a*b
    return mul

#print(addition(5,10))
#print(subtraction(10,5))
#print(mul(20,10))

#a=int(sys.argv[1])
a=float(sys.argv[1])
operation=sys.argv[2]

#b=int(sys.argv[3])
b=float(sys.argv[3])

if operation == "add":
    output = add(a,b)
    print(output)

if operation == "sub":
    output = sub(a,b)
    print(output)

if operation == "mul":
    output = mul(a,b)
    print(output)
#python calculator_cla.py 2.5 add 5.5
#python calculator_cla.py 2.5 mul 5.5
#python calculator_cla.py 8.8 sub 2.8
