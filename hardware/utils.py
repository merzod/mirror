def check(val, min, max):
    if val < min:
        val = min
    if val > max:
        val = max
    return val
