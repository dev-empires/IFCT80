import RPi.GPIO as GPIO
import time
import threading
import board
import adafruit_dht

# --------------------------------------------------
# Configuración de pines
# --------------------------------------------------
TRIG = 17
ECHO = 25
RS = 4
E = 18
D4 = 27
D5 = 22
D6 = 23
D7 = 24
PAUSA = 0.02

# Configuración del sensor DHT11 con la librería moderna
dht_sensor = adafruit_dht.DHT11(board.D26)

# Variables compartidas por los hilos
distancia = 0
temperatura = 0.0
humedad = 0.0
aturar = threading.Event()

# --------------------------------------------------
# Funciones de control de la pantalla LCD
# --------------------------------------------------
def alfabet(caracter):
    b_repr = ' '.join(bin(ord(char))[2:].zfill(8) for char in caracter)
    st1 = b_repr[0:4]
    rst1 = st1[::-1]
    st2 = b_repr[4:8]
    rst2 = st2[::-1]
    mylist = rst1 + rst2
    mylistint = tuple(int(num) for num in mylist)
    return mylistint

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup([TRIG,RS,E,D4,D5,D6,D7], GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)
GPIO.output([RS,E,D4,D5,D6,D7], 0)

def modecomandament(valor):
    if valor == False:
         GPIO.output(RS, 1)  
    else:
         GPIO.output(RS,0)
    GPIO.output(E, 0)  
 
def escriu_a_fila_u():
     modecomandament(True)  
     escriu4bits(0,0,0,0)   
     escriu4bits(0,0,0,0)
  
def escriu_a_fila_dos():
     modecomandament(True) 
     escriu4bits(0,0,1,1)  
     escriu4bits(0,0,0,0)
              
def escriu4bits(b1,b2,b3,b4):
     GPIO.output(D4, b1)
     GPIO.output(D5, b2)
     GPIO.output(D6, b3)
     GPIO.output(D7, b4)  
     time.sleep(PAUSA)
     GPIO.output(E, 1) 
     GPIO.output(E, 0)       
     time.sleep(PAUSA)
     
def esborra_la_pantalla():
    modecomandament(True)
    time.sleep(PAUSA)
    escriu4bits(0,0,0,0) 
    escriu4bits(1,0,0,0) 
 
def envia_dades_al_display(dada):
    modecomandament(False) 
    escriu4bits(dada[0], dada[1], dada[2], dada[3]) 
    escriu4bits(dada[4], dada[5], dada[6], dada[7]) 
   
def inicia_pantalla():
   modecomandament(True) 
   for index in range(3):
        escriu4bits(1,1,0,0)
   for index in range(2):
        escriu4bits(0,1,0,0)
   escriu4bits(1,0,1,1)   
   escriu4bits(0,0,0,0)
   escriu4bits(1,1,1,1)
   esborra_la_pantalla()

# --------------------------------------------------
# Funciones de los sensores (Hilos)
# --------------------------------------------------
def echo_timeout(estat):
    inici = time.time()
    while GPIO.input(ECHO) == estat:
        if time.time() - inici > 0.03:
            return True
    return False

def mesura_distancia():
    global distancia
    while not aturar.is_set():
        GPIO.output(TRIG, True)
        time.sleep(0.00001)
        GPIO.output(TRIG, False)
        
        if echo_timeout(0):
            distancia = -1
        else:
            start_time = time.time()
            if echo_timeout(1):
                distancia = -1
            else:
                end_time = time.time()
                temps_total = end_time - start_time
                distancia = (temps_total * 34300) / 2
        time.sleep(0.5)

def mesura_dht():
    global temperatura, humedad
    while not aturar.is_set():
        try:
            t = dht_sensor.temperature
            h = dht_sensor.humidity
            if t is not None and h is not None:
                temperatura = t
                humedad = h
        except RuntimeError as error:
            pass
        except Exception as error:
            dht_sensor.exit()
            raise error
            
        time.sleep(2.0)

# --------------------------------------------------
# Función principal de actualización del LCD y Consola
# --------------------------------------------------
def escriure_lcd():
    global distancia, temperatura, humedad
    while not aturar.is_set():
        if distancia != -1:
            texto_fila1 = f"Dist: {round(distancia,1)} cm"
        else:
            texto_fila1 = "Dist: Fora rang"
            
        texto_fila2 = f"T:{round(temperatura,1)}C H:{round(humedad,1)}%"
        
        # Rellenar con espacios hasta 16 caracteres para limpiar la línea
        texto_fila1 = texto_fila1.ljust(16)
        texto_fila2 = texto_fila2.ljust(16)

        # IMPRIMIR EN LA TERMINAL PARA COMPROBAR LOS SENSORES
        print(f"Terminal -> {texto_fila1} | {texto_fila2}")

        esborra_la_pantalla()
        
        escriu_a_fila_u()
        for char in texto_fila1:
            envia_dades_al_display(alfabet(char))
            
        escriu_a_fila_dos()
        for char in texto_fila2:
            envia_dades_al_display(alfabet(char))
            
        time.sleep(1)

# --------------------------------------------------
# Inicialización y ejecución
# --------------------------------------------------
inicia_pantalla()

fil_1 = threading.Thread(target=mesura_distancia)
fil_2 = threading.Thread(target=escriure_lcd)
fil_3 = threading.Thread(target=mesura_dht)

fil_1.start()
fil_3.start()
time.sleep(2) 
fil_2.start()

try:
    print("Programa en execució. Prem CTRL+C per aturar.")
    while True:
        time.sleep(1)

except KeyboardInterrupt:
    print("\nAturant programa...")
    aturar.set()

    fil_1.join()
    fil_2.join()
    fil_3.join()

    dht_sensor.exit()
    GPIO.cleanup()
    print("Programa finalitzat correctament.")