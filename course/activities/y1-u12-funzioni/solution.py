from time import sleep
from romeo.easy import forward, stop

def avanza_per(secondi):
    forward(0.5)
    sleep(secondi)
    stop()

avanza_per(2)
