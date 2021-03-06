#!/usr/bin/env python
__author__ = 'bentanne'

import sys
import argparse
import random
import math
import string
import json



class BASE (object):
    def select(self,container, weights):
        total_weight = float(sum(weights))
        rel_weight = [w / total_weight for w in weights]

        # Probability for each element
        if(self.probs == None):
            self.probs = [sum(rel_weight[:i + 1]) for i in range(len(rel_weight))]

        for (i, element) in enumerate(container):
            if random.random() <= self.probs[i]:
                break

        return element

class NUMBERS (BASE):
    def __init__(self,prime_weight):
        self.primes= []
        self.non_primes= []
        self.squares= []
        self.weight= prime_weight
        self.weighted_array= []
        self.fill_arrays()
        self.current_value=0
        self.probs=None


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

    def generate(self):
        '''
        Based on weighted random selection, pick a random from the correct list
        :return
        '''
        selection= self.select(['prime','square','non_prime'],[self.weight,self.weight/3,1])
        if selection == 'prime':
            self.current_value= random.choice(self.primes)
        elif selection == 'square':
            self.current_value= random.choice(self.squares)
        else:
            self.current_value= random.choice(self.non_primes)
        return self.current_value

class LETTERS(BASE):
    def __init__(self,weight):
        self.letter_dictionary= {}
        self.vowel_dictionary= {}
        self.weight = weight
        self.weighted_array= []
        self.current_value=0
        self.probs=None
        self.vowels= 'a','e','i','o','u'
        self.y_weight=2
        self.fill_dictionary()

    def fill_dictionary(self):

        for i in list(string.ascii_lowercase):
            if(i in self.vowels):
                self.vowel_dictionary.update({string.ascii_lowercase.index(i)+1:i})
            elif(i != 'y'):
                self.letter_dictionary.update({string.ascii_lowercase.index(i)+1:i})

    def generate(self):
        '''
        Based on weighted random selection, pick a random from the correct list
        :return
        '''
        selection= self.select(['vowels','Y','consonants'],[self.weight,self.weight*self.y_weight,1])
        if selection == 'vowels':
            self.current_value= random.choice(list(self.vowel_dictionary.keys()))
        elif selection == 'consonants':
            self.current_value= random.choice(list(self.letter_dictionary.keys()))
        else:
            # Value position of "Y"
            self.current_value= 25
        return self.current_value

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

    if args.num_challenges <= 0:
        sys.exit("No challenges to process")

    if args.prime_likelihood < 0:
        sys.exit("prime_liklihood needs to be a positive integer")

    if args.vowels_likelihood < 0:
        sys.exit("vowel liklihood needs to be a positive integer")

    main()
