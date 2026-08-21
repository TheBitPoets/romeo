import pytest
from main import drive_safely

class Safety:
    def __init__(self,fail=False): self.calls=[]; self.fail=fail
    def claim_controller(self,c): self.calls.append(("claim",c))
    def set_motor_speeds_for(self,c,l,r): self.calls.append(("move",c,l,r));                (_ for _ in ()).throw(RuntimeError("motor")) if self.fail else None
    def release_controller(self,c): self.calls.append(("release",c))

def test_ownership_velocita_e_release():
    safety=Safety(); drive_safely(safety,"student-7",0.34)
    assert safety.calls == [("claim","student-7"),("move","student-7",0.34,0.34),("release","student-7")]

def test_release_anche_su_errore():
    safety=Safety(True)
    with pytest.raises(RuntimeError): drive_safely(safety,"student",0.2)
    assert safety.calls[-1] == ("release","student")
