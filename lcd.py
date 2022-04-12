from time import sleep_ms, ticks_ms 
from machine import SoftI2C, Pin, RTC
import machine
from machine_i2c_lcd import I2cLcd

#LCD Definitions
i2c = SoftI2C(scl = Pin(32), sda = Pin(33), freq = 400000)
DEFAULT_I2C_ADDR = 0x27


lcd = I2cLcd(i2c, DEFAULT_I2C_ADDR, 2, 16)
rtc = RTC()
lcd.clear()

#button definition
hours_button = machine.Pin(23, machine.Pin.IN, machine.Pin.PULL_DOWN)
minutes_button = machine.Pin(22, machine.Pin.IN, machine.Pin.PULL_DOWN)
seconds_button = machine.Pin(25, machine.Pin.IN, machine.Pin.PULL_DOWN)

alarm_in = machine.Pin(12, machine.Pin.IN, machine.Pin.PULL_DOWN)
time_in = machine.Pin(13, machine.Pin.IN, machine.Pin.PULL_DOWN)

hoursincrease = rtc.datetime()[4]
minutesincrease = rtc.datetime()[5]
secondsincrease = rtc.datetime()[6]

#debug loops, these will become functions to be called in the main loop for the device

#this loop will take the time and alarm input, it will most likely just exist within the main clock loop as a function
#to update the clock dynamically using conditionals as opposed to this debug state


while True:

    if time_in.value() == 1:
        
        if hoursincrease < 24:
            hoursincrease = hoursincrease + hours_button.value()
            
        if hoursincrease == 24:
            hoursincrease = 0
           
        if minutesincrease < 60:
            minutesincrease = minutesincrease + minutes_button.value()
            
        if minutesincrease == 60:
            minutesincrease = 0
            hoursincrease = hoursincrease + 1
        if secondsincrease < 60:
            secondsincrease = secondsincrease + seconds_button.value()
            
        if secondsincrease == 60:
           secondsincrease = 0
           minutesincrease = minutesincrease + 1
        
        newtime = (hoursincrease, minutesincrease, secondsincrease)
        rtc.datetime((2022, 2, 8, 2, newtime[0], newtime[1],newtime[2],0))
   
    lcd.clear()
    Year = str(rtc.datetime()[0])
    Month = str(rtc.datetime()[1])
    Day = str(rtc.datetime()[2])
    hours = str(rtc.datetime()[4])
    minutes = str(rtc.datetime()[5])
    seconds = str(rtc.datetime()[6])
                              
    if len(minutes) < 2:
        minutes = "0"+ minutes
    if len(hours) < 2:
        hours = "0"+ hours
    if len(seconds) < 2:
         seconds = "0"+ seconds
    Date = "Date: " + Month + " " + Day + " " + Year
    time = "Time: " + hours + ":" + minutes + ":" + seconds
    lcd.putstr(time + "  " + Date)
    sleep_ms(1000)
    


#    need to determine a good button input time that feels natural and will exist within the tick of the main clock, probably <1s to catch the clock before it ticks a second
    

# while True:
#     #these need to become functions to be called by the main loop in the boot file
#     
#     lcd.clear()
#     Year = str(rtc.datetime()[0])
#     Month = str(rtc.datetime()[1])
#     Day = str(rtc.datetime()[2])
#     hours = str(rtc.datetime()[4])
#     minutes = str(rtc.datetime()[5])
#     hours = str(rtc.datetime()[4])
#     seconds = str(rtc.datetime()[6])
#                               
#     if len(minutes) < 2:
#         minutes = "0"+ minutes
#     if len(hours) < 2:
#         hours = "0"+ hours
#     if len(seconds) < 2:
#          seconds = "0"+ seconds
#     Date = "Date: " + Month + " " + Day + " " + Year
#     time = "Time: " + hours + ":" + minutes + ":" + seconds
#     lcd.putstr(time + "  " + Date)
#     sleep_ms(1000)
#     
