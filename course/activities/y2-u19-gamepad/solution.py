from romeo.gamepad import GamepadMapping, wheel_speeds

def stick_to_wheels(x, y, max_speed=0.6):
    """Converte gli assi dello stick in velocità delle ruote."""
    return wheel_speeds(x, y, GamepadMapping(max_speed=max_speed))
