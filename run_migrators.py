# run migrators
from commonssite.migrators import *

if __name__ == '__main__':
	HvacMigrator.migrate('/home/controlroom/code/hvac/log-snapshots/0206.csv')