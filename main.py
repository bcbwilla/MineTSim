# run it




matches = aotc_up + rotlw_up
teams = TeamStats('rotlw_stats.csv',0,1,2,3,4,5,append_s='rotlw').read_stats()
teams.update(TeamStats('aotc_stats.csv',0,1,2,3,4,5,append_s='aotc').read_stats())

print len(matches)
GeneticAlgorithm(TournamentFormula(teams,matches,size=1000,limit=1000,num_params=5,printerval=50)).run()
