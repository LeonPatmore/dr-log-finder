import logging

logger = logging.getLogger("dr_log_finder")
logger.setLevel(logging.INFO)

_c_handler = logging.StreamHandler()
_c_handler.setLevel(logging.INFO)
_c_format = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
_c_handler.setFormatter(_c_format)

_f_handler = logging.FileHandler('messaging.log')
_f_handler.setLevel(logging.INFO)
_f_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
_f_handler.setFormatter(_f_format)

logger.addHandler(_c_handler)
logger.addHandler(_f_handler)
