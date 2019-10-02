import os
import multiprocessing as mp
from multiprocessing import Pool
import math


class WordCounter:

    def __init__(self, name):
        self.file_name = name
        self.words_counter_map = dict()

    def count(self, word):
        """
        Add one to an existing word in words_counter_map or assign one to a new word.
        :param word: A word
        """
        if not self.search(word):
            self.words_counter_map[word] = 1
        else:
            self.words_counter_map[word] += 1

    def search(self, word):
        """
        Search for a word in the words_counter_map
        :param word: A word
        :return: A boolean that signify the result of the search
        """
        return word in self.words_counter_map


def find_files_paths(directory_path, files_list):
    """
    A recursive function that transverse through the subdirectories in order to find all of the files paths.
    at the end return a list of the files path.
    :param directory_path: The root directory path
    :param files_list: The list which contains the files path.
    :return: return the files_list
    """
    words_directory = os.path.join(directory_path)
    if not os.path.isdir(words_directory):
        return None

    for entry in os.listdir(words_directory):
        entry = os.path.join(directory_path, entry)

        if os.path.isdir(entry):
            find_files_paths(entry, files_list)
        else:
            files_list.append(entry)

    return files_list


def single_file_word_count(file_path):
    """
    Count the words in a single file and store the results in a WordCounter object.
    :param file_path: The file path
    :return: The file name and the map of the words in that file
    """
    file_name = file_path.split('\\')[-1]
    words_counter = WordCounter(file_name)

    with open(file_path, 'r') as f:
        content = f.read()
        # split the words from the initial string
        words = content.splitlines()

        # count the words
        for word in words:
            words_counter.count(word.lower())

    return file_name, words_counter.words_counter_map


def get_num_of_workers(files_number):
    """
    Get the number of processes to create based the minimum number of processors or the number of the files
    :param files_number: The number of the files
    :return: The number of processes that need to be created
    """
    return min(files_number, mp.cpu_count())


def CountTheWordsInFiles(directory_path):
    """
    Given a directory path this function find all of the files path in it. Then create a suitable number of processes
    to count the words at each file.
    :param directory_path: The directory path
    :return: return a dictionary with the file name and the occurrences of words in it.
    """

    # Retrieve the files path in the directory
    files_list = find_files_paths(directory_path, [])

    num_of_files = len(files_list)
    word_count_map = []

    if num_of_files == 0:
        return word_count_map

    # Decide how many processes to create
    workers_number = get_num_of_workers(num_of_files)

    # Compute the chunk size for each process
    chunk_size = math.ceil(num_of_files/workers_number)

    # Create and operate the processes on the files
    with Pool(processes=workers_number) as pool:
        word_count_map = pool.map(single_file_word_count, files_list, chunk_size)

    return word_count_map


def ShowSortedByWordCount(word, word_count_map):
    """
    Sort the files by amount of occurrences of the word in each file.
    :param word: The word to sort by
    :param word_count_map: A dictionary that contain the files name and the words in it.
    :return: A sorted list of the files and the occurrences of the word in them.
    """
    sorted_files = []
    # Transverse on every file in the directory
    for file in word_count_map:
        # Check the word was in the file
        if word in file[1]:
            sorted_files.append((file[0], file[1][word]))
        else:
            sorted_files.append((file[0], 0))

    # Sort
    sorted_files = sorted(sorted_files, key=lambda tup: tup[1])

    return sorted_files


def search_directory(dir_path, word):
    """
    Search the files in the directory for the word.
    :param dir_path: The directory path
    :param word: The word
    :return: A dictionary containing the result -for each file there is the number of times the words occur it the file.
    """
    # Count and map occurrences of any words in the files
    word_count_map = CountTheWordsInFiles(dir_path)

    # Sort the word_count_map by the specific word
    sorted_word_map = ShowSortedByWordCount(word, word_count_map)
    return {'word_map': sorted_word_map}

