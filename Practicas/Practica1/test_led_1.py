import RPi.GPIO as GPIO
import time

# Configuramos la numeración en modo BCM
GPIO.setmode(GPIO.BCM)

# Configuramos los pines 17 y 25 como salidas
GPIO.setup([17, 25], GPIO.OUT)

try:
    while True:
        # Estado 1: Pin 17 encendido, Pin 25 apagado
        GPIO.output(17, GPIO.HIGH)
        GPIO.output(25, GPIO.LOW)
        time.sleep(1)
        
        # Estado 2: Pin 17 apagado, Pin 25 encendido
        GPIO.output(17, GPIO.LOW)
        GPIO.output(25, GPIO.HIGH)
        time.sleep(1)

except KeyboardInterrupt:
    # Limpiamos los pines al interrumpir el programa con Ctrl+C
    GPIO.cleanup()