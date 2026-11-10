class Calculator:
    def __init__(self, value):
        self.value = value

    def apply_operations(self, other):
        self.value += other
        self.value *= 2
        self.value ^= other
        return self.value

    def conditional_logic(self):
        return "Even" if self.value % 2 == 0 else "Odd"

    def recursive_calculate(self, n):
        if n == 0:
            return self.value
        return self.recursive_calculate(n - 1) + (self.value // n) if n % 2 == 0 else self.recursive_calculate(n - 1) - (self.value % n)

def string_manipulation(s):
    shifted = ''.join(chr(ord(char) + 2) for char in s)
    return shifted[::-1] if len(s) % 2 == 0 else shifted

a, b = 12, 5
calc = Calculator(a)
print(calc.apply_operations(b))
print(calc.conditional_logic())
print(calc.recursive_calculate(4))
print(string_manipulation("Python"))
print(string_manipulation("Complexity"))
