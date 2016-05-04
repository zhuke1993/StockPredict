__author__ = 'MALONG'

import logging

log_filename = "C:/logs/stock_predict.log"
log_format = '%(filename)s [%(asctime)s] [%(levelname)s] %(message)s'

logging.basicConfig(filename=log_filename, filemode="w", level=logging.DEBUG, format=log_format,
                    datefmt='%Y-%m-%d %H:%M:%S %p')

console = logging.StreamHandler()
console.setLevel(logging.INFO)
formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
console.setFormatter(formatter)
logging.getLogger('').addHandler(console)
