import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO
import time

GPIO.setwarnings(False) # ça permet de libirer channel si elle est déja ocuppée

GPIO.setmode(GPIO.BCM) # Mode de GPIO
GPIO.setup(12, GPIO.OUT) 
servo = GPIO.PWM(12,45)
 

def on_connect(client, userdata, flags, rc):
    client.subscribe("test_channel")

def on_message(client, userdata, msg):
    print(msg.payload)
    
    if float(msg.payload)<20.0:
        servo.start(0)
        angle = 0
        servo.ChangeDutyCycle(2+(angle/18)) 
        time.sleep(1)
        servo.ChangeDutyCycle(0) 
    elif float(msg.payload)>= 20.0 and float(msg.payload)<40.0:
        servo.start(0)
        angle = 90
        servo.ChangeDutyCycle(2+(angle/18)) 
        time.sleep(1)
        servo.ChangeDutyCycle(0)
    else :
        servo.start(0)
        angle = 180
        servo.ChangeDutyCycle(2+(angle/18)) 
        time.sleep(1)
        servo.ChangeDutyCycle(0)

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect("192.168.43.37", 1883, 60)
client.loop_forever()
GPIO.cleanup()
