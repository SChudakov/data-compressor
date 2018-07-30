from schema import Schema, Or, Use

import characters_distribution
import elias
import lzw
import util

_compress_command = 'compress'
_decompress_command = 'decompress'

_read_file_parameter = '<read_file>'
_write_file_parameter = '<write_file>'

_lzw_option = '--lzw'
_elias_option = '--elias'
_divergence_option = '--divergence'
_code_option = '--code'
_high_performance_option = '--hp'

_gamma_code_type = 'gamma'
_delta_code_type = 'delta'
_omega_code_type = 'omega'

_read_file_error = 'read_file should exist and be readable'
_write_file_error = 'write_file must be readable'
_divergence_error = 'divergence must be a float number'
_elias_code_error = 'elias code type should be gamma, delta, or omega'

_default_divergence_exceed_error = "The characters distribution in file {} is diverged more than by " \
                                   "default value {} from the optimal distribution to be compressed " \
                                   "with any elias code. Specify greater divergence value by using " \
                                   "--divergence option or force using specific elias code by using " \
                                   "--code option"
_specified_divergence_exceed_error = "The characters distribution in file {} is diverged more than by specified " \
                                     "value {} from the optimal distribution to be compressed with any elias code. " \
                                     "Specify greater divergence value by using --divergence option or force using " \
                                     "specific elias code by using --code option"
_default_divergence = 0.05


def execute(arguments):
    _validate_arguments(arguments)
    _enrich_arguments(arguments)

    compress_value = arguments[_compress_command]

    read_file_value = arguments[_read_file_parameter]
    write_file_value = arguments[_write_file_parameter]

    lzw_value = arguments[_lzw_option]
    elias_value = arguments[_elias_option]

    code_value = arguments[_code_option]
    high_performance_value = arguments[_high_performance_option]

    if compress_value:
        if lzw_value:
            lzw.compress(read_file_value, write_file_value)
        elif elias_value:
            elias.compress(read_file_value, write_file_value, code_type=code_value,
                           high_performance=high_performance_value)
    else:
        if lzw_value:
            lzw.decompress(read_file_value, write_file_value)
        elif elias_value:
            elias.decompress(read_file_value, write_file_value, code_type=code_value,
                             high_performance=high_performance_value)


def _validate_arguments(arguments):
    schema = Schema({
        _read_file_parameter: Use(_validate_read_file, error=_read_file_error),
        _write_file_parameter: Or(None, Use(_validate_write_file, error=_write_file_error)),
        _divergence_option: Or(None, Use(float, error=_divergence_error)),
        _code_option: Or(None, _gamma_code_type, _delta_code_type, _omega_code_type, error=_elias_code_error),
        str: object
    })
    schema.validate(arguments)


def _validate_read_file(file):
    with open(file, 'r'):
        pass


def _validate_write_file(file):
    with open(file, 'w'):
        pass


def _enrich_arguments(arguments):
    compress_value = arguments[_compress_command]

    read_file_value = arguments[_read_file_parameter]
    write_file_value = arguments[_write_file_parameter]

    divergence_value = arguments[_divergence_option]
    code_value = arguments[_code_option]

    lzw_value = arguments[_lzw_option]
    elias_value = arguments[_elias_option]

    write_file_value_changed = False
    lzw_value_changed = False
    divergence_value_changed = False
    code_value_changed = False

    if write_file_value is None:
        if compress_value:
            command = _compress_command
        else:
            command = _decompress_command

        write_file_value = util.default_write_file_path(read_file_value, command)
        write_file_value_changed = True

    if not elias_value and not lzw_value:
        lzw_value = True
        lzw_value_changed = True
    elif elias_value:
        default_divergence_case = False
        if (divergence_value is None) and (code_value is None):
            divergence_value = _default_divergence_exceed_error
            default_divergence_case = True

        if not (divergence_value is None):
            divergence_value = float(divergence_value)
            divergence_value_changed = True

        if code_value is None:
            code_value = characters_distribution.code_type(read_file_value, distribution_divergence=divergence_value)
            _ensure_correct_code_value(code_value, read_file_value, divergence_value, default_divergence_case)
            code_value_changed = True

    if write_file_value_changed:
        arguments[_write_file_parameter] = write_file_value
    if lzw_value_changed:
        arguments[_lzw_option] = lzw_value
    if divergence_value_changed:
        arguments[_divergence_option] = divergence_value
    if code_value_changed:
        arguments[_code_option] = code_value


def _ensure_correct_code_value(code_value, read_file, divergence, is_default_divergence):
    if code_value is None:
        if is_default_divergence:
            error_message = _default_divergence_exceed_error
        else:
            error_message = _specified_divergence_exceed_error

        raise ValueError(error_message.format(read_file, divergence))
