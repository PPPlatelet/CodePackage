import math

from timer import Timer

def hsv2rgb(h: float, s: float, v: float) -> tuple[int, int, int]:
    h60 = h / 60.0
    c = s * v
    x = c * (1 - abs(h60 % 2 - 1))
    m = v - c
    if h60 < 1:
        r, g, b = c, x, 0
    elif h60 < 2:
        r, g, b = x, c, 0
    elif h60 < 3:
        r, g, b = 0, c, x
    elif h60 < 4:
        r, g, b = 0, x, c
    elif h60 < 5:
        r, g, b = x, 0, c
    else:
        r, g, b = c, 0, x
    
    return int((r + m) * 255), int((g + m) * 255), int((b + m) * 255)

def rgb2hsv(r: int, g: int, b: int) -> tuple[float, float, float]:
    r, g, b = r / 255.0, g / 255.0, b / 255.0
    cmax = max(r, g, b)
    cmin = min(r, g, b)
    delta = cmax - cmin

    if delta == 0:
        h = 0.0
    elif cmax == r:
        h = 60 * (((g - b) / delta) % 6)
    elif cmax == g:
        h = 60 * (((b - r) / delta) + 2)
    else:
        h = 60 * (((r - g) / delta) + 4)

    if h < 0:
        h += 360.0
    
    if cmax == 0:
        s = 0.0
    else:
        s = delta / cmax
    
    v = cmax

    return h, s, v

def spectral_cycle(duration = 90, interval = 0.03, start_hue = 300):
    steps = int(duration / interval)
    hue_step = 360 / steps
    s = 1.0
    v = 1.0

    for i in range(steps):
        current_hue = (start_hue + i * hue_step) % 360
        rgb = hsv2rgb(current_hue, s, v)
        yield rgb

if __name__ == "__main__":
    timer = Timer(0.03).start()
    for rgb in spectral_cycle():
        print(rgb)
        timer.wait()
        timer.reset()
