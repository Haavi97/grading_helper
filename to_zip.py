import os
import shutil
from tqdm import tqdm

from get_codes import get_files_with_code


def zip_student_folders(path='.'):
    # Path can be given in case it is not executing 
	# from directory where are the files to be zipped
    if path != '.':
        os.chdir(path)
    # calling function to get all file paths in the directory
    file_paths = tqdm(get_files_with_code())

    # printing the list of all files to be zipped
    print('Following files will be zipped:')
    for file_name in file_paths:
        file_paths.set_description('Compressing: {:<20}'.format(file_name))
        shutil.make_archive(file_name, 'zip', file_name)

    print('All files zipped successfully!')


if __name__ == "__main__":
    zip_student_folders()
