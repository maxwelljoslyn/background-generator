from random import *
from decimal import *
from Details import *
from math import floor
from pathlib import Path

# 2021-08-15 asssign NAMES to the family members o h thats a splendid idea!
# and draw up a rudimentary family tree!!!!

import MageSpells
# 18h = area where 18 (or 3) are hardcoded as limits of PC ability score spectrum (no longer true once races are added)

getcontext().prec = 3

def advantageMagnitude(abiScore):
    """Subtract a d20 roll from the score.
    This results in a value from -17 (worst) to +17 (best),
    which determines the nature of background characteristic granted by this ability score.

todo fixme: the range is assumed to be -17 to 17, but if racial (or other) ability score adjustments are used, the range will be 2-19 or even 1-20 (depending on the adjustments used).
furthermore it is probably hardcoded in many other places that -17/+17 are the edges."""
    roll = randint(1,20)
    result = abiScore - roll
    return result

def input_sex():
    def get_sex():
        return input("Enter sex:\n").lower()
    sex = get_sex()
    males = {"m", "male", "man", "boy"}
    females = {"f", "female", "woman", "girl"}
    while sex not in males.union(females):
        print("Invalid sex.")
        sex = get_sex()
    if sex in males:
        return "Male"
    else:
        return "Female"

def input_ability_score(prompt, race="human"):
    def get_score():
        return int(input("Enter "+prompt.capitalize()+":\n"))
    score = get_score()
    # todo extract this to rules or globals or races.py as racial maximums per stat, based on their modifiers
    if race == "human":
        minimum = 3
        maximum = 18
    else:
        minimum = 2
        maximum = 19
    while score < minimum:
        print(str(score) + " is too low.")
        score = get_score()
    while score > maximum:
        print(str(score) + " is too high.")
        score = get_score()
    return score

# todo import from classes.py
possibleClassNames = ["fighter","paladin","ranger","cleric","druid","mage","illusionist","thief","assassin","monk"]


def input_charclass():
    def get_charclass():
        return input("Enter character class:\n").lower()
    pClass = get_charclass()
    while pClass not in possibleClassNames:
        print("Invalid class.")
        pClass = get_charclass()
    return pClass.capitalize()

baseStartingAge = {"Fighter":15,"Paladin":19,"Ranger":17,"Cleric":20,"Druid":20,"Mage":22,
               "Illusionist":24,"Thief":17,"Assassin":19,"Monk":22}

def getStartingAge(pClass):
    base = baseStartingAge[pClass]
    if pClass in ["Fighter","Paladin","Ranger"]:
        base += randint(1,4)
    elif pClass in ["Cleric","Druid"]:
        base += randint(2,4)
    elif pClass in ["Mage","Illusionist"]:
        base += randint(1,6) + randint(1,6)
    else:
        base += randint(1,3)
    return base

# todo update this for races, then move to characters/rules/globals
baseMaleWeight = Decimal(175) # pounds
baseMaleHeight = Decimal(70) # inches
baseFemaleWeight = Decimal(140)
baseFemaleHeight = Decimal(66)

def calcHeightWeight(player):
    source = randint(1,6) + randint(1,6) + randint(1,6) + randint(1,6)
    # bell curve for this 4d6 roll has peak at value 14:  ((6 * 4) + (1 * 4)) / 2 = 14
    avg = 14
    difference = source - avg
    # low source, e.g. 4, means 4 - 14 = -10
    # high source, e.g. 18, means 18 - 14 = 4
    heightMod = 1 + (difference * 0.01)
    weightMod = 1 + (difference * 0.025)
    
    if player.sex == "Male":
        height = Decimal(baseMaleHeight) * Decimal(heightMod)
        weight = Decimal(baseMaleWeight) * Decimal(weightMod)
    else:
        height = Decimal(baseFemaleHeight) * Decimal(heightMod)
        weight = Decimal(baseFemaleWeight) * Decimal(weightMod)
    height = round(height)
    weight = round(weight)
    return (height, weight)


# area where 18 is hardcoded as max ability score
idealEncumbranceTable = {strength:(65 + 5 * strength) for strength in range(3,19)}
# todo:
# def ideal_encumbrance(strength) = 65 * (5 * strength)

def calcMaxEncumbrance(player):
    proportion = 0
    if player.sex == "Male":
        proportion = player.weight / baseMaleWeight
    else:
        proportion = player.weight / baseFemaleWeight
    idealMaxEncumbrance = idealEncumbranceTable[player.Strength]
    unmodifiedMaxEncumbrance = proportion * idealMaxEncumbrance
    actualMax = unmodifiedMaxEncumbrance * player.encMult
    return actualMax

# 2021-08-15
# todo redefine as function mapping weights to penalties
def encumbrancePenaltyCutoffs(maxEnc):
    """Calculate the encumbrance levels at which character suffers reduced Action Points."""
    maxEnc = Decimal(maxEnc)
    nopenalty =   Decimal(0.4) * maxEnc
    minus1penalty = Decimal(0.55) * maxEnc
    minus2penalty = Decimal(0.7) * maxEnc
    minus3penalty = Decimal(0.85) * maxEnc
    # between the -3 penalty cutoff and maxEnc, the penalty is -4
    return nopenalty, minus1penalty, minus2penalty, minus3penalty

def inchesToFeetInches(arg):
   feet = floor(arg/12)
   inches = arg % 12
   return (feet, inches)


# 2021-08-15
# having e.g. Strength as a field on PC struc
# is bad. should be a map field within the PC struct
# with keys being bility enums (strings if you HAVE To but thats dumb) adn values being abi scores
# one use case for this: being able to get races['orc']['strength'] modifier and add that to new_pc['abilities']['strength'], with that code generic to all 6 abilities, rather than having to switch on a string 6 times to add to the corrent ability score field (pc.strength, pc.wisdom, etc.)
# AS USUAL, python inconsistency of data access between dict entries and object fields is an irritation ----- especially in light of fields being a dict under hte hood anyway, IIRC!
def function1(a_PC):
    abilities = [("Strength", a_PC.Strength),
                 ("Dexterity", a_PC.Dexterity),
                 ("Constitution", a_PC.Constitution),
                 ("Intelligence", a_PC.Intelligence),
                 ("Wisdom", a_PC.Wisdom),
                 ("Charisma", a_PC.Charisma)]
    filtered = [(a[0], a[1] - 10) for a in abilities if (a[1] - 10) >= 1]
    return dict(filtered)

def function2(above_tens):
    choices = []
    for name, points in above_tens.items():
        choices.extend([name] * points)
    chosen = choice(choices)
    return (chosen, above_tens[chosen])

def parent_profession(a_PC):
    above_average_scores = function1(a_PC)
    if above_average_scores == []:
    # no character scores above 10
    # (cannot happen for main PCs, given the "above 15" rule, but can happen for henchmen)
        return None
    else:
        chosen_ability, delta_10 = function2(above_average_scores)
        # todo change to {'strength' : professionStrength, 'wisdom' : ...} dictionary, and select within that
        # in general, prefer map lookups to literal switches -- ie prefer data to imperative code
        if chosen_ability == "Strength":
            return professionStrength()
        elif chosen_ability == "Dexterity":
            return professionDexterity()
        elif chosen_ability == "Constitution":
            return professionConstitution()
        elif chosen_ability == "Wisdom":
            return professionWisdom()
        elif chosen_ability == "Intelligence":
            return professionIntelligence()
        else:
            return professionCharisma()
            
class PC():
    def __init__(self):
        # todo: distinguish between values/variables used only in character generation, and values which characterize the resulting PC
        # e.g. moneyMult
        # this will come into play when *returning a PC object* (whether it's a PC instance, or perhaps utlimately a ditionary) for use in the rest of the game code, storing in database, etc.
        # eventually there may be no diference (eg why not keep around the "added age" var from prison detail so you always know how long that was?) but at current time no reason to worry those cases

        self.seed = randint(0,1000000000)
        self.pClass = ""
        self.Strength = 0
        self.Dexterity = 0
        self.Constitution = 0
        self.Intelligence = 0
        self.Wisdom = 0
        self.Charisma = 0
        self.weight = 0 # pounds
        self.height = 0 # inches
        self.sex = ""
        # multiply this by final calculated "ideal" max enc. to determine final max enc
        self.encMult = Decimal(1.0)
        # this will be set later, don't change it
        self.maxEncumbrance = Decimal(0)
        # mult this value times default starting money to determine actual starting money
        self.moneyMult = Decimal(1)
        # used to calculate abnormal weight in the case of fatness
        # (see the main function for details on how we avoid incorporating the new
        # fat weight into encumbrance -- it's a question of function-call ordering.)
        self.weightMult = Decimal(1)
        # add this to normal starting age to get actual starting age
        self.addedAge = 0
        self.credit = 0
        # set this to false if getting the orphan result
        self.hasFamily = True
        self.baseHair = getBaseHairColor()
        self.eyeColor = getEyeColor(self.baseHair)
        # certain classes and background results will set this to true
        self.literate = False
        self.fatherProf = None
        self.motherProf = None



def writeline(f,text):
    f.write(text)
    f.write("\n")

def main():
    c = PC()
    seed(c.seed)
    testing = False
    if testing:
        c.pClass = "Mage"
        c.Strength, c.Dexterity, c.Wisdom, c.Constitution, c.Intelligence, c.Charisma = 12,18,12,12,12,12
        c.sex = "Male"
        from datetime import datetime
        c.name = "Foobar" + datetime.now().isoformat()
    else:
        c.pClass = input_charclass()
        c.Strength = input_ability_score("Strength")
        c.Dexterity = input_ability_score("Dexterity")
        c.Constitution = input_ability_score("Constitution")
        c.Intelligence = input_ability_score("Intelligence")
        c.Wisdom = input_ability_score("Wisdom")
        c.Charisma = input_ability_score("Charisma")
        c.sex = input_sex()
        c.name = input("Enter character name:\n")
    
    # base height and weight
    # these must be calculated BEFORE any weight modifiers, i.e. fatness,
    # are accounted for in final printed weight,
    # so that e.g. fatness does not increase player's max encumbrance
    c.height, c.weight = calcHeightWeight(c)

    # base encumbrance
    # it may be changed by details.
    c.maxEncumbrance = Decimal(calcMaxEncumbrance(c))
    
    # Calculation of background details
    # some of these internally modify other aspects of the Player record
    characters_dir = MageSpells.dnd_dir / Path("src/background-generator/Characters")
    output_file = characters_dir / Path(c.name + ".txt")
    with open(output_file, "w") as f:
        # todo: except file not found, f = stndaard out instaed
        f.write("[seed " + str(c.seed))
        f.write("]\n\n")

        abis = [("Strength",c.Strength),
                ("Dexterity",c.Dexterity),
                 ("Constitution",c.Constitution),
                 ("Intelligence",c.Intelligence),
                 ("Wisdom",c.Wisdom),
                 ("Charisma",c.Charisma)]
        f.write("Ability scores:\n")
        for name, stat in abis:
            dotlength = 10 - len(name)
            dots = "." * (16 - len(name))
            f.write("{0}{1}{2}".format(name,dots,stat))
            f.write("\n")
        f.write("Background for " + c.name + ":")
        f.write("\n\n")
        f.write("Family:")
        f.write("\n")
        # this detail sets the hasFamily flag, so it has to come before interpersonal
        familyDetail = detailFamily(advantageMagnitude(c.Strength),c)
        f.write(familyDetail)
        f.write("\n\n")

        f.write("Your father's profession: ")
        c.fatherProf = parent_profession(c)
        f.write(str(c.fatherProf))
        f.write("\n")
        f.write("Gained from your father: ")
        f.write(profession_effect(c,c.fatherProf))
        f.write("\n\n")
        

        f.write("Feats of strength:")
        f.write("\n")
        featsDetail = detailFeats(advantageMagnitude(c.Strength),c)
        f.write(featsDetail)
        f.write("\n\n")

        f.write("Interpersonal relationships:")
        f.write("\n")
        interpersonalDetail = detailInterpersonal(advantageMagnitude(c.Wisdom),c)
        f.write(interpersonalDetail)
        f.write("\n\n")

        f.write("Tendencies:")
        f.write("\n")
        tendencyDetail = detailTendency(advantageMagnitude(c.Wisdom),c)
        f.write(tendencyDetail)
        f.write("\n\n")

        f.write("Choices:")
        f.write("\n")
        choicesDetail = detailChoices(advantageMagnitude(c.Intelligence),c)
        f.write(choicesDetail)
        f.write("\n\n")

        f.write("Physical appearance:")
        f.write("\n")
        beautyDetail = detailBeauty(advantageMagnitude(c.Charisma),advantageMagnitude(c.Charisma),c)
        f.write(beautyDetail)
        f.write("\n\n")

        f.write("Bodily health:")
        f.write("\n")
        healthDetail = detailHealth(advantageMagnitude(c.Constitution),c)
        f.write(healthDetail)
        f.write("\n\n")

        f.write("Agility and coordination:")
        f.write("\n")
        agilityDetail = detailAgility(advantageMagnitude(c.Dexterity),c)
        f.write(agilityDetail)
        f.write("\n\n")

        age = getStartingAge(c.pClass) + c.addedAge
        f.write("Age: " + str(age))
        f.write("\n")
        f.write("Birthday: " + birthday(age))
        f.write("\n")
        hairInfo = makeFinalHair(c.baseHair, age, c.Constitution, c.sex)
        hair = hairInfo.haircolor
        for attribute in [hairInfo.hairdesc, hairInfo.haircond]:
            if attribute == "":
                pass
            else:
                hair = hair + ", " + attribute
        f.write("Hair: " + hair)
        f.write("\n")
        f.write("Eyes: " + c.eyeColor)
        f.write("\n")

        # override any background result which would take literacy away
        if c.pClass in ["Mage", "Illusionist", "Cleric", "Druid"]:
            c.literate = True
        if c.literate:
            f.write("Literate: Yes\n")
        else:
            f.write("Literate: No\n")
        
        baseMoney = Decimal(20) + Decimal(randint(2,6) * 10)
        actualMoney = baseMoney * c.moneyMult
        f.write("Starting money: " + str(actualMoney) + " gold pieces")
        f.write("\n")
        f.write("Credit: " + str(c.credit) + " gold pieces")
        f.write("\n")


        # actual encumbrance
        # this must be done after detail calculation,
        # in case one of those alters the max encumbrance from the base value (as certain strength results can do)
        eNoPen, eMin1, eMin2, eMin3  = encumbrancePenaltyCutoffs(c.maxEncumbrance)

        # however, final weight must be calculated AFTER encumbrance,
        # since if the character's weight is modified to be fat,
        # encumbrance SHOULD NOT take that into account.
        ft, ins = inchesToFeetInches(c.height)
        f.write("Height: " + str(ft) + " ft. " + str(ins) + " in.")
        f.write("\n")
        if c.weightMult == Decimal(1):
            # weight is normal; character has not grown fat
            f.write("Weight: " + str(c.weight) + " lbs")
            f.write("\n\n")
        else:
            oldWeight = c.weight
            adjustedWeight = c.weight * c.weightMult
            diff = adjustedWeight - oldWeight
            f.write("Weight: " + str(adjustedWeight) + " lbs; " + str(diff) + " lbs of this is fat, and counts against encumbrance!")
            f.write("\n\n")
        f.write("Encumbrance Information:")
        f.write("\n")
        f.write("Carried weight <= " + str(eNoPen) + " lbs: no AP penalty.")
        f.write("\n")
        f.write(str(eNoPen) + " lbs < carried weight <= " + str(eMin1) + " lbs: -1 AP.")
        f.write("\n")
        f.write(str(eMin1) + " lbs < carried weight <= " + str(eMin2) + " lbs: -2 AP.")
        f.write("\n")
        f.write(str(eMin2) + " lbs < carried weight <= " + str(eMin3) + " lbs: -3 AP.")
        f.write("\n")
        f.write(str(eMin3) + " lbs < carried weight <= " + str(c.maxEncumbrance) + " lbs: -4 AP.")
        f.write("\n")
        f.write("Above that, no movement is possible, regardless of remaining AP.")

        if c.pClass == "Mage":
            f.write("\n\n")
            f.write("Pick one of these first-level spells:\n")
            for p in MageSpells.getPickableSpells(c.Intelligence):
                f.write(p)
                f.write('\n')

if __name__ == "__main__":
    main()
