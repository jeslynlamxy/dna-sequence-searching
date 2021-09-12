"""
Written by: Jeremiah Chan
Edited by: Lam Xin Yi, Jeslyn
Last edited: 07/09/2021

algorithm kmp_search:
    input:
        an array of characters, S (the text to be searched)
        an array of characters, W (the word sought)
    output:
        an array of integers, P (positions in S at which W is found)
        an integer, nP (number of positions)

    define variables:
        an integer, j ← 0 (the position of the current character in S)
        an integer, k ← 0 (the position of the current character in W)
        an array of integers, T (the table, computed elsewhere)

    let nP ← 0

    while j < length(S) do
        if W[k] = S[j] then
            let j ← j + 1
            let k ← k + 1
            if k = length(W) then
                (occurrence found, if only first occurrence is needed, m ← j - k  may be returned here)
                let P[nP] ← j - k, nP ← nP + 1
                let k ← T[k] (T[length(W)] can't be -1)
        else
            let k ← T[k]
            if k < 0 then
                let j ← j + 1
                let k ← k + 1
"""


class KnuthMorris:
    def __init__(self, pat):
        self.pat = pat
        self.buffer_size = len(pat)
        self.pi_table = self.pi_table()

    def pi_table(self):
        pat_len = len(self.pat)
        lng_ps = 0  # longest prefix suffix

        # generate the array based on the length of the search string
        lps_arr = [0] * pat_len
        lps_arr[0] = 0  # first element is always 0
        i = 1  # because first element is always 0, we start from 1

        while i < pat_len:
            # a match is found
            if self.pat[i] == self.pat[lng_ps]:
                lng_ps += 1
                # we store the occurrence where it is found
                lps_arr[i] = lng_ps
                i += 1

            # mismatch
            else:

                # have occurrence before
                if lng_ps != 0:
                    # we move back the longest prefix suffix counter to start the check again
                    # this will continue until we end up with a match OR the counter is reset to 0
                    lng_ps = lps_arr[lng_ps - 1]

                # no occurrence before
                else:
                    # just set the occurrence to 0 and move on
                    lps_arr[i] = 0
                    i += 1
        return lps_arr

    def search(self, txt):
        pat_len = len(self.pat)
        txt_len = len(txt)
        pat_idx = 0  # iterator for the pattern
        txt_idx = 0  # iterator for the text we are searching
        found = []

        # start searching
        while txt_idx < txt_len:

            # found a match
            if self.pat[pat_idx] == txt[txt_idx]:
                txt_idx += 1
                pat_idx += 1

            # found an exact match
            if pat_idx == pat_len:
                found.append(txt_idx - pat_idx)
                pat_idx = self.pi_table[pat_idx - 1]

            # mismatch
            elif txt_idx < txt_len and self.pat[pat_idx] != txt[txt_idx]:

                # in the event of a mismatch, we will traverse the pi table until it finds a match OR it goes back to 0
                # this is the same as when computing the pi table
                if pat_idx != 0:
                    pat_idx = self.pi_table[pat_idx - 1]
                else:
                    # in this case, we know that this part is a goner so we move on
                    txt_idx += 1

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
