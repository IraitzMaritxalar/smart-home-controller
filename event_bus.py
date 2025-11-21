from global_state import state

subscribers = []

def subscribe(handler):
    subscribers.append(handler)

def publish(event):
    # store event in global logs
    device = event["device"]
    if device in state["logs"]:
        state["logs"][device].append(event)
        if len(state["logs"][device]) > 50:
            state["logs"][device].pop(0)

    # notify subscribers
    for s in subscribers:
        try:
            s(event)
        except:
            pass
