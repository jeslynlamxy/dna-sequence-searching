"""
Written By: Lam Xin Yi, Jeslyn / Olichuuwon
Date: 30/08/2021
For: CZ2001 Algorithm Module
Intro: This is where you can perform searches
Implementation is as below with proper comments to understand the different sections
For testing:
(1)
-q AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA -g covid.fna -a all
(2)
-q AAAAAAAAAAAAAGGGGAAAAAAAAAAAAAAAA -g covid.fna -a all
"""

import argparse
import os
import time

import boyer_moore
import brute_force
import knuth_morris
import rabin_karp
import semi_brute_force
import test

CHUNK_SIZE = 100000000  # 100 megabytes (following github/commercial storage limits)


class Font:
    """
    for adding fancy colours
    """
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    PURPLE = '\033[35m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'


def argparse_manager():
    """
    to manage the inputs and outputs of the program
    prints guide if you do a -h
    for easier usage on the command line
    :return: args.query.upper(), genome_file, args.algo.upper()
    which is the query sequence, genome file and the algo to use
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('-q', '--query',
                        type=str,
                        required=True,
                        help='input the query string to look for in genome sequence, for example: CCCAAATTT')
    parser.add_argument('-g', '--genome',
                        type=str,
                        required=True,
                        help='input the name of the target fna file, for example: target.fna')
    parser.add_argument('-a', '--algo',
                        choices=('all', 'bf', 'bm', 'rk', 'kmp', 'sbf', 'brute', 'boyer', 'rabin', 'knuth', 'semi'),
                        type=str,
                        required=True,
                        help='indicate which of string searching algorithm to use')
    args = parser.parse_args()
    # print(args.query, args.genome, args.type)
    genome_file = args.genome
    while not os.path.isfile(genome_file):
        genome_file = input("Invalid genome file, please re-enter valid fna file: ")
    return args.query.upper(), genome_file, args.algo.upper()


def split_file_into_smaller_chunks_and_remove_newlines(file_name):
    """
    function splits up files into chunks
    chunks would then become new files
    names of files will be appended to the files_created list
    CHUNK_SIZE: dictates the size of the chunks that is created
    :param file_name: name/path of file
    :return: FILES_CREATED: a list consisting of names of new files created
    """
    if not os.path.isfile(file_name):
        return None
    file_number = 1
    files_created = []
    with open(file_name, "r") as f:
        chunk = f.read(CHUNK_SIZE)
        while chunk:
            new_file = str(file_number) + '_' + file_name
            files_created.append(new_file)
            clean_file = ""
            for item in chunk:
                if item != '\n':
                    clean_file += item
            with open(new_file, "w") as chunk_file:
                chunk_file.write(clean_file)
            file_number += 1
            chunk = f.read(CHUNK_SIZE)
    return files_created


def delete_created_files(files_created):
    """
    function deletes the files passed to it
    files have to be in a list
    :param files_created: list of files you want to delete
    :return: nil
    """
    for file in files_created:
        if os.path.exists(file):
            os.remove(file)


def get_file_name_and_returns_string(file_path):
    """
    gets file and reads it
    returns the file as a joined string
    :param file_path: file to be read
    :return: conjoined string of the file parsed in
    """
    if not os.path.isfile(file_path):
        return None
    with open(file_path, "r") as infile:
        file_content = infile.read()
    return file_content


def merge_multiple_files_into_one(list_of_files, new_file_name):
    """
    gets a list of files and outputs a new file with all files in list merged
    essentially creates a file with just one long dna sequence
    :param list_of_files: a list of files to be merged
    :param new_file_name: new file name
    :return: nil but new file will be created
    """
    with open(new_file_name, 'w') as file:
        file.write("")
    for item in list_of_files:
        with open(item, 'r') as file:
            data = file.read()
        with open(new_file_name, 'a') as file:
            file.write(data)


def time_and_return_result(function, obj):
    """
    starts a timer then let a function and obj run
    stop the timer and find out how long it took
    time as chunks
    :param function: the function to be ran
    :param obj: the object to be parsed into the function
    :return: any output given from the function
    """
    start = time.perf_counter()
    result = function(obj)
    stop = time.perf_counter()
    time_taken = stop - start
    to_print = f"COMPLETED IN {time_taken:0.10f} SECONDS"
    print(Font.BOLD + Font.BLUE + to_print + Font.END)
    return result


def perform_search_for_fna_file(algo_object, fna_file):
    """
    performs the search on the fna file for user
    the results will be printed onto the console
    if further processing is needed in the future
    the list of matches is also returned to the caller
    :param algo_object: the object created with the query sequence to be found
    :param fna_file: the file you want to search for the query sequence
    :return: list of matches in the fna file
    """
    buffer = ""
    matches = []
    chunks_created = split_file_into_smaller_chunks_and_remove_newlines(fna_file)
    merge_multiple_files_into_one(chunks_created, "new_" + fna_file)
    for chunk in range(len(chunks_created)):
        genome_string = buffer + get_file_name_and_returns_string(chunks_created[chunk])
        result, buffer = time_and_return_result(algo_object.search, genome_string)
        if result is None:
            break
        if result:
            indexes = []
            for item in result:
                if chunk != 0:
                    indexes.append(item - len(buffer))
                else:
                    indexes.append(item)
            unit = (chunk, chunks_created[chunk], indexes)
            matches.append(unit)
            result_msg = str(len(indexes)) + " MATCHES FOUND AT INDEXES " + str(indexes) + " IN " + str(
                chunks_created[chunk])
            print(Font.BOLD + Font.GREEN + result_msg + Font.END)

    if matches:
        file_sizes = []
        for file_name in chunks_created:
            file_sizes.append(len(get_file_name_and_returns_string(file_name)))

        offset = []
        for chunk, file, indexes in matches:
            prev_chunks = sum(file_sizes[:chunk])
            for index in indexes:
                offset.append(prev_chunks + index)

        success_msg = "TOTAL OF " + str(len(offset)) + " MATCHES FOUND AT INDEXES " + str(offset) + " IN " + fna_file
        print(Font.BOLD + Font.PURPLE + success_msg + Font.END)
        delete_created_files(chunks_created)
        return offset

    else:
        print(Font.BOLD + Font.RED + "NO MATCHES FOUND IN " + fna_file + Font.END)
        delete_created_files(chunks_created)
        return None


def main():
    # handle argparse and prints out values received
    query, genome, algo = argparse_manager()
    print("--- Query sequence to look for:", query)
    print("--- Genome file to search through:", genome)
    print("--- Type of searching algorithm:", algo)

    # creates search objects
    if algo == 'BF' or algo == 'BRUTE':
        bf = brute_force.BruteForce(query)
        bm = None
        rk = None
        kmp = None
        sbf = None
    elif algo == 'BM' or algo == 'BOYER':
        bf = None
        bm = boyer_moore.BoyerMoore(query)
        rk = None
        kmp = None
        sbf = None
    elif algo == 'RK' or algo == 'RABIN':
        bf = None
        bm = None
        rk = rabin_karp.RabinKarp(query)
        kmp = None
        sbf = None
    elif algo == 'KMP' or algo == 'KNUTH':
        bf = None
        bm = None
        rk = None
        kmp = knuth_morris.KnuthMorris(query)
        sbf = None
    elif algo == 'SBF' or algo == 'SEMI':
        bf = None
        bm = None
        rk = None
        kmp = None
        sbf = semi_brute_force.SemiBruteForce(query)
    else:  # all
        bf = brute_force.BruteForce(query)
        bm = boyer_moore.BoyerMoore(query)
        rk = rabin_karp.RabinKarp(query)
        kmp = knuth_morris.KnuthMorris(query)
        sbf = semi_brute_force.SemiBruteForce(query)

    while True:
        # begin search
        if bf:
            print(Font.BOLD + Font.YELLOW + "=== BRUTE FORCE TEST" + Font.END)
            perform_search_for_fna_file(bf, genome)
        if kmp:
            print(Font.BOLD + Font.YELLOW + "=== KNUTH MORRIS TEST" + Font.END)
            perform_search_for_fna_file(kmp, genome)
        if bm:
            print(Font.BOLD + Font.YELLOW + "=== BOYER MOORE TEST" + Font.END)
            perform_search_for_fna_file(bm, genome)
        if rk:
            print(Font.BOLD + Font.YELLOW + "=== RABIN KARP TEST" + Font.END)
            perform_search_for_fna_file(rk, genome)
        if sbf:
            print(Font.BOLD + Font.YELLOW + "=== SEMI BRUTE FORCE TEST" + Font.END)
            perform_search_for_fna_file(sbf, genome)

        # perform next search if needed
        answer = input("Enter 'x' to exit, and 'y' to continue searching: ").upper()

        # manage invalid inputs
        if 'X' in answer:
            break
        if answer != 'Y':
            print("Well, 'y' was not entered, this is y i am terminating!")
            break

        # enter new/modified fna file to be checked, genome will be replaced and searched on again
        genome = input("Enter name of new fna file: ")
        while not os.path.isfile(genome):
            genome = input("Invalid genome file, please re-enter valid fna file: ")

    print("End of program, adios!")


if __name__ == "__main__":
    test.test()
    main()
