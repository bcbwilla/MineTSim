from MineTSim import MineTSim
from data.brackets import *

m = MineTSim(matches,method="genetic",cycles=300, size=100)
m.add_teams('data/rotlw_stats.csv', append_s='rotlw')
m.add_teams('data/aotc_stats.csv', append_s='aotc')
m.run()
