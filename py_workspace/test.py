"""
Written By: Lam Xin Yi, Jeslyn / Olichuuwon
Date: 30/08/2021
For: CZ2001 Algorithm Module
Intro: Test Function
"""

import boyer_moore
import brute_force


def test():
    """
    test function to check and ensure that the search is generating correct outputs
    works quick for easy debugging
    for brute force and boyer moore only
    :return: nil
    """
    query = "abc"
    genome = "abababababababababababababcabababababcabcabcabababababca"
    expected_results = [24, 35, 38, 41, 52]
    bf = brute_force.BruteForce(query)
    bm = boyer_moore.BoyerMoore(query)
    bf_result = bf.search(genome)
    bm_result = bm.search(genome)
    assert bf_result[0] == expected_results
    assert bm_result[0] == expected_results


def main():
    test()


if __name__ == "__main__":
    main()
