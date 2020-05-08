import pyb
from pyb import Pin
 
Pin_All1=[Pin(p,Pin.OUT_PP) for p in ['X1','X2','X3','X4']]
Pin_All2=[Pin(q,Pin.OUT_PP) for q in ['X8','X7','X6','X5']]
Pin_All3=[Pin(m,Pin.OUT_PP) for m in ['Y9','Y10','Y11','Y12']]
Pin_All4=[Pin(n,Pin.OUT_PP) for n in ['X20','X19','X18','X17']]
 
#转速(ms) 数值越大转速越慢 最小值1.8ms
speed=2
 
STEPER_ROUND=512 #转动一圈(360度)的周期
ANGLE_PER_ROUND=STEPER_ROUND/360 #转动1度的周期
print('ANGLE_PER_ROUND:',ANGLE_PER_ROUND)
 
def SteperWriteData(data):
    count=0
    for i in data:
        Pin_All1[count].value(i)
        Pin_All2[count].value(i)
        Pin_All3[count].value(i)
        Pin_All4[count].value(i)
        count+=1
def SteperFrontTurn():
    global speed
     
    SteperWriteData([1,1,0,0])
    pyb.delay(speed)
 
    SteperWriteData([0,1,1,0])
    pyb.delay(speed)
 
    SteperWriteData([0,0,1,1])
    pyb.delay(speed)
     
    SteperWriteData([1,0,0,1])   
    pyb.delay(speed)
     
def SteperBackTurn():
    global speed
     
    SteperWriteData([1,1,0,0])
    pyb.delay(speed)
     
    SteperWriteData([1,0,0,1])   
    pyb.delay(speed)
     
    SteperWriteData([0,0,1,1])
    pyb.delay(speed)
 
    SteperWriteData([0,1,1,0])
    pyb.delay(speed)
 
 
def SteperStop():
    SteperWriteData([0,0,0,0])
     
def SteperRun(angle):
    global ANGLE_PER_ROUND
     
    val=ANGLE_PER_ROUND*abs(angle)
    if(angle>0):
        for i in range(0,val):
            SteperFrontTurn()
    else:
        for i in range(0,val):
            SteperBackTurn()
    angle = 0
    SteperStop()
print('ANGLE_PER_ROUND:',ANGLE_PER_ROUND)
 
