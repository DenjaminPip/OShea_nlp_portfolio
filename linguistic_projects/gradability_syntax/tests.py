import unittest
from make_survey_one import count_syllables, is_word_with_multiple_syllables, get_adjective_modifier, random_string, create_phrases
from make_survey_two import write_new_prompt

class SurveyOneTests(unittest.TestCase):

    def test_count_syllables(self):
        self.assertEqual(count_syllables("hello"), 2)
        self.assertEqual(count_syllables("world"), 1)
        self.assertEqual(count_syllables("beautiful"), 3)

    def test_is_word_with_multiple_syllables(self):
        self.assertTrue(is_word_with_multiple_syllables("beautiful"))
        self.assertFalse(is_word_with_multiple_syllables("world"))
        self.assertFalse(is_word_with_multiple_syllables("cat"))

    def test_get_adjective_modifier(self):
        self.assertEqual(get_adjective_modifier("big"), "biger")
        self.assertEqual(get_adjective_modifier("best"), "better")
        self.assertEqual(get_adjective_modifier("happy"), "more happy")

    def test_random_string(self):
        cls = ["apple", "banana", "orange"]
        self.assertEqual(random_string(cls, seed=123), "apple")

    def test_create_phrases(self):
        nouns = ["cat", "dog", "bird"]
        adjective = "slow"
        self.assertEqual(create_phrases(nouns, adjective, seed=123), """Mary thinks this cat is slower than that cat.
John doesn't think so.
Can they both be right or must one be wrong?""")

class SurveyTwoTests(unittest.TestCase):

    def test_write_new_prompt(self):
        adjective_1 = 'old'
        adjective_2 = 'soft'
        noun = 'chair'
        self.assertEqual(write_new_prompt(noun, adjective_1, adjective_2), ("the old soft chair", "the soft old chair"))

if __name__ == '__main__':
    unittest.main()