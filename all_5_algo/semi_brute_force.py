"""
Written By: He Wan Ru
Edited by: Lam Xin Yi, Jeslyn
Last edited: 07/09/2021

Let i = position of text k = position of pattern j = position of next letters same as pattern first letters
while (i < length of text-length of pattern+1) ← outer loop
 While (half of pattern length >= k) ← inner loop

  if first index of pattern match with text
        If last index of pattern match with text
   k +=1
                            else
   Find the position j for next match of pattern first letter
                  i=i+j
                  Break
  else
         Find the position j for next match of pattern first letter
                  i=i+j
                  Break
          If pattern occur in text record the position
  Record position in record list
          i+=1
"""

import brute_force


class SemiBruteForce:
    def __init__(self, query_sequence):
        """
        constructor
        :param query_sequence: the sequence that you are looking for
        """
        self.query_sequence = query_sequence
        self.buffer_size = len(query_sequence)

    def search(self, genome_sequence):
        """
        find occurrences where query sequence matches genome sequence,
        and append index where match is found in the matches list,
        returns an empty list if there is no matches found
        :param genome_sequence: the string to be searched
        :return: matches - a list of matches
                 buffer_for_last_few_chars - a string of the last few chars in genome_sequence
        """
        result = []
        query_len = len(self.query_sequence)
        if query_len == 1 or query_len == 2:
            bf = brute_force.BruteForce(self.query_sequence)
            result = bf.search(genome_sequence)[0]
        else:
            i = 0
            while i <= (len(genome_sequence) - len(self.query_sequence)):
                j = 0
                k = 0
                while int((len(self.query_sequence) - 1) / 2) != k:
                    if (((self.query_sequence[k]) == (genome_sequence[i + k])) & (
                            (self.query_sequence[len(self.query_sequence) - 1 - k]) == (
                            genome_sequence[i + len(self.query_sequence) - 1 - k]))):
                        k += 1
                    else:
                        for j in range(len(self.query_sequence) - 1):
                            if self.query_sequence[0] == genome_sequence[i + j + 1]:
                                break
                        i = i + j
                        break
                if int((len(self.query_sequence) - 1) / 2) == k:
                    result.append(i)
                i += 1
            if (i <= (len(genome_sequence) - len(self.query_sequence))) & (
                    (genome_sequence[len(genome_sequence) - 1]) == (self.query_sequence[len(self.query_sequence) - 1])):
                result.append(i)
        return result, genome_sequence[-self.buffer_size:]


def main():
    query = 'a'
    genome = 'abcabcabcabcdabcde'
    sbf = SemiBruteForce(query)
    result = sbf.search(genome)
    print("RESULTS:", result)
    assert result == ([0, 3, 6, 9, 13], 'e')


if __name__ == "__main__":
    main()
