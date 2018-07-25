import utilities


def _ensure_correct_number(number):
    if number <= 0:
        raise ValueError('number should be >= 1')


def gamma_code(number):
    _ensure_correct_number(number)
    bits = utilities.to_binary(number)
    return '0' * (len(bits) - 1) + bits


def delta_code(number):
    _ensure_correct_number(number)
    bits = utilities.to_binary(number)
    return gamma_code(len(bits)) + bits[1:]


def omega_code(number):
    _ensure_correct_number(number)
    result = list()
    result.append('0')

    current_value = number
    while not (current_value == 1):
        value_bits = utilities.to_binary(current_value)
        result.append(value_bits)
        current_value = len(value_bits) - 1

    result.reverse()
    return ''.join(result)
