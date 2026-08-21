from time import sleep
from romeo.easy import forward, stop

modalita_sicura = True
if modalita_sicura:
    forward(0.3)
    sleep(10 / 3)
else:
    forward(0.5)
    sleep(2)
stop()
