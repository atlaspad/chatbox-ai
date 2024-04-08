import asyncio
from datetime import datetime
import requests
import sys
import os
# Add the root directory of your project to the Python path to import from parent directory
# to fix configs import problem

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from side_tasks.keep_updated import *

uk = UpdatedKeeper()
uk.run()

def get_funding():

    return uk.get_funding()


# asyncio.run(get_funding())
