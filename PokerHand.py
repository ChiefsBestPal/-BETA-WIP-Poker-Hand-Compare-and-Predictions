class PokerHand(object):
    
    RESULT = ["Loss", "Tie", "Win"]

    def __init__(self, hand):
        pass
        
    def compare_with(self, other):
        pass

from collections import Counter
import functools #reduce and partial
import re
import itertools as it
#000
#*suit: symbol #*rank: Card Power
#*Special rule : no suit ranking and no low aces

#*Make it numerical sometime? 
rank_to_rank_name = {2: 'two',
3: 'three',
4: 'four',
5: 'five',
6: 'sixe',
7: 'seven',
8: 'eight',
9: 'nine',
10: 'ten',
11: 'jack',
12: 'queen',
13: 'king',
14: 'high-ace'}

suit_to_suit_names = {'S': 'spades',
'H': 'hearts',
'D': 'diamonds',
'C': 'clubs'}
#!S(pades), H(earts), D(iamonds), C(lubs)
#!2, 3, 4, 5, 6, 7, 8, 9, T(en)10, J(ack)11, Q(ueen)12, K(ing)13, A(ce)14

power = int()

replacements = 10 * [None]
replacements.extend(['T','J','Q','K','A'])

def format_input(Input):
    """Output: list of tuples
            tuples have structure: (rank,suit)
            tuples are ordered in list by key=int(tup[0])
    """
    temp = Input
    for value in range(10,14+1):
        temp = re.sub(replacements[value],str(value),temp)
    Output = [(card[0:-1],card[-1]) for card in re.split('\s',temp)]

    return sorted(Output,key=lambda tup: int(tup[0]),reverse=True)

def evaluate_hand(hand):
    try:
        hand = format_input(hand)
        hand_ranks,hand_suits = [tup[0] for tup in hand],[tup[1] for tup in hand]
    except TypeError:
        hand_ranks,hand_suits = hand[0],['H']

    check_suits = lambda suits: bool(len(dict.fromkeys(suits)) == 1)
    counter_str = Counter(hand_ranks)
    counter = dict(zip(map(int,counter_str.keys()),counter_str.values())) #Casting int type to keys for convenience
    hand_ranks = list(map(int,hand_ranks))
    #print(counter)

    #print(hand_suits)
    #print(hand_ranks)

    #1 Royal Flush:     A,K,Q,J,10 Same suit
    #? All same suit, A,K,Q,J,T 
    if hand_ranks == list(range(14,10-1,-1)) and check_suits(hand_suits):
        power = 10

        identity = "Royal Flush, All " + str(suit_to_suit_names[hand_suits[-1]]).title()
        compare = hand_ranks 
    #2 Straight Flush:  9,8,7,6,5 (consecutive five cards) Same suit
    #? All same suit, if sorted(hand,reverse=True) == hand, the best will always be highest sum(hand)
    elif hand_ranks == list(range(int(hand_ranks[0]),int(hand_ranks[0])-5,-1)) and check_suits(hand_suits):
        power = 9
        highest = max(hand_ranks)
        identity = str(rank_to_rank_name[highest]).title() + "-high Straight Flush,  All " + str(suit_to_suit_names[hand_suits[-1]]).title()
        compare = hand_ranks
    #3 Four of a kind: four cards of the same rank HIGHEST RANK WORTH MORE, IF ranks of 2 players are equal, Highest 5th card wins
    #? if max(collections.Counter(rank_ix)) == 4, the best here will be highest sum(hand) (the 5th differentiats two same fourofakind)
    elif counter[max(counter)] == 4:
        power = 8
        FourOfAKind = max(counter)
        fifth = min(counter)

        identity = "Four of kind ; of rank {}; and with {} as kicker".format(rank_to_rank_name[FourOfAKind],rank_to_rank_name[fifth])
        compare = [FourOfAKind,fifth]
    #4 Full house: 3 cards of the same rank  + 2 cards of other same rank   (3cardsrank "full of" 2cardsrank). the Three of a kind worth more
    #? if collections.Counter(rank_ix) == {3,2} : best is highest rank of 3 (if equal, highest rank of 2)
    elif list(counter.values())[:] == [3,2]:
        power = 7
        trio = list(counter.keys())[0]
        duo = list(counter.keys())[1]

        identity = str("{}s full of {}s".format(rank_to_rank_name[trio],rank_to_rank_name[duo]))
        compare = [trio,duo]
    #5 Flush: 5 cards of the same suit, highest card rank determines rank of the flush (rank-high flush)
    #? if [symbols] == list(dict.fromkeys(symbols)) best is highest rank card, (if equal, do second, then third,etc)
    elif check_suits(hand_suits):
        power = 6
        best_cards_in_order = sorted(hand_ranks, reverse=True) #If == first, check second, then third and so on
        
        identity = "Flush, suit: " + str(suit_to_suit_names[hand_suits[-1]]).title()
        compare = best_cards_in_order
    #6 Straight: five consecutive cards of different suits
    #? if [for i in range(min(hands),min(hands)+5,-1)] == sorted(hand,reverse=True), highest first card rank wins
    elif [i for i in range(min(map(int,hand_ranks))+4,min(map(int,hand_ranks))-1,-1)] == list(map(int,hand_ranks)):
        power = 5
        Rank_of_Straight = max(map(int,hand_ranks)) #if equal, then tie

        identity = str(rank_to_rank_name[Rank_of_Straight]).title() + "-high Straight"
        compare = Rank_of_Straight
    #7 Three of a kind: three cards of the same rank, IF ranks of 2 players are equal, Highest 2 remaining cards wins
    #? if collections.Counter(rank_ix)[0] == 3: best is highest rank of 3 (if same, then highest sum(remainders) wins)
    elif counter[max(counter)] == 3:
        power = 4
        Rank_of_TOAK = max(counter)
        remainders_in_order = sorted(hand_ranks, reverse=True)[-2:]

        identity = "Three of a kind, rank " + rank_to_rank_name[Rank_of_Straight]
        compare = [Rank_of_TOAK]
        compare.extend(remainders_in_order)
    #8 Two Pair: 2 pairs of cards with same respective rank, the highest rank pair determines the two-pair ranks   (If equal, the fifth determines winner?) 
    #? if collections.Counter(rank_ix) == {2,2} : best is highest rank of a 2 (if equal, highest rank of other 2, then fifth card)
    elif list(counter.values())[:] == [2,2,1]:
        power = 3
        HighestPair = list(counter)[0]
        SecondHighestPair = list(counter)[1]
        fifth = list(counter)[2]
        
        identity = "Two pairs: pair of " + rank_to_rank_name[HighestPair] + " and pair of " + rank_to_rank_name[SecondHighestPair]
        compare = [HighestPair,SecondHighestPair,fifth]
    #9 One pair: 1 pair of cards with same rank (if equal, sum the last 3 cards values)
    elif list(counter.values())[:] == [2,1,1,1]:
        power = 2
        Pair = list(counter)[0]
        best_cards_in_order = sorted(list(counter)[1:], reverse=True)

        identity = "One pair of rank " + rank_to_rank_name[Pair]
        compare = [Pair]
        compare.extend(best_cards_in_order)
        

    #10 High card: If not part of the above hands, then Highest card wins (if same two high card, second highest, and etc)
    else:
        power = 1
        best_cards_in_order = sorted(list(counter)[:], reverse=True)
        
        identity = "High card: " + rank_to_rank_name[best_cards_in_order[0]]
        compare = best_cards_in_order


    return [power,compare,identity]
#! LOOP VARIABLE CALL BEST CARDS IN ORDER IF EQUALITIES BETWEEN TWO HANDS 

#? Pairs and groups are lists, and other are ints (So order them in importance)
identity2 = "" # This will indicate if two hands of the same power were compared in the final string message
def all_hands(*power_and_compare):
    global identity2
    #first hand is OUR player

    highest_power = max([arr[0] for arr in power_and_compare]) #?#000 ERROR HERE #000
    equal_hands = []
    for player_number,i in enumerate(power_and_compare):
        if i[0] == highest_power:
            equal_hands.append([i[1],player_number+1,i[2]]) #i[2] is the identify for displayed message

    if len(equal_hands) == 1:
        res = list(it.chain(*equal_hands))[1]
    else:
        identity2 = "Highest " #add to final message if there is a sole winner
    temp = equal_hands[0][0]
    for hand in equal_hands[1:]:
        for x,y in zip(hand[0],temp):
            if x > y:
                temp = hand[0]
                break
            elif x < y:
                temp = temp
                break
            else:
                continue
    winner = temp
    tie = [hand[1] for hand in equal_hands if hand[0] == winner]
    full_hand_identity = [hand for hand in equal_hands if hand[0] == winner]
    full_hand_identity = list(it.chain(*full_hand_identity))

    re_last_hand = str(tie[-1]) #@ (or [0])
    if len(tie) > 1:
        tie = ", ".join(map(str,tie))
        tie_formatted = re.sub(',[\s][\d]$',' and '+ re_last_hand ,tie).upper()
        print("TIE BETWEEN PLAYERS " +  tie_formatted,end="\n")

        print(full_hand_identity[2]) #? IDENTITY MIGHT BE IMPRECISE HERE (JUST VISUALS)

        return "Tie"
    else:
        print("WINNER IS PLAYER " + str(res),end="\n")

        print(identity2 + full_hand_identity[2]) #? IDENTITY MIGHT BE IMPRECISE HERE (JUST VISUALS)

        if str(res) == '1':
            return "Win"
        else:
            return "Loss"

def main():
    hand1 = input("Enter player hand")
    other_hands = []
    while True:
        hand2 = input("Enter adversary hand")
        print("Enter 'ok' in the next entry to stop entering enemy hands",end='\n',flush=True)
        if hand2 == "ok":
            break
        else:
            other_hands.append(hand2.encode())
            continue
    
    #! Im proud of this part----------------------
    other_hands_evaluated = functools.reduce(lambda hand: evaluate_hand(hand),other_hands)    
    compare_function = all_hands #*<function object>
    hands_iter = iter(other_hands_evaluated) #*in OOP use __iter__

    while True:
        try:
            current = next(hands_iter)
            compare_function = functools.partial(compare_function,current)
        except StopIteration as end_iter:
            print(end_iter,end="\t")
            break
        else:
            print(str(current))
    #!--------------------------
    last_hand_value = other_hands_evaluated[-1] #* Forced to do this due to the nature of partial()
    print(compare_function(last_hand_value))

#if __name__ == '__main__':
    #main()

print(all_hands(evaluate_hand("2H 3H 4H 5H 6H"),evaluate_hand("KS AS TS QS JS")))    
#! USE FULL TERMS: https://www.tightpoker.com/poker_terms.html
#* !!!!!!!! DO GIT REPO !!!!!!!!!!!!!
#! DO A FULL SOFTWARE OF THIS !
