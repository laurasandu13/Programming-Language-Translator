print("=== JAVA-TO-PYTHON TRANSLATOR DEMO ===")
print("\n=== SECTION 1: VARIABLES ===")
count = 10
pi = 3.14159
temperature = 98.6
message = "Hello World"
grade = 'A'
isActive = True
print("Integer: ", count)
print("Double: ", pi)
print("Float: ", temperature)
print("String: ", message)
print("Char: ", grade)
print("Boolean: ", isActive)
print("\n=== SECTION 2: IF-ELSE STATEMENTS ===")
age = 25
print("Age: ", age)
if age >= 18:
    print("You are an adult")
if age >= 21:
    print("Can drink in US")
else:
    print("Cannot drink in US")
score = 85
print("Score: ", score)
if score >= 90:
    print("Grade: A")
elif score >= 80:
    print("Grade: B")
elif score >= 70:
    print("Grade: C")
else:
    print("Grade: F")
hasLicense = True
if (age >= 16) and (hasLicense):
    print("Can drive!")
isWeekend = True
isHoliday = False
if (isWeekend) or (isHoliday):
    print("Day off!")
temp = 75
isSunny = True
if (temp > 70) and ((temp < 85) and (isSunny)):
    print("Perfect weather!")
print("\n=== SECTION 3: SWITCH STATEMENTS ===")
day = 3
print("Day number: ", day)
if day == 1:
    print("Monday")
elif day == 2:
    print("Tuesday")
elif day == 3:
    print("Wednesday")
elif day == 4:
    print("Thursday")
elif day == 5:
    print("Friday")
else:
    print("Weekend")
month = 7
print("Month number: ", month)
if month == 12 or month == 1 or month == 2:
    print("Winter")
elif month == 3 or month == 4 or month == 5:
    print("Spring")
elif month == 6 or month == 7 or month == 8:
    print("Summer")
elif month == 9 or month == 10 or month == 11:
    print("Fall")
operation = '+'
num1 = 15
num2 = 5
print("Calculator test:")
if operation == '+':
    addResult = num1 + num2
    print("Addition result: ", addResult)
elif operation == '-':
    subResult = num1 - num2
    print("Subtraction result: ", subResult)
elif operation == '*':
    mulResult = num1 * num2
    print("Multiplication result: ", mulResult)
elif operation == '/':
    divResult = num1 / num2
    print("Division result: ", divResult)
print("\n=== SECTION 4: WHILE LOOPS ===")
i = 1
while i <= 5:
    print("Count: ", i)
    i += 1
x = 0
y = 10
while (x < 3) and (y > 5):
    print("x=", x, " y=", y)
    x += 1
    y -= 1
print("\n=== SECTION 5: FOR LOOPS ===")
for j in range(0, 5):
    print("Iteration: ", j)
for k in range(5, 0, -1):
    print("Countdown: ", k)
for m in range(1, 4):
    print("Step ", m, " of 3")
for n in range(0, 10):
    if n == 5:
        print("Halfway at ", n)
print("\n=== SECTION 6: INCREMENT/DECREMENT ===")
value = 10
print("Initial: ", value)
value += 1
print("After increment: ", value)
value -= 1
print("After decrement: ", value)
print("\n=== SECTION 7: COMPARISON OPERATORS ===")
a = 10
b = 20
print("a=", a, " b=", b)
if a == b:
    print("a equals b")
if a != b:
    print("a not equal b")
if a < b:
    print("a less than b")
if a <= b:
    print("a less or equal b")
if a > b:
    print("a greater than b")
if a >= b:
    print("a greater or equal b")
print("\n=== DEMO COMPLETE ===")
