import RPi.GPIO as GPIO
import time

# Configuración de los pines
GPIO.setmode(GPIO.BCM)
TRIG = 17  # Pin de Trigger (basado en la v2)
ECHO = 25  # Pin de Echo (basado en la v2)
LED1 = 12
LED2 = 13
LED3 = 16

# Setup de pines de salida y entrada
GPIO.setup([TRIG, LED1, LED2, LED3], GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)

def mesura_distancia():
    # Envío del pulso de Trigger
    GPIO.output(TRIG, True)
    time.sleep(0.00001)  # Pulso de 10 microsegundos
    GPIO.output(TRIG, False)
    
    # ¡Clave de seguridad! Inicialización previa para evitar UnboundLocalError
    start_time = time.time()
    end_time = time.time()
    
    # Medida del tiempo de respuesta
    while GPIO.input(ECHO) == 0:
        start_time = time.time()
        
    while GPIO.input(ECHO) == 1:
        end_time = time.time()
        
    # Cálculo de la distancia
    temps_total = end_time - start_time
    distancia = (temps_total * 34300) / 2  # Resultado en cm
    
    return distancia

try:
    while True:
        distancia = mesura_distancia()
        print(f"Distància: {distancia:.2f} cm")
        
        # Lógica de LEDs optimizada con if/elif/else
        if 0 <= distancia <= 20:
            GPIO.output(LED1, 1)
            GPIO.output(LED2, 0)
            GPIO.output(LED3, 0)
        elif 20 < distancia <= 50:
            GPIO.output(LED1, 0)
            GPIO.output(LED2, 1)
            GPIO.output(LED3, 0)
        elif 50 < distancia <= 400:
            GPIO.output(LED1, 0)
            GPIO.output(LED2, 0)
            GPIO.output(LED3, 1)
        else: 
            # Caso de error o fuera de rango (<0 o >400)
            GPIO.output(LED1, 1)
            GPIO.output(LED2, 1)
            GPIO.output(LED3, 1)
            
        time.sleep(1)
        
except KeyboardInterrupt:
    print("\nMesura aturada per l'usuari")
    GPIO.cleanup()