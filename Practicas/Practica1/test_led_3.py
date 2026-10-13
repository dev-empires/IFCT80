import RPi.GPIO as IO
import time
import threading

pin_led1 = 17
pin_led2 = 25

IO.setmode(IO.BCM)
IO.setup(pin_led1, IO.OUT)
IO.setup(pin_led2, IO.OUT)

def led1_blink():
    while True:
        IO.output(pin_led1, not IO.input(pin_led1))
        time.sleep(5)

def led2_blink():
    while True:
        IO.output(pin_led2, not IO.input(pin_led2))
        time.sleep(1)

# Añadimos daemon=True para que los hilos se cierren automáticamente al salir
fil_1 = threading.Thread(target=led1_blink, daemon=True)
fil_2 = threading.Thread(target=led2_blink, daemon=True)

try:
    fil_1.start()
    fil_2.start()

    # Mantenemos el hilo principal activo pero libre para capturar el Ctrl+C
    while True:
        time.sleep(1)

except KeyboardInterrupt:
    # Limpiamos los pines de forma segura al detener el programa
    IO.cleanup()