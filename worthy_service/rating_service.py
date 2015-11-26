# encoding: utf-8

RATING_MAXTRIX = [
    1.0202,
    1.00658,
    0.997094,
    0.98037,
    0.90355,
]

def getRatingDiffScore(score):

    idx = 0
    for base in RATING_MAXTRIX:
        if score >= base:
            break
        idx += 1

    return 5-idx

# print getRatingDiffScore(0.88)