from romeo.gamepad import GamepadMapping, wheel_speeds

left, right = wheel_speeds(0.0, -1.0, GamepadMapping(max_speed=0.6))
assert left == 0.6 and right == 0.6
assert wheel_speeds(0.02, 0.02) == (0.0, 0.0)
print("GAMEPAD OK")
