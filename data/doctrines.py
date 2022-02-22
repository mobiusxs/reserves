from doctrine.database import create_doctrine
from utils.parsers import parse_eft

file = open('doctrines.txt', 'r')
fits = file.read().split('\n\n')
for fit in fits:
    fit = fit.splitlines()
    qty = int(fit[0])
    fit = '\n'.join(fit[1:])
    fit = parse_eft(fit)
    create_doctrine(fit, qty)

