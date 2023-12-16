# Loop Control Statements (break and continue)

## Introduction

Loop control statements are used to modify the behavior of loops, providing greater control and flexibility during iteration. In Python, two primary loop control statements are "break" and "continue."

## `break` Statement

The "break" statement is used to exit the loop prematurely. It can be applied to both "for" and "while" loops, allowing you to terminate the loop when a particular condition is met.

**Example:**

```python
numbers = [1, 2, 3, 4, 5]
for number in numbers:
    if number == 3:
        break
    print(number)
```

**Output:**

```
1
2
```

In this example, the loop stops when it encounters the number 3.

## `continue` Statement

The "continue" statement is used to skip the current iteration of the loop and proceed to the next one. It can be used in both "for" and "while" loops, enabling you to bypass certain iterations based on a condition.

**Example:**

```python
numbers = [1, 2, 3, 4, 5]
for number in numbers:
    if number == 3:
        continue
    print(number)
```

**Output:**

```
1
2
4
5
```

In this example, the loop skips the iteration where the number is 3 and continues with the next iteration.

## Practice Exercise - Automating Log File Analysis

#### Introduction

In this practice exercise, we use a "for" loop to automate the analysis of a log file and identify lines containing the word "error." This demonstrates how loops can be used to process data and extract relevant information efficiently.

**Example:**

```python
log_file = [
   "INFO: Operation successful",
   "ERROR: File not found",
   "DEBUG: Connection established",
   "ERROR: Database connection failed",
]

for line in log_file:
   if "ERROR" in line:
       print(line)
```

**Output:**

```
ERROR: File not found
ERROR: Database connection failed
```

In this exercise, the loop iterates through the "log_file" list and prints lines containing the word "ERROR."