def point_camera(robot, pan, tilt):
    """Orienta la camera attraverso la API Robot."""
    robot.look(pan, tilt)
