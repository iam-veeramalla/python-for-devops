import re

text = "The quick brown fox jumps over the lazy brown dog"
pattern = r"brown"

replacement = "red"

new_text = re.sub(pattern, replacement, text)
print("Modified text:", new_text)



test = "the cow is black and calf is also black."
pattern1 = r"black"
replacement1 =  "white"
test1 = re.sub(pattern1, replacement1, test)
print("modified text:", test1)