from time import sleep_ms, ticks_ms 
from machine import SoftI2C, Pin, RTC,DAC
import machine
from machine_i2c_lcd import I2cLcd
import math
import motor_direction_test
import Sensors
import mpu6050
import hcsr04
import Alarm_clock_subsystem

#Main Loop
while True:
#check if the alarm should be triggered
    print(alarmTime)
    alarmon = isWakeup((rtc.datetime()[4], rtc.datetime()[5]), alarmTime)
    print(alarmon)
    alarm(alarmon)
    alarmTime= AlarmInput(alarmTime)
    ClockInput()
    lcd.clear()


'''
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
'''