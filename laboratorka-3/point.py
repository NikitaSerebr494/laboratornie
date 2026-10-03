a=int(input())
b=int(input())
if (a<5 and a>0) and (b>0 and b<3):
    print('Внутри ')
elif ((a==5 or a==0) and 0<=b<=3) or ((b==0 or b==3) and 0<=a<=5):
    print('На границе')
elif (a>0 or a>5) or (b<0 or b>3):
    print('За границей')
