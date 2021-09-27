#!/usr/bin/python3
import logging
import re
import subprocess
import zipfile

from config import *

command = "ros launch $$/launch"

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def extract_zipfile_to_path(file_path):
    if not zipfile.is_zipfile(file_path):
        raise TypeError(f"{file_path} is not a zip file.")
    logger.debug(f"Extracting zip file {homework_bundle_path} to path {catkin_ws}")
    z = zipfile.ZipFile(file_path)
    z.extractall(path=catkin_ws)


def extract_projects(zipfilename):
    # TODO: check if only supplemental exists.
    ws_file_count = len(os.listdir(path=catkin_ws))
    if ws_file_count != 1:
        logger.warning(f'catkin_ws has {ws_file_count} entries. For extraction it has to be empty besides '
                       f'"{supplemental_dir}" directory. No extraction is executed.')
        return
    else:
        logger.info(f'Extraction of projects from {zipfilename} is executing...')

    if not zipfile.is_zipfile(zipfilename):
        raise TypeError(f"{zipfilename} is not a zip file.")
    # z = zipfile.ZipFile(zipfilename)
    # files = z.filelist
    # correct_list = []
    with zipfile.ZipFile(zipfilename) as zip_file:
        for member in zip_file.namelist():
            filename = os.path.basename(member)
            # skip directories
            if not re.fullmatch(r'.*\.zip$', filename):
                logger.warning(f"{filename} inf file {zip_file.filename} not matching what should be correct format. "
                               f"Not extracting it! This file has to be checked manually.")
                continue
            if not filename:
                logger.warning(f"{filename} file not existing! Not extracting it! "
                               f"This file has to be checked manually.")

            # copy file (taken from zipfile's extract)
            source = zip_file.open(member)
            # target = open(os.path.join(catkin_ws, filename), "wb")
            target_path = os.path.join(catkin_ws, os.path.splitext(filename)[0])
            # target_path = catkin_ws  # this is more correct but students may not include directory.
            with source:
                try:
                    internal_zipfile = zipfile.ZipFile(source)
                    internal_zipfile.extractall(path=target_path)
                except zipfile.BadZipFile as e:
                    logger.error(f"{member} cannot be extracted. Has to be checked manually")
                # shutil.copyfileobj(source, target)
                logger.debug(f"Extracting internal zip {source=} {internal_zipfile=}")
    """
    for file in files:
        if not re.fullmatch(r'.*\.zip$', file.filename):
            logger.warning(f"{file.filename} not matching what should be correct format. Not extracting it! 
            This file has to be checked manually.")
        else:
            correct_list.append(file.filename)
    for f in correct_list:
        z.extract(f, path=catkin_ws)
    return None
    """


# TODO: execute the shit.
# TODO: if directory isn't empty except supplementary, say it, skip extraction and continue with execution.


def catkin_make():
    p = os.path.normpath(f"{catkin_ws}/..")
    logger.info(f"executing catkin_make in {p}")

    sub = subprocess.run([catkin_command], shell=True, cwd=p, capture_output=True, check=True)
    logger.info(f"{sub=} {p=}")

def rospack():
    p = os.path.normpath(f"{catkin_ws}/..")
    logger.info(f"executing catkin_make in {p}")

    sub = subprocess.run([rospack_command], shell=True, cwd=p, capture_output=True, check=True)
    logger.info(f"{sub=} {p=}")


# os.system(f"cd {catkin_ws} && catkin_make")

def rename_files_to_latin(files_path):
    # TODO: make this latin stuff
    s = os.listdir(files_path)
    for e in s:
        # extract_zipfile_to_path(f"{files_path}/{e}")
        logger.info(e)
        # traverse_zipfile(f"{files_path}/{e}")
        break
        # normal = unicodedata.normalize('NFKD', e[1]).encode('ASCII', 'ignore')
        print(e)


def main():
    s = os.listdir(homework_bundle_path)
    for e in s:
        # extract_zipfile_to_path(f"{files_path}/{e}")
        extract_projects(f"{homework_bundle_path}/{e}")
        logger.info("Executing catkin_make. NOT IMPLEMENTED YET.")
        # catkin_make()
        break
        return
        # rename_files_to_latin(files_path)
        # print(files_path)

        answer = ["y", "Y", "n", "N"]
        v = "_"
        while v not in answer:
            break
            v = input("Did it work (y/n)?")


if __name__ == "__main__":
    main()

"""
students submit work on moodle on Monday evening
a grader downloads zip with all folders --> extracts to catkin_ws/src

* rename to latin
'catkin_make' all student packages --> check for conflicts (bad package names, missing libraries, etc)
'rospack profile' to crawl through the packages and update package list
run script to recursively run/launch (depending on each week's assignment) each student's work --> visually check for errors/exceptions/etc
manually ctrl+c (or somehow trigger SIGINT in script) to skip to next submission
get list of submissions that failed to run
inform students who need to fix and resubmit within one(?) day
anonymize packages (remove names/emails from package.xml etc) and forward to students for grading.
"""
