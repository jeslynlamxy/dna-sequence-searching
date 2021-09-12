"""
Written by Jeremiah Chan
Written by: Jeremiah Chan
Edited by: Lam Xin Yi, Jeslyn
Last edited: 07/09/2021

function RabinKarp(string s[1..n], string pattern[1..m])
    hatter := hash(pattern[1..m]);
    for i from 1 to n-m+1
        hs := hash(s[i..i+m-1])
        if hs = hatter
            if s[i..i+m-1] = pattern[1..m]
                return i
    return not found
"""

import string


class RabinKarp:

    def __init__(self, search_string):
        self.small_letters = list(string.ascii_lowercase)
        self.big_letters = list(string.ascii_uppercase)
        self.digits = list(string.digits)
        self.punctuation = list(string.punctuation)
        self.space = list(string.whitespace)
        self.for_hashing = self.small_letters + self.big_letters + self.digits + self.punctuation + self.space
        self.v = self.for_hashing
        self.search_string = search_string
        self.ssHash = self.hash_generator(search_string)

    def hash_generator(self, hash_string):
        # function for generating hash

        pos = len(hash_string) - 1
        hashed = 0

        for c in hash_string:
            # hash generation formula ->  c * a ^ k - 1
            # c -> value of character
            # a  -> constant of our choice (for our case we based it off the length of the genome alphabet list)
            # k -> position of that character in the string

            hashed += (self.v.index(c) + 1) * (4 ** pos)
            pos -= 1

        # we modulo it by a prime n.o (3 in our case) to keep the hash small, easier to deal with
        hashed = hashed % 3

        return hashed

    def rolling_hash_generator(self, hashed, lfc, rgc, max_pos):
        # function for generating rolling hash

        # formula for generating rolling hash -> ((h - l) * 10  + r ) % 3
        # h -> the current hash
        # l -> the character that is currently is current at the starting position of the string (or leftmost character)
        # r -> the new character that we want to add in (or rightmost character)
        # multiply by 10 to 'increase' the base of the existing characters in the hash
        # modulo the hash to make it easier to deal with

        max_pos -= 1
        left_char = (self.v.index(lfc) + 1) * (4 ** max_pos)
        right_char = (self.v.index(rgc) + 1) * (4 ** 0)
        hashed = (((hashed - left_char) * 10) + right_char) % 3

        return hashed

    def search(self, text):
        found = []
        ss_length = len(self.search_string)
        txt_length = len(text)
        ss_hash = self.ssHash
        t_string = ''

        # generate hash of first window
        for h in range(0, ss_length):
            t_string += text[h]

        r_hash = self.hash_generator(t_string)

        # rolling hash generation + check
        for idx in range(txt_length - ss_length + 1):

            # check if the hash matches up with the search before we move on
            if ss_hash == r_hash:
                matched = 0
                # check characters 1 by 1 to prevent false positive
                for c in range(0, ss_length):
                    if self.search_string[c] != text[idx + c]:
                        break
                    else:
                        matched += 1

                    if matched == ss_length:
                        found.append(idx)

            # left most (character we want to remove) would be the current index
            # right most (character we want to add) would be current index + length of search string
            if idx < txt_length - ss_length:
                r_hash = self.rolling_hash_generator(
                    r_hash, text[idx], text[idx + ss_length], ss_length)

        return found, self.search_string[-len(text):]


def main():
    rbk = RabinKarp("AAC")
    print(rbk.search('ABABABABAAC'))


if __name__ == "__main__":
    main()
