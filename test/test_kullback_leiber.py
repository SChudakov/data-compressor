import unittest

import kullback_leiber


class TestKullbackLeiber(unittest.TestCase):
    def test_1(self):
        first_distribution = [1 / 2, 1 / 4, 1 / 8, 1 / 8]
        second_distribution = [1 / 4, 1 / 8, 1 / 8, 1 / 2]
        expected_first_to_second_kl_distance = 1 / 2
        expected_second_to_first_kl_distance = 5 / 8


        first_to_second_kl_distance = kullback_leiber.kullback_leiber_distance(first_distribution, second_distribution)
        second_to_first_kl_distance = kullback_leiber.kullback_leiber_distance(second_distribution, first_distribution)

        self.assertEqual(expected_first_to_second_kl_distance, first_to_second_kl_distance)
        self.assertEqual(expected_second_to_first_kl_distance, second_to_first_kl_distance)
