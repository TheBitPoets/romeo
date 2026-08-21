"""Primo programma Romeo: avanza lentamente, poi fermati."""

from time import sleep

from romeo.easy import forward, stop


def main() -> None:
    forward(0.3)
    sleep(1)
    stop()


if __name__ == "__main__":
    main()
