import os
import re


def set_path(path):
    # Path can be given in case it is not executing
    # from directory where are the files to be zipped
    if path != '.':
        os.chdir(path)


def is_code(str_number):
    return bool(re.search(r'\d{6}', str_number))


def get_codes(path='.'):
    set_path(path)
    return list(filter(lambda z: is_code(z), map(lambda x: str(
        ''.join(list(filter(lambda y: y.isdigit(), x)))), os.listdir())))


def get_files_with_code(path='.'):
    set_path(path)
    return list(filter(lambda x: is_code(x), os.listdir()))


if __name__ == '__main__':
    print('Students in current folder')
    print('\n'.join(get_codes()))
    print('Files with code in current folder')
    print('\n'.join(get_files_with_code()))
