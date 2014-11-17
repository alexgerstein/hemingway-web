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

import nltk
from nltk.wsd import lesk as nltk_lesk

import random
import string
from config import *

from nltk.tokenize import RegexpTokenizer

nltk.data.path.append('./nltk_data')

REGEX = "|".join([WORD, PRICE, PUNCTUATION_EXCEPT_HYPHEN])
ADJ, ADJ_SAT, ADV, NOUN, VERB = 'a', 's', 'r', 'n', 'v'

def tokenize_string(line):
    tokenizer = RegexpTokenizer(REGEX)
    return tokenizer.tokenize(line)

def reduce_pos_tagset(ptb_tag):
    """
    Converts Penn Tree bank pos tags to wordnet pos tags.
    """

    if ptb_tag[0] == 'V':
        wn_pos = VERB
    elif ptb_tag[0] == 'N':
        wn_pos = NOUN
    elif ptb_tag[0] == 'J':
        wn_pos = ADJ
    elif ptb_tag[0] == 'R':
        wn_pos = ADV
    else:
        wn_pos = None

    return wn_pos


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


    def style_convert_string(self, input_text):
        """ For each word in input text, look up synonyms in the
            author's thesaurus and probabilistically select a
            replacement word. Write output to outfile. """

        text = tokenize_string(input_text)
        output = ""

        tagged_tuples = nltk.pos_tag(text)

        tagged_string = '' # tagged string
        untagged_string = '' # normal string
        for word, tag in tagged_tuples:
            untagged_string += word + ' '
            tagged_string += word + '_' + tag + ' '

        for index, tagged_tuple in enumerate(tagged_tuples):

            orig_word, temp_pos = tagged_tuple

            word = orig_word.strip().lower()
            was_title = orig_word.istitle()        # "Title"
            was_capitalized = orig_word.isupper()  # "UPPER"
            was_lower = orig_word.islower()        # "lower"

            # Don't replace determinants
            if temp_pos == u'DT':
                weighted_key = word
            else:      
                # converts penn tree bank parts of speech to wordnet parts of speech
                wordnet_pos = reduce_pos_tagset(temp_pos)
                if wordnet_pos:
                    synset = nltk_lesk(untagged_string, orig_word.strip().lower(), wordnet_pos)
                else:
                    synset = nltk_lesk(untagged_string, orig_word.strip().lower())

                # Probabilistically choose a synonym in thesaurus[synset]
                weighted_key = self._weighted_choice_lesk(str(synset), word)

            # Match capitalization of original word
            if was_title:
                weighted_key = weighted_key.title()
            elif was_capitalized:
                weighted_key = weighted_key.upper()
            elif not was_lower: 
                weighted_key = orig_word

            # Add a space between words, no space for punctuation
            if word not in string.punctuation and index != 0: 
                output += " "

            output += weighted_key

        return output

    def _weighted_choice_lesk(self, synset, orig_word):
        """
        Returns a probabilistically-selected synonym for a word.

        Works by randomly choosing a number 'n', iterating through
        synonyms in thesaurus[word] in random order, & decreasing
        'n' by the 'weight' (frequency) of each synonym.
        """
        if not synset or synset not in self.thesaurus:
            return self._weighted_choice(orig_word) 

        # Obtain random normal_pdf weight value from [0, total_weight]
        word_dict = self.thesaurus[synset]
        total_weight = sum(word_dict[item] for item in word_dict)
        n = random.uniform(0, total_weight)

        # Randomize word order and select word with weight capturing 'n'
        mix_keys = word_dict.keys()
        random.shuffle(mix_keys)
        for choice in mix_keys:
            weight = word_dict[choice]
            if n < weight:
                return choice
            n = n - weight

        # Return final word as best choice (e.g. tail 'n' value)
        return mix_keys[-1]

    def _weighted_choice(self, word):
        """
        Returns a probabilistically-selected synonym for a word.

        Works by randomly choosing a number 'n', iterating through
        synonyms in thesaurus[word] in random order, & decreasing
        'n' by the 'weight' (frequency) of each synonym.
        """
        if word not in self.thesaurus:
            return word

        # Obtain random normal_pdf weight value from [0, total_weight]
        word_dict = self.thesaurus[word]
        total_weight = sum(word_dict[item] for item in word_dict)
        n = random.uniform(0, total_weight)

        # Randomize word order and select word with weight capturing 'n'
        mix_keys = word_dict.keys()
        random.shuffle(mix_keys)
        for choice in mix_keys:
            weight = word_dict[choice]
            if n < weight:
                return choice
            n = n - weight

        # Return final word as best choice (e.g. tail 'n' value)
        return mix_keys[-1]
