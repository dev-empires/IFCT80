import time
import RPi.GPIO as GPIO
RS = 4
E = 18
D4 = 27
D5 = 22
D6 = 23
D7 = 24
PAUSA = 0.02
ALFABET = {
               "A":(0,0,1,0, 1,0,0,0),
               "B":(0,0,1,0, 0,1,0,0 ),
               "C":(0,0,1,0, 1,1,0,0),
               "D":(0,0,1,0, 0,0,1,0),
               "E":(0,0,1,0, 1,0,1,0),
               "F":(0,0,1,0, 0,1,1,0),
               "G":(0,0,1,0, 1,1,1,0),
               "H":(0,0,1,0, 0,0,0,1),
               "I":(0,0,1,0, 1,0,0,1),
               "J":(0,0,1,0, 0,1,0,1),
               "K":(0,0,1,0, 1,1,0,1),
               "L":(0,0,1,0, 0,0,1,1),
               "M":(0,0,1,0, 1,0,1,1),
               "N":(0,0,1,0, 0,1,1,1),
               "O":(0,0,1,0, 1,1,1,1),
               "P":(1,0,1,0, 0,0,0,0),
               "Q":(1,0,1,0, 1,0,0,0),
               "R":(1,0,1,0, 0,1,0,0),
               "S":(1,0,1,0, 1,1,0,0),
               "T":(1,0,1,0, 0,0,1,0),
               "U":(1,0,1,0, 1,0,1,0),
               "V":(1,0,1,0, 0,1,1,0),
               "W":(1,0,1,0, 1,1,1,0),
               "X":(1,0,1,0, 0,0,0,1),
               "Y":(1,0,1,0, 1,0,0,1),
               "Z":(1,0,1,0, 0,1,0,1),
               " ":(0,1,0,0, 0,0,0,0),
               ".":(0,1,0,0, 0,1,1,1)
               }

FRASE = "TENGO UN DEFECTO EN LA NARIZ QUE ES MUY MOLESTO QUE ME SUCEDE IGUAL EN VIGO QUE EN MADRID NO SE POR QUE CUANDO ME PONGO MUY NERVIOSO \
ME DA UN PICOR IRRESISTIBLE EN LA NARIZ. SI EN EL COLEGIO HAY UN EXAMEN IMPORTANTE O POR LAS NOTAS ME REGANA MI PAPA ME DA ENSEGUIDA ESE PICOR TAN EXCITANTE \
QUE POR DESGRACIA SIEMPRE ME HACE ESTORNUDAR AH  AH ACHIS COMO ME PICA LA NARIZ COMO ME PICA LA NARIZ YA NO LO PUEDO RESISTIR COMO ME PICA LA NARIZ"

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

def peripheral_loop() :
    comptador = 0
    for index in range(len(FRASE)):
        if index % 16 == 0:
             if comptador % 2 == 0:
                esborra_la_pantalla()
                escriu_a_fila_u()
             else:
                escriu_a_fila_dos()
             comptador  += 1
        envia_dades_al_display(ALFABET[FRASE[index]])
    esborra_la_pantalla()
    
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

def peripheral_setup () :
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup([RS,E,D4,D5,D6,D7],GPIO.OUT)
    GPIO.output([RS,E,D4,D5,D6,D7], 0)

def main () :
    peripheral_setup()
    inicia_pantalla()

    while 1 :
        try:
            peripheral_loop()
        except KeyboardInterrupt:
            esborra_la_pantalla()
            detencio_pantalla()
            break

if __name__ == '__main__' :
    main()