from time import sleep
from romeo.easy import forward, stop

def tratto(durata):
    forward(0.5)
    sleep(durata)
    stop()

tratto(3)
