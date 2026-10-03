a=int(input('Введите время:'))
b=(a//60)//60
c=(a//60)%60
d=(a%60)%60
print(str(b)+'ч '+ str(c)+'м '+ str(d)+'с ')
