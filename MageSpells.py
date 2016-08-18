import os
import random
import re

def camelCaseToSpaced(name):
    x = re.sub(r'(.)([A-Z][a-z]+)', r'\1 \2',name)
    return re.sub(r'([a-z0-9])([A-Z])',r'\1 \2',x)

basedir =  "/Users/maxwelljoslyn/Desktop/projects/D&D/BackgroundGenerator"
# switch to spell directory
firstLevelSpellDirectory = "/Users/maxwelljoslyn/Desktop/projects/D&D/MageSpellDescriptions/Level1/"

# retrieve and format spell names
firstLevelSpells = [f for f in os.listdir(firstLevelSpellDirectory) if ".txt" in f and "un~" not in f]
firstLevelSpells = [camelCaseToSpaced(s[:-4]) for s in firstLevelSpells]

minimumFirstLevelSpells = 6

def getPickableSpells(intelligence):
    pickableSpells = []
    for s in firstLevelSpells:
        # an Intelligence check
        x = random.randint(1,20)
        if x <= intelligence:
            pickableSpells.append(s)
            firstLevelSpells.remove(s)
        else:
            pass
    # keep going if there's too few:
    while len(pickableSpells) < minimumFirstLevelSpells:
        s = random.choice(firstLevelSpells)
        x = random.randint(1,20)
        if x <= intelligence:
            pickableSpells.append(s)
            firstLevelSpells.remove(s)
    return pickableSpells
