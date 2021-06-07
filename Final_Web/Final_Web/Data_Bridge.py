signal = True
A = 1

def control():
    global signal
    signal = not signal
    print(signal)

def give_value(arg):
    global A
    A = arg

def get_signal():
    global signal
    return signal

def get_value():
    return A
