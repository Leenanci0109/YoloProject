import math as m
a: str = input("enter string:")
x = ""
y = ""
h = len(a)
for j in range(h):
    if j % 2 != 0:
        x = x+a[j]
    else:
        y = y+a[j]
print("encoded:"+x+y)
z = x+y
k = m.ceil(len(z)/2)
a = z[0:k]
b = z[k:len(z)]
ans = ''
for j in range(k):

        ans += b[j]
        ans += a[j]
print("decoded:"+ans)


