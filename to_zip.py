import os
from zipfile import ZipFile
from tqdm import tqdm

from get_codes import get_files_with_code


def zip_student_folders(path='.'):
    # Path can be given in case it is not executing 
	# from directory where are the files to be zipped
    if path != '.':
        os.chdir(path)
    # calling function to get all file paths in the directory
    file_paths = tqdm(os.get_files_with_code())

    # printing the list of all files to be zipped
    print('Following files will be zipped:')
    for file_name in file_paths:
        file_paths.set_description('Compressing: {:<20}'.format(file_name))
        # writing files to a zipfile
        with ZipFile(file_name + '.zip', 'w') as zip:
            # writing each file one by one
            for file in file_paths:
                zip.write(file)

    print('All files zipped successfully!')


if __name__ == "__main__":
    zip_student_folders()
