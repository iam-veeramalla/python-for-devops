import re

text = "The quick brown fox"
pattern = r"brown"

search = re.search(pattern, text)
if search:
    print("Pattern found:", search.group())
else:
    print("Pattern not found")

test = "hi i am pramod muktawar"
pattern1 = r"pramod"

search1 = re.search(pattern1, test)
if search1:
    print("pattern found:", search1.group())
else: 
    print("pattern not found") 
