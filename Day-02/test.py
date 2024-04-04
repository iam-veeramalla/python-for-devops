arn = "arn:aws:iam::123456789012:user/Development/product_1234/"
name = "pramod"
sur = "MUKTAWAR"

print(arn.split("/")[3])
print(arn.split(":"))


print(name.upper())
print(sur.lower())

num1 = 2.05555
num2 = 3.55558

result = num1 + num2 
print("addition:", result)

result1 = round(result, 2)
print("round of:", result1)
