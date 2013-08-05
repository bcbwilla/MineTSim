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
