import os
import random
import re
from pathlib import Path

#todo 
# randomization in this file should be seeded from variable so easier to write unit tests
# probably sufficien to pass a seed value to get_pickable_spells with default value = random.randint()

# todo move to globals
dnd_dir = Path("/Users/maxwelljoslyn/Desktop/projects/dnd/")

def camel_case_to_spaced(name):
    x = re.sub(r'(.)([A-Z][a-z]+)', r'\1 \2',name)
    return re.sub(r'([a-z0-9])([A-Z])',r'\1 \2',x)

# switch to spell directory
first_level_spell_directory = dnd_dir / Path("before-2021/MageSpellDescriptions/Level1/")

# retrieve and format spell names
first_level_spells = [f for f in os.listdir(first_level_spell_directory) if ".txt" in f and "un~" not in f]
first_level_spells = [camel_case_to_spaced(s[:-4]) for s in first_level_spells]

minimum_first_level_spells = 6

# todo refactor the repetition
# move while len(pickable_spells) ...
def get_pickable_spells(intelligence):
    pickable_spells = []
    # todo bias: goes thru spells in wahtever order they are put into first_level_spells var
    # all else being equal, spells near end of that order less likely to get chosen
    # to fix: for s in randomize(first_level_spells):
    for s in first_level_spells:
        # an Intelligence check
        x = random.randint(1,20)
        if x <= intelligence:
            pickable_spells.append(s)
            first_level_spells.remove(s)
        else:
            pass
    # keep going if there's too few:
    while len(pickable_spells) < minimum_first_level_spells:
        s = random.choice(first_level_spells)
        x = random.randint(1,20)
        if x <= intelligence:
            pickable_spells.append(s)
            first_level_spells.remove(s)
    return pickable_spells
