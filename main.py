#!/usr/bin/python3
"""
This module does following things:
* Extract projects from zipfile in directory specified in configuration.
* Execute catkin_make in catkin_ws
* Execute rospack command in catkin_ws

"""
import logging
import re
import subprocess
import zipfile

from config import *


logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
# format="%(asctime)s %(levelname)s %(threadName)s %(name)s %(message)s"
logger = logging.getLogger(__name__)


def extract_projects(zipfilename):
    """
    Extract zipped projects from zipfile to catkin_ws. If the directory has files already then skip.
    :param zipfilename:
    :return:
    """
    ws_file_count = len(os.listdir(path=catkin_ws))
    if ws_file_count > 2:
        logger.warning(f'{catkin_ws} has {ws_file_count} entries. For extraction it has to be empty besides '
                       f'"{supplemental_dir}" directory and CMake file. No extraction is executed.')
        return
    else:
        logger.info(f'Extraction of projects from {zipfilename} is executing...')

    if not zipfile.is_zipfile(zipfilename):
        raise TypeError(f"{zipfilename} is not a zip file.")

    good_files = 0
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
            target_path = os.path.join(catkin_ws, os.path.splitext(filename)[0])
            # target_path = catkin_ws  # this is more correct but students may not include directory.
            with source:
                try:
                    internal_zipfile = zipfile.ZipFile(source)
                    internal_zipfile.extractall(path=target_path)
                    good_files += 1
                except zipfile.BadZipFile as e:
                    logger.error(f"{member} cannot be extracted. This file has to be checked manually")
                logger.debug(f"Extracting internal zip {source=} {internal_zipfile=}")
        logger.info(f"Extracted {good_files} projects.")


def catkin_make():
    """
    Execute catkin_make command in catkin_ws.
    :return: success
    """
    p = os.path.normpath(f"{catkin_ws}/..")
    logger.info(f"executing catkin_make in {p}")
    try:
        sub = subprocess.run([catkin_command], shell=True, cwd=p, capture_output=True, check=True, universal_newlines=True)
    except subprocess.CalledProcessError as e:
        logger.error(e.stderr)
        logger.error("catkin_make failed.")
        return False
    logger.info(sub.stdout)
    logger.info("catkin_make succeeded.")
    return True


def rospack():
    """
    Execute rospack profile command in caktin_ws,
    :return: success
    """
    p = os.path.normpath(f"{catkin_ws}/..")
    logger.info(f"executing  rospack profile  in {p}")
    try:
        sub = subprocess.run([rospack_command], shell=True, cwd=p, capture_output=True, check=True, universal_newlines=True)
    except subprocess.CalledProcessError as e:
        logger.error(e.stderr)
        logger.error("rospack profile failed.")
        return False
    logger.info(sub.stdout)
    logger.info("rospack profile succeeded.")
    return True


def rename_files_to_latin(files_path):
    # TODO: make this latin stuff
    s = os.listdir(files_path)
    for e in s:
        # extract_zipfile_to_path(f"{files_path}/{e}")
        logger.info(e)
        # traverse_zipfile(f"{files_path}/{e}")
        break
        # normal = unicodedata.normalize('NFKD', e[1]).encode('ASCII', 'ignore')


def main():
    dirlist = os.listdir(homework_bundle_path)
    project_file = None
    for filename in dirlist:
        extension = os.path.splitext(filename)[-1]
        if extension == '.zip':
            project_file = filename
            break
    if not project_file:
        logger.error(f"No zip file found in {homework_bundle_path}.")
    extract_projects(f"{homework_bundle_path}/{project_file}")
    if not catkin_make():
        return
    rospack()


if __name__ == "__main__":
    main()

"""
students submit work on moodle on Monday evening
a grader downloads zip with all folders --> extracts to catkin_ws/src

* rename to latin
OK 'catkin_make' all student packages --> check for conflicts (bad package names, missing libraries, etc)
OK 'rospack profile' to crawl through the packages and update package list
OK run script to recursively run/launch (depending on each week's assignment) each student's work --> visually check for errors/exceptions/etc
OK manually ctrl+c (or somehow trigger SIGINT in script) to skip to next submission
get list of submissions that failed to run
inform students who need to fix and resubmit within one(?) day
anonymize packages (remove names/emails from package.xml etc) and forward to students for grading.
"""
