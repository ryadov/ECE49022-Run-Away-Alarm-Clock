import machine
from machine import *
import time

#setup output pins
p5 = Pin(5, Pin.OUT)
m1_fwd = machine.PWM(p5)
m1_fwd.deinit()
m1_fwd.init(freq=1000, duty=0)

p18 = Pin(18, Pin.OUT)
m1_rev = machine.PWM(p18)
m1_rev.deinit()
m1_rev.init(freq=1000, duty=0)

p19 = Pin(19, Pin.OUT)
m2_fwd = machine.PWM(p19)
m2_fwd.deinit()
m2_fwd.init(freq=1000, duty=0)

p21 = Pin(21, Pin.OUT)
m2_rev = machine.PWM(p21)
m2_rev.deinit()
m2_rev.init(freq=1000, duty=0)

d = int(50 / 100 * 1023)    # duty = 10%

while(1):
    print("Direction? ")
    direction = input()
    if direction == '0':
        m1_fwd.duty(0)
        m1_rev.duty(0)
        m2_fwd.duty(0)
        m2_rev.duty(0)
    elif direction == 'f':
        m1_fwd.duty(d)
        m1_rev.duty(0)
        m2_fwd.duty(d)
        m2_rev.duty(0)
    elif direction == 'b':
        m1_fwd.duty(0)
        m1_rev.duty(d)
        m2_fwd.duty(0)
        m2_rev.duty(d)
    elif direction == 'l':
        m1_fwd.duty(d)
        m1_rev.duty(0)
        m2_fwd.duty(0)
        m2_rev.duty(0)
    elif direction == 'r':
        m1_fwd.duty(0)
        m1_rev.duty(0)
        m2_fwd.duty(d)
        m2_rev.duty(0)
    else:
        print("ERROR: invalid direction")
        