import logging
import os
import subprocess

from config import *

logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
logger = logging.getLogger(__name__)


def main():
    p = os.listdir(catkin_ws)
    for i in p:
        if i == supplemental_dir:
            continue
        c = launch_command.format(i)

        try:
            logger.info(f"Executing {c}")
            sub = subprocess.Popen([c], stdout=subprocess.PIPE,  stderr=subprocess.PIPE, cwd=catkin_ws, shell=True, universal_newlines=True)
            while sub.poll() is None:
                ste, sto =  sub.communicate()
                logger.info(ste)
                logger.error(sto)
            if sub.returncode == 0:
                logger.info(f"{c} succeeded.")
            else:
                logger.error(f"{c} failed.")
        except OSError as e:
            ste, sto =  sub.communicate()
            # logger.i(f"{ste=} {sto=}")
            logger.info(sto)
            logger.error(ste)
            raise(e)
        except subprocess.CalledProcessError as e:
            logger.error("Called process error")
            logger.error(e)
            raise(e)

        input(f"'{c}' completed, press <Enter>")


if __name__ == "__main__":
    main()