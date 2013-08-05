import csv
import random
import math

from bin.genetic import GeneticAlgorithm
from bin.genetic import GeneticFunctions

# Main Class
class MineTSim(object):
    
    def __init__(self,matches,method="monte",outfile="out.log",cycles=10000,printerval=None,
                 size=400, prob_crossover=0.7, prob_mutation=0.6, num_params=5):
        # general attributes
        self.matches = matches
        self.method = method
        self.outfile = outfile
        self.teams = {}
        self.cycles = cycles

        # genetic algorithm attributes
        self.size = size
        self.prob_crossover = prob_crossover
        self.prob_mutation = prob_mutation
        self.num_params = num_params


        if printerval is None:
            self.printerval = int(math.floor(cycles/10))

    def add_teams(self,filename, name_col=0, kills_col=1,deaths_col=2,
                  cores_col=3, monuments_col=4,wools_col=5,append_s=""):

        """reads teams stats from csv file"""
        f = csv.reader(open(filename,"rb"))    
        #skip header row
        f.next()
        teams = {}    
        for r in f:  
            name = r[name_col] + append_s
            kills = float(r[kills_col])
            deaths = float(r[deaths_col])
            cores = float(r[cores_col])
            monuments = float(r[monuments_col])
            wools = float(r[wools_col])
            teams[name] = Team(name=name, kills=kills, deaths=deaths, 
                               cores=cores, monuments=monuments, wools=wools)
        self.teams.update(teams)
        return self.teams

    def genetic(self):
        g = GeneticTournament(self.teams,self.matches,size=self.size,limit=self.cycles,
                              num_params=self.num_params,printerval=self.printerval,
                              outfile=self.outfile)
        GeneticAlgorithm(g).run()
    

    def monte(self):
        MonteTournament(self.teams,self.matches,cycles=self.cycles,
                        printerval=self.printerval,outfile=self.outfile)
        

    def run(self):
   
        if len(self.teams) == 0:
            print "Please add teams to the tournament!"
            return False

        if self.method == "genetic":
            print "Running genetic prediction optimization\n"
            self.genetic()
            return True
        elif self.method == "monte":
            print "Running Monte Carlo prediction optimization\n"
            self.monte()
            return True
        else:
            print "Please provide an optimization method."
            return False


#
# Supporting Classes
#

class Tournament(object):
    """Simulates a tournament"""    

    def __init__(self,matches,teams,weights):
        self.matches = matches
        self.teams = teams
        self.weights = weights

    def run(self):
        correct = 0
        for match in self.matches:
            t1 = self.teams[match[0]]
            t2 = self.teams[match[1]]
                        
            if t1.calc_score(self.weights) > t2.calc_score(self.weights):
                correct = correct + 1
        return float(correct)/len(self.matches)


class Team(object):
    """Tournament team"""
    def __init__(self,name="",kills=0.0,deaths=0.0,cores=0.0,monuments=0.0,wools=0.0):
        self.name = name
        self.kills = kills
        self.deaths = deaths
        self.cores = cores
        self.monuments = monuments
        self.wools = wools

    def calc_score(self, c):
        """General formula - linear combination of team stats"""
        return c[0]*self.kills+c[1]*self.deaths+c[2]*self.cores+c[3]*self.monuments+c[4]*self.wools


class MonteTournament(object):

    def __init__(self,teams,matches,cycles=1000,printerval=None,outfile="mout.log"):
        self.matches = matches
        self.teams = teams
        
        most_accurate = 0.0        
        
        f = open(outfile,'w')

        for cycle in range(1,cycles):
            weights = self.make_weights()
            accuracy = self.accuracy(weights)

            if accuracy > most_accurate:
                most_accurate = accuracy
                best_weights = weights
                f.write('new winner: '+str(most_accurate)+'. found on cycle '+str(cycle)+"\n")

            if cycle % printerval == 0:
                print "cycle ",cycle
        
        f.write('\n\nResults\naccuracy: '+str(most_accurate)+'\n\ncoefficients:\n'+str(best_weights))
    
    def make_weights(self):
        # weights for score, random.
        kills = random.uniform(-0.01, 1) 
        deaths = random.uniform(-1.0, 0.001)
        cores = random.uniform(-0.01, 10)
        monuments = random.uniform(-0.01, 10)
        wools = random.uniform(-0.01, 10)
     
        return [kills, cores, monuments, wools, deaths]

    def accuracy(self,weights):
        return Tournament(self.matches,self.teams,weights).run()
        


class GeneticTournament(GeneticFunctions):
    """OcTc tournament formula to optimize by genetic algorithm"""
    def __init__(self, teams, matches, limit=300, size=400, 
                 prob_crossover=0.5, prob_mutation=0.8, printerval=10, 
                 outfile="out.log", num_params=5):
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
         return Tournament(self.matches,self.teams,chromo).run()

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
        index1 = random.randint(1, self.num_params - 1)
        index2 = random.randint(1, self.num_params - 1)
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
        kills = random.uniform(0.0, 1) 
        deaths = random.uniform(-1.0, 0.0001)
        cores = random.uniform(0.0, 10)
        monuments = random.uniform(0.0, 10)
        wools = random.uniform(0.0, 10)            
        return [kills, cores, monuments, wools, deaths]
    
    def print_cycle(self, fits_populations):
        if self.counter % self.printerval == 0:
            print "generation " + str(self.counter)
            best_match = list(sorted(fits_populations))[-1][1]
            fits = [f for f, ch in fits_populations]
            best = max(fits)
            worst = min(fits)
            ave = sum(fits) / len(fits)
            if self.counter <= self.printerval:
                f = open(self.outfile, 'w')
                f.write("Optimizing OcTc tournament prediction formula\n\n")
            else:
                f = open(self.outfile, 'a')              
            s = 'generation: '+str(self.counter) + '\n best: '+str(best)+' average: '+str(ave)
            s += ' worst: '+str(worst)+'\n best match: '+str(best_match)+'\n\n'
            f.write(s)
            f.close()


