import RPi.GPIO as IO
import time

pin_led1 = 17
pin_led2 = 25
interval_led1 = 5
interval_led2 = 1

IO.setmode(IO.BCM)
IO.setup(pin_led1, IO.OUT)
IO.setup(pin_led2, IO.OUT)

last_time_led1 = time.time()
last_time_led2 = time.time()

try:
    while True:
        current_time = time.time()
        
        if current_time - last_time_led1 >= interval_led1:
            IO.output(pin_led1, not IO.input(pin_led1))
            last_time_led1 = current_time

        if current_time - last_time_led2 >= interval_led2:
            IO.output(pin_led2, not IO.input(pin_led2))
            last_time_led2 = current_time

        time.sleep(0.01)

except KeyboardInterrupt:
    # Limpiamos los pines al interrumpir el programa con Ctrl+C
    IO.cleanup()