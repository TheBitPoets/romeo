from collections import deque

events = deque([{"type": "key", "value": "w"}, {"type": "key", "value": "space"}])
handled = []
while events:
    handled.append(events.popleft()["value"])
assert handled == ["w", "space"]
print("EVENTI OK")
