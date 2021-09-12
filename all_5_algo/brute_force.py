"""
Written By: Lam Xin Yi, Jeslyn / Olichuuwon
Date: 30/08/2021
For: CZ2001 Algorithm Module
Intro: BruteForce Class
To Test: Run test.py
"""


class BruteForce:
    def __init__(self, query_sequence):
        """
        constructor
        :param query_sequence: the sequence that you are looking for
        """
        self.buffer_size = len(query_sequence)
        self.query_sequence = query_sequence

    def search(self, genome_sequence):
        """
        find occurrences where query sequence matches genome sequence,
        and append index where match is found in the matches list,
        returns an empty list if there is no matches found
        :param genome_sequence: the string to be searched
        :return: matches - a list of matches
                 buffer_for_last_few_chars - a string of the last few chars in genome_sequence
        """
        if not genome_sequence or not self.query_sequence:
            return None

        matches = []
        len_query = len(self.query_sequence)
        len_genome = len(genome_sequence)
        if len_genome <= len_query:
            return matches, genome_sequence[-self.buffer_size:]

        for genome_index in range(1 + (len_genome - len_query)):
            match = True
            for query_index in range(len_query):
                if genome_sequence[genome_index + query_index] != self.query_sequence[query_index]:
                    match = False
                    break
            if match:
                matches.append(genome_index)
        return matches, genome_sequence[-self.buffer_size:]  # buffer of last few chunks
