import unittest

from src import elias_code_functions


class TestEliasFunction(unittest.TestCase):

    def test_gamma_code_incorrect_number(self):
        self.assertRaises(ValueError, elias_code_functions.gamma_code, 0)
        self.assertRaises(ValueError, elias_code_functions.gamma_code, -1)

    def test_delta_code_incorrect_number(self):
        self.assertRaises(ValueError, elias_code_functions.delta_code, 0)
        self.assertRaises(ValueError, elias_code_functions.delta_code, -1)

    def test_omega_code_incorrect_number(self):
        self.assertRaises(ValueError, elias_code_functions.omega_code, 0)
        self.assertRaises(ValueError, elias_code_functions.omega_code, -1)

    def test_gamma_code(self):
        self.assertEqual('1', elias_code_functions.gamma_code(1))
        self.assertEqual('010', elias_code_functions.gamma_code(2))
        self.assertEqual('011', elias_code_functions.gamma_code(3), )
        self.assertEqual('00100', elias_code_functions.gamma_code(4))
        self.assertEqual('00101', elias_code_functions.gamma_code(5))
        self.assertEqual('00110', elias_code_functions.gamma_code(6))
        self.assertEqual('00111', elias_code_functions.gamma_code(7))
        self.assertEqual('0001000', elias_code_functions.gamma_code(8))
        self.assertEqual('0001001', elias_code_functions.gamma_code(9))
        self.assertEqual('0001010', elias_code_functions.gamma_code(10))
        self.assertEqual('0001011', elias_code_functions.gamma_code(11))
        self.assertEqual('0001100', elias_code_functions.gamma_code(12))
        self.assertEqual('0001101', elias_code_functions.gamma_code(13))
        self.assertEqual('0001110', elias_code_functions.gamma_code(14))
        self.assertEqual('0001111', elias_code_functions.gamma_code(15))
        self.assertEqual('000010000', elias_code_functions.gamma_code(16))
        self.assertEqual('000010001', elias_code_functions.gamma_code(17))

    def test_delta_code(self):
        self.assertEqual('1', elias_code_functions.delta_code(1))
        self.assertEqual('0100', elias_code_functions.delta_code(2))
        self.assertEqual('0101', elias_code_functions.delta_code(3))
        self.assertEqual('01100', elias_code_functions.delta_code(4))
        self.assertEqual('01101', elias_code_functions.delta_code(5))
        self.assertEqual('01110', elias_code_functions.delta_code(6))
        self.assertEqual('01111', elias_code_functions.delta_code(7))
        self.assertEqual('00100000', elias_code_functions.delta_code(8))
        self.assertEqual('00100001', elias_code_functions.delta_code(9))
        self.assertEqual('00100010', elias_code_functions.delta_code(10))
        self.assertEqual('00100011', elias_code_functions.delta_code(11))
        self.assertEqual('00100100', elias_code_functions.delta_code(12))
        self.assertEqual('00100101', elias_code_functions.delta_code(13))
        self.assertEqual('00100110', elias_code_functions.delta_code(14))
        self.assertEqual('00100111', elias_code_functions.delta_code(15))
        self.assertEqual('001010000', elias_code_functions.delta_code(16))
        self.assertEqual('001010001', elias_code_functions.delta_code(17))

    def test_omega_code(self):
        self.assertEqual('0', elias_code_functions.omega_code(1))
        self.assertEqual('100', elias_code_functions.omega_code(2))
        self.assertEqual('110', elias_code_functions.omega_code(3))
        self.assertEqual('101000', elias_code_functions.omega_code(4))
        self.assertEqual('101010', elias_code_functions.omega_code(5))
        self.assertEqual('101100', elias_code_functions.omega_code(6))
        self.assertEqual('101110', elias_code_functions.omega_code(7))
        self.assertEqual('1110000', elias_code_functions.omega_code(8))
        self.assertEqual('1110010', elias_code_functions.omega_code(9))
        self.assertEqual('1110100', elias_code_functions.omega_code(10))
        self.assertEqual('1110110', elias_code_functions.omega_code(11))
        self.assertEqual('1111000', elias_code_functions.omega_code(12))
        self.assertEqual('1111010', elias_code_functions.omega_code(13))
        self.assertEqual('1111100', elias_code_functions.omega_code(14))
        self.assertEqual('1111110', elias_code_functions.omega_code(15))
        self.assertEqual('10100100000', elias_code_functions.omega_code(16))
        self.assertEqual('10100100010', elias_code_functions.omega_code(17))
