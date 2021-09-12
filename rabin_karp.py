"""
Written by Jeremiah Chan
"""

import string


class RabinKarp:

    def __init__(self, searchString):
        self.small_letters = list(string.ascii_lowercase)
        self.big_letters = list(string.ascii_uppercase)
        self.digits = list(string.digits)
        self.punctuation = list(string.punctuation)
        self.space = list(string.whitespace)
        self.for_hashing = self.small_letters + self.big_letters + self.digits + self.punctuation + self.space
        self.v = self.for_hashing
        self.searchString = searchString
        self.ssHash = self.hashGenerator(searchString)

    def hashGenerator(self, hashString):
        # function for generating hash

        pos = len(hashString) - 1
        hash = 0

        for c in hashString:
            # hash generation formula ->  c * a ^ k - 1
            # c -> value of character
            # a  -> constant of our choice (for our case we based it off the length of the genome alphabet list)
            # k -> position of that character in the string

            hash += (self.v.index(c) + 1) * (4 ** pos)
            pos -= 1

        # we modulo it by a prime n.o (3 in our case) to keep the hash small, easier to deal with
        hash = hash % 3

        return hash

    def rollingHashGenerator(self, hash, lfc, rgc, maxPos):
        # function for generating rolling hash

        # formula for generating rolling hash -> ((h - l) * 10  + r ) % 3
        # h -> the current hash
        # l -> the character that is currently is current at the starting position of the string (or leftmost character)
        # r -> the new character that we want to add in (or rightmost character)
        # multiply by 10 to 'increase' the base of the existing characters in the hash
        # modulo the hash to make it easier to deal with

        maxPos -= 1
        lfch = (self.v.index(lfc) + 1) * (4 ** maxPos)
        rgch = (self.v.index(rgc) + 1) * (4 ** 0)
        hash = (((hash - lfch) * 10) + rgch) % 3

        return hash

    def search(self, text):
        found = []
        ssLength = len(self.searchString)
        txtLength = len(text)
        ssHash = self.ssHash
        tString = ''

        # generate hash of first window
        for h in range(0, ssLength):
            tString += text[h]

        rHash = self.hashGenerator(tString)

        # rolling hash generation + check
        for idx in range(txtLength - ssLength + 1):

            # check if the hash matches up with the search before we move on
            if ssHash == rHash:
                matched = 0
                # check characters 1 by 1 to prevent false positive
                for c in range(0, ssLength):
                    if self.searchString[c] != text[idx + c]:
                        break
                    else:
                        matched += 1

                    if matched == ssLength:
                        found.append(idx)

            # left most (character we want to remove) would be the current index
            # right most (character we want to add) would be current index + length of search string
            if idx < txtLength - ssLength:
                rHash = self.rollingHashGenerator(
                    rHash, text[idx], text[idx + ssLength], ssLength)

        return found, self.searchString[-len(text):]


def main():
    rbk = RabinKarp("AAC")
    print(rbk.search('ABABABABAAC'))


if __name__ == "__main__":
    main()
