from romeo.backends.mock import MockBackend
from romeo.safety import SafetyBackend

backend = MockBackend()
safety = SafetyBackend(backend, background_watchdog=False)
safety.claim_controller("student-client")
safety.set_motor_speeds_for("student-client", 0.4, 0.4)
safety.release_controller("student-client")
assert (backend.left_speed, backend.right_speed) == (0.0, 0.0)
safety.close()
print("SAFETY STOP OK")
