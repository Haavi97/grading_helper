"""
This module does traverse projects in catkin_ws and executes command from configuration in them.
Project execution can be terminated using ctr-c hotkey.

..versionchanged::30.09.21
	* Showing package count and current progress.
	* Fixed CMakelist.txt trying to be launched.
	* Print a report in the end.
"""
import logging
import os
import subprocess

from config import *

logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
logger = logging.getLogger(__name__)

good_answers = ["y", "Y"]
possible_answers = good_answers + ["n", "N"]

def main():
    """
    Traverse the "catkin_src" directory from config file for projects and execute 'launch_command' in them.
    While process is running it is safe to terminate it with CTR-C hotkey. The script intercepts it and terminates project.
    :return:
    """
    results = []
    p = [i for i in os.scandir(catkin_ws) if i.is_dir() and i.name != supplemental_dir]
    all_count = len(p)
    for count, i in enumerate(p, start=1):
        # if i == supplemental_dir or not i.is_dir():
        #    continue
        c = launch_command.format(i.name)
        logger.debug(f"{c=} {i=}")
        try:
            logger.info(f"Executing {c}")
            sub = subprocess.Popen([c], stdout=subprocess.PIPE,  stderr=subprocess.PIPE, cwd=catkin_ws, shell=True, universal_newlines=True)
            while sub.poll() is None:
                try:
                    ste, sto = sub.communicate()  # timeout=5
                    logger.info(ste)
                    logger.error(sto)
                except subprocess.TimeoutExpired:
                    # The command is not giving any output, maybe we should terminate it?
                    # sub.kill()
                    pass
                except KeyboardInterrupt:
                    sub.kill()
            logger.info(f"'{c}' finished with code {sub.returncode}. Package: ({count}/{all_count})")
        except subprocess.CalledProcessError as e:
            logger.error(f"'{c}' had called process error. ({count}/{all_count})")
            raise(e)

        v = "_"
        while v not in possible_answers:
            v = input(f"Did project '{c}' succeed (y/n)?")
        results.append((c,v,))

    report(results)

def report(results):

    logger.info("RESULTS:")
    logger.info("=======================================================================")
    for project, result in results:
        r = "OK" if result in good_answers else "Fail"
        logger.info(f"{project}\t\t{r}")
    logger.info("=======================================================================")



if __name__ == "__main__":
    main()
