from random import *
from decimal import *
from collections import namedtuple

getcontext().prec = 3

def getGenderWords(sex):
    if sex == "Male":
        return ("he","him", "his")
    else:
        return ("she","her","her")

# based on Strength
def detailFeats(magnitude, player):
    bigPercent = choice([30,40])
    smallPercent = choice([10,20])
    result = ""
    subj, obj, poss = getGenderWords(player.sex)
    if magnitude == -17:
        result = "Cannot move faster than normal speed."
    elif magnitude <= -14:
        result = "When stunned, must make save against Paralyzation to end the stun and rejoin combat."
    elif magnitude <= -12:
        result = "Character is forever incapable of swimming, regardless of character class or skills."
    elif magnitude <= -11:
        result = "Poor endurance. Character cannot run for more than 1 round at a time, no matter " + poss + " Constitution score."
    elif magnitude <= -10:
        result = "One-handed melee weapons must be used two-handed (even daggers); two-handed melee weapons suffer the non-proficiency penalty (if already nonproficient with a given weapon, increase its penalty by 50%, round down.)"
    elif magnitude <= -9:
        result = "Encumbrance limits reduced by " + str(bigPercent) + "%."
        player.maxEncumbrance = player.maxEncumbrance * Decimal(0.01 * (100 - bigPercent))
    elif magnitude <= -8:
        result = "Too weak to draw or load any bow or crossbow."
    elif magnitude <= -7:
        result = "One-handed melee weapons must be used two-handed (except daggers); two-handed melee weapons have a -1 penalty to attack and damage."
    elif magnitude <= -6:
        result = "Encumbrance limits reduced by " + str(smallPercent) + "%."
        player.maxEncumbrance = player.maxEncumbrance * Decimal(0.01 * (100 - smallPercent))
    elif magnitude <= -5:
        result = "Too weak to draw a longbow or load a heavy crossbow."
    elif magnitude <= -4:
        result = "Poor cardiovascular health. Character can only hold breath for 1/3 of the normal time."
    elif magnitude <= -2:
        result = "Weak arms and legs. Treat character's Dexterity as half its actual value (round down) for the purpose of no-fault climbing. Danger climbing ability is reduced by " + str(randint(10,15)) + "%." 
    elif magnitude <= -1:
        result = "Throwing weapons deal 1 less damage (minimum 0.)"
    elif magnitude <= 1:
        result = "Throwing weapons deal 1 extra damage."
    elif magnitude <= 3:
        result = "Strong arms and legs. Treat character's Dexterity as 50% higher (round down) for no-fault climbing."
    elif magnitude == 4:
        result = "Strong hands and arms allow a 50% chance to spend 3 fewer AP when loading a crossbow."
    elif magnitude <= 6:
        result = "Character is capable of swimming."
    elif magnitude <= 8:
        result = "Encumbrance limits increased by " + str(smallPercent) + "%."
        player.maxEncumbrance = player.maxEncumbrance * Decimal(0.01 * (100 + smallPercent))
    elif magnitude <= 9:
        result = "Strong upper body. For slings, bows (not crossbows), and all thrown weapons, increase close range by 1 hex, medium range by 10%, and long range by 20%."
    elif magnitude <= 11:
        result = "Can hold breath for three times the normal duration."
    elif magnitude <= 13:
        result = "Powerful muscles add +3 on rolls made to escape manacles, ropes, or other constraints."
    elif magnitude <= 15:
        result = "Each day, the first time the character is stunned, after rejoining combat " + subj + " gains +2 to melee attack and damage for 10 rounds."
    else:
        result = "Each day, the first time the character is stunned, after rejoining combat " + subj + " gains hysterical strength. Roll 1d3+1: for 10 rounds, character gains that amount as a bonus to melee attack and damage."
    return result

manAtArmsWeapons = ["dagger","club","quarterstaff","sling"] * 3 + ["shortbow","shortsword","longsword","mace","bastard sword","greatsword"]
manAtArmsArmor = ["no armor"] * 2 + ["gambeson"] * 4 + ["leather armor"] * 3 + ["studded leather"] * 2 + ["haubergeon"]

def manAtArmsEquipment():
    numWeapons = 1 if randint(1,10) < 7 else 2
    weapons = sample(manAtArmsWeapons, numWeapons)
    armor = choice(manAtArmsArmor)
    equipment = namedtuple("equipment",["weapons","armor"])
    return equipment(weapons,armor)

# based on Wisdom
def detailInterpersonal(magnitude, player):
    subj, obj, poss = getGenderWords(player.sex)
    townDir = choice(["north","south","east","west"])
    result = ""
    if magnitude == -17:
       result = "The character inadverdently revealed information to the enemy of the land where they are from, enabling that enemy to invade and seize wealth and property. A death sentence has been laid upon the character."
    elif magnitude == -16:
        result = "Ill-considered opinions and bad intentions caused the character to be excommunicated from " + poss + " original religion. " + subj.capitalize() + " is marked as an apostate and all sites of organized worship will shun " + obj + "."
    elif magnitude <= -14:
        crimes = ["murdered a peasant, and is being sought to receive lashes and time in the stocks.",
                  "damaged property, and is being sought to pay restitution and receive time in the stocks.",
                  "committed petty theft, and is being sought to receive lashes and pay restitution.",
                  "murdered a merchant, and is being sought for prison time and a hefty fine.",
                  "committed a serious theft, and is being sought to pay restitution and to have a hand chopped off.",
                  "murdered a noble, and is being sought for execution."]
        roll = randint(1,20)
        resultStart = "Character has "
        if roll <= 3:
            result = resultStart + crimes[0]
        elif roll <= 7:
            result = resultStart + crimes[1]
        elif roll <= 11:
            result = resultStart + crimes[2]
        elif roll <= 14:
            result = resultStart + crimes[3]
        elif roll <= 18:
            result = resultStart + crimes[4]
        else: # 19 and 20
            result = resultStart + crimes[5]
    elif magnitude == -13:
        result = "Character's strange proclivities and morals prevent the character from retaining hirelings for more than a month. Henchmen and followers received from leveling up are not affected."
    elif magnitude <= -11:
        result = "Character is exiled from " + poss + " homeland, and will face a life sentence or execution if they return, although " + poss + " only 'crime' is that of having powerful enemies."
    elif magnitude <= -9:
       enemyFamilyMember = ["wife"] * 9 + ["daughter"] * 10 + ["mother"] * 1
       sexCutoff = 1
       if player.sex == "Female":
           sexCutoff = 11
       enemyReasons = [("foolishly slept with the enemy's " + choice(enemyFamilyMember) + ", making her pregnant."),
                       "stole a large sum of money from the enemy, and then lost it.",
                       "destroyed a possession which the enemy held in great personal significance."] 
       roll = randint(sexCutoff,20)
       resultStart = "The character is pursued by a sworn enemy, who seeks revenge for the character having "
       if roll <= 10:
           result = resultStart + enemyReasons[0]
       elif roll <= 15:
           result = resultStart + enemyReasons[1]
       else:
           result = resultStart + enemyReasons[2]
    elif magnitude <= -8:
        if player.hasFamily:
            result = "Character has been ostracized by " + poss + " family because of " + poss + " poor decisions. The character has no access to any family possessions or talents."
        else:
            result = "Character has been ostracized by " + poss + " mentor because of " + poss + " poor decisions. The character's training was incomplete, so " + subj + " has no weapon proficiencies."
    elif magnitude <= -6:
        result = "People in this area treat the character with profound dislike. Thus, " + subj + " has been banned from all town establishments save the market."
    elif magnitude == -5:
        result = "Word has spread that the character's word cannot be trusted. " + subj.capitalize() + " will be unable to obtain hirelings or make contracts in this town."
    elif magnitude == -4:
        if player.hasFamily:
            result = "Family members strongly dislike the character, and will provide nothing more than a night's lodging, no more than once every every six months."
        else:
            result = "Character's occasional displays of foolishness means that hirelings and followers will take twice as long to earn morale increases for extended service. "
    elif magnitude <= -2:
        num = randint(3,8)
        result = "A group of " + str(num) + " local tough guys have been threatening and harassing the character whenever they can. These toughs certainly have class levels, but aren't too powerful."
    elif magnitude == -1:
        result = "The character's conduct has led to " + poss + " being banned from inns and taverns in this town."
    elif magnitude == 0:
        if player.hasFamily:
            result = "Family members treat the character as hopeless and without prospects, but will provide lodging. Any brothers and sisters will work as hirelings, but will start with a morale of only 7."
        else:
            result = "Hirelings are made uneasy by character's small-mindedness. Base morale will be 1 point below normal, even if they are gained through this generator."
    elif magnitude == 1:
        result = "Character has made friends with a man-at-arms, who has a morale of 8."
    elif magnitude <= 3:
        if player.hasFamily:
            result = "Family members treat the character and " + poss + " friends well, and look forward to news and visits. Brothers, sisters, and cousins will work as hirelings with a starting morale of 9."
        else:
            lover = "daughter"
            if player.sex == "Female":
                lover = "son"
            result = "The character is loved by the " + lover + " of an artisan."
    elif magnitude == 4:
        result = "Character has made friends with two men-at-arms, who have a morale of 9."
    elif magnitude == 5:
        result = "Character is well-known and liked around these parts. Can easily obtain as many hirelings as needed (normally each one requires a reaction roll.) Limits based on town size still apply."
    elif magnitude == 6:
        if player.hasFamily:
            result = "Character is the family favorite and will receive regular gifts from home. The family will look forward to news and visits, and treat the character's friends well. All family members will work as hirelings, with starting morale of 10."
        else:
            result = "Character has a particularly warm relationship with the mentor who taught " + obj + " class skills. The mentor will help find hirelings or procure items when the character is in town."
    elif magnitude == 7:
        result = "Locals treat the character as a wise teacher, and will seek him or her out for advice. There is a 50% chance for the character to obtain a night's lodging for free each time he or she visits."
    elif magnitude == 8:
        result = "Character enjoys the favor of local farmers and peasants, and can count on a night's free lodging on each visit. Prices at nearest market are 10% lower for him or her."
    elif magnitude == 9:
        result = "Character is so popular here that " + subj + " can count on free lodging indefinitely no matter how long the stay. This also applies to any area in which " + subj + " lives for at least 6 straight months."
    elif magnitude <= 11:
        guild = choice(["alchemist","stonemason","merchant","blacksmith"])
        result = "Character has made influential contacts in the local " + guild + " guild, and can count on a favor related to that industry."
    elif magnitude == 12:
        result = "Character has received the notice of the local government. The character may seek one favor."
    elif magnitude <= 14:
        num = randint(3,5)
        result = "Character has made friends with " + str(num) + " men-at-arms, who have a morale of 10."
    elif magnitude <= 16:
        result = "Character has been made a member of the Illuminati."
    else:
        result = "Events surrounding the character have caused people to believe that the character had a major part in a religious miracle. The character has received the goodwill of the highest religious figure in the land, and may seek one favor."
    return result

# based on Wisdom
def detailTendency(magnitude, player):
    subj, obj, poss = getGenderWords(player.sex)
    result = ""
    if magnitude == -17:
        num = randint(6,8) * -1
        result = "Character is deeply ignorant and superstitious. Saves against fear and mind-affecting spells suffer a " + str(num) + " penalty."
    elif magnitude == -16:
        num = randint(3,5) * -1
        result = "Character is foolish, ignorant, and superstitious. Saves against fear and mind-affecting spells suffer a " + str(num) + " penalty."
    elif magnitude <= -14:
        result = "Character is cowardly and lacks confidence. If stunned, a save must be made vs. Paralyzation, or else the character will avoid all combat, including spellcasting, for 1d4 rounds."
    elif magnitude == -13:
        result = "Character has an awful temper. If character's weapon breaks or if he or she is hit by friendly fire, a save vs. Magic must be made; otherwise, for 1d4+1 rounds, the character will be -3 to hit, +1 to damage, and unaffected by fear, morale, or attempts to communicate."
    elif magnitude <= -11:
        weightGain = Decimal(1) + Decimal(randint(15,25) * 0.01)
        result = "Gluttony and laziness has caused the character to gain fat."
        player.weightMult *= weightGain
    elif magnitude <= -9:
        result = "Gullibility causes the character to frivolously spend and give away money. Whenever " + subj + " goes to market, if a Wisdom check is not successful, the character will lose 5d4 gold to the likes of confidence men, beggars, and snake-oil salesmen."
    elif magnitude <= -7:
        result = "Character's Wisdom is treated as 2 points lower when resisting seduction."
    elif magnitude <= -5:
        result = "Character is overly cautious about combat. Must succeed at a Wisdom check before being able to make attacks (including discharging offensive spells) in a given combat. Check can be attempted on character's turn each round."
    elif magnitude <= -3:
        ungained = randint(2,3) * 5
        result = "Character has not quite completed " + poss + " training, and starts the game with negative experience equal to " + str(ungained) + "% of the number needed to attain 2nd level."
    elif magnitude <= -1:
        result = "Should the character sample an addictive substance, the Wisdom check to determine addiction is made with a -3 penalty."
    elif magnitude == 0:
        result = "A painful love affair has left the character emotionally toughened. " + poss.capitalize() + " Wisdom is treated as 2 points higher when resisting seduction."
    elif magnitude == 1:
        result = "Character has a +3 bonus on Wisdom checks to avoid addiction."
    elif magnitude == 2:
        result = "Character is able to identify the exact time of day, to the half-hour, when out of doors."
    elif magnitude == 3:
        result = "Character has the ability to counsel others, which will give them a +2 bonus on their next save against addiction, overcaution in combat, or gullibility."
    elif magnitude <= 5:
        result = "The character's good will causes all hirelings and followers within five hexes to have +1 morale."
    elif magnitude == 6:
        xp = randint(6,9) * 50
        result = "If the character's class gives 10% bonus XP for high scores, but the character's scores are not high enough, or if " + poss + " class does not offer that bonus, the character receives 10% bonus XP. If they already qualify for 10% bonus XP, they instead begin adventuring with " + str(xp) + " XP."
    elif magnitude == 7:
        result = "When the possibility arises, a successful save vs. Poison will reveal to the character the location of a cursed item or location within 50 feet."
    elif magnitude <= 9:
        result = "Character can detect secret and concealed doors. Merely passing within 10 feet gives a 1/6 chance to notice it; actively searching an area gives a 2/6 chance."
    elif magnitude == 10:
        secret = choice(["the location of buried or hidden treasure",
                         "a secret shrine to a demon or obscure god",
                         "the location of an area which is haunted",
                         "the location of a magic portal"])
        result = "Character possesses secret knowledge: " + secret + "."
    elif magnitude <= 12:
        result = "One time per week, if the character failed to purchase some item at the last-visited marketplace which would be useful now, the character is considered to have done so."
    elif magnitude <= 15:
        result = "Character is able to overcome being stunned in combat, once per day."
    elif magnitude == 16:
        bonus = randint(2,4)
        result = "Character is very pious. All saves against fear and mind-affecting spells are made with a +" + str(bonus) + " bonus."
    else:
        bonus = randint(5,7)
        result = "Character is very pious. All saves against fear and mind-affecting spells are made with a +" + str(bonus) + " bonus."
    return result

def makeSibling():
    ageDiff = randint(1,6)
    sibling = choice(["brother","sister"]) + " who is " + str(ageDiff) + " years " + choice(["older","younger"])
    return sibling

def getSiblings(num):
    if num == 0:
        return "no siblings"
    else:
        acc = []
        while num > 0:
            acc.append(makeSibling())
            num = num - 1
        res = ", ".join(acc)
        return res


grandparents = ["paternal grandfather","paternal grandmother","maternal grandfather","maternal grandmother"]
def getGrandparents(num):
    if num == 0:
        return "no grandparents"
    if num == 4:
        return "all grandparents"
    else:
        res = ", ".join(sample(grandparents,num)) + ""
        return res

# based on Strength
def detailFamily(magnitude,c):
    result = ""
    if magnitude <= -7:
       result = "Orphan. No known relatives."
       c.hasFamily = False
    elif magnitude <= -1:
        uncle = randint(0,1)
        aunt = randint(0,1)
        combined = uncle + aunt
        resultStart = "Few living relations: "
        if uncle == 1 and aunt == 1:
           result = resultStart + "character has an aunt and uncle."
        elif uncle == 1:
            result = resultStart + "character has an uncle."
        elif aunt == 1:
            result = resultStart + "character has an aunt."
        else:
            roll = randint(2,4)
            result = resultStart + "character has " + str(roll) + " cousins."
    elif magnitude == 0:
        relative = choice(["grandparents"] * 3 + ["aunt and uncle"] * 2 + ["grandfather", "grandmother", "aunt", "uncle"])
        matPat = choice(["on father's side","on mother's side"])
        raisedBy = relative + " " + matPat
        numCousins = randint(1,4) + randint(1,4) - 2
        result = "Character raised by " + (raisedBy) + ". Number of first cousins: " + str(numCousins) + "."
    elif magnitude == 1:
        parent = choice(["father","mother"])
        hasGrandparent = choice([True,False])
        if hasGrandparent:
            grandparent = choice(["paternal","maternal"]) + " " + choice(["grandfather","grandmother"])
        else:
            grandparent = "no grandparents"
        hasSibling = choice([True,False])
        if hasSibling:
            sib = makeSibling()
        else:
            sib = "no siblings"
        result = "Character raised by " + parent + ". Has " + grandparent + "; " + sib + "."
    elif magnitude == 2:
        parents = choice(["mother and father","mother and father","mother","father"])
        grands = getGrandparents(randint(0,2))
        hasSib = choice([True,False])
        if hasSib:
            sib = makeSibling()
        else:
            sib = "no siblings"
        result = "Character raised by " + parents + ". Has " + grands + "; " + sib + "."
    elif magnitude <= 4:
       grands = getGrandparents(randint(0,3)) 
       numsibs = randint(0,2) + randint(0,2)
       sibs = getSiblings(numsibs)
       result = "Character raised by mother and father. Has " + grands + "; " + sibs + "."
    elif magnitude <= 6:
        grands = getGrandparents(randint(0,4))
        numsibs = randint(0,3) + randint(0,3)
        sibs = getSiblings(numsibs)
        result = "Character raised by mother and father. Has " + grands + "; " + sibs + "."
    elif magnitude <= 8:
        grands = getGrandparents(randint(1,4))
        numsibs = randint(0,4) + randint(0,4)
        sibs = getSiblings(numsibs)
        result = "Character raised by mother and father. Has " + grands + "; " + sibs + "."
    elif magnitude <= 10:
        grands = getGrandparents(randint(2,4))
        numsibs = randint(0,5) + randint(0,5)
        sibs = getSiblings(numsibs)
        result = "Character raised by mother and father. Has " + grands + "; " + sibs + "."
    elif magnitude <= 12:
        grands = getGrandparents(randint(2,4))
        numsibs = randint(0,6) + randint(0,6)
        sibs = getSiblings(numsibs)
        result = "Character raised by mother and father. Has " + grands + "; " + sibs + "."
    elif magnitude <= 14:
        grands = getGrandparents(randint(2,4))
        numsibs = randint(0,7) + randint(0,7)
        sibs = getSiblings(numsibs)
        result = "Character raised by mother and father. Has " + grands + "; " + sibs + "."
    else:
        grands = getGrandparents(randint(2,4))
        numsibs = randint(1,7) + randint(1,7)
        sibs = getSiblings(numsibs)
        result = "Character raised by mother and father. Has " + grands + "; " + sibs + "."
    return result

# based on Intelligence
def detailChoices(magnitude, player):
    subj, obj, poss = getGenderWords(player.sex)
    result = ""
    whichHalf = choice(["right","left"])
    if magnitude <= -16:
        result = "Character is missing lower half of " + whichHalf + " leg, and has a peg leg. One less AP than normal."
    elif magnitude <= -14:
        result = "Character is missing left hand. Cannot use two-handed weapons. Can choose hook-hand as a weapon proficency, but does not start with one to use."
    elif magnitude == -13:
        result = "Character is missing " + whichHalf + " eye. Ranged weapons have attack penalty: -1 at close range, -4 at medium, -10 at long."
    elif magnitude == -12:
        m = randint(1,8) + randint(1,8) + randint(1,8) + randint(1,8)
        result = "Character has spent " + str(m) + " miserable years in prison."
        player.addedAge += m
    elif magnitude ==  -11:
        h = randint(1,6) + randint(1,6) + randint(1,6)
        result = "Character has spent " + str(h) + " hard years in prison."
        player.addedAge += h
    elif magnitude == -10:
        p = randint(1,4) + randint(1,4)
        result = "Character has spent " + str(p) + " years in prison."
        player.addedAge += p
    elif magnitude == -9:
        num = randint(1,3)
        result = "Missing " + str(num) + " fingers on " + whichHalf + " hand. -2 on attack rolls when using that hand (including two-handed weapons.)"
    elif magnitude == -8:
        num = randint(2,3)
        result = "Missing " + str(num) + " toes on " + whichHalf + " foot. -1 penalty on all Dexterity checks involving the feet."
    elif magnitude == -7:
        months = randint(3,9)
        if player.sex == "Male":
            result = "Character has fathered a child out of wedlock. The mother is " + str(months) + " months pregnant."
        else:
            result = "Character is pregnant and " + str(months) + " months along."
    elif magnitude == -6:
        result = "Character has been swindled of all money and possessions, leaving " + obj + " with only shirt-underwear and breeches."
        player.moneyMult = Decimal(0)
    elif magnitude == -5:
        result = "Trust and generosity to family or others has left the character with little money."
        player.moneyMult = player.moneyMult * Decimal(0.3)
    elif magnitude == -4:
        ozTobacco = randint(1,3)
        ozLiquor = randint(2,4) + randint(1,6) + randint(1,6)
        ozBeer = ozLiquor * randint(3,4)
        isCig = choice([True,False])
        consequence = "until the addiction is fed each day, the character's Wisdom will be treated as 50% normal, and other stats will be treated as 90% normal."
        if isCig:
            result = "Character is addicted to " + str(numCigarettes) + " oz. of tobacco per day; " + consequence
        else:
            result = "Character is addicted to " + str(ozLiquor) + " fl oz. of liquor per day (or " + str(ozBeer) + " fl oz. of beer); " + consequence
    elif magnitude == -3:
        if player.sex == "Male":
            p = "fathered"
        else:
            p = "mothered"
        kidGender = choice(["son","daughter"])
        result = "Character has " + p + " a bastard child, a " + kidGender + ". If character has family, child is in their care; otherwise child was given up as a foundling, and its whereabouts are unknown."
    elif magnitude == -2:
        result = "Gambling, waste, and foolishness has lost the character half " + poss + " money."
        player.moneyMult = player.moneyMult * Decimal(0.5)
    elif magnitude == -1:
        years = randint(2,5)
        result = "A misspent youth cost the character " + str(years) + " extra years to finish training."
        player.addedAge += years
    elif magnitude == 0:
        scar = randint(3,8)
        result = "Character has a " + str(scar) + "-inch scar on a normally-covered part of " + poss + " body, received as a child during a moment of pure stupidity."
    elif magnitude <= 2:
        result = "Good luck has slightly increased the character's money."
        player.moneyMult *= Decimal(2)
    elif magnitude <= 4:
        result = "Ability to play a musical instrument of the player's choosing."
    elif magnitude == 5:
        dir = choice(["north","south","east","west"])
        result = "Distinguished effort has earned a writ of passage, free of tolls, between this kingdom and the nearest one to the " + dir + "."
    elif magnitude <= 7:
        result = "Prudence and savings have significantly increased the character's money."
        player.moneyMult *= Decimal(3)
    elif magnitude <= 9:
        credit = (randint(1,6) + randint(1,6) + randint(1,6)) * 50
        interestAmount = randint(6,8)
        result = "Character possesses credit with the local merchant guild, borrowable at " + str(interestAmount) + "% monthly interest."
        player.credit = credit
    elif magnitude <= 11:
        num = randint(4,6)
        result = "Prudence and savings have greatly increased the character's money."
        player.moneyMult *= Decimal(num)
    elif magnitude <= 13:
        num = randint(6,9)
        result = "Diligent effort has hugely increased the character's money."
        player.moneyMult *= Decimal(num)
    elif magnitude == 14:
        result = "Character possesses a magic item."
    elif magnitude <= 16:
        num = randint(9,12)
        result = "Smart and frugal behavior has grown the character's money to an incredible degree."
        player.moneyMult *= Decimal(num)
    else:
        title = choice(["an academic degree", "former advisor to the nobility"])
        result = "Character has gained a title or honor through work done during training: " + title + ". The character adds 1d6 points to one skill within " + poss + " 1st-level focus, representing the knowledge they cultivated to earn the title."
    return result


# based on Charisma, requires two magnitude rolls 
def detailBeauty(faceMag, bodyMag, player):
    # to be added on to
    subj, obj, poss = getGenderWords(player.sex)
    def faceBeauty():
        whichSide = choice(["right","left"])
        if faceMag <= -15:
            scarLength = randint(3,7)
            scarType = choice(["a blade", "an animal bite", "an animal's claws"])
            scar = "has " + str(scarLength) + "-inch scar across the face, received from " + scarType
            choices = [scar,"is missing " + poss + " " + whichSide + " ear","is missing " + poss + " nose","has a distinctly misshapen head"]
            return choice(choices)
        elif faceMag <= -8:
            choices = ["has a lazy " + whichSide + " eye","has a whiny, irritating voice","has a crackly, annoying voice","suffers from halitosis if teeth are not brushed 3 times daily","has an always-runny nose","has a greasy, oily face"]
            return choice(choices)
        elif faceMag <= -1:
            noseProblem = choice(["bulbous","squashed","piggish"])
            missingTeeth = randint(0,1) + randint(1,3)
            teethProblem = choice(["buck","crooked",str(missingTeeth) + " missing"])
            choices = ["has bushy eyebrows","has a caveman-like protruding brow","has distinctly large ears","has a " + noseProblem + " nose","has " + teethProblem + " teeth","has acne scars","has eyes which are unnervingly close together"]
            return choice(choices)
        elif faceMag <= 7:
            choices = ["has a beautiful aquiline nose","has attractively straight teeth","has a clean and healthy complexion"]
            if player.sex == "Male":
                choices = choices + ["has a strong chin"]
            else:
                choices = choices + ["has lovely full lips"]
            return choice(choices)
        elif faceMag <= 13:
            choices = ["perfectly-shaped, brilliantly white teeth","marvelous high cheekbones"]
            if player.sex == "Male":
                choices = choices + ["a deep, compelling voice","a strong jawline"]
            else:
                choices = choices + ["a throaty, seductive voice","charmingly delicate features"]
            return ("has " + choice(choices))
        else:
            choices = ["has a rich, velvety voice","has dazzling eyes","has a flawless complexion"]
            return choice(choices)

    def bodyBeauty():
        # redefine whichSide so it can be different for face and body results
        whichSide = choice(["right","left"])
        if bodyMag <= -16:
            burnPercent = randint(20,80)
            return "has nasty burn scars covering " + str(burnPercent) + "% of " + poss + " body"
        elif bodyMag <= -14:
            scarLength = randint(2,6)
            scarPlace = choice([whichSide + " cheek","chin","throat","nose","forehead"])
            scar = "has a " + str(scarLength) + "-inch scar across " + poss + " " + scarPlace
            choices = [scar, "gives off a nasty, unwashable odor","has lumpy limbs","has a misshapen torso","is a hunchback"]
            return choice(choices)
        elif bodyMag <= -8:
            scarLength = randint(1,3)
            scarPlace = choice([whichSide + " arm",whichSide + " hand","scalp","chin"])
            scar = "has a " + str(scarLength) + "-inch scar across " + poss + " " + scarPlace
            choices = [scar,"is bow-legged","is knock-kneed","moves with an awkward, loping gait","has a sunken chest"]
            return choice(choices)
        elif bodyMag <= -1:
            choices = ["has a weak " + whichSide + " leg and walks with a pronounced limp","has a swayback","has a overlong torso with stumpy legs","has a stumpy torso with overlong legs"]
            return choice(choices)
        elif bodyMag == 0:
            footKind = choice(["very small feet (-5% footwear cost)", "small feet","large feet","very large feet (+5% footwear cost)"])
            freckleCount = choice(["scattered","many","excessive"])
            choices = ["has " + footKind,"has " + freckleCount + " freckles"]
            return choice(choices)
        elif bodyMag <= 7:
            choices = ["gives off a pleasant body odor","has well-proportioned legs and arms","has an elegant neck","has healthy, glossy hair"]
            return choice(choices)
        elif bodyMag <= 13:
            if player.sex == "Male":
                choices = ["has wide shoulders","has a broad back","has muscular arms","has muscular legs", "has a six-pack"]
            else:
                choices = ["has a flat, toned belly","has strong thighs","has a narrow waist","has wide, curvy hips"]
            return choice(choices)
        else:
            choices = ["has radiant skin","has luxurious hair","always has perfect posture"]
            return choice(choices)
    # putting it all together
    faceResult = "Character " + faceBeauty()
    bodyResult = ", and also " + bodyBeauty()
    result = faceResult + bodyResult + "."
    return result

# helper for healthDetail
def getHealthCondition(roll):
    # the higher the number, the more severe the condition
    # the idea is to use these with a random roll in the specified range
    if roll <= 2:
        return "Motion sickness: repeated waves of nausea and vomiting will occur with the rhythmic motion of any vehicle."
    elif roll <= 4:
        return "Flaring pain in joints: character finds outdoor travel difficult, and will suffer an extra point of damage each day when traveling."
    elif roll <= 6:
        return "Low tolerance for alcohol: character takes 1d3 damage for each 8 ounces consumed."
    elif roll <= 8:
        return "Dry and flaky skin: while armored, character will suffer 1 damage per two hours spent walking or riding."
    elif roll <= 10:
        return "Weak stomach: character will suffer 1 point of damage per pound of food eaten which is raw or unprocessed."
    elif roll == 11:
        return "Muscle pulls: after each combat, character must save vs. paralyzation or suffer a -1 penalty to attacks for 3 days due to a pulled muscle. Multiple occurrences stack up to -3."
    elif roll == 12:
        colors = choice([["red","orange","green"],["blue","purple","black"]])
        sentenceTail = ", ".join(colors)
        return "Color confusion: character cannot distinguish between " + sentenceTail + "."
    elif roll == 13:
        return "Color blindness: character cannot distinguish between any colors of the spectrum. Everything appears to be in shades of gray."
    elif roll <= 15:
        return "Tone deafness: character cannot distinguish chords of sound, and thus receives neither positive nor negative effects of music."
    elif roll == 16:
        return "Chronic migraines: each day, the character has a 1 in 20 chance of being -5 to hit and -3 to saves and ability checks."
    elif roll <= 18:
        return "Mild hemorrhaging: if wounded, the character will bleed 1 extra HP per round. If bandages are used, character's wounds must be bound twice in order to stop the bleeding."
    elif roll == 19:
        return "Shortened breath: character is unable to run for more than two rounds. If any strenuous activity (such as combat) continues for more than 10 rounds, the character must succeed at a save vs. death or else be struck with a coughing spasm, incapacitating them for 1 round (counts as stunned) and causing 3d4 damage."
    elif roll == 20:
        return "Brittle bones: all falling damage dice for the character are increased by one step (e.g. d6 -> d8)."
    elif roll == 21:
        return "Cataracts: character cannot make out any detail further away than 60 feet, and cannot target attacks or spells beyond that range."
    elif roll == 22:
        return "Major hemorrhaging: if wounded, the character will bleed 2 extra HP per round. If bandages are used, character's wounds must be bound three times in order to stop the bleeding."
    elif roll == 23:
        return "Complete deafness: character cannot hear any sound at all, and will be unable to respond to or be affected by sound. Character can still sense vibration."
    elif roll == 24:
        return "Oversensitive skin: due to extreme discomfort, character cannot wear any kind of armor."
    elif roll == 25:
        return "Temporary demonic possession: while talking to strangers, character may suddenly lapse into abusive outbursts. 1 in 20 chance per round."
    elif roll <= 27:
        return "Weak heart: if reduced to -6 or fewer HP, character must make save vs. death or suffer a heart attack and die."
    elif roll == 28:
        return "Severe hemorrhaging: if wounded, the character will bleed 3 extra HP per round. If bandages are used, character's wounds must be bound four times in order to stop the bleeding."
    elif roll == 29:
        return "Blindness: character cannot see at all, and is altogether unable to sense light. Chief among the consequences is that all attacks are treated as if attacking invisible creatures (-8 normally, -4 if someone spends their turn helping to direct your strikes) and that all missile/thrown attacks which miss can cause friendly fire, in any direction."
    else:
        return "Crippled legs: while the character's legs appear whole and undamaged, they are in fact entirely without feeling or strength. The character cannot walk under their own power."


def detailHealth(magnitude, player):
    subj, obj, poss = getGenderWords(player)
    # get 4 health conditions, each with different possibilities of being mild or severe
    condition4 = getHealthCondition(randint(24,30))
    condition3 = getHealthCondition(randint(16,24))
    condition2 = getHealthCondition(randint(8,16))
    condition1 = getHealthCondition(randint(1,8))
    result = ""
    if magnitude <= -16:
        result = condition4
    elif magnitude <= -12:
        result = condition3
    elif magnitude <= -7:
        result = condition2
    elif magnitude <= -1:
        result = condition1
    elif magnitude == 0:
        numDays = randint(7,14)
        result = "Character is suffering from a head cold at the start of the campaign. For the next " + str(numDays) + " days, character will be -2 to attack and damage."
    elif magnitude == 1:
        result = "Character saves vs. poison as if one level higher."
    elif magnitude == 2:
        result = "Character saves vs. paralysis and petrification as if one level higher."
    elif magnitude == 3:
        result = "Character saves vs. death as if one level higher."
    elif magnitude == 4:
        result = "Character saves vs. magic as if one level higher."
    elif magnitude == 5:
        source = choice(["snake or reptile","insect"])
        result = "Character is resistant against " + source + " poison/venom. Damage is reduced by 50%."
    elif magnitude == 6:
        source = choice(["marine creature","spider"])
        result = "Character is resistant against " + source + " poison/venom. Damage is reduced by 50%."
    elif magnitude <= 8:
        result = "Character heals an extra HP from a day's rest."
    elif magnitude == 9:
        result = "Character saves vs. poison as if two levels higher."
    elif magnitude == 10:
        result = "Character saves vs. paralysis and petrification as if two levels higher."
    elif magnitude == 11:
        result = "Character saves vs. death as if two levels higher."
    elif magnitude == 12:
        result = "Character saves vs. magic as if two levels higher."
    elif magnitude <= 14:
        result = "Character heals 2 extra HP from a day's rest."
    elif magnitude == 15:
        result = "Character saves against everything as if one level higher."
    elif magnitude == 16:
        result = "Character saves against everything as if two levels higher."
    elif magnitude == 17:
        result = "Character saves against everything as if three levels higher."
    return result

# governed by Dex
def detailAgility(magnitude, player):
    subj, obj, poss = getGenderWords(player)
    whichSide = choice(["right","left"])
    result = ""
    if magnitude == -17:
        result = "Fused bones in the character's " + whichSide + " leg causes a severe, dragging limp. Normal movement is reduced by 2."
    elif magnitude == -16:
        result = "Character must save vs. Paralyzation before drawing a weapon; failure indicates " + subj + " cannot do it this round. No save is needed for subsequent attempts for the same weapon in the same combat." 
    elif magnitude == -15:
        result = "Character's " + whichSide + " hand is deformed and useless. Opposite hand is dominant."
    elif magnitude == -14:
        result = "Character's " + whichSide + " foot is deformed, and " + subj + " has a permanent limp. Normal movement is reduced by 1."
    elif magnitude == -13:
        result = "Character suffers from severe vertigo, and will fall unconscious if " + subj + " is positioned above a drop of 15 or more feet. Once awakened, " + subj + " will be nauseated for 2d4 rounds."
    elif magnitude == -12:
        result = "Each time the character moves among delicate objects, including in a marketplace, " + subj + " must make a save vs. Paralyzation to avoid accidentally breaking something."
    elif magnitude == -11:
        result = "Character is wholly unable to ride any mount of any kind, regardless of " + poss + " character class."
    elif magnitude == -10:
        result = "Character is unable to use two-handed weapons or weapons which strike further away than five feet."
    elif magnitude == -9:
        result = "Character is incapable of loading or working any kind of bow, crossbow, or similar mechanical device."
    elif magnitude == -8:
        num = randint(1,2)
        result = "Character suffers a -" + str(num) + " penalty to hit with all ranged weapons."
    elif magnitude == -7:
        result = "Character requires triple normal time to mount or dismount from an animal."
    elif magnitude == -6:
        result = "Character's armor class has a penalty of 2 when moving at a speed above normal."
    elif magnitude == -5:
        result = "Character requires 3 more AP than normal to load any bow."
    elif magnitude == -4:
        result = "If character causes friendly fire, it is 50% likely to be in ANY direction."
    elif magnitude == -3:
        result = "Character's clumsiness means that dropped weapons will break on 2 in 6 instead of 1 in 6."
    elif magnitude == -2:
        result = "Character requires 1 more AP than normal to draw any weapon."
    elif magnitude == -1:
        result = "Character suffers from mild vertigo. If positioned above a drop of 15 or more feet, " + subj + " will become somewhat nauseated and suffer a -1 to hit. Nausea passes 1 round after moving away."
    elif magnitude == 0:
        num = randint(1,20)
        if num <= 18:
            howHurt = "maimed"
        else:
            howHurt = "killed"
        result = "Through accidental clumsiness, the character caused a family member to be " + howHurt + "."
    elif magnitude == 1:
        result = "Character requires no AP to draw a weapon weighing 2 lbs or less."
    elif magnitude == 2:
        result = "Character requires no AP to draw a weapon weighing 3 lbs or less."
    elif magnitude == 3:
        result = "The character's penalty for shooting or throwing at long range is lessened by 1."
    elif magnitude == 4:
        result = "Character automatically takes a defensive stance when surprised, improving " + poss + " AC by 1 until no longer surprised."
    elif magnitude <= 6:
        result = "Character is quick to find an opening in enemy defenses. " + subj.capitalize() + " has an extra +1 modifier to hit opponents from the flank or rear."
    elif magnitude == 7:
        result = "Friendly fire committed by this character is ignored if the affected ally is within 20 feet."
    elif magnitude == 8:
        result = "Character has a talent for cheating at cards; base 20% chance plus more favorable of: 2% per point of Dex OR (if a thief) 1/2 of pickpocketing success target."
    elif magnitude == 9:
        result = "The character's penalty for shooting at both medium and long ranges is lessened by 1."
    elif magnitude == 10:
        result = "Character can climb poles and free-hanging ropes as if climbing an ordinary wall."
    elif magnitude == 11:
        if player.pClass == "Thief":
            result = "Character notices traps as if one level higher."
        else:
            result = "Character has a 15% chance to notice traps."
    elif magnitude == 12:
        result = "Character can catch and handle ordinary snakes if " + subj + " successfully saves vs. Poison (with a +4 bonus.)"
    elif magnitude == 13:
        num = randint(1,2)
        if num == 1:
            result = "Character gains " + obj + " a +1 bonus to hit with bolas, sling, and other weapons which are spun before throwing."
        else:
            result = "Character is +1 to hit with any weapon or object which has a splash effect, including certain orb spells."
    elif magnitude == 14:
        result = "Character requires no AP to draw a weapon weighing 5 lbs or less."
    elif magnitude == 15:
        result = "Character requires no AP to draw any weapon."
    elif magnitude == 16:
        bodyPart = choice(["hip","shoulder"])
        result = "Character can dislocate " + poss + " " + whichSide + " " + bodyPart + " at will, though doing so causes 1d4+1 damage."
    else:
        result = "Character can climb poles and free-hanging ropes, and walk tightropes, as if climbing an ordinary wall."
    return result

def birthday(age, currentYear = 1700):
    birthYear = (currentYear - age) + 1
    # the addition of 1 year here was supposed to correct so that even if the
    # characters' birthday had already passed this yar, they would still be the right age
    # but it's an off-by-one error making them too old if the birthday hasn't passed yet
    # the opposite error (making them too young) happens if we subtract 1
    # the solution, which I won't do yet, is to use not only the current day,
    # but also the current year
    leapYear = ((birthYear % 4) == 0)
    if leapYear:
        febLength = 29
    else:
        febLength = 28
    endJanuary = 31
    endFebruary = febLength + endJanuary
    endMarch = 31 + endFebruary
    endApril = 30 + endMarch
    endMay = 31 + endApril
    endJune = 30 + endMay
    endJuly = 31 + endJune
    endAugust = 31 + endJuly
    endSeptember = 30 + endAugust
    endOctober = 31 + endSeptember
    endNovember = 30 + endOctober
    endDecember = 31 + endNovember
    monthEnds = [endJanuary, endFebruary, endMarch, endApril, endMay, endJune, endJuly,
                 endAugust, endSeptember, endOctober, endNovember, endDecember]
    monthNames = ["January","February","March","April","May","June","July",
                  "August","September", "October","November","December"]
    # initialize the two-way correspondence between final ordinal day of year,
    # and name of the month whose last day is that day of the year
    monthRelations = {}
    for x in range(0,len(monthNames)):
        n = monthNames[x]
        end = monthEnds[x]
        monthRelations[n] = end
        monthRelations[end] = n

    # endDecember is also the number of days in this year
    dayOfTheYear = randint(1,endDecember)

    birthdayMonthDay = ""
    for end in monthEnds:
        if dayOfTheYear <= end:
            m = monthRelations[end]
            d = end - dayOfTheYear + 1
            # the extra 1 added to d is so that days are number 1 to end, instead of 0 to (end-1)
            birthdayMonthDay = m + " " + str(d)
            break
        else:
            pass

    return birthdayMonthDay
hairColors = ["black"] * 40 + ["brown"] * 30 + ["blonde"] * 20 + ["red"] * 10

def getBaseHairColor():
    return choice(hairColors)

def adjustHairColorForAging(baseHairColor, age, constitution):
    aging = randint(1,100)
    hair = namedtuple("hair", ["color","description"])
    baseCase = hair(baseHairColor,"")
    if age <= 20:
        return baseCase
    elif age <= 29:
        if aging > 7 * constitution:
            return hair(baseHairColor,"prematurely graying")
        else:
            return baseCase
    elif age <= 39:
        if aging > 6 * constitution:
            return hair(baseHairColor,"graying")
        else:
            return baseCase
    elif age <= 49:
        if aging > 5 * constitution:
            return hair("gray","was once " + baseHairColor)
        else:
            return baseCase
    elif age <= 59:
        if aging > 4 * constitution:
            return hair("gray", "was once " + baseHairColor)
        else:
            return hair(baseHairColor,"graying")
    else:
        return hair("gray","was once " + baseHairColor)

def hairStatusAfterAging(age, constitution, sex):
    aging = randint(1,100)

    if sex == "Male":
        if age <= 20:
            return ""
        elif age <= 29:
            if aging > 7 * constitution:
                return "bald"
            if aging > 6 * constitution:
                return "thinning"
            else:
                return ""
        elif age <= 39:
            if aging > 6 * constitution:
                return "bald"
            elif aging > 5 * constitution:
                return "thinning"
            else:
                return ""
        elif age <= 49:
            if aging > 5 * constitution:
                return "bald"
            elif aging > 4 * constitution:
                return "thinning"
            else:
                return ""
        elif age <= 59:
            if aging > 3 * constitution:
                return "bald"
            elif aging > 2 * constitution:
                return "thinning"
            else:
                return ""
        else:
            if aging > 2 * constitution:
                return "bald"
            elif aging > constitution:
                return "thinning"
            else:
                return ""
    else:
        # sex is Female
        hairIfMale = hairStatusAfterAging(age - 10, constitution, "Male")
        if hairIfMale == "bald":
            if aging > 10 * constitution:
                return "bald"
            else:
                return "wispy"
        else:
            return hairIfMale

def getEyeColor(baseHairColor):
    if baseHairColor not in hairColors:
        raise ValueError("unrecognized hair color")
    score = randint(1,100)
    if baseHairColor == "black":
        if score < 40:
            return "brown"
        elif score < 80:
            return "black"
        else:
            return "green"

    elif baseHairColor == "red":
        if score < 50:
            return "green"
        else:
            return "blue"

    elif baseHairColor =="blonde":
        if score < 50:
            return "blue"
        elif score < 75:
            return "green"
        else:
            return "brown"

    else:
        # baseHair is brown
        if score < 15:
            return "blue"
        elif score < 35:
            return "green"
        elif score < 60:
            return "brown"
        else:
            return "black"

def makeFinalHair(baseHair, age, con, sex):
    hairData = namedtuple("hair",["haircolor","hairdesc","haircond"])
    hairColorAdj = adjustHairColorForAging(baseHair, age, con)
    hairLevelAdj = hairStatusAfterAging(age, con, sex)
    if hairLevelAdj == "bald":
        return hairData("bald", "was once " + baseHair,"")
    else:
        return hairData(hairColorAdj.color, hairColorAdj.description, hairLevelAdj)
