import logging
import sys

formatter = logging.Formatter('%(levelname)s - %(message)s')

log = logging.getLogger()
log.setLevel(logging.DEBUG)
# logger.setLevel(logging.INFO)
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.INFO)
handler.setFormatter(formatter)

log.addHandler(handler)
