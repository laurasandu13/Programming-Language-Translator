count = 0
max = 10
message = "Hello from Java"
initial = 'A'
price = 19.99
pi = 3.14159
isActive = True
isDone = False
print("Starting translation test")
print(message)
print(count)
if count < max:
    print("Count is less than max")
if isActive:
    print("System is active")
else:
    print("System is inactive")
score = 85
if score >= 90:
    print("Grade A")
elif score >= 80:
    print("Grade B")
elif score >= 70:
    print("Grade C")
else:
    print("Grade F")
age = 25
hasLicense = True
if (age >= 18) and (hasLicense):
    print("Can drive")
isWeekend = False
isHoliday = True
if (isWeekend) or (isHoliday):
    print("Day off")
temperature = 75
isSunny = True
if ((temperature > 70) and (temperature < 85)) and (isSunny):
    print("Perfect weather")
i = 0
while i < 5:
    print(i)
    i += 1
x = 0
y = 10
while (x < 5) and (y > 5):
    x += 1
    y -= 1
for j in range(0, 5):
    print(j)
for k in range(10, 0, -1):
    print(k)
for m in range(1, 6):
    print(m)
for counter in range(0, 3):
    print("Loop iteration")
for n in range(0, 10):
    if n == 5:
        print("Halfway")
value = 5
value += 1
print(value)
value -= 1
print(value)
num = 42
if num > 0:
    if num < 100:
        print("Number in range")
flag = True
if flag:
    print("Flag is true")
a = 10
b = 20
if a == b:
    print("Equal")
if a != b:
    print("Not equal")
if a < b:
    print("Less than")
if a > b:
    print("Greater than")
if a <= b:
    print("Less or equal")
if a >= b:
    print("Greater or equal")
print("Translation test complete")
