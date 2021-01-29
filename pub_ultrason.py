import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO
import time


SERVEUR = '192.168.43.37' # IP  de notre Raspberry pi
GPIO.setwarnings(False) # ça permet de libirer channel si elle est déja ocuppée

INTERVAL= 2
next_reading = time.time()
client = mqtt.Client()
GPIO.setmode(GPIO.BCM) # Mode de GPIO

TRIG = 23 
ECHO = 24 
GPIO.setup(TRIG,GPIO.OUT) # nous définissons la broche TRIG-pin (= 23) comme une broche de sortie
GPIO.setup(ECHO,GPIO.IN)  # nous définissons la broche ECHO-pin (= 24) comme une broche d’entrée

GPIO.output(TRIG, False)  # Nous mettons la broche TRIG en position basse 

# Set access token
# client.username_pw_set(ACCESS_TOKEN)

# Connect to ThingsBoard using default MQTT port and 60 seconds keepalive interval
client.connect(SERVEUR, 1883, 60)

client.loop_start()
time.sleep(2)



try:
    while True:
        
        GPIO.output(TRIG, True)
        time.sleep(0.00001)
        GPIO.output(TRIG, False) # nous envoyons une impulsion de 10 µs avec la broche TRIG

        while GPIO.input(ECHO)==0:
            pulse_start = time.time() # ceci est une boucle qui nous permet d’enregistrer le dernier horodatage avant que le signal atteigne le récepteur.
                                
        while GPIO.input(ECHO)==1:
            pulse_end = time.time() #  nous enregistrons ici le dernier horodatage auquel le récepteur détecte le signal

        pulse_duration = pulse_end - pulse_start #nous calculons la différence de temps entre les deux horodatages
        distance = pulse_duration * 17165 # nous calculons la distance en fonction du temps calculé : 
                                          # distance = 34330 * temps / 2 , ou distance = 17165 * temps, 
                                          # tel que 34330 est la vitesse du son.
        distance = round(distance, 1) # nous arrondissons le résultat avec une précision de une décimale
        print ('Distance:',distance,'cm')
        

        # Sending humidity and temperature data to ThingsBoard
        client.publish('test_channel', distance , 1) # On envoie la distance par la voie nommée test_channel

        next_reading += INTERVAL
        sleep_time = next_reading-time.time()
        if sleep_time > 0:
            time.sleep(sleep_time)

        
except KeyboardInterrupt:
    pass

client.loop_stop() 
client.disconnect()