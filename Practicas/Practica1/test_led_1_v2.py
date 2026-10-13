import RPi.GPIO as GPIO
import time

# Definimos las variables para los pines y el tiempo de pausa
led1 = 17
led2 = 25
pausa = 1

# Creamos una función para simplificar el cambio de estado y el retraso
def estat(estat1, estat2, delay):
    GPIO.output(led1, estat1)
    GPIO.output(led2, estat2)
    time.sleep(delay)

# Configuramos la numeración en modo BCM
GPIO.setmode(GPIO.BCM)

# Configuramos los pines usando las variables definidas
GPIO.setup([led1, led2], GPIO.OUT)

try:
    # Bucle infinito que alterna los estados usando la función creada
    while True:
        estat(GPIO.HIGH, GPIO.LOW, pausa)
        estat(GPIO.LOW, GPIO.HIGH, pausa)

except KeyboardInterrupt:
    # Limpiamos los pines al interrumpir el programa con Ctrl+C
    GPIO.cleanup()