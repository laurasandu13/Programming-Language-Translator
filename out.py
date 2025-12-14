count = 0
message = "Hello"
letter = 'A'
price = 9.99
pi = 3.14
isActive = True
score = 85
if score >= 90:
    print("A")
elif score >= 80:
    print("B")
elif score >= 70:
    print("C")
else:
    print("F")
i = 0
while i < 3:
    print(i)
    i += 1
j = 5
while j > 2:
    print(j)
    j -= 1
for i in range(0, 4):
    print(i)
for i in range(1, 4):
    print(i)
for i in range(5, 2, -1):
    print(i)
for i in range(4, 0, -1):
    print(i)
outer = 0
while outer < 2:
    inner = 0
    for inner in range(0, 2):
        if outer == inner:
            print("Equal")
        else:
            print("Different")
    outer += 1
x = 5
y = 10
if (x < 10 and y > 5):
    print("Both true")
if (x > 10 or y > 5):
    print("At least one true")
num = 0
while num < 5:
    if num < 2:
        print("Small")
    else:
        if num == 3:
            print("Three")
        else:
            print("Other")
    num += 1
flag = False
if flag:
    print("True branch")
else:
    print("False branch")
