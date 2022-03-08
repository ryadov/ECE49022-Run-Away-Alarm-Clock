#Generic modules
import math as m
from time import sleep
#Ultrasonic Sensor Driver code
from hcsr04 import HCSR04
#Accelerometer driver code
from machine import I2C
from machine import SoftI2C
from machine import Pin
import mpu6050

#UDF for the mean
def mean(lis):
    return sum(lis)/len(lis)

#Ultrasonic init
sensor1 = HCSR04(trigger_pin=18, echo_pin=5, echo_timeout_us=10000)
sensor2 = HCSR04(trigger_pin=2, echo_pin=4, echo_timeout_us=10000)

#Accel init
i2c = SoftI2C(scl=Pin(22), sda=Pin(21))     #initializing the I2C method for ESP32
mpu= mpu6050.accel(i2c)
mpu.__init__(i2c, addr=0x68)

#constants init
factor = 2**14
n_samples = 50
m_samples = 100
spacing = 30
stdMax = 100
tolerance = 0.9

ms = 1/1000
Daydream = 10*ms
Nap = 50*ms
Sleep = 100*ms
Slumber = 500*ms
Hibernation = 1000*ms

L, R, F, B = 0, 1, 2, 3
counter = 0

#main loop
for i in range(1000):
    #Accel algorithm

    listX = []
    listY = []
    listZ = []
    for k in range(m_samples):
        dict1 = mpu.get_values()
        listX.append(dict1['AcX'])
        listY.append(dict1['AcY'])
        listZ.append(dict1['AcZ'])
    meanX = mean(listX)
    meanY = mean(listY)
    meanZ = mean(listZ)
    
    diffX = [x - meanX for x in listX]
    sqSumX = sum([x*x for x in diffX])
    stdX = (sqSumX/len(listX))**(1/2)
    
    diffY = [y - meanY for y in listY]
    sqSumY = sum([y*y for y in diffY])
    stdY = (sqSumY/len(listY))**(1/2)
    
    diffZ = [z - meanZ for z in listZ]
    sqSumZ = sum([z*z for z in diffZ])
    stdZ = (sqSumZ/len(listZ))**(1/2)

    
    xAxis = round((meanX/factor)**3)
    yAxis = round((meanY/factor)**3)
    zAxis = round((meanZ/factor)**3)
    if (xAxis > 0 and meanZ > 16000):
        print(f"{counter}: +X")
        sleep(Slumber)
    elif (xAxis < 0):
        print(f"{counter}:-X")
        sleep(Slumber)
    elif (yAxis < 0):
        print(f"{counter}:-Y")
        sleep(Slumber)
    elif (yAxis > 0):
        print(f"{counter}:+Y")
        sleep(Slumber)
    else:
        if (meanZ < 16000): print("tilted too much")
        else: print(f"{counter}: No motion")
    counter += 1


    
#Ultrasonic Algorithm
'''
    countBack = 0
    countRight = 0
    countLeft = 0
    countForward = 0
    
    for j in range(n_samples):
        #dList1 = [sensor1.distance_cm() for i in range(5)]
        #distance1 = mean(dList1)
        #dList2 = [sensor2.distance_cm() for i in range(5)]
        #distance2 = mean(dList2)
        distance1 = sensor1.distance_cm()
        distance2 = sensor2.distance_cm()
        if (distance1 > spacing or distance1 < 0) and (distance2 >spacing  or distance2 < 0):
            countForward   += 1
            #print('{:<2}'.format("stationary") if stdX < stdMax else '{:<2}'.format("in motion"), '{:<3}'.format("forward"))
        elif (distance1 < spacing and distance1 > 0) or (distance2 < spacing and distance2 > 0):
            if (distance1 < spacing and distance1 > 0) and (distance2 < spacing and distance2 > 0):
                countBack += 1
                #print("blocked, go backward and turn")
            elif (distance1 < spacing and distance1 > 0):
                countRight += 1
                #print("{}".format(distance1),  "turn right!")
            elif (distance2 < spacing and distance2 > 0):
                countLeft  += 1
                #print("{}".format(distance2), "turn left!")
                
    dict1 = {countLeft: 'Left', countRight: 'Right', countForward: 'Forward', countBack: 'Backward'}
    
    I = dict1.items()
    I = list(I)
    I = sorted(I)
    First = max(I)
    I.pop()
    Second = max(I)
    
    
    
    #First = I[3]
    #Second = I[2]
    #Third = I[1]
    #Fourth = I[0]
    #k = dict1.keys()
    
    if(First[1] == 'Forward'):
        print("Go Forward")
        sleep(Sleep)
    elif (First[1] == 'Backward'):
        print("STOP, Go Backward")
        sleep(Sleep)
    else: #0 for value, 1 for direction
        if (First[1] == 'Left' and Second[1] == 'Right'):
            print("STOP, Go Left")
            sleep(Sleep)
        elif (First[1] == 'Right' and Second[1] == 'Left'):
            print("STOP, Go Right")
            sleep(Sleep)
        elif (First[1] == 'Left' and Second[1] != 'Right'):
            quotient = Second[0]/First[0]
            print(f"STOP, Go {Second[1]}" if quotient > tolerance else f"STOP, Go {First[1]}")
            sleep(Sleep)
        elif (First[1] == 'Right' and Second[1] != 'Left'):
            quotient = Second[0]/First[0]
            print(f"STOP, Go {Second[1]}" if quotient > tolerance else f"STOP, Go {First[1]}")
            sleep(Sleep)
'''
