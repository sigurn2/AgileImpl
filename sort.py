
from util.distribution import fill_zero, QuantileAdaption
from util.clip import clipper
import numpy as np
if __name__ == '__main__':

    data = [
        96.9,
        91.0,
        46.2,
        55.9,
        76.9,
        55.0,
        33.0,
        91.7,
        29.3,
        38.9,
        22.3,
        22.4,
        47.0,
        26.6,
        61.7,
        84.7,
        18.8,
        25.7,
        22.2,
        32.1,
        83.0,
        31.4,
        42.7,
        14.6,
        25.6,
        14.3,
        27.0,
        14.7,
        17.4,
        11.5,
        17.1,
        11.0,
        26.6,
        19.5,
        12.8,
        17.9,
        32.1,
        12.1,
        22.3,
        27.3,
    ]
    a = clipper(data)
    for b in a:
        print(b)