__author__ = 'bentanne'

import main
import junitxml
import unittest

class TestNumberOutput(unittest.TestCase):

    def test_is_prime(self):
        a_number= main.NUMBERS(30)
        self.assertTrue(a_number.is_prime_number(2))
        self.assertTrue(a_number.is_prime_number(37))
        self.assertTrue(a_number.is_prime_number(97))
        self.assertFalse(a_number.is_prime_number(1))
        self.assertFalse(a_number.is_prime_number(55))

    def test_is_square(self):
        a_number= main.NUMBERS(100)
        self.assertTrue(a_number.is_square_number(1))
        self.assertTrue(a_number.is_square_number(49))
        self.assertTrue(a_number.is_square_number(100))
        self.assertFalse(a_number.is_square_number(2))
        self.assertFalse(a_number.is_square_number(66))

    def test_filled_array(self):
        # test number of primes, non primes and squares in 1-99
        a_number= main.NUMBERS(0)
        self.assertTrue(len(a_number.primes) == 25,msg="primes array size = %d" % len(a_number.primes) )
        self.assertTrue(len(a_number.squares) == 9,msg="squares size = %d" % len(a_number.squares) )
        self.assertTrue(len(a_number.non_primes) == 65,msg="non primes size = %d" % len(a_number.non_primes) )

    def test_weighted_array(self):
        a_number= main.NUMBERS(0)
        num = a_number.generate()
        self.assertTrue(a_number.weighted_array.count('prime') == 3,msg="Weighted array prime count expected [3] got [%s]" %a_number.weighted_array.count('prime'))
        self.assertTrue(a_number.weighted_array.count('non_prime') == 3, msg="Weighted array prime count expected [3] got [%d]" %a_number.weighted_array.count('non_prime'))
        self.assertTrue(a_number.weighted_array.count('square') == 1, msg="Weighted array prime count expected [1] got [%d]" %a_number.weighted_array.count('squares'))

        a_number= main.NUMBERS(2)
        num = a_number.generate()
        self.assertTrue(a_number.weighted_array.count('prime') == 6,msg="Weighted array prime count expected [6] got [%s]" %a_number.weighted_array.count('prime'))
        self.assertTrue(a_number.weighted_array.count('non_prime') == 3, msg="Weighted array prime count expected [3] got [%d]" %a_number.weighted_array.count('non_prime'))
        self.assertTrue(a_number.weighted_array.count('square') == 2, msg="Weighted array prime count expected [2] got [%d]" %a_number.weighted_array.count('squares'))

        a_number= main.NUMBERS(10)
        num = a_number.generate()
        self.assertTrue(a_number.weighted_array.count('prime') == 30,msg="Weighted array prime count expected [3] got [%s]" %a_number.weighted_array.count('prime'))
        self.assertTrue(a_number.weighted_array.count('non_prime') == 3, msg="Weighted array prime count expected [3] got [%d]" %a_number.weighted_array.count('non_prime'))
        self.assertTrue(a_number.weighted_array.count('square') == 10, msg="Weighted array prime count expected [1] got [%d]" %a_number.weighted_array.count('squares'))

    def test_generate(self):
        #run this a million times and verify all output is valid
        for i in range(1,1000000):
            a_number= main.NUMBERS(0)
            self.assertTrue(a_number.generate() in range(1,100),msg="%d out of range" % a_number.current_value)

class TestLetterOutput(unittest.TestCase):

    def test_fill_dictionary(self):
        a_letter= main.LETTERS(10)
        self.assertTrue(a_letter.letter_dictionary[2] =='b',msg="Position of 'b' is incorrect %s" %a_letter.letter_dictionary[2])
        self.assertTrue(a_letter.letter_dictionary[26] =='z',msg="Position of 'z' is incorrect %s" %a_letter.letter_dictionary[26])
        self.assertTrue(a_letter.vowel_dictionary[1] == 'a', msg="Position of 'a' is incorrect %s" %a_letter.vowel_dictionary[1])

    def test_weighted_array(self):
        test_value = 0
        a_letter= main.LETTERS(test_value)
        num = a_letter.generate()

        self.assertTrue(a_letter.weighted_array.count('vowels') == a_letter.weighted_array.count('consonants'))
        self.assertTrue(a_letter.weighted_array.count('Y') == a_letter.weighted_array.count('vowels') * 2 )

        test_value= 10
        a_letter= main.LETTERS(test_value)
        num = a_letter.generate()

        self.assertTrue(a_letter.weighted_array.count('vowels') == a_letter.weighted_array.count('consonants') * test_value )
        self.assertTrue(a_letter.weighted_array.count('Y') == a_letter.weighted_array.count('vowels') *2 )

    def test_generate(self):
        #run this a million times and verify all output is valid
        for i in range(1,1000000):
            a_letter= main.LETTERS(0)
            self.assertTrue(a_letter.generate() in range(1,27),msg="%d out of range" % a_letter.current_value)



if __name__ == '__main__':

    # Test Suites
    numberTests = unittest.TestLoader().loadTestsFromTestCase(TestNumberOutput)
    letterTests = unittest.TestLoader().loadTestsFromTestCase(TestLetterOutput)
    # Combine Test Suites
    allTests = unittest.TestSuite([numberTests,letterTests])

    fp = file('test_results.xml', 'wb')
    result = junitxml.JUnitXmlResult(fp)

    # Execute
    result.startTestRun()
    allTests.run(result)
    result.stopTestRun()

    # Print Result
    if result.wasSuccessful():
        print "Test Passed"
    else:
        print "Test Failure"
