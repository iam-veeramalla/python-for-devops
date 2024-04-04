import re

text = " brown The quick brown fox"
pattern = r"brown"
replacement = "red"
pattern1 = " , "

search = re.search(pattern, text)
if search:
    print("Pattern found:", search.group())
else:
    print("Pattern not found")

new = re.sub(pattern, replacement, text)
print("modified text:", new)

new1 = re.split(pattern1, new)
print("split result:", new1)