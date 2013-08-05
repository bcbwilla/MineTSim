from MineTSim import MineTSim
from data.brackets import *

m = MineTSim(matches,method="monte",cycles=10000)
m.add_teams('data/rotlw_stats.csv', append_s='rotlw')
m.add_teams('data/aotc_stats.csv', append_s='aotc')
m.run()
