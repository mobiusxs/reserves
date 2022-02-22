from doctrine.database import create_doctrine
from utils.parsers import parse_eft

from core import config

file = open(config.DOCTRINES_PATH, 'r')
fits = file.read().split('\n\n')
for fit in fits:
    fit = fit.splitlines()
    qty = int(fit[0])
    fit = '\n'.join(fit[1:])
    fit = parse_eft(fit)
    create_doctrine(fit, qty)

