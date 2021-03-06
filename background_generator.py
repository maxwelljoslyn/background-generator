from random import *
from decimal import *
from details import *
from math import floor
from pathlib import Path
import mage_spells
from datetime import datetime

# 2021-08-15 asssign NAMES to the family members o h thats a splendid idea!
# and draw up a rudimentary family tree!!!!

# 18h = area where 18 (or 3) are hardcoded as limits of PC ability score spectrum (no longer true once races are added)

getcontext().prec = 3

def advantage_magnitude(abi_score):
    """Subtract a d20 roll from the score.
    This results in a value from -17 (worst) to +17 (best),
    which determines the nature of background characteristic granted by this ability score.

todo fixme: the range is assumed to be -17 to 17, but if racial (or other) ability score adjustments are used, the range will be 2-19 or even 1-20 (depending on the adjustments used).
furthermore it is probably hardcoded in many other places that -17/+17 are the edges."""
    roll = randint(1,20)
    result = abi_score - roll
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
possible_class_names = ["fighter","paladin","ranger","cleric","druid","mage","illusionist","thief","assassin","monk"]

def input_charclass():
    def get_charclass():
        return input("Enter character class:\n").lower()
    pClass = get_charclass()
    while pClass not in possible_class_names:
        print("Invalid class.")
        pClass = get_charclass()
    return pClass.capitalize()

base_age = {"Fighter":15,"Paladin":19,"Ranger":17,"Cleric":20,"Druid":20,"Mage":22,
               "Illusionist":24,"Thief":17,"Assassin":19,"Monk":22}

def starting_age(pClass):
    base = base_age[pClass]
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
base_male_weight = Decimal(175) # pounds
base_male_height = Decimal(70) # inches
base_female_weight = Decimal(140)
base_female_height = Decimal(66)

def calc_height_weight(player):
    source = randint(1,6) + randint(1,6) + randint(1,6) + randint(1,6)
    # bell curve for this 4d6 roll has peak at value 14:  ((6 * 4) + (1 * 4)) / 2 = 14
    avg = 14
    difference = source - avg
    # low source, e.g. 4, means 4 - 14 = -10
    # high source, e.g. 18, means 18 - 14 = 4
    height_mod = 1 + (difference * 0.01)
    weight_mod = 1 + (difference * 0.025)
    
    if player.sex == "Male":
        height = Decimal(base_male_height) * Decimal(height_mod)
        weight = Decimal(base_male_weight) * Decimal(weight_mod)
    else:
        height = Decimal(base_female_height) * Decimal(height_mod)
        weight = Decimal(base_female_weight) * Decimal(weight_mod)
    height = round(height)
    weight = round(weight)
    return (height, weight)


# 18h area where 18 is hardcoded as max ability score
ideal_encumbrance_table = {strength:(65 + 5 * strength) for strength in range(3,19)}
# todo:
# def ideal_encumbrance(strength) = 65 * (5 * strength)

def calc_max_encumbrance(player):
    proportion = 0
    if player.sex == "Male":
        proportion = player.weight / base_male_weight
    else:
        proportion = player.weight / base_female_weight
    ideal_max_encumbrance = ideal_encumbrance_table[player.Strength]
    unmodified_max_encumbrance = proportion * ideal_max_encumbrance
    actual_max = unmodified_max_encumbrance * player.enc_mult
    return actual_max

# 2021-08-15
# todo redefine as function mapping weights to penalties
def encumbrance_penalty_cutoffs(max_enc):
    """Calculate the encumbrance levels at which character suffers reduced Action Points."""
    max_enc = Decimal(max_enc)
    nopenalty =   Decimal(0.4) * max_enc
    minus1penalty = Decimal(0.55) * max_enc
    minus2penalty = Decimal(0.7) * max_enc
    minus3penalty = Decimal(0.85) * max_enc
    # between the -3 penalty cutoff and max_enc, the penalty is -4
    return nopenalty, minus1penalty, minus2penalty, minus3penalty

def inches_to_feet_and_inches(arg):
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
        # todo change to {'strength' : profession_strength, 'wisdom' : ...} dictionary, and select within that
        # in general, prefer map lookups to literal switches -- ie prefer data to imperative code
        if chosen_ability == "Strength":
            return profession_strength()
        elif chosen_ability == "Dexterity":
            return profession_dexterity()
        elif chosen_ability == "Constitution":
            return profession_constitution()
        elif chosen_ability == "Wisdom":
            return profession_wisdom()
        elif chosen_ability == "Intelligence":
            return profession_intelligence()
        else:
            return profession_charisma()
            
class PC():
    def __init__(self):
        # todo: distinguish between values/variables used only in character generation, and values which characterize the resulting PC
        # e.g. money_mult
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
        self.enc_mult = Decimal(1.0)
        # this will be set later, don't change it
        self.max_encumbrance = Decimal(0)
        # mult this value times default starting money to determine actual starting money
        self.money_mult = Decimal(1)
        # used to calculate abnormal weight in the case of fatness
        # (see the main function for details on how we avoid incorporating the new
        # fat weight into encumbrance -- it's a question of function-call ordering.)
        self.weight_mult = Decimal(1)
        # add this to normal starting age to get actual starting age
        self.added_age = 0
        self.credit = 0
        # set this to false if getting the orphan result
        self.has_family = True
        self.base_hair = get_base_hair_color()
        self.eye_color = get_eye_color(self.base_hair)
        # certain classes and background results will set this to true
        self.literate = False
        self.father_prof = None
        self.mother_prof = None



def main():
    c = PC()
    seed(c.seed)
    testing = False
    if testing:
        c.pClass = "Mage"
        c.Strength, c.Dexterity, c.Wisdom, c.Constitution, c.Intelligence, c.Charisma = 12,18,12,12,12,12
        c.sex = "Male"
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
    c.height, c.weight = calc_height_weight(c)

    # base encumbrance
    # it may be changed by details.
    c.max_encumbrance = Decimal(calc_max_encumbrance(c))
    
    # Calculation of background details
    # some of these internally modify other aspects of the Player record
    characters_dir = mage_spells.dnd_dir / Path("code/background-generator/Characters")
    # todo write to standard out if fail to open file
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
            dots = "." * (16 - len(name))
            f.write("{0}{1}{2}".format(name,dots,stat))
            f.write("\n")
        f.write("Background for " + c.name + ":")
        f.write("\n\n")
        f.write("Family:")
        f.write("\n")
        # this detail sets the has_family flag, so it has to come before interpersonal
        family_detail = detail_family(advantage_magnitude(c.Strength),c)
        f.write(family_detail)
        f.write("\n\n")

        f.write("Your father's profession: ")
        c.father_prof = parent_profession(c)
        f.write(str(c.father_prof))
        f.write("\n")
        f.write("Gained from your father: ")
        f.write(profession_effect(c,c.father_prof))
        f.write("\n\n")
        

        f.write("Feats of strength:")
        f.write("\n")
        feats_detail = detail_feats(advantage_magnitude(c.Strength),c)
        f.write(feats_detail)
        f.write("\n\n")

        f.write("Interpersonal relationships:")
        f.write("\n")
        interpersonal_detail = detail_interpersonal(advantage_magnitude(c.Wisdom),c)
        f.write(interpersonal_detail)
        f.write("\n\n")

        f.write("Tendencies:")
        f.write("\n")
        tendency_detail = detail_tendency(advantage_magnitude(c.Wisdom),c)
        f.write(tendency_detail)
        f.write("\n\n")

        f.write("Choices:")
        f.write("\n")
        choices_detail = detail_choices(advantage_magnitude(c.Intelligence),c)
        f.write(choices_detail)
        f.write("\n\n")

        f.write("Physical appearance:")
        f.write("\n")
        beauty_detail = detail_beauty(advantage_magnitude(c.Charisma),advantage_magnitude(c.Charisma),c)
        f.write(beauty_detail)
        f.write("\n\n")

        f.write("Bodily health:")
        f.write("\n")
        health_detail = detail_health(advantage_magnitude(c.Constitution),c)
        f.write(health_detail)
        f.write("\n\n")

        f.write("Agility and coordination:")
        f.write("\n")
        agility_detail = detail_agility(advantage_magnitude(c.Dexterity),c)
        f.write(agility_detail)
        f.write("\n\n")

        age = starting_age(c.pClass) + c.added_age
        f.write("Age: " + str(age))
        f.write("\n")
        f.write("Birthday: " + birthday(age))
        f.write("\n")
        hair_info = make_final_hair(c.base_hair, age, c.Constitution, c.sex)
        hair = hair_info.haircolor
        for attribute in [hair_info.hairdesc, hair_info.haircond]:
            if attribute == "":
                pass
            else:
                hair = hair + ", " + attribute
        f.write("Hair: " + hair)
        f.write("\n")
        f.write("Eyes: " + c.eye_color)
        f.write("\n")

        # override any background result which would take literacy away
        if c.pClass in ["Mage", "Illusionist", "Cleric", "Druid"]:
            c.literate = True
        if c.literate:
            f.write("Literate: Yes\n")
        else:
            f.write("Literate: No\n")
        
        base_money = Decimal(20) + Decimal(randint(2,6) * 10)
        actual_money = base_money * c.money_mult
        f.write("Starting money: " + str(actual_money) + " gold pieces")
        f.write("\n")
        f.write("Credit: " + str(c.credit) + " gold pieces")
        f.write("\n")


        # actual encumbrance
        # this must be done after detail calculation,
        # in case one of those alters the max encumbrance from the base value (as certain strength results can do)
        enc_nopenalty, enc_minus1, enc_minus2, enc_minus3 = encumbrance_penalty_cutoffs(c.max_encumbrance)

        # however, final weight must be calculated AFTER encumbrance,
        # since if the character's weight is modified to be fat,
        # encumbrance SHOULD NOT take that into account.
        feet, inches = inches_to_feet_and_inches(c.height)
        f.write("Height: " + str(feet) + " ft. " + str(inches) + " in.")
        f.write("\n")
        # todo more robust check: there could in the future be a result where weight_mult is BELOW 1 (result of starvation, prison, etc.)
        if c.weight_mult == Decimal(1):
            # weight is normal; character has not grown fat
            f.write("Weight: " + str(c.weight) + " lbs")
            f.write("\n\n")
        else:
            old_weight = c.weight
            adjusted_weight = c.weight * c.weight_mult
            diff = adjusted_weight - old_weight
            f.write("Weight: " + str(adjusted_weight) + " lbs; " + str(diff) + " lbs of this is fat, and counts against encumbrance!")
            f.write("\n\n")
        f.write("Encumbrance Information:")
        f.write("\n")
        f.write("Carried weight <= " + str(enc_nopenalty) + " lbs: no AP penalty.")
        f.write("\n")
        f.write(str(enc_nopenalty) + " lbs < carried weight <= " + str(enc_minus1) + " lbs: -1 AP.")
        f.write("\n")
        f.write(str(enc_minus1) + " lbs < carried weight <= " + str(enc_minus2) + " lbs: -2 AP.")
        f.write("\n")
        f.write(str(enc_minus2) + " lbs < carried weight <= " + str(enc_minus3) + " lbs: -3 AP.")
        f.write("\n")
        f.write(str(enc_minus3) + " lbs < carried weight <= " + str(c.max_encumbrance) + " lbs: -4 AP.")
        f.write("\n")
        f.write("Above that, no movement is possible, regardless of remaining AP.")

        if c.pClass == "Mage":
            f.write("\n\n")
            f.write("Pick one of these first-level spells:\n")
            for p in mage_spells.get_pickable_spells(c.Intelligence):
                f.write(p)
                f.write('\n')

if __name__ == "__main__":
    main()
