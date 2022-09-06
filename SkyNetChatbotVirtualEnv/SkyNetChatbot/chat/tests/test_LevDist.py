from django.test import TestCase
from chat.lev_dist import lev_dist, lev_dist_str_correct_w, lev_dist_custom_dist, lev_dist_str


class LevDistTest(TestCase):

    def setUp(self):
        pass

    def test_perfect_matching_words(self):
        """TU71: Test per il controllo che due parole siano perfettamente uguali"""
        self.assertEqual(lev_dist_custom_dist(["cane"], ["cane"], 0), True)

    def test_non_matching_words(self):
        """TU72: Test che controlla la distanza tra due parole sia > 2"""
        self.assertEqual(lev_dist(["cane"], ["gatto"]), False)

    def test_matching_words(self):
        """TU73: Test che controlla la distanza tra due parole sia <= 2"""
        self.assertEqual(lev_dist(["cane"], ["cani"]), True)

    def test_matching_words_custom_distance(self):
        """TU75: Test che controlla che la distanza tra due parole sia <= x"""
        self.assertEqual(lev_dist_custom_dist(["cane"], ["canini"], 4), True)

    def test_word_non_matches_in_words_list(self):
        """TU76: Test per il controllo di quale parola di una lista si avvicina a una parola data"""
        self.assertEqual(lev_dist_str(['Pallone'], ['check-in', 'checkin', 'check in', 'arrivato', 'entrato', 'entro',
                                                    'presenza']), None)

    def test_word_best_match_in_words_list(self):
        """TU77: Test per il controllo della miglior parola in una lista"""
        self.assertEqual(lev_dist_str_correct_w(['check-on'], ['check-in', 'checkin', 'check in', 'arrivato', 'entrato',
                                                               'entro', 'presenza']), 'check-in')

    def test_word_matches_in_words_list(self):
        """Test per il controllo di quale parola di una lista si avvicina a una parola data"""
        self.assertEqual(lev_dist_str(['check-on'], ['check-in', 'checkin', 'check in', 'arrivato', 'entrato', 'entro',
                                                     'presenza']), 'check-on')

    def test_word_non_match_in_words_list_at_all(self):
        """Test per il controllo della miglior parola in una lista"""
        self.assertEqual(lev_dist_str_correct_w(['Pallone'], ['check-in', 'checkin', 'check in', 'arrivato', 'entrato',
                                                              'entro', 'presenza']), None)

    def test_perfect_matching_different_words(self):
        """Test per il controllo che due parole non siano perfettamente uguali"""
        self.assertEqual(lev_dist_custom_dist(["cane"], ["cani"], 0), False)
