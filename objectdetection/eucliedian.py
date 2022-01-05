a = int(input("a:"))
b = int(input("b:"))
r = 1
while r != 0:
    r = a%b
    a = b
    b = r
print(a)
