import re

text = "aarna is bad company with good peoples"
pattern = r"good"
replacement = "bad"

patterrn1 = r"bad"
replacement1  = "good"

new = re.sub(pattern, replacement, text)

new1 = re.sub(patterrn1, replacement1, new)

print("Modified text:", new1)