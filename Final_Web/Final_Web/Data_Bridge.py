signal = False
A = 1
B = 0

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
    global A
    return A
