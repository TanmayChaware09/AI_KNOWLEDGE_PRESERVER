import logging

import sys


logger = logging.getLogger("KnowledgeLossPrevention")


logger.setLevel(logging.INFO)


formatter = logging.Formatter(

    "%(asctime)s | %(levelname)s | %(message)s"

)


console = logging.StreamHandler(sys.stdout)

console.setFormatter(formatter)


if not logger.handlers:

    logger.addHandler(console)