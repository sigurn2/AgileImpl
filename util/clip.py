import numpy as np

def clipper(data):
    mean = np.mean(data)
    std = np.std(data, ddof=1)
    standardized = [25 * (x - mean) / std + 50 for x in data]
    clipped = np.clip(standardized, 0, 100)
    return [round(x, 0) for x in clipped]



if __name__ == '__main__':
    data = [
        66.66666667,
        83.33333333,
        100,
        100,
        16.66666667,
        50,
        100,
        83.33333333,
        66.66666667,
        33.33333333,
        50,
        0,
        33.33333333,
        0,
        33.33333333,
        50,
        16.66666667,
        16.66666667,
        0,
        0,
        33.33333333,
        0,
        100,
        66.66666667,
        66.66666667,
        66.66666667,
        33.33333333,
        66.66666667,
        50,
        50,
        66.66666667,
        66.66666667,
        66.66666667,
        100,
        66.66666667,
        66.66666667,
        0,
        16.66666667,
        16.66666667,
        0,
    ]
    for x in clipper(data):
        print(x)