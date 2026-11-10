import re

a = "The quick brown fox"
b = r"quick"

match = re.match(b, a)
if match:
    print("Match found:", match.group())
else:
    print("No match")
