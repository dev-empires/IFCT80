import RPi.GPIO as GPIO
import time
import threading

TRIG = 17
ECHO = 25
RS = 4
E = 18
D4 = 27
D5 = 22
D6 = 23
D7 = 24
PAUSA = 0.02

def alfabet(caracter):
    b_repr = ' '.join(bin(ord(char))[2:].zfill(8) for char in caracter)
    #print("Binary Representation:", b_repr)
    st1 = b_repr[0:4]
    rst1 = st1[::-1]
    st2 = b_repr[4:8]
    rst2 = st2[::-1]
    mylist=rst1+rst2
    mylistint = tuple(int(num) for num in mylist)
    return mylistint

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup([TRIG,RS,E,D4,D5,D6,D7], GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)
GPIO.output([RS,E,D4,D5,D6,D7], 0)

# Variable compartida pels dos fils
distancia = 0

# Senyal compartit per indicar als fils que han de parar
aturar = threading.Event()


def modecomandament(valor):
    if valor == False:
         GPIO.output(RS, 1)  
    else:
         GPIO.output(RS,0)
    GPIO.output(E, 0)  
 
def escriu_a_fila_u():
     modecomandament(True)  # El que entrarem sera un comandament
     escriu4bits(0,0,0,0)   # Es posiciona el cursor a l'inici de la filera 1 
     escriu4bits(0,0,0,0)
  
def escriu_a_fila_dos():
     modecomandament(True) # El que entrarem sera un comandament
     escriu4bits(0,0,1,1)  # Es posiciona el cursor a l'inici de la filera 2 
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
    modecomandament(True)# El que entrarem sera un comandament
    time.sleep(PAUSA)
    escriu4bits(0,0,0,0) # Entrem el primer nibble del comandament esborrar pantalla
    escriu4bits(1,0,0,0) # Entrem el segon nibble del comandament esborrar pantalla
 
def envia_dades_al_display(dada):
    modecomandament(False) # El que entrarem sera un caracter per escriure en pantalla.
    escriu4bits(dada[0],dada[1],dada[2], dada[3]) 
    escriu4bits(dada[4],dada[5], dada[6], dada[7]) 
    #GPIO.output(RS, 0)
    #time.sleep(PAUSA)
  
def detencio_pantalla():
    modecomandament(True)# El que entrarem sera un comandament
    escriu4bits(0,0,0,0) # Entrem el Primer nibble del caracter a detencio_pantalla
    escriu4bits(0,0,1,1) # Entrem el Segon nibble del caracter a detencio_pantalla
   
def inicia_pantalla():
   modecomandament(True) # El que entrarem sera la sequencia d'inicializacio
   for index in range(3):
        escriu4bits(1,1,0,0)
   for index in range(2):
        escriu4bits(0,1,0,0)
   escriu4bits(1,0,1,1)   # Canvi a la sequencia inicialitzacio per habilitar dues fileres
   escriu4bits(0,0,0,0)
   escriu4bits(1,1,1,1)
   esborra_la_pantalla()

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

            # Esperem que ECHO passi de 1 a 0
            if echo_timeout(1):
                distancia = -1

            else:
                end_time = time.time()

                temps_total = end_time - start_time
                distancia = (temps_total * 34300) / 2

        time.sleep(1)
    
    
    
def lcd(mytext):

    esborra_la_pantalla()
    escriu_a_fila_u()
    for index in range(len(mytext)):
        caracter=alfabet(mytext[index])
        envia_dades_al_display(caracter)
    time.sleep(1)
    #esborra_la_pantalla()

  


def escriure_lcd():
    global distancia
    
    while not aturar.is_set():

        if distancia != -1:
            distancia_print = str(round(distancia,2))
            lcd(f"{distancia_print} cm")

        else:
            lcd("NA")
                
        time.sleep(0.5)


# --------------------------------------------------
# Creació dels fils
# --------------------------------------------------

inicia_pantalla()

fil_1 = threading.Thread(target=mesura_distancia)
fil_2 = threading.Thread(target=escriure_lcd)

fil_1.start()
fil_2.start()


# --------------------------------------------------
# Programa principal
# --------------------------------------------------

try:

    while True:
        time.sleep(1)

except KeyboardInterrupt:

    print("Aturant programa...")

    aturar.set()

    fil_1.join()
    fil_2.join()

    GPIO.cleanup()

    print("Programa finalitzat")
