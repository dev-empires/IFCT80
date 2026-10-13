import RPi.GPIO as IO
import time
import multiprocessing

pin_led1 = 17
pin_led2 = 25

def led1_blink():
    while True:
        IO.output(pin_led1, not IO.input(pin_led1))
        time.sleep(5)

def led2_blink():
    while True:
        IO.output(pin_led2, not IO.input(pin_led2))
        time.sleep(1)

if __name__ == '__main__':
    # Configuración de los pines
    IO.setmode(IO.BCM)
    IO.setup(pin_led1, IO.OUT)
    IO.setup(pin_led2, IO.OUT)

    # Creación de los procesos independientes
    proc_1 = multiprocessing.Process(target=led1_blink)
    proc_2 = multiprocessing.Process(target=led2_blink)

    try:
        # Inicio de los procesos
        proc_1.start()
        proc_2.start()
        
        # El programa principal espera a que los procesos terminen
        proc_1.join()
        proc_2.join()
        
    except KeyboardInterrupt:
        # Finalización segura al pulsar Ctrl+C
        proc_1.terminate()
        proc_2.terminate()
        IO.cleanup()