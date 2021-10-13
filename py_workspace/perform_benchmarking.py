"""
Written By: Lam Xin Yi, Jeslyn / Olichuuwon
Date: 03/09/2021
For: CZ2001 Algorithm Module
Intro: This is where i create a short snippet to be able to quickly
Generate dataframes for analysis
Dataframes are converted to csv
Csv can be parsed into ipynb files for graphical analysis
"""

import random
import time
from random import randrange

import boyer_moore
import brute_force
import knuth_morris
import pandas as pd
import perform_search

DEFAULT_LIST = [
    "AAAAAAAAAA", "AAAAAAAAAB", "AAAAAAAABB", "AAAAAAABBB", "AAAAAABBBB",
    "AAAAABBBBB", "AAAABBBBBB", "AAABBBBBBB", "AABBBBBBBB", "ABBBBBBBBB",
    "ABABABABAB", "ABCABCABCA", "ABCDABCDAB", "ABCDEABCDE", "ABCDEFABCD",
    "ABCDEFGABC", "ABCDEFGHAB", "ABCDEFGHIA", "ABCDEFGHIJ",
    "ACGTACGTACGT", "AACCGGTTAACCGGTT", "AAAGGGCCCTTT", "AAAAGGGGCCCCTTT",
    "AAACAAAAGAAATAAACAAA", "ACGACGACGACG", "ACACACACACAC", "ACCACCACCACC",
    "ACCCACCCACCC", "ACCCCACCCCAC", "ACCCCCACCCCA", "ACCCCCCACCCC",
    "ACCCCCCCACCC", "ACCCCCCCCACC", "ACCCCCCCCCAC", "ACCCCCCCCCCA"
]


def test_case_generator(default_list):
    """
    function to create more test cases from the default list
    :param default_list: a list of pre designed strings for testing
    :return: a list of generated test cases where duplicates are removed
    """
    reverse_list = []
    final_list = []
    # reverses all the strings
    for string in default_list:
        reverse_list.append(string[::-1])
    long_list = default_list + reverse_list
    # get rids of chars one by one
    for string in long_list:
        final_list.append(string)
        for number in range(1, 10):
            final_list.append(string[:-number])
    # return all the strings created by functions above together with default list
    return sorted(list(set(final_list)))


def insert_query_string_into_genome_string(genome_sequence, query, index):
    """
    inserts query in the genome at a specific index
    :param genome_sequence: genome to search from
    :param query: query to search for
    :param index: index to add the query
    :return: new string created
    """
    return genome_sequence[:index] + query + genome_sequence[index:]


def test_string(query, genome_sequence, algo):
    """
    to perform the test on the string
    :param query: query to search for
    :param genome_sequence: genome to search from
    :param algo: searching algo to use
    :return: time_taken, spawned_position, result
    """
    if algo == "bf":
        algo_obj = brute_force.BruteForce(query)
    elif algo == "bm":
        algo_obj = boyer_moore.BoyerMoore(query)
    elif algo == "kmp":
        algo_obj = knuth_morris.KnuthMorris(query)
    else:
        print("Error occurred!")
        return None
    spawned_position = random.randrange(1, 5000)
    modified_genome_sequence = insert_query_string_into_genome_string(genome_sequence, query, spawned_position)
    start = time.perf_counter()
    result, buffer = algo_obj.search(modified_genome_sequence)
    stop = time.perf_counter()
    time_taken = round(stop - start, 5)
    return time_taken, spawned_position, result


def test_and_create_dataframe(genome_sequence, test_list, algo):
    """
    makes use of the test string function to run repetitive test with generated test list
    :param genome_sequence: genome to search from
    :param test_list: generated test list
    :param algo: searching algo to use
    :return: csv_dataframe which is a dataframe with all the data generated
    """
    csv_columns = ["Query", "Query Length", "Time Taken", "Search Successful", "Position Placed"]
    csv_data = []
    for query in test_list:
        time_taken, spawned_position, result = test_string(query, genome_sequence, algo)
        assert spawned_position in result  # Ensure that artificially added string in successfully found by algorithm
        csv_data.append([query, len(query), time_taken, spawned_position in result, spawned_position])
    csv_dataframe = pd.DataFrame(csv_data, columns=csv_columns)
    return csv_dataframe


def get_all_csv_for_analysis(fna_list, algo_list):
    """
    outputs the results of the searching analysis
    outputs would then assert that the algorithms are implemented properly
    as we force the algorithm to be searched thoroughly by automating it
    :param fna_list:
    :param algo_list:
    :return: nil - generates csv files for analysis
    """
    test_list = test_case_generator(DEFAULT_LIST)
    for fna in fna_list:
        genome_sequence = perform_search.get_file_name_and_returns_string(fna + '.fna')
        if genome_sequence:
            # generate test cases from default list
            for algo in algo_list:
                # test on all algo and create csv files
                print("get_all_csv_for_analysis:", fna, algo)
                csv_dataframe = test_and_create_dataframe(genome_sequence, test_list, algo)
                csv_dataframe.to_csv(fna + "_" + algo + "_searching_analysis.csv")
        else:
            # if fna file does not exist
            print("Invalid fna file!")


def dna_generator(length_to_spawn):
    """
    simple function to generate a random dna sequence
    :param length_to_spawn: the length of dna you want to spawn
    :return: the dna as a string with the length that you want to spawn
    """
    dna_list = []
    pool = ["A", "C", "G", "T"]
    for unit in range(length_to_spawn):
        dna_list.append(pool[randrange(4)])
    return "".join(dna_list)


def test_fixed_query():
    """
    fixed query means query to look for is fixed at 10
    but the size of the genome sequence keeps on increasing from 10 to x
    :return: nil but outputs a csv file named test_fixed_query.csv
    """
    query_string = dna_generator(10)
    csv_columns = ["Genome Size", "BF Time", "BM Time", "KMP Time"]
    csv_data = []
    bf = brute_force.BruteForce(query_string)
    bm = boyer_moore.BoyerMoore(query_string)
    kmp = knuth_morris.KnuthMorris(query_string)
    x = 10000

    for value in range(10, x):
        print("test_fixed_query:", value, "/", x)
        genome_string = dna_generator(value)

        # brute force
        start = time.perf_counter()
        bf.search(genome_string)
        stop = time.perf_counter()
        bf_time_taken = round(stop - start, 5)

        # boyer moore
        start = time.perf_counter()
        bm.search(genome_string)
        stop = time.perf_counter()
        bm_time_taken = round(stop - start, 5)

        # knuth morris
        start = time.perf_counter()
        kmp.search(genome_string)
        stop = time.perf_counter()
        kmp_time_taken = round(stop - start, 5)

        # append data
        csv_data.append([value, bf_time_taken, bm_time_taken, kmp_time_taken])
    csv_dataframe = pd.DataFrame(csv_data, columns=csv_columns)
    csv_dataframe.to_csv("test_fixed_query.csv")


def test_fixed_genome():
    """
    fixed genome means genome to search through - fixed at 100,000
    but the size of the query sequence to look for keeps on increasing from 1 to x
    :return:
    """
    genome_string = dna_generator(100000)
    csv_columns = ["Query Size", "BF Time", "BM Time", "KMP Time"]
    csv_data = []
    x = 1000

    for value in range(1, x):
        print("test_fixed_genome:", value, "/", x)
        query_string = dna_generator(value)
        bf = brute_force.BruteForce(query_string)
        bm = boyer_moore.BoyerMoore(query_string)
        kmp = knuth_morris.KnuthMorris(query_string)

        # brute force
        start = time.perf_counter()
        bf.search(genome_string)
        stop = time.perf_counter()
        bf_time_taken = round(stop - start, 5)

        # boyer moore
        start = time.perf_counter()
        bm.search(genome_string)
        stop = time.perf_counter()
        bm_time_taken = round(stop - start, 5)

        # knuth morris
        start = time.perf_counter()
        kmp.search(genome_string)
        stop = time.perf_counter()
        kmp_time_taken = round(stop - start, 5)

        # append data
        csv_data.append([value, bf_time_taken, bm_time_taken, kmp_time_taken])
    csv_dataframe = pd.DataFrame(csv_data, columns=csv_columns)
    csv_dataframe.to_csv("test_fixed_genome.csv")


def main():
    pass
    # generate csv(s) for searching analysis
    fna_list = ["covid"]  # should be a relatively small fna like the salmonella or the covid one
    algo_list = ["bf", "bm", "kmp"]
    get_all_csv_for_analysis(fna_list, algo_list)

    # generate csv(s) for plotting analysis
    test_fixed_query()
    test_fixed_genome()

    # generate some random dna
    for value in range(1, 100):
        print(dna_generator(value))


if __name__ == "__main__":
    main()
