from main import point_camera

class Robot:
    def __init__(self): self.calls=[]
    def look(self, pan, tilt): self.calls.append((pan,tilt))

def test_inoltra_angoli_diversi():
    robot=Robot(); point_camera(robot, 31, 149); point_camera(robot, 90, 45)
    assert robot.calls == [(31,149),(90,45)]
