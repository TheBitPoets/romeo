from time import sleep

from romeo.easy import forward, left, stop

for _ in range(4):
    forward(0.3)
    sleep(1)
    left(0.3)
    sleep(0.5)

stop()
