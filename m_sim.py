import random

def m_sim(teams, matches, outfile='out.log', cycles=10, printerval=100000):
    # out file
    f = open(outfile,'a')
    
    # best run
    most_accurate = 0.0
    best_fit = {}
    
    for cycle in range(1,cycles):
        
        if cycle == 1:
            # weights for score. kd only.
            avgkd = 1
            kills = 0
            avgcd = 0
            avgmd = 0
            avgwd = 0
        else:
            # weights for score, random.
            avgkd = random.uniform(0, 10) 
            kills = random.uniform(0, 0.0001)
            avgcd = random.uniform(0, 1000)
            avgmd = random.uniform(0, 1000)
            avgwd = random.uniform(0, 1000)
        
        coeff = [avgkd, kills, avgcd, avgmd, avgwd]
        
        total = 0
        correct = 0
        for match in matches:
            t1 = teams[match[0]]
            t2 = teams[match[1]]
                        
            if t1.calc_score(coeff) > t2.calc_score(coeff):
                correct = correct + 1
            total = total + 1
           
        accuracy = correct/float(total)
      
        if accuracy > most_accurate:
            most_accurate = accuracy
            best_fit['avgkd'] = avgkd
            best_fit['kills'] = kills
            best_fit['avgcd'] = avgcd
            best_fit['avgmd'] = avgmd
            best_fit['avgwd'] = avgwd
            print most_accurate, 'cycle ',cycle
            f.write('new winner: '+str(most_accurate)+'. found on cycle '+str(cycle)+"\n")
        
        if cycle% printerval == 0:
            print "cycle ",cycle
    
    f.write('\n\nResults\naccuracy: '+str(most_accurate)+'\n\ncoefficients:\n')
    
    for name,value in best_fit.iteritems():
        f.write(name+': '+str(value)+'\n')
    f.write('\n\n')  
    f.close() 
    return most_accurate, best_fit


