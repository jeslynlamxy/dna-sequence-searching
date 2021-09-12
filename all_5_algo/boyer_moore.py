"""
Written By: Lam Xin Yi, Jeslyn / Olichuuwon
Date: 30/08/2021
For: CZ2001 Algorithm Module
Intro: BoyerMoore Class
To Test: Run test.py
"""


class BoyerMoore:
    def __init__(self, query_sequence):
        """
        constructor
        :param query_sequence: the sequence that you are looking for
        """
        self.ASCII = 256
        self.buffer_size = len(query_sequence)
        self.query_sequence = query_sequence
        self.last_occurrence = self.generate_bad_char_rule()
        self.border_position, self.shift = self.generate_whole_suffix_rule()
        self.border_position, self.shift = self.generate_partial_suffix_rule()

    def generate_bad_char_rule(self):
        """
        generates the bad char look up table
        it contains an array of all the last occurrences of the char
        in the query sequence
        potato where index goes from 0 at p to 5 at the last 0
        the result would be p=0, o=5, t=4, a=3, the rest of the values would be -1
        :return:
        """
        query_len = len(self.query_sequence)
        last_occurrence = [-1] * self.ASCII
        for number in range(query_len):
            last_occurrence[ord(self.query_sequence[number])] = number
        return last_occurrence

    def generate_whole_suffix_rule(self):
        """
        when the algorithm has some matches, it would make use of those matches
        being the suffix to find out how much the algorithm can be skipped further
        :return: border_position, shift - information with data that would aid in shifting
        """
        query_len = len(self.query_sequence)
        border_position = [0] * (query_len + 1)
        shift = [0] * (query_len + 1)
        i = query_len
        j = query_len + 1
        border_position[i] = j
        while i > 0:
            while j <= query_len and self.query_sequence[i - 1] != self.query_sequence[j - 1]:
                if shift[j] == 0:
                    shift[j] = j - i
                j = border_position[j]
            i -= 1
            j -= 1
            border_position[i] = j
        return border_position, shift

    def generate_partial_suffix_rule(self):
        """
        when the algorithm has some matches, it would make use of those matches
        being the suffix to find out how much the algorithm can be skipped further
        in this function we do not just look at the full suffix but look at the sub
        components in the suffix as well
        :return: border_position, shift - information with data that would aid in shifting
        """
        query_len = len(self.query_sequence)
        j = self.border_position[0]
        for number in range(query_len):
            if self.shift[number] == 0:
                self.shift[number] = j
            if number == j:
                j = self.border_position[j]
        return self.border_position, self.shift

    def search(self, genome_sequence):
        """
        find occurrences where query sequence matches genome sequence,
        and append index where match is found in the matches list,
        returns an empty list if there is no matches found
        :param genome_sequence: the genome sequence you would like to search on
        :return: a list of indexes where the query sequence is found
        """
        result = []

        if not genome_sequence or not self.query_sequence:
            return None

        query_len = len(self.query_sequence)
        genome_len = len(genome_sequence)

        if genome_len < query_len:
            return result, genome_sequence[-self.buffer_size:]

        i = 0
        while i <= (genome_len - query_len):
            j = query_len - 1
            while j >= 0 and self.query_sequence[j] == genome_sequence[i + j]:
                j -= 1
            if j < 0:
                result.append(i)
                i = i + self.shift[0]
            else:
                next_shift = max(self.shift[j + 1], j - self.last_occurrence[ord(genome_sequence[i + j])])
                i = i + next_shift

        return result, genome_sequence[-self.buffer_size:]  # buffer of last few chunks
