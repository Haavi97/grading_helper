import logging
import os
import subprocess

from config import *

logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
logger = logging.getLogger(__name__)


def main():
    """
    Traverse the "catkin_src" directory from config file for projects and execute 'launch_command' in them.
    While process is running it is safe to terminate it with CTR-C hotkey. The script intercepts it and terminates project.
    :return:
    """
    p = os.listdir(catkin_ws)
    for i in p:
        if i == supplemental_dir:
            continue
        c = launch_command.format(i)

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
            logger.info(f"'{c}' returned with code {sub.returncode}.")
        except subprocess.CalledProcessError as e:
            logger.error(f"'{c}' had called process error.")
            raise(e)

        input(f"'{c}' completed, press <Enter>")


if __name__ == "__main__":
    main()
