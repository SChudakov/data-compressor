import utilities


def gamma_code(number):
    if number <= 0:
        raise ValueError('number should be >= 1')
    bits = utilities.to_binary(number)
    return '0' * (len(bits) - 1) + bits