import os
import unittest

from mock import mock

import execution

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

_read_file_path = 'D:\workspace.python\data-compressor\\test_files\\test_execute_read.txt'
_write_file_path = 'D:\workspace.python\data-compressor\\test_files\\test_execute_write.txt'

_not_existing_read_file_path = 'D:\workspace.python\data-compressor\\test_files\\not_existing_file.txt'

_test_code_type = 'test code type'
_wrong_code_type = 'wrong code type'

_specified_divergence_str = '1.0'
_specified_divergence = 1.0

_default_divergence_str = '0.05'
_default_divergence = 0.05


def _get_arguments_dict(compress, decompress, read_file, write_file,
                        lzw, elias, divergence, code):
    return {_compress_command: compress,
            _decompress_command: decompress,
            _read_file_parameter: read_file,
            _write_file_parameter: write_file,
            _lzw_option: lzw,
            _elias_option: elias,
            _divergence_option: divergence,
            _code_option: code}


@mock.patch('util.default_write_file_path')
@mock.patch('lzw.compress')
@mock.patch('lzw.decompress')
@mock.patch('elias.compress')
@mock.patch('elias.decompress')
class TestExecutionLzw(unittest.TestCase):

    #  compress   <read_file> [-o <write_file>]
    #                                 0
    #                                 1

    #  decompress <read_file> [-o <write_file>] [--lzw]
    #                                 0             0
    #                                 0             1
    #                                 1             0
    #                                 1             1

    # -----------   test execute compress -------------

    @classmethod
    def setUpClass(cls):
        open(_read_file_path, 'a+').close()

    @classmethod
    def tearDownClass(cls):
        os.remove(_read_file_path)

    def test_execute_compress(self,
                              mocked_elias_decompress,
                              mocked_elias_compress,
                              mocked_lzw_decompress,
                              mocked_lzw_compress,
                              mocked_default_write_file):
        command = _compress_command

        mocked_default_write_file.return_value = _write_file_path
        arguments = _get_arguments_dict(True, False, _read_file_path, None,
                                        False, False, None, None)

        execution.execute(arguments)

        mocked_default_write_file.assert_called_with(_read_file_path, command)

        mocked_lzw_compress.assert_called_with(_read_file_path, _write_file_path)

        self.assertFalse(mocked_lzw_decompress.called)
        self.assertFalse(mocked_elias_compress.called)
        self.assertFalse(mocked_elias_decompress.called)

    def test_execute_compress_write_file(self,
                                         mocked_elias_decompress,
                                         mocked_elias_compress,
                                         mocked_lzw_decompress,
                                         mocked_lzw_compress,
                                         mocked_default_write_file):
        arguments = _get_arguments_dict(True, False, _read_file_path, _write_file_path,
                                        False, False, None, None)

        execution.execute(arguments)

        self.assertFalse(mocked_default_write_file.called)

        mocked_lzw_compress.assert_called_with(_read_file_path, _write_file_path)
        self.assertFalse(mocked_lzw_decompress.called)
        self.assertFalse(mocked_elias_compress.called)
        self.assertFalse(mocked_elias_decompress.called)

    # -----------   test execute compress lzw -------------

    def test_execute_compress_lzw(self,
                                  mocked_elias_decompress,
                                  mocked_elias_compress,
                                  mocked_lzw_decompress,
                                  mocked_lzw_compress,
                                  mocked_default_write_file):
        command = _compress_command

        mocked_default_write_file.return_value = _write_file_path
        arguments = _get_arguments_dict(True, False, _read_file_path, None,
                                        True, False, None, None)

        execution.execute(arguments)

        mocked_default_write_file.assert_called_with(_read_file_path, command)
        mocked_lzw_compress.assert_called_with(_read_file_path, _write_file_path)
        self.assertFalse(mocked_lzw_decompress.called)
        self.assertFalse(mocked_elias_compress.called)
        self.assertFalse(mocked_elias_decompress.called)

    def test_execute_compress_write_file_lzw(self,
                                             mocked_elias_decompress,
                                             mocked_elias_compress,
                                             mocked_lzw_decompress,
                                             mocked_lzw_compress,
                                             mocked_default_write_file):
        arguments = _get_arguments_dict(True, False, _read_file_path, _write_file_path,
                                        True, False, None, None)

        execution.execute(arguments)

        self.assertFalse(mocked_default_write_file.called)

        mocked_lzw_compress.assert_called_with(_read_file_path, _write_file_path)
        self.assertFalse(mocked_lzw_decompress.called)
        self.assertFalse(mocked_elias_compress.called)
        self.assertFalse(mocked_elias_decompress.called)

    # -----------   test execute decompress lzw -------------

    def test_execute_decompress_lzw(self,
                                    mocked_elias_decompress,
                                    mocked_elias_compress,
                                    mocked_lzw_decompress,
                                    mocked_lzw_compress,
                                    mocked_default_write_file):
        command = _decompress_command

        mocked_default_write_file.return_value = _write_file_path
        arguments = _get_arguments_dict(False, True, _read_file_path, None,
                                        True, False, None, None)

        execution.execute(arguments)

        mocked_default_write_file.assert_called_with(_read_file_path, command)
        self.assertFalse(mocked_lzw_compress.called)
        mocked_lzw_decompress.assert_called_with(_read_file_path, _write_file_path)
        self.assertFalse(mocked_elias_compress.called)
        self.assertFalse(mocked_elias_decompress.called)

    def test_execute_decompress_write_file_lzw(self,
                                               mocked_elias_decompress,
                                               mocked_elias_compress,
                                               mocked_lzw_decompress,
                                               mocked_lzw_compress,
                                               mocked_default_write_file):
        arguments = _get_arguments_dict(False, True, _read_file_path, _write_file_path,
                                        True, False, None, None)

        execution.execute(arguments)

        self.assertFalse(mocked_default_write_file.called)

        self.assertFalse(mocked_lzw_compress.called)
        mocked_lzw_decompress.assert_called_with(_read_file_path, _write_file_path)
        self.assertFalse(mocked_elias_compress.called)
        self.assertFalse(mocked_elias_decompress.called)


@mock.patch('characters_distribution.code_type')
@mock.patch('util.default_write_file_path')
@mock.patch('lzw.compress')
@mock.patch('lzw.decompress')
@mock.patch('elias.compress')
@mock.patch('elias.decompress')
class TestExecutionElias(unittest.TestCase):

    # compress <read_file> [-o <write_file>] --elias [--divergence <divergence>|--code <code>] [--hp]
    #                        0                                                0                   0
    #                        0                                                0                   1
    #                        0                                                1                   0
    #                        0                                                1                   1
    #                        0                                                2                   0
    #                        0                                                2                   1
    #                        1                                                0                   0
    #                        1                                                0                   1
    #                        1                                                1                   0
    #                        1                                                1                   1
    #                        1                                                2                   0
    #                        1                                                2                   1

    # decompress <read_file> [-o <write_file>] --code <code> [--hp]
    #                               0                          0
    #                               0                          1
    #                               1                          0
    #                               1                          1

    @classmethod
    def setUpClass(cls):
        open(_read_file_path, 'a+').close()

    @classmethod
    def tearDownClass(cls):
        os.remove(_read_file_path)

    # -------------------------------------------  test execute compress elias  --------------------------------------

    def test_execute_compress_elias(self,
                                    mocked_elias_decompress,
                                    mocked_elias_compress,
                                    mocked_lzw_decompress,
                                    mocked_lzw_compress,
                                    mocked_default_write_file,
                                    mocked_code_type):
        command = _compress_command
        code_type = _test_code_type
        divergence_str = _default_divergence_str
        divergence = _default_divergence

        mocked_default_write_file.return_value = _write_file_path
        mocked_code_type.return_value = code_type

        arguments = _get_arguments_dict(True, False, _read_file_path, None,
                                        False, True, divergence_str, None)

        execution.execute(arguments)

        mocked_code_type.assert_called_with(_read_file_path, distribution_divergence=divergence)
        mocked_default_write_file.assert_called_with(_read_file_path, command)

        self.assertFalse(mocked_lzw_compress.called)
        self.assertFalse(mocked_lzw_decompress.called)
        mocked_elias_compress.assert_called_with(_read_file_path, _write_file_path, code_type=code_type)
        self.assertFalse(mocked_elias_decompress.called)

    def test_execute_compress_elias_divergence(self,
                                               mocked_elias_decompress,
                                               mocked_elias_compress,
                                               mocked_lzw_decompress,
                                               mocked_lzw_compress,
                                               mocked_default_write_file,
                                               mocked_code_type):
        command = _compress_command
        code_type = _test_code_type
        divergence_str = _specified_divergence_str
        divergence = _specified_divergence

        mocked_default_write_file.return_value = _write_file_path
        mocked_code_type.return_value = code_type

        arguments = _get_arguments_dict(True, False, _read_file_path, None,
                                        False, True, divergence_str, None)

        execution.execute(arguments)

        mocked_code_type.assert_called_with(_read_file_path, distribution_divergence=divergence)
        mocked_default_write_file.assert_called_with(_read_file_path, command)

        self.assertFalse(mocked_lzw_compress.called)
        self.assertFalse(mocked_lzw_decompress.called)
        mocked_elias_compress.assert_called_with(_read_file_path, _write_file_path, code_type=code_type)
        self.assertFalse(mocked_elias_decompress.called)

    def test_execute_compress_elias_code(self,
                                         mocked_elias_decompress,
                                         mocked_elias_compress,
                                         mocked_lzw_decompress,
                                         mocked_lzw_compress,
                                         mocked_default_write_file,
                                         mocked_code_type):
        command = _compress_command
        code_type = _gamma_code_type
        divergence_str = None

        mocked_default_write_file.return_value = _write_file_path

        arguments = _get_arguments_dict(True, False, _read_file_path, None,
                                        False, True, divergence_str, code_type)

        execution.execute(arguments)

        self.assertFalse(mocked_code_type.called)
        mocked_default_write_file.assert_called_with(_read_file_path, command)

        self.assertFalse(mocked_lzw_compress.called)
        self.assertFalse(mocked_lzw_decompress.called)
        mocked_elias_compress.assert_called_with(_read_file_path, _write_file_path, code_type=code_type)
        self.assertFalse(mocked_elias_decompress.called)

    # -------------------------------------   test execute compress write_file elias  --------------------------------

    def test_execute_compress_write_file_elias(self,
                                               mocked_elias_decompress,
                                               mocked_elias_compress,
                                               mocked_lzw_decompress,
                                               mocked_lzw_compress,
                                               mocked_default_write_file,
                                               mocked_code_type):
        code_type = _test_code_type
        divergence_str = _default_divergence_str
        divergence = _default_divergence

        mocked_default_write_file.return_value = _write_file_path
        mocked_code_type.return_value = code_type

        arguments = _get_arguments_dict(True, False, _read_file_path, _write_file_path,
                                        False, True, divergence_str, None)

        execution.execute(arguments)

        mocked_code_type.assert_called_with(_read_file_path, distribution_divergence=divergence)
        self.assertFalse(mocked_default_write_file.called)

        self.assertFalse(mocked_lzw_compress.called)
        self.assertFalse(mocked_lzw_decompress.called)
        mocked_elias_compress.assert_called_with(_read_file_path, _write_file_path, code_type=code_type)
        self.assertFalse(mocked_elias_decompress.called)

    def test_execute_compress_write_file_elias_divergence(self,
                                                          mocked_elias_decompress,
                                                          mocked_elias_compress,
                                                          mocked_lzw_decompress,
                                                          mocked_lzw_compress,
                                                          mocked_default_write_file,
                                                          mocked_code_type):
        code_type = _test_code_type
        divergence_str = _specified_divergence_str
        divergence = _specified_divergence

        mocked_default_write_file.return_value = _write_file_path
        mocked_code_type.return_value = code_type

        arguments = _get_arguments_dict(True, False, _read_file_path, _write_file_path,
                                        False, True, divergence_str, None)

        execution.execute(arguments)

        mocked_code_type.assert_called_with(_read_file_path, distribution_divergence=divergence)
        self.assertFalse(mocked_default_write_file.called)

        self.assertFalse(mocked_lzw_compress.called)
        self.assertFalse(mocked_lzw_decompress.called)
        mocked_elias_compress.assert_called_with(_read_file_path, _write_file_path,code_type=code_type)
        self.assertFalse(mocked_elias_decompress.called)

    def test_execute_compress_write_file_elias_code(self,
                                                    mocked_elias_decompress,
                                                    mocked_elias_compress,
                                                    mocked_lzw_decompress,
                                                    mocked_lzw_compress,
                                                    mocked_default_write_file,
                                                    mocked_code_type):
        code_type = _gamma_code_type
        divergence_str = None

        mocked_default_write_file.return_value = _write_file_path

        arguments = _get_arguments_dict(True, False, _read_file_path, _write_file_path,
                                        False, True, divergence_str, code_type)

        execution.execute(arguments)

        self.assertFalse(mocked_code_type.called)
        self.assertFalse(mocked_default_write_file.called)

        self.assertFalse(mocked_lzw_compress.called)
        self.assertFalse(mocked_lzw_decompress.called)
        mocked_elias_compress.assert_called_with(_read_file_path, _write_file_path, code_type=code_type)
        self.assertFalse(mocked_elias_decompress.called)

    # ----------------------------------------   test execute decompress elias  -------------------------------------

    def test_execute_decompress_elias_code_gamma(self,
                                                 mocked_elias_decompress,
                                                 mocked_elias_compress,
                                                 mocked_lzw_decompress,
                                                 mocked_lzw_compress,
                                                 mocked_default_write_file,
                                                 mocked_code_type):
        command = _decompress_command
        code_type = _gamma_code_type
        divergence_str = None

        mocked_default_write_file.return_value = _write_file_path

        arguments = _get_arguments_dict(False, True, _read_file_path, None,
                                        False, True, divergence_str, code_type)

        execution.execute(arguments)

        self.assertFalse(mocked_code_type.called)
        mocked_default_write_file.assert_called_with(_read_file_path, command)

        self.assertFalse(mocked_lzw_compress.called)
        self.assertFalse(mocked_lzw_decompress.called)
        self.assertFalse(mocked_elias_compress.called)
        mocked_elias_decompress.assert_called_with(_read_file_path, _write_file_path, code_type=code_type)

    def test_execute_decompress_elias_code_delta(self,
                                                 mocked_elias_decompress,
                                                 mocked_elias_compress,
                                                 mocked_lzw_decompress,
                                                 mocked_lzw_compress,
                                                 mocked_default_write_file,
                                                 mocked_code_type):
        command = _decompress_command
        code_type = _delta_code_type
        divergence_str = None

        mocked_default_write_file.return_value = _write_file_path

        arguments = _get_arguments_dict(False, True, _read_file_path, None,
                                        False, True, divergence_str, code_type)

        execution.execute(arguments)

        self.assertFalse(mocked_code_type.called)
        mocked_default_write_file.assert_called_with(_read_file_path, command)

        self.assertFalse(mocked_lzw_compress.called)
        self.assertFalse(mocked_lzw_decompress.called)
        self.assertFalse(mocked_elias_compress.called)
        mocked_elias_decompress.assert_called_with(_read_file_path, _write_file_path, code_type=code_type)

    def test_execute_decompress_elias_code_omega(self,
                                                 mocked_elias_decompress,
                                                 mocked_elias_compress,
                                                 mocked_lzw_decompress,
                                                 mocked_lzw_compress,
                                                 mocked_default_write_file,
                                                 mocked_code_type):
        command = _decompress_command
        code_type = _omega_code_type
        divergence_str = None

        mocked_default_write_file.return_value = _write_file_path

        arguments = _get_arguments_dict(False, True, _read_file_path, None,
                                        False, True, divergence_str, code_type)

        execution.execute(arguments)

        self.assertFalse(mocked_code_type.called)
        mocked_default_write_file.assert_called_with(_read_file_path, command)

        self.assertFalse(mocked_lzw_compress.called)
        self.assertFalse(mocked_lzw_decompress.called)
        self.assertFalse(mocked_elias_compress.called)
        mocked_elias_decompress.assert_called_with(_read_file_path, _write_file_path, code_type=code_type)

    # -------------------------------------   test execute decompress write file elias  -------------------------------

    def test_execute_decompress_write_file_elias_code(self,
                                                      mocked_elias_decompress,
                                                      mocked_elias_compress,
                                                      mocked_lzw_decompress,
                                                      mocked_lzw_compress,
                                                      mocked_default_write_file,
                                                      mocked_code_type):
        code_type = _gamma_code_type
        divergence_str = None

        mocked_default_write_file.return_value = _write_file_path

        arguments = _get_arguments_dict(False, True, _read_file_path, _write_file_path,
                                        False, True, divergence_str, code_type)

        execution.execute(arguments)

        self.assertFalse(mocked_code_type.called)
        self.assertFalse(mocked_default_write_file.called)

        self.assertFalse(mocked_lzw_compress.called)
        self.assertFalse(mocked_lzw_decompress.called)
        self.assertFalse(mocked_elias_compress.called)
        mocked_elias_decompress.assert_called_with(_read_file_path, _write_file_path,code_type=code_type)


class TestExecutionWrongParameters(unittest.TestCase):

    def test_execute_wrong_code_type(self):
        code_type = _wrong_code_type
        arguments = _get_arguments_dict(False, True, _read_file_path, None,
                                        False, True, None, code_type)

        self.assertRaises(Exception, execution.execute, arguments)

    def test_execute_not_existing_read_file(self):
        read_file = _not_existing_read_file_path
        arguments = _get_arguments_dict(False, True, read_file, None,
                                        False, True, None, None)

        self.assertRaises(Exception, execution.execute, arguments)

    def test_execute_default_divergence_exceeded(self):
        pass

    def test_execute_specified_divergence_exceeded(self):
        pass
