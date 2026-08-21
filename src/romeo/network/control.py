"""Transport-independent execution of validated Romeo commands."""

from romeo.network.protocol import Command
from romeo.safety import SafetyBackend


def execute_command(backend: SafetyBackend, controller_id: str, command: Command) -> None:
    """Apply a validated text or WebSocket command through a controller lease."""

    if command.name == "PING":
        backend.heartbeat(controller_id)
        return
    if command.name == "LOOK":
        pan, tilt = command.arguments
        backend.set_camera_angles_for(controller_id, pan, tilt)
        return
    if command.name == "STOP":
        backend.set_motor_speeds_for(controller_id, 0.0, 0.0)
        return
    speed = command.arguments[0]
    wheel_speeds = {
        "FORWARD": (speed, speed),
        "BACKWARD": (-speed, -speed),
        "LEFT": (-speed, speed),
        "RIGHT": (speed, -speed),
    }
    left, right = wheel_speeds[command.name]
    backend.set_motor_speeds_for(controller_id, left, right)

