"""Esempio progressivo: quattro segmenti e quattro svolte."""

from time import sleep

from romeo.easy import forward, left, stop


def main() -> None:
    for _ in range(4):
        forward(0.3)
        sleep(1)
        left(0.3)
        sleep(0.5)
    stop()


if __name__ == "__main__":
    main()
