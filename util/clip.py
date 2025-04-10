import numpy as np

def clipper(data):
    mean = np.mean(data)
    std = np.std(data, ddof=1)
    standardized = [25 * (x - mean) / std + 50 for x in data]
    clipped = np.clip(standardized, 0, 100)
    return [round(x, 0) for x in clipped]



if __name__ == '__main__':
    data = [
        89.5,
        92.5,
        37.0,
        24.0,
        32.0,
        69.0,
        36.0,
        52.5,
        53.5,
        82.0,
        17.0,
        38.5,
        8.5,
        8.5,
        70.5,
        50.0,
        11.5,
        5.5,
        18.0,
        35.0,
        67.0,
        68.5,
        27.5,
        25.0,
        29.5,
        12.5,
        60.5,
        46.0,
        5.0,
        4.0,
        29.5,
        12.0,
        53.5,
        24.5,
        15.0,
        23.5,
        46.0,
        5.5,
        20.5,
        39.5,
    ]
    for x in clipper(data):
        print(x)