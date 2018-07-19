default_file_encoding = 'utf-8'

_read_mode = 'r'
_write_bytes_mode = 'wb'

_read_bytes_mode = 'rb'
_write_mode = 'w'

_multiple_write_bytes_mode = 'ab'

encode_read_configuration = {'mode': _read_mode, 'encoding': default_file_encoding}
encode_write_configuration = {'mode': _write_bytes_mode}

decode_read_configuration = {'mode': _read_bytes_mode}
decode_write_configuration = {'mode': _write_mode, 'encoding': default_file_encoding}

combine_read_configuration = {'mode': _read_bytes_mode}
combine_write_configuration = {'mode': _multiple_write_bytes_mode}
