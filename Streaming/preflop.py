# Beware: Shitty code ahead

from preflopTab import tab

def getHandType(hand: str):
    if hand[0] == hand[2]:
        return "PP"
    else:
        if hand[1] == hand[3]:
            return "Suited"
        else:
            return "Offsuit"

def letterToRank(letter):
    ranks = "23456789TJQKA"
    for i in range(13):
        if letter == ranks[i]:
            return i

def getSuitedness(hand1: str, handType1: str, hand2: str, handType2: str):
    if handType1 == "PP":
        if handType2 == "PP":
            suitCount = len(set([hand1[1], hand1[3], hand2[1], hand2[3]]))
            if suitCount == 2:
                return "Two suits"
            elif suitCount == 3:
                return "One suit"
            else:
                return "No suits"
        elif handType2 == "Suited":
            suitCount = len(set([hand1[1], hand1[3], hand2[1], hand2[3]]))
            if suitCount == 2:
                return "One suit"
            else:
                return "No suits"
        else:
            if (hand1[1] == hand2[1] and hand1[3] == hand2[3]) or (hand1[1] == hand2[3] and hand1[3] == hand2[1]):
                return "2Top"
            elif (hand1[1] == hand2[1]) or (hand1[3] == hand2[1]):
                return "1TopTop"
            elif (hand1[1] == hand2[3]) or (hand1[3] == hand2[3]):
                return "1TopBot"
            else:
                return "No suits"
    elif handType1 == "Suited":
        if handType2 == "Suited":
            if (hand1[1] == hand2[1]):
                    return "One suit"
            else:
                return "No suits"
        else:
            if hand1[1] == hand2[1] or hand1[1] == hand2[3]:
                return "1TopTop"
            elif hand1[3] == hand2[1] or hand1[3] == hand2[3]:
                return "1TopBot"
            else:
                return "No suits"
    else:
        if hand1[1] == hand2[1] and hand1[3] == hand2[3]:
            return "2Top"
        elif hand1[1] == hand2[3] and hand1[3] == hand2[1]:
            return "2Bot"
        elif hand1[1] == hand2[1]:
            return "1TopTop"
        elif hand1[1] == hand2[3]:
            return "1TopBot"
        elif hand1[3] == hand2[1]:
            return "1BotTop"
        elif hand1[3] == hand2[3]:
            return "1BotBot"
        else:
            return "No suits"

def getMainHand(hand1: str, hand2: str):
    handType1 = getHandType(hand1)
    handType2 = getHandType(hand2)
    if handType1 == "PP" or handType2 == "PP":
        if handType2 != "PP":
            return hand1
        elif handType1 != "PP":
            return hand2
        elif letterToRank(hand1[0]) >= letterToRank(hand2[0]):
            return hand1
        else:
            return hand2
    elif handType1 == "Suited" or handType2 == "Suited":
        if handType2 != "Suited":
            return hand1
        elif handType1 != "Suited":
            return hand2
        elif letterToRank(hand1[0]) > letterToRank(hand2[0]) or (letterToRank(hand1[0]) == letterToRank(hand2[0]) and letterToRank(hand1[2]) > letterToRank(hand2[2])):
            return hand1
        else:
            return hand2
    else:
        if letterToRank(hand1[0]) > letterToRank(hand2[0]) or (letterToRank(hand1[0]) == letterToRank(hand2[0]) and letterToRank(hand1[2]) > hand2[2]):
            return hand1
        else:
            return hand2

def categorizeMatchup(hand1: str, hand2: str):
    rev: bool = False
    mainHand = getMainHand(hand1, hand2)
    secondHand = None
    suitedness = None

    if mainHand == hand1:
        secondHand = hand2
    else:
        secondHand = hand1
        rev = True
    mainHandType = getHandType(mainHand)
    secondHandType = getHandType(secondHand)
    return [rev, mainHandType, secondHandType, getSuitedness(mainHand, mainHandType, secondHand, secondHandType)]

def genHand(hand: str, suits: str):
    return hand[0] + suits[0] + hand[2] + suits[1]

def genericMatchup(hand1: str, hand2: str):
    ret = categorizeMatchup(hand1, hand2)
    if ret[0] == True:
        res = [hand2, hand1]
    else:
        res = [hand1, hand2]
    if ret[1] != "Suited":
        res[0] = genHand(res[0], "hd")
    else:
        res[0] = genHand(res[0], "hh")
    if ret[2] == "Suited":
        if ret[3] == "One suit":
            res[1] = genHand(res[1], "hh")
        else:
            res[1] = genHand(res[1], "ss")
    elif ret[2] == "PP":
        if ret[3] == "Two suits":
            res[1] = genHand(res[1], "hd")
        elif ret[3] == "One suit":
            res[1] = genHand(res[1], "hs")
        else:
            res[1] = genHand(res[1], "sc")
    else:
        if ret[3] == "2Top":
            res[1] = genHand(res[1], "hd")
        elif ret[3] == "2Bot":
            res[1] = genHand(res[1], "dh")
        elif ret[3] == "1TopTop":
            res[1] = genHand(res[1], "hs")
        elif ret[3] == "1TopBot":
            res[1] = genHand(res[1], "sh")
        elif ret[3] == "1BotTop":
            res[1] = genHand(res[1], "ds")
        elif ret[3] == "1BotBot":
            res[1] = genHand(res[1], "sd")
        else:
            res[1] = genHand(res[1], "sc")
    res = tab[res[0]][res[1]]
    if ret[0] == True:
        res.reverse()
    return res

# print(categorizeMatchup("9h9d", "6h6d"))
def preflop_eq(cards):
    if letterToRank(cards[0][0]) >= letterToRank(cards[1][0]):
        hand1 = f"{cards[0]}{cards[1]}"
    else:
        hand1 = f"{cards[1]}{cards[0]}"
    if letterToRank(cards[2][0]) >= letterToRank(cards[3][0]):
        hand2 = f"{cards[2]}{cards[3]}"
    else:
        hand2 = f"{cards[3]}{cards[2]}"
    return genericMatchup(hand1, hand2)
