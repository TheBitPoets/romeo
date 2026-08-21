from romeo.backends.mock import BackendCommand, MockBackend
from romeo.easy import close, forward, left, stop, use_backend


def test_function_api_delegates_to_configured_backend() -> None:
    backend = MockBackend()
    use_backend(backend)

    forward()
    left(0.25)
    stop()

    assert backend.history[:3] == [
        BackendCommand("set_motor_speeds", (0.5, 0.5)),
        BackendCommand("set_motor_speeds", (-0.25, 0.25)),
        BackendCommand("stop", ()),
    ]
    close()

