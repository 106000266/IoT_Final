signal = False

def control():
    global signal
    signal = not signal
    print(signal)

def get_signal():
    global signal
    return signal
