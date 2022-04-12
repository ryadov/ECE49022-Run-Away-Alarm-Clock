from time import sleep_ms, ticks_ms 
from machine import SoftI2C, Pin, RTC,DAC
import machine
from machine_i2c_lcd import I2cLcd
import math

'''init''' 
#global variables
DEFAULT_I2C_ADDR = 0x27
#object calls
i2c = SoftI2C(scl = Pin(27), sda = Pin(14), freq = 400000)
lcd = I2cLcd(i2c, DEFAULT_I2C_ADDR, 2, 16)
rtc = RTC()
lcd.clear()
dac= machine.DAC(Pin(25))
hours_button = machine.Pin(15, machine.Pin.IN, machine.Pin.PULL_DOWN)
minutes_button = machine.Pin(2, machine.Pin.IN, machine.Pin.PULL_DOWN)
alarm_in = machine.Pin(4, machine.Pin.IN, machine.Pin.PULL_DOWN)
time_in = machine.Pin(16, machine.Pin.IN, machine.Pin.PULL_DOWN)
switch = machine.Pin(17,machine.Pin.IN, machine.Pin.PULL_DOWN)
alarmTime = (0, 0)

'''UDFs''' 
#changing clock current time value with external inputs
def ClockInput():
    while time_in.value() == 1:
        hoursincrease = rtc.datetime()[4]
        minutesincrease = rtc.datetime()[5]
        if hoursincrease < 24:
            hoursincrease = hoursincrease + hours_button.value()
        if hoursincrease == 24:
            hoursincrease = 0    
        if minutesincrease < 60:
            minutesincrease = minutesincrease + minutes_button.value()       
        if minutesincrease == 60:
            minutesincrease = 0
            
        newtime = (hoursincrease, minutesincrease)
#MAKING LCD PRETTY
        hoursstr = str(hoursincrease)
        minsstr = str(minutesincrease)
        
        if len(hoursstr) < 2:
            hoursstr = "0" + hoursstr
        if len(minsstr) < 2:
            minsstr = "0" + minsstr         
#LCD CODE
        lcd.clear()
        lcd.putstr("Time: " + hoursstr + ":" + minsstr)
        sleep_ms(250)
        rtc.datetime((2022, 2, 8, 2, newtime[0], newtime[1],0,0))
''''''   
#Changing alarm time value with external inputs
def AlarmInput(alarm):
    hoursincrease = alarm[0]
    minutesincrease = alarm[1]
    while alarm_in.value() == 1:
        
        if hoursincrease < 24:
            hoursincrease = hoursincrease + hours_button.value()
                
        if hoursincrease == 24:
            hoursincrease = 0
               
        if minutesincrease < 60:
            minutesincrease = minutesincrease + minutes_button.value()
                
        if minutesincrease == 60:
            minutesincrease = 0
        
        alarm = (hoursincrease, minutesincrease)
        
        hoursstr = str(hoursincrease)
        minsstr = str(minutesincrease)
        
        if len(hoursstr) < 2:
            hoursstr = "0" + hoursstr
        if len(minsstr) < 2:
            minsstr = "0" + minsstr
        lcd.clear()
        lcd.putstr("Alarm: " + str(hoursstr) + ":" + str(minsstr))
        sleep_ms(250)
    return alarm

#this does alarm sound stuff
def alarm(trigger):
    if trigger == True:
        intarray = []
        def sawtooth_sample(amplitude, freq, samplerate, i): #https://stackoverflow.com/questions/65543325/generating-sawtooth-wave-with-python-math-module
            value = math.atan(math.tan(2.0 * math.pi * float(freq) * (float(i) / float(samplerate))))  
            return amplitude * value
        
#this loop creates the sound array. there is a few seconds of delay when the alarm function is called, this is what that delay comes from.
        for i in range(4000):
            intval = math.floor(sawtooth_sample(127, 7000, 60000, i)) + 128
            
            if intval > 255:
                intval = 255
            if intval <0:
                intval = 0
            intarray.append(intval)
            
                
#this is the loop where we are concerned
#runs for 120 seconds real time on ESP32, makes the noises. Can be modified for interrupt purposes, this is going to be our main concern
        for y in range (0,42):
            if switch.value() == 0:
                for x in range(0,30):
                    for j in intarray:
                        dac.write(intarray[j])
                    sleep_ms(20)
                sleep_ms(1000)
            else:
                break

#this is checking alarm time against current time and if the alarm switch is on or off   
def isWakeup(currenttime, alarmtime):
    if currenttime == alarmtime and switch.value()== 0:
        return True
    else:
        return False

'''Main Loop'''
while True:
#check if the alarm should be triggered
    print(alarmTime)
    alarmon = isWakeup((rtc.datetime()[4], rtc.datetime()[5]), alarmTime)
    print(alarmon)
    alarm(alarmon)
    alarmTime= AlarmInput(alarmTime)
    ClockInput()
    lcd.clear()
    

#making the output Pretty
    hours = str(rtc.datetime()[4])
    minutes = str(rtc.datetime()[5])
    
                              
    if len(minutes) < 2:
        minutes = "0"+ minutes
    if len(hours) < 2:
        hours = "0"+ hours
    
    time = "Time: " + hours + ":" + minutes 
    lcd.putstr(time)
    sleep_ms(1000)


