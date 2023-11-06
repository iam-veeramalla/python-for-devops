# Identity Operations in Python

## Introduction

Identity operators in Python are used to compare the memory locations of two objects to determine if they are the same object or not. The two identity operators are "is" and "is not."

## List of Identity Operators

1. **is:** Returns `True` if both operands refer to the same object.
2. **is not:** Returns `True` if both operands refer to different objects.

### Examples

#### is Operator

```python
x = [1, 2, 3]
y = x  # y now refers to the same object as x
result = x is y
# result will be True
```

#### is not Operator

```python
a = "hello"
b = "world"
result = a is not b
# result will be True
```