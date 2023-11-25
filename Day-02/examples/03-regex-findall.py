import re

text = "The quick brown fox"
pattern = r"The"

search = re.search(pattern, text)
if search:
    print("Pattern found:", search.group())
else:
    print("Pattern not found")
