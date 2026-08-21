from romeo import Robot
from romeo.backends.mock import MockBackend

backend = MockBackend()
robot = Robot(backend)
robot.look(60, 120)
assert (backend.pan_angle, backend.tilt_angle) == (60.0, 120.0)
robot.close()
print("PAN TILT OK")
