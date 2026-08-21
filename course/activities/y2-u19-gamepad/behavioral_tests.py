import pytest
from main import stick_to_wheels

@pytest.mark.parametrize("x,y,expected", [(0,-1,(0.6,0.6)),(0,1,(-0.6,-0.6)),(0.02,0.02,(0,0))])
def test_direzioni_dead_zone_e_limiti(x,y,expected):
    assert stick_to_wheels(x,y) == pytest.approx(expected)

def test_max_speed_non_hardcoded():
    assert stick_to_wheels(0,-1,0.35) == pytest.approx((0.35,0.35))
