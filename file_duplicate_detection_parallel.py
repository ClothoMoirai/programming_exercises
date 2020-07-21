#!/usr/bin/python3
# This came from a live-coding interview which I bombed and decided to use as a learning experience.
# None of this is code from the interview; that was via CoderPad and ended before I could grab a copy.
# From memory of the assignment: given a starting path find duplicate files in that directory and subdirectories.

import hashlib
import os
from typing import List
from multiprocessing import Pool
from collections import defaultdict

# Depending on usage it can be useful to exclude directories that are expected to change rapidly
exclude_dirs = ['.cache', '.config']
# temporary hardcoding during development
basedir = '~/test'
# blocksize for hashing
blocksize = 65536
# Hash algorithm desired
hash_algo = 'sha512'
# Number of parallel threads/processes for hashing
parallel = 8


def islink(filename: str) -> bool:
    return os.path.islink(filename)


def isfile(filename: str) -> bool:
    # for this purpose we want to exclude links.
    return os.path.isfile(filename) and not islink(filename)


def isdir(filename: str) -> bool:
    # for this purpose we want to exclude links.
    return os.path.isdir(filename) and not islink(filename)


def get_file_stats(filename: str) -> dict:
    # Return a dict with the filename, size and, if there are multiple links, the hardlinks
    stat_dict = {'filename': filename}
    this_file_stat = os.stat(filename)
    stat_dict['size'] = this_file_stat.st_size
    if this_file_stat.st_nlink > 1:
        stat_dict['hardlinks'] = this_file_stat.st_ino
    return stat_dict


def generate_file_list(path: str) -> List[str]:
    files_list = []
    for this_path, these_dirs, these_files in os.walk(path, followlinks=False):
        these_dirs[:] = [d for d in these_dirs if d not in exclude_dirs]
        for this_file in these_files:
            if isfile(this_path + '/' + this_file):
                files_list.append(this_path + '/' + this_file)
    return files_list


def concatonate_stat_dicts(stat_dict_list: List[dict]) -> dict:
    return_stats_dict = {'size': defaultdict(list), 'hardlinks': defaultdict(list)}
    for this_file_dict in stat_dict_list:
        return_stats_dict['size'][this_file_dict['size']].append(this_file_dict['filename'])
        if 'hardlinks' in this_file_dict:
            return_stats_dict['hardlinks'][this_file_dict['hardlinks']].append(this_file_dict['filename'])
    return return_stats_dict


def run_file_stats(file_list: List[str]) -> dict:
    # Multiprocessing this doesn't gain much; about 0.5-1 second in my testing.
    # files_dict = {'size': {}, 'hardlinks': {}}
    # for this_file in file_list:
    #     stats_dict = get_file_stats(this_file)
    #     if not stats_dict['size'] in files_dict['size']:
    #         files_dict['size'][stats_dict['size']] = [this_file]
    #     else:
    #         files_dict['size'][stats_dict['size']].append(this_file)
    #     if 'hardlinks' in stats_dict:
    #         if not stats_dict['hardlinks'] in files_dict['hardlinks']:
    #             files_dict['hardlinks'][stats_dict['hardlinks']] = [this_file]
    #         else:
    #             files_dict['hardlinks'][stats_dict['hardlinks']].append(this_file)
    stats_pool = Pool(processes=parallel)
    file_stats_list = stats_pool.map(get_file_stats, file_list)
    files_dict = concatonate_stat_dicts(file_stats_list)
    return files_dict


def scan_directory(path: str) -> dict:
    files_list = generate_file_list(path)
    files_dict = run_file_stats(files_list)
    return files_dict


def clear_single_entries(sub_dict: dict) -> dict:
    return {k: v for k, v in sub_dict.items() if len(v) > 1}


def dict_values_to_list(source_dict: dict) -> List[List[str]]:
    return [v for v in source_dict.values() if len(v) > 1]


def clean_stat_dict(files_dict: dict) -> dict:
    # clean up the data before returning
    files_dict['size'] = clear_single_entries(files_dict['size'])
    files_dict['hardlinks'] = dict_values_to_list(files_dict['hardlinks'])
    return files_dict


# noinspection SpellCheckingInspection
def hash_this_file(this_file: str) -> dict:
    with open(this_file, 'rb') as read_this_file:
        hasher = hashlib.new(hash_algo)
        for my_buffer in iter(read_this_file.read, b''):
            hasher.update(my_buffer)
    return {hasher.hexdigest(): this_file}


def get_file_hashes(file_size_dict: dict) -> dict:
    file_hashes_dict = defaultdict(list)
    hash_file_list = []
    for file_list in file_size_dict.values():
        for this_file in file_list:
            if os.access(this_file, os.R_OK):
                hash_file_list.append(this_file)
    # If you want single-thread
    # for this_file in hash_file_list:
    #     this_hash_dict = hash_this_file(this_file)
    #     for key in this_hash_dict:
    #         file_hashes_dict[key].append(this_hash_dict[key])
    mypool = Pool(processes=parallel)
    list_of_dicts = mypool.map(hash_this_file, hash_file_list)
    mypool.close()
    for this_dict in list_of_dicts:
        for key in this_dict:
            file_hashes_dict[key].append(this_dict[key])
    return file_hashes_dict


def get_duplicate_files(sub_dict: dict) -> List[List[str]]:
    sub_dict = get_file_hashes(sub_dict)
    return dict_values_to_list(clear_single_entries(sub_dict))


def main(mydir: str) -> dict:
    mydir = os.path.expanduser(mydir)  # gets the absolute path if given in a form like ~/mydir
    if isdir(mydir):
        dup_dict = clean_stat_dict(scan_directory(mydir))
        dup_dict['duplicates'] = get_duplicate_files(dup_dict['size'])
        dup_dict.pop('size')
        return dup_dict
    else:
        print('{} is not a directory.'.format(mydir))
        return {'error': '{} is not a directory.'.format(mydir)}


main(basedir)
