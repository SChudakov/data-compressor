import math


def kullback_leiber_distance(first_distribution, second_distribution):
    if not (len(first_distribution) == len(second_distribution)):
        raise ValueError('distributions should be of the same length')

    result = 0

    for i in range(len(first_distribution)):
        result += first_distribution[i] * math.log(first_distribution[i] / second_distribution[i], 2)

    return result
