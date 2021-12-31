import os
import random
import re
from pathlib import Path

#todo 
# randomization in this file should be seeded from variable so easier to write unit tests
# probably sufficien to pass a seed value to getPickableSpells with default value = random.randint()

# todo move to globals
dnd_dir = Path("/Users/maxwelljoslyn/Desktop/projects/dnd/")

def camelCaseToSpaced(name):
    x = re.sub(r'(.)([A-Z][a-z]+)', r'\1 \2',name)
    return re.sub(r'([a-z0-9])([A-Z])',r'\1 \2',x)

# switch to spell directory
firstLevelSpellDirectory = dnd_dir / Path("before-2021/MageSpellDescriptions/Level1/")

# retrieve and format spell names
firstLevelSpells = [f for f in os.listdir(firstLevelSpellDirectory) if ".txt" in f and "un~" not in f]
firstLevelSpells = [camelCaseToSpaced(s[:-4]) for s in firstLevelSpells]

minimumFirstLevelSpells = 6

# todo refactor the repetition
# move while len(pickableSpells) ...
def getPickableSpells(intelligence):
    pickableSpells = []
    # todo bias: goes thru spells in wahtever order they are put into firstLevelSpells var
    # all else being equal, spells near end of that order less likely to get chosen
    # to fix: for s in randomize(firstLevelSpells):
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
