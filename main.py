#!/usr/bin/env python
__author__ = 'bentanne'

import sys
import argparse
import random
import math
import string
import json

class NUMBERS (object):
    def __init__(self,prime_weight):
        self.primes= []
        self.non_primes= []
        self.squares= []
        self.weight= prime_weight
        self.weighted_array= []
        self.fill_arrays()

    def is_prime_number(self,x):
        if x >= 2:
            for y in range(2,x):
                if not ( x % y ):
                    return False
        else:
	        return False
        return True

    def is_square_number(self,x):
        '''
        Valid method for 32bit integers
        '''
        return math.sqrt(x).is_integer()

    def fill_arrays(self):
        '''
        Sort 1-99 into 3 lists primes, squares, non primes
        Do this once
        '''
        for i in range(1,100):
            if self.is_prime_number(i):
                self.primes.append(i)
            elif self.is_square_number(i):
                self.squares.append(i)
            else:
                self.non_primes.append(i)

    def weighted_random_selection(self):
        '''
        Create a weighted random selection and return either prime, square or non_prime
        Prime = is three times more likely then square and "prime_weight" more likely then non prime.
        '''

        if not self.weighted_array:
            #if empty create it
            SQUARE_WEIGHT = 3
            if self.weight == 0:
                # [prime] [prime] [prime] [square] [non prime] [non prime] [non prime]
                self.weighted_array= ['prime'] * SQUARE_WEIGHT + ['square'] + ['non_prime'] * SQUARE_WEIGHT
            else:
                self.weighted_array= ['square'] * self.weight  + ['prime'] * (self.weight * SQUARE_WEIGHT)  + ['non_prime'] * SQUARE_WEIGHT

        return random.choice(self.weighted_array)

    def generate(self):
        '''
        Based on weighted random selection, pick a random from the correct list
        :return
        '''
        selection= self.weighted_random_selection()
        if selection == 'prime':
            result= random.choice(self.primes)
        elif selection == 'square':
            result= random.choice(self.squares)
        else:
            result= random.choice(self.non_primes)
        return result

class LETTERS(object):
    def __init__(self,weight):
        self.letter_dictionary= {}
        self.vowel_dictionary= {}
        self.weight = weight
        self.weighted_array= []
        self.fill_dictionary()

    def fill_dictionary(self):
        vowels = 'a','e','i','o','u'
        for i in list(string.ascii_lowercase):
            if(i in vowels):
                self.vowel_dictionary.update({string.ascii_lowercase.index(i)+1:i})
            elif(i != 'y'):
                self.letter_dictionary.update({string.ascii_lowercase.index(i)+1:i})

    def weighted_random_selection(self):
        '''
        Create a weighted random selection and return either wowels, consonants or Y
        Vowels have a weight greater chance, Y has a 2x vowel chance
        '''
        if not self.weighted_array:
            #if empty create it
            Y_WEIGHT = 2
            if self.weight == 0:
                self.weighted_array= ['vowels'] + ['Y'] * Y_WEIGHT + ['consonants']
            else:
                self.weighted_array= ['vowels'] * self.weight  + ['Y'] * (self.weight * Y_WEIGHT) + ['consonants']

        return random.choice(self.weighted_array)

    def generate(self):
        '''
        Based on weighted random selection, pick a random from the correct list
        :return
        '''
        selection= self.weighted_random_selection()
        if selection == 'vowels':
            result= random.choice(list(self.vowel_dictionary.keys()))
        elif selection == 'consonants':
            result= random.choice(list(self.letter_dictionary.keys()))
        else:
            # Value position of "Y"
            result= 25
        return result

class CHALLENGE(object):
    def __init__(self,challenges,num_gen,letter_gen):
        self.challenges= challenges
        self.letter_wins= 0
        self.number_wins= 0
        self.highest_letter_streak= 0
        self.highest_number_streak= 0
        self.number_generator = num_gen
        self.letter_generator = letter_gen
        self.current_letter_streak= 0
        self.current_number_streak= 0
        self.tie_count= 0

    def compare(self):
        '''
        Determine which is greater
        Increment correct win counter and increment current streak counter
        Check the losers current streak, update if larger, reset it
        '''
        for i in range(self.challenges):
            number_value= self.number_generator.generate()
            letter_value= self.letter_generator.generate()
            if(number_value > letter_value):
                self.number_wins+= 1
                self.current_number_streak+= 1
                if self.current_letter_streak > self.highest_letter_streak:
                    self.highest_letter_streak= self.current_letter_streak
                    self.current_letter_streak= 0
            elif(letter_value > number_value):
                self.letter_wins+= 1
                self.current_letter_streak+= 1
                if self.current_number_streak > self.highest_number_streak:
                    self.highest_number_streak= self.current_number_streak
                    self.current_number_streak= 0
            else:
                # its a tie, end streaks
                # TODO Find out what else to do
                self.tie_count+= 1
                if self.current_number_streak > self.highest_number_streak:
                    self.highest_number_streak= self.current_number_streak
                    self.current_number_streak= 0
                if self.current_letter_streak > self.highest_letter_streak:
                    self.highest_letter_streak= self.current_letter_streak
                    self.current_letter_streak= 0

    def output_json(self):
        s = '{"letters": {"wins": %d, "streak": %d}, "numbers": {"wins": %d, "streak": %d} }' \
            % (self.letter_wins,self.highest_letter_streak,self.number_wins,self.highest_number_streak)
        d = json.loads(s)
        print json.dumps(d)

def main():

    a_number = NUMBERS(args.prime_likelihood)
    a_letter = LETTERS(args.vowels_likelihood)
    a_challenge = CHALLENGE(args.num_challenges,a_number,a_letter)
    a_challenge.compare()
    a_challenge.output_json()


if __name__ == '__main__':

    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("num_challenges", type=int, default=0,help = "The number of challenges, default= 0")
    arg_parser.add_argument("prime_likelihood",type=int, help = "Number of time more likelihood of prime number, default= 0")
    arg_parser.add_argument("vowels_likelihood", type=int, default=sys.stdout, help = "Number of times more likelihood of vowels, default=0")

    args = arg_parser.parse_args()

    if args.num_challenges == 0:
        sys.exit("No challenges to process")

    if args.prime_likelihood < 0:
        sys.exit("prime_liklihood needs to be a positive integer")

    if args.vowels_likelihood < 0:
        sys.exit("vowel liklihood needs to be a positive integer")

    main()
