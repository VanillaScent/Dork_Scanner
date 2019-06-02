import logging
import sys
from termcolor import colored, cprint
#logging.basicConfig(format=(colored("%(asctime)s ", "yellow"), colored("%(levelname)s ", "blue"), colored("%(message)s", "blue") ) )

logging.basicConfig(stream=sys.stdout, level=logging.INFO, format=(colored("%(asctime)s ", "yellow"), colored("%(levelname)s ", "blue"), colored("%(message)s", "blue")))
