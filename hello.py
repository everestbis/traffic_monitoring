
import RPi.GPIO as GPIO
import time
import paho.mqtt.client as mqtt
GPIO.setmode(GPIO.BCM)

topic = "george"


# led output
r1 = 18
g1 = 23
r2 = 24
g2 = 25

GPIO.setup(r1, GPIO.OUT)
GPIO.setup(r2, GPIO.OUT)
GPIO.setup(g1, GPIO.OUT)
GPIO.setup(g2, GPIO.OUT)


#Number of cars per road
Num_car_A = 4
Num_car_B = 6

def on_message(client, data, message):
    print ("we are in on message")
    a = f"Received:{message.payload.decode('UTF-8')} on topic {message.topic}"
    print(a)

def publish(state):
        msg = f"" + state
        result = client.publish(topic, msg)
        # result: [0, 1]
        status = result[0]
        if status == 0:
            print(f"Send `{msg}` to topic `{topic}`")
        else:
            print(f"Failed to send message to topic {topic}")  

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
        elif dif <= 0:
                TimeB = 30
        else: TimeB = Max_Time
        return TimeB


def switch_A():
        state = "green for A"
        TimeA = Calculate_TimeA()
        print(state)
        publish(state)
        GPIO.output(r2, GPIO.HIGH)
        GPIO.output(g1, GPIO.HIGH)
        time.sleep(TimeA)
        

def switch_B():
        state = "green for B"
        TimeB = Calculate_TimeB()
        print(state)
        publish(state)
        GPIO.output(r1, GPIO.HIGH)
        GPIO.output(g2, GPIO.HIGH)
        time.sleep(TimeB)

def traffic():
       while (Num_car_A == 0):
             GPIO.output(r1, GPIO.HIGH)
             GPIO.output(g2, GPIO.HIGH)
       while (Num_car_B == 0):
             GPIO.output(r2, GPIO.HIGH)
             GPIO.output(g1, GPIO.HIGH)
       if(Num_car_B > Num_car_A):
        print("you are here")
        switch_B()
        GPIO.output(r1, GPIO.LOW)
        GPIO.output(g2, GPIO.LOW)
        switch_A()
        GPIO.output(r2, GPIO.LOW)
        GPIO.output(g1, GPIO.LOW)
       else: 
        switch_A()
        GPIO.output(r2, GPIO.LOW)
        GPIO.output(g1, GPIO.LOW)
        switch_B()
        GPIO.output(r1, GPIO.LOW)
        GPIO.output(g2, GPIO.LOW)


if __name__ == '__main__':
        client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
        client.connect('10.12.220.101', 1883, 120)
        client.subscribe(topic, qos=0)
        client.on_message = on_message
        client.loop_start()
        try:
                while True:
                        traffic()
        finally: 
              GPIO.cleanup()
              time.sleep(60)
              client.loop_stop()
        


