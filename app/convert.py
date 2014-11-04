#!/usr/bin/env python
"""
Authors: Alex Gerstein, Scott Gladstone, Vikram Narayan
CS 73 Final Project: Write Like Hemingway

Pseudocode:
1. Read in a corpus X from author (e.g. Hemingway)
2. For each word w in corpus X:
3.    Increment count of w in dict thesaurus
4.    Look up all synonyms of w in WordNet
5.    Map all synonyms of w to thesaurus[w]
6. Read in a user input Y
7. For each word y in input Y:
8.    If y is in thesarus:
9.        Use pdf to map y --> synonym(y)

Input:
    (1) Tokenized corpus file at 'corpus/author.txt'

Output:

Description:

Parameters:

Enhancements:

"""

import os
import re
from collections import defaultdict, Counter

THESAURI_FOLDER = "thesauri"

from nltk.tokenize import RegexpTokenizer
import random
import string


class WriteLike:
    def __init__(self, author, debug=False):
        self.author = author
        self.debug = debug
        self.thesaurus = self._read_thesaurus()

    def _read_thesaurus(self):
        current_path = os.path.dirname(os.path.abspath(__file__))
        filename = current_path + "/static" + "/" + THESAURI_FOLDER + "/" + self.author + ".thes"

        thesaurus = defaultdict(lambda: Counter())

        with open(filename, 'r') as f:
            for line in f:
                if not re.match('^[\s]', line):
                    dict_key = line.strip()
                    current_word = thesaurus[dict_key]
                else:
                    syn, count = line.strip().split()
                    current_word.update({syn: int(count)})
        return thesaurus

    def style_convert_file(self, infile, outfile):
        """ For each word in input text, look up synonyms in the
            author's thesaurus and probabilistically select a
            replacement word. Write output to outfile. """

        source = open("input/" + infile + ".txt", 'r')
        dest = open("output/" + outfile + ".out", 'w')
        first_write = True

        # Tokenize full input file by spaces + punctuation
        tokenizer = RegexpTokenizer('\w+|\$[\d\.]+|\S+')
        text = tokenizer.tokenize(source.read())

        if self.debug:
            print "text: ", text

        for word in text:
            orig_word = word  # preserve capitalization
            word = word.strip().lower()
            # Reject non-ASCII characters
            try:
                word = word.decode('ascii')
            except (UnicodeDecodeError,UnicodeEncodeError):
                continue

            if self.debug:
                print
                print word, "\t-->\t", self.thesaurus[word]

            # Check if word is in thesaurus: copy word exactly if not, replace if yes
            if len(self.thesaurus[word]) == 0:
                # Word not in thesaurus, so copy original word
                if first_write:
                    dest.write(orig_word)
                    first_write = False
                else:
                    dest.write(" " + orig_word)

            else:
                # Probabilistically choose a synonym in thesaurus[word]
                weighted_key = self._weighted_choice(word)
                # Make replaced word uppercase if original word was uppercase
                if orig_word[0].isupper():
                    weighted_key = weighted_key.title()

                # Write to output file
                if first_write:
                    dest.write(weighted_key)
                    first_write = False
                else:
                    # Don't add a space when printing punctuation
                    if word in string.punctuation:
                        dest.write(orig_word)
                    else:
                        dest.write(" " + weighted_key)

        source.close()
        dest.close()

        return outfile

    def style_convert_string(self, input_text):
        """ For each word in input text, look up synonyms in the
            author's thesaurus and probabilistically select a
            replacement word. Return output string. """

        first_write = True

        # Tokenize full input file by spaces + punctuation
        tokenizer = RegexpTokenizer('\w+|\$[\d\.]+|\S+')
        text = tokenizer.tokenize(input_text)
        output = ""

        for word in text:
            orig_word = word  # preserve capitalization
            word = word.strip().lower()
            # Reject non-ASCII characters
            try:
                word = word.decode('ascii')
            except (UnicodeDecodeError, UnicodeEncodeError):
                continue

            # Check if word is in thesaurus: copy word exactly if not, replace if yes
            if len(self.thesaurus[word]) == 0:
                # Word not in thesaurus, so copy original word
                if first_write:
                    output += orig_word
                    first_write = False
                else:
                    output += " " + orig_word

            else:
                # Probabilistically choose a synonym in thesaurus[word]
                weighted_key = self._weighted_choice(word)
                # Make replaced word uppercase if original word was uppercase
                if orig_word[0].isupper():
                    weighted_key = weighted_key.title()

                # Write to output file
                if first_write:
                    output += weighted_key
                    first_write = False
                else:
                    # Don't add a space when printing punctuation
                    if word in string.punctuation:
                        output += orig_word
                    else:
                        output += " " + weighted_key

        return output

    def _weighted_choice(self, word):
        """ Returns a probabilistically-selected synonym for a word.
            Works by randomly choosing a number 'n', iterating through
            synonyms in thesaurus[word] in random order, & decreasing
            'n' by the 'weight' (frequency) of each synonym. """
        # Obtain random normal_pdf weight value from [0, total_weight]
        word_dict = self.thesaurus[word]
        total_weight = sum(word_dict[item] for item in word_dict)
        n = random.uniform(0, total_weight)

        choice = word

        # Randomize word order and select word with weight capturing 'n'
        mix_keys = word_dict.keys()
        random.shuffle(mix_keys)
        for choice in mix_keys:
            weight = word_dict[choice]
            if n < weight:
                return choice
            n = n - weight

        # Return final word as best choice (e.g. tail 'n' value)
        return choice
