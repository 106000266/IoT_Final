signal = True

def control_gate():
    global signal
    signal = not signal
    print(signal)
