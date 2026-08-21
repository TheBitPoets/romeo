def dispatch_events(events, handler):
    """Consegna ogni evento al callback nello stesso ordine."""
    for event in events:
        handler(event)
