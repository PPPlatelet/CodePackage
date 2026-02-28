#include <algorithm>
#include <cmath>

#include "types.h"

typedef struct {
    u64 r;
    u64 g;
    u64 b;
    f64 a;
} RGB;

typedef struct {
    u64 h;
    f64 s;
    f64 l;
    f64 a;
} HSL;

typedef struct {
    u64 h;
    f64 s;
    f64 v;
    f64 a;
} HSV;

typedef struct {
    f64 y;
    f64 u;
    f64 v;
    f64 a;
} YUV, YCbCr;

// RGB -> HSL
HSL RGB2HSL(RGB rgb) {
    f64 r = rgb.r / 255.0, g = rgb.g / 255.0, b = rgb.b / 255.0;
    f64 max = std::max({r, g, b}), min = std::min({r, g, b});
    f64 h = 0, s = 0, l = (max + min) / 2;

    if (max == min) {
        h = s = 0; // achromatic
    } else {
        f64 d = max - min;
        s = l > 0.5 ? d / (2 - max - min) : d / (max + min);

        if (max == r) {
            h = (g - b) / d + (g < b ? 6 : 0);
        } else if (max == g) {
            h = (b - r) / d + 2;
        } else {
            h = (r - g) / d + 4;
        }

        h /= 6;
    }
    return HSL{ .h = static_cast<u64>(std::round(h * 360.0)), .s = s, .l = l, .a = rgb.a };
}

// HSL -> RGB
RGB HSL2RGB(HSL hsl) {
    f64 h = hsl.h / 360.0, s = hsl.s, l = hsl.l;
    f64 r = 0, g = 0, b = 0;

    if (s == 0) {
        r = g = b = l; // achromatic
    } else {
        auto hue2rgb = [](f64 p, f64 q, f64 t) -> f64 {
            if (t < 0.0) t += 1;
            if (t > 1.0) t -= 1;
            if (t < 1 / 6.0) return p + (q - p) * 6 * t;
            if (t < 1 / 2.0) return q;
            if (t < 2 / 3.0) return p + (q - p) * (2 / 3.0 - t) * 6;

            return p;
        };

        f64 q = l < 0.5 ? l * (1 + s) : l + s - l * s;
        f64 p = 2 * l - q;

        r = hue2rgb(p, q, h + 1 / 3.0);
        g = hue2rgb(p, q, h);
        b = hue2rgb(p, q, h - 1 / 3.0);
    }
    return RGB{ .r = static_cast<u64>(std::round(r * 255)), .g = static_cast<u64>(std::round(g * 255)), .b = static_cast<u64>(std::round(b * 255)), .a = hsl.a };
}

// RGB -> HSV
HSV RGB2HSV(RGB rgb) {
    f64 r = rgb.r / 255.0, g = rgb.g / 255.0, b = rgb.b / 255.0;
    f64 max = std::max({r, g, b}), min = std::min({r, g, b});
    f64 h = 0, s = 0, v = max;

    if (max == min) {
        h = s = 0; // achromatic
    } else {
        f64 d = max - min;
        s = max == 0 ? 0 : d / max;

        if (max == r) {
            h = (g - b) / d + (g < b ? 6 : 0);
        } else if (max == g) {
            h = (b - r) / d + 2;
        } else {
            h = (r - g) / d + 4;
        }

        h /= 6;
    }
    return HSV{ .h = static_cast<u64>(std::round(h * 360.0)), .s = s, .v = v, .a = rgb.a };
}

// HSV -> RGB
RGB HSV2RGB(HSV hsv) {
    f64 r = 0, g = 0, b = 0, h = hsv.h / 360.0, s = hsv.s, v = hsv.v;

    u64 i = static_cast<u64>(std::floor(h * 6));
    f64 f = h * 6 - i;
    f64 p = v * (1 - s);
    f64 q = v * (1 - f * s);
    f64 t = v * (1 - (1 - f) * s);

    switch (i % 6) {
        case 0: r = v, g = t, b = p; break;
        case 1: r = q, g = v, b = p; break;
        case 2: r = p, g = v, b = t; break;
        case 3: r = p, g = q, b = v; break;
        case 4: r = t, g = p, b = v; break;
        case 5: r = v, g = p, b = q; break;
    }
    return RGB{ .r = static_cast<u64>(std::round(r * 255)), .g = static_cast<u64>(std::round(g * 255)), .b = static_cast<u64>(std::round(b * 255)), .a = hsv.a };
}

// HSL -> HSV
HSV HSL2HSV(HSL hsl) {
    f64 h = hsl.h / 360.0, s = hsl.s, l = hsl.l;
    f64 v = l + s * std::min(l, 1 - l);
    f64 s_hsv = v == 0 ? 0 : 2 * (1 - l / v);
    return HSV{ .h = static_cast<u64>(std::round(h * 360.0)), .s = s_hsv, .v = v, .a = hsl.a };
}

// HSV -> HSL
HSL HSV2HSL(HSV hsv) {
    f64 h = hsv.h / 360.0, s = hsv.s, v = hsv.v;
    f64 l = v * (1 - s / 2);
    f64 s_hsl = l == 0 || l == 1 ? 0 : (v - l) / std::min(l, 1 - l);

    return HSL{ .h = static_cast<u64>(std::round(h * 360.0)), .s = s_hsl, .l = l, .a = hsv.a };
}

// RGB -> YUV
YUV RGB2YUV(RGB rgb) {
    f64 y = 0.257 * rgb.r + 0.504 * rgb.g + 0.098 * rgb.b + 16;
    f64 u = -0.148 * rgb.r - 0.291 * rgb.g + 0.439 * rgb.b + 128;
    f64 v = 0.439 * rgb.r - 0.368 * rgb.g - 0.071 * rgb.b + 128;
    return YUV{ .y = y, .u = u, .v = v, .a = rgb.a };
}

// YUV -> RGB
RGB YUV2RGB(YUV yuv) {
    f64 r = 1.164 * (yuv.y - 16) + 1.596 * (yuv.v - 128);
    f64 g = 1.164 * (yuv.y - 16) - 0.392 * (yuv.u - 128) - 0.813 * (yuv.v - 128);
    f64 b = 1.164 * (yuv.y - 16) + 2.017 * (yuv.u - 128);
    return RGB{ .r = static_cast<u64>(std::round(std::clamp(r, 0.0, 255.0))), .g = static_cast<u64>(std::round(std::clamp(g, 0.0, 255.0))), .b = static_cast<u64>(std::round(std::clamp(b, 0.0, 255.0))), .a = yuv.a };
}