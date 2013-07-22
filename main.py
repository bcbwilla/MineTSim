import csv
import random

from genetic import GeneticAlgorithm
from genetic import GeneticFunctions

class TournamentFormula(GeneticFunctions):
    """OcTc tournament formula to optimize by genetic algorithm"""
    def __init__(self, teams, matches, limit=200, size=400, 
                 prob_crossover=0.5, prob_mutation=0.8, printerval=10, 
                 outfile="out.log", num_params=4):
        self.counter = 0
        self.num_params = num_params
        self.limit = limit
        self.size = size
        self.prob_crossover = prob_crossover
        self.prob_mutation = prob_mutation
        self.teams = teams
        self.matches = matches
        self.printerval = printerval
        self.outfile = outfile

    # GeneticFunctions interface impls
    def probability_crossover(self):
        return self.prob_crossover

    def probability_mutation(self):
        return self.prob_mutation

    def initial(self):                    
        return [self.random_chromo() for j in range(self.size)]

    def fitness(self, chromo):
        correct = 0
        for match in self.matches:
            t1 = self.teams[match[0]]
            t2 = self.teams[match[1]]
            if t1.calc_score(chromo) > t2.calc_score(chromo):
                correct = correct + 1
        return correct

    def check_stop(self, fits_populations):
        self.counter += 1
        if self.counter % 10 == 0:
            self.print_cycle(fits_populations)
        return self.counter >= self.limit

    def parents(self, fits_populations):
        while True:
            father = self.compete(fits_populations)
            mother = self.compete(fits_populations)
            yield (father, mother)

    def crossover(self, parents):
        father, mother = parents
        index1 = random.randint(1, self.num_params - 2)
        index2 = random.randint(1, self.num_params - 2)
        if index1 > index2: index1, index2 = index2, index1
        child1 = father[:index1] + mother[index1:index2] + father[index2:]
        child2 = mother[:index1] + father[index1:index2] + mother[index2:]
        return (child1, child2)

    def mutation(self, chromosome):
        index = random.randint(0, self.num_params - 1)
        vary = random.randint(-1, 1)
        mutated = list(chromosome)
        mutated[index] += vary
        return mutated

    # internals
    def compete(self, fits_populations):
        alicef, alice = self.select_random(fits_populations)
        bobf, bob = self.select_random(fits_populations)
        return alice if alicef > bobf else bob

    def select_random(self, fits_populations):
        return fits_populations[random.randint(0, len(fits_populations)-1)]

    def random_chromo(self):
        kills = random.uniform(0, 1) 
        deaths = random.uniform(-1.0, 0.0001)
        cores = random.uniform(0, 10)
        monuments = random.uniform(0, 10)
        wools = random.uniform(0, 10)            
        return [kills, cores, monuments, wools, deaths]
    
    def print_cycle(self, fits_populations):
        if self.counter % self.printerval == 0:
            best_match = list(sorted(fits_populations))[-1][1]
            fits = [f for f, ch in fits_populations]
            best = max(fits)
            worst = min(fits)
            ave = sum(fits) / len(fits)
            accuracy = best / float(len(self.matches))
            if self.counter <= self.printerval:
                f = open(self.outfile, 'w')
                f.write("Optimizing OcTc tournament prediction formula\n\n")
            else:
                f = open(self.outfile, 'a')              
            s = 'generation: '+str(self.counter) + '\n best: '+str(best)+' average: '+str(ave)
            s += ' worst: '+str(worst)+'\n best match: '+str(best_match)
            s += '\n accuracy: '+str(accuracy)+'\n\n'
            f.write(s)
            f.close()


class Team(object):
    """Tournament team"""
    def __init__(self,name="",kills=0.0,deaths=0.0,cores=0.0,monuments=0.0,wools=0.0):
        self.name = name
        self.kills = kills
        self.deaths = deaths
        self.cores = cores
        self.monuments = monuments
        self.wools = wools
        
#    def calc_score(self, c):
#        """General formula - linear combination of team stats"""
#        return (c[0]*self.kills+c[1]*self.cores+c[2]*self.monuments+c[3]*self.wools)/self.deaths
    
#    def calc_score(self, c):
#        """General formula - linear combination of team stats"""
#        return self.kills/float(self.deaths)

    def calc_score(self, c):
        """General formula - linear combination of team stats"""
        return c[0]*self.kills+c[1]*self.cores+c[2]*self.monuments+c[3]*self.wools+c[4]*self.deaths


class TeamStats(object):
    """ Reads team stats from .csv file and builds a 
    list of team objects competeing in tournament
    """
    def __init__(self, filename, name_col, kills_col, deaths_col, 
                 cores_col, monuments_col, wools_col,append_s=""):
        self.filename = filename
        self.name_col = name_col
        self.kills_col = kills_col
        self.deaths_col = deaths_col
        self.cores_col = cores_col
        self.monuments_col = monuments_col
        self.wools_col = wools_col
        self.append_s = append_s
        
    def read_stats(self):
        """ reads teams stats from csv file"""
        cr = csv.reader(open(self.filename,"rb"))    
        #skip header row
        cr.next()    
        teams = {}
        for r in cr:  
            name = r[self.name_col] + self.append_s
            kills = float(r[self.kills_col])
            deaths = float(r[self.deaths_col])
            cores = float(r[self.cores_col])
            monuments = float(r[self.monuments_col])
            wools = float(r[self.wools_col])
            teams[name] = Team(name=name, kills=kills, deaths=deaths, 
                               cores=cores, monuments=monuments, wools=wools)
        self.teams = teams
        return teams

# run it
# ROTLW
# main bracket
#first
rotlw_main  = [('Nope',"Tasty Mofo's"),('Loading...', 'Code9'),("Team Soup 'n' Creme",'Dragonite'),
           ('Team Fishy','The Imposters'),('Multiple Scoregasms', 'The Elite Assassins'),('Sand Bag','Duncanites'),
           ('LungGlove','Implosion'),('Badlion','BrainCrack'),('Vicious And Delicious','Gummy Bears'),
           ('SexySquad','DeathSquad'),('TreeFrogs','TeamXD'),('#YOLOSwag','Team Synergy'),
           ('OmegaGamers','Team Ligers'),('Impact','Turquaars'),('BichesGonCrazy','Madhouse')]
#second 
rotlw_main += [("Team Soup 'n' Creme",'Loading...' ),('Team Fishy','Multiple Scoregasms'),('Sand Bag','LungGlove'),
                       ('Badlion','Vicious And Delicious'),('SexySquad','TreeFrogs'),('#YOLOSwag','OmegaGamers'),
                       ('Impact','BichesGonCrazy')]

#third 
rotlw_main += [('Starfish',"Team Soup 'n' Creme"),('Team Fishy','Sand Bag'),('Badlion','SexySquad'),
                      ('#YOLOSwag','Impact')]
#fourth
rotlw_main += [('Starfish','Team Fishy'),('Impact','Badlion')]

#bronze 
rotlw_main += [('Team Fishy', 'Badlion')]



# loser bracket
#first
rotlw_lower = [('Code9','Dragonite'),('The Imposters','The Elite Assassins'),('Duncanites','Implosion'),
         ('Gummy Bears','BrainCrack'),('TeamXD','DeathSquad'),('Team Ligers','Team Synergy'),('Madhouse','Turquaars')]
#second
rotlw_lower += [("Tasty Mofo's",'Code9'),('TeamXD','Gummy Bears'), ('Madhouse','Team Ligers')]
#third
rotlw_lower += [("Tasty Mofo's",'Duncanites'),('Madhouse','TeamXD')]
#final
rotlw_lower += [("Tasty Mofo's",'Madhouse')]

rotlw = rotlw_main + rotlw_lower

#AOTC
#first
aotc = [('BadLion','Fellowship of project ares'),('OmegaWolves','OCBP'),('Ursa Major', 'BichesGonCrazy'),
         ('Loading...','Girl Scouts'),('Better Get a Broom','Normania'),('Impact','Broseidon'),
         ('Sexy squad','FishBears'),('Starfish','Team Synergy'),('Omega Gamers','Divinance'),
         ('Team Supreme','Multiple Scoregasms'),('Game Mode 1','Ligers'),('#YOLOSwag','The Imposters'),
         ('SC','PhatKidz')]
#second
aotc += [('BadLion','OmegaWolves'),('Loading...','Ursa Major'),('Better Get a Broom','SpiderBronies'),
          ('Impact','Sexy squad'),('Starfish','Omega Gamers'),('Game Mode 1','Team Supreme'),
          ('#YOLOSwag','Fairytales'),('Team Fishy','SC')]
#third 
aotc += [('BadLion','Loading...'),('Impact','Better Get a Broom'),('Starfish', 'Game Mode 1'),('#YOLOSwag','Team Fishy')]
#fourth 
aotc += [('BadLion','Impact'),('Starfish','#YOLOSwag')]
#final
aotc += [('Starfish','BadLion')]
#bronze
aotc += [('#YOLOSwag','Impact')]


aotc_up = []
for match in aotc:
    aotc_up.append((match[0]+'aotc',match[1]+'aotc'))
    
rotlw_up = []
for match in rotlw:
    rotlw_up.append((match[0]+'rotlw',match[1]+'rotlw'))


matches = aotc_up + rotlw_up
teams = TeamStats('rotlw_stats.csv',0,1,2,3,4,5,append_s='rotlw').read_stats()
teams.update(TeamStats('aotc_stats.csv',0,1,2,3,4,5,append_s='aotc').read_stats())

print len(matches)
GeneticAlgorithm(TournamentFormula(teams,matches,size=1000,limit=1000,num_params=5,printerval=50)).run()
