def drive_safely(safety, controller_id, speed):
    """Acquisisce il controllo, muove e rilascia sempre la lease."""
    safety.claim_controller(controller_id)
    try:
        safety.set_motor_speeds_for(controller_id, speed, speed)
    finally:
        safety.release_controller(controller_id)
