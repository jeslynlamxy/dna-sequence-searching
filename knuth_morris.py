"""
Written by: Jeremiah Chan
"""


class KnuthMorris:
    def __init__(self, pat):
        self.pat = pat
        self.buffer_size = len(pat)
        self.pi_table = self.pi_table()

    def pi_table(self):
        len_pat = len(self.pat)
        table = [0] * (len_pat + 1)
        chars = list(self.pat)
        for i in range(1, len_pat):
            j = table[i + 1]
            while j > 0 and chars[j] is not chars[i]:
                j = table[j]
            if j > 0 or chars[j] == chars[i]:
                table[i + 1] = j + 1
        return table

    def search(self, txt):
        found = []
        j = 0
        for i in range(len(txt)):
            if j < len(self.pat) and txt[i] == self.pat[j]:
                j = j + 1
                if j == len(self.pat):
                    found.append(i - j + 1)
            elif j > 0:
                j = self.pi_table[j]
                i = i - 1  # with for loop
        return found, txt[-self.buffer_size:]


def main():
    query = 'a'
    genome = 'abcabcabcabcdabcde'
    kmp = KnuthMorris(query)
    result = kmp.search(genome)
    print("RESULTS:", result)
    assert result == ([0, 3, 6, 9, 13], 'e')


if __name__ == "__main__":
    main()
