a=0
b=0
z=-1000000
for i in range(int(input())):
 c=int(input())
if c>0:
 a+=1
 b+=c
z=max(z,c)
print(a, b, z)
