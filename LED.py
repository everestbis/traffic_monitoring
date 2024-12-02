import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)

# led output
r1 = 18
g1 = 23
r2 = 24
g2 = 25

GPIO.setup(r1, GPIO.OUT)
GPIO.setup(r2, GPIO.OUT)
GPIO.setup(g1, GPIO.OUT)
GPIO.setup(g2, GPIO.OUT)

#TimeL greenlight


#Number of cars per road
Num_car_A = 4
Num_car_B = 6

def Calculate_TimeA():
        Max_Time = 50
        TimeA = 30
        dif = Num_car_A - Num_car_B
        if (dif > 0) and dif < 10:
                TimeA += dif *2
        elif dif <= 0:
                TimeL = 30
        else: TimeA = Max_Time
        return TimeA

def Calculate_TimeB():
        Max_Time = 50
        TimeB = 30
        dif = Num_car_B - Num_car_A
        if (dif > 0) and dif < 10:
                TimeB += dif *2
