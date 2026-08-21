import pytest
from main import dispatch_events

def test_dispatch_fifo():
    events=[{"type":"key","value":"w"},{"type":"key","value":"space"}]
    handled=[]; dispatch_events(events, handled.append)
    assert handled == events

def test_si_ferma_se_handler_fallisce():
    handled=[]
    def handler(event):
        handled.append(event)
        if event == 2: raise RuntimeError("stop")
    with pytest.raises(RuntimeError): dispatch_events([1,2,3], handler)
    assert handled == [1,2]
