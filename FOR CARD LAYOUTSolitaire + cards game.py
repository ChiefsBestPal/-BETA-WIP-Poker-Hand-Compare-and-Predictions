#u"x"        ascii()       encode()       decode()       repr      !!!compile()!!!
#⚜GROS QUEB⚜
import itertools as it
import random as rand
import re
import UnicodeWriting as uw
# def get_active_pos():
#     print('press keboard interrupt to exit')
#     try:
#         while True:
#             x, y = p.position()
#             positionStr = execute("x  " + str(x).rjust(2)+"     "+ "y  "+str(y).rjust(2))
#             print(positionStr, end="")
#             print("\b\n\r" * len(positionStr), end="", flush=True)#flush() just to ignore buffer
#     except KeyboardInterrupt:
#         print("\n")
# print(u"WHITES:      \r|\t\u2654\t|\t\u2655\t|\t\u2656\t|\t\u2657\t|\t\u2658\t|\t\u2659\t|\r\n")
# print(u"BLACKS:      \r|\t\u265A\t|\t\u265B\t|\t\u265C\t|\t\u265D\t|\t\u265E\t|\t\u265F\t|\r\n")
# print(u"CARDS SYMBOLS:      \r|\t\u2660\t|\t\u2661\t|\t\u2662\t|\t\u2663\t|\r\n")
# print(u"DICE:      \r|\t\u2680\t|\t\u2681\t|\t\u2682\t|\t\u2683\t|\t\u2684\t|\t\u2685\t|\r\n")
color = {"BLACK": (u"\u2660",u"\u2663"),"WHITE": (u"\u2661",u"\u2662")}#dictfromkeys
cards = [str(i + " " + j)if j != "10" else str(i + j) for i in ["\u2660","\u2661","\u2662","\u2663"] for j in ["2","3","4","5","6","7","8","9","10","J","Q","K","A"]]
#!print(cards)

cards_deck = cards
rand.shuffle(cards_deck)
rand.shuffle(cards_deck)
deck1 = rand.sample(cards_deck,1)
cards_deck = list(filter(lambda x: x not in deck1, cards_deck))
rand.shuffle(cards_deck)
deck2 = rand.sample(cards_deck,2)
cards_deck = list(filter(lambda x: x not in deck2,cards_deck))
rand.shuffle(cards_deck)
deck3 = rand.sample(cards_deck,3)
cards_deck = list(filter(lambda x: x not in deck3,cards_deck))
rand.shuffle(cards_deck)
deck4 = rand.sample(cards_deck,4)
cards_deck = list(filter(lambda x: x not in deck4,cards_deck))
rand.shuffle(cards_deck)
deck5 = rand.sample(cards_deck,5)
cards_deck = list(filter(lambda x: x not in deck5,cards_deck))
rand.shuffle(cards_deck)
deck6 = rand.sample(cards_deck,6)
cards_deck = list(filter(lambda x: x not in deck6,cards_deck))
rand.shuffle(cards_deck)
deck7 = rand.sample(cards_deck,7)
cards_deck = list(filter(lambda x: x not in deck7,cards_deck))
rand.shuffle(cards_deck)
up_pile = cards_deck
#!-------------------------------------TEMP: SAME SHUFFLE FOR TESTING -----------------------------------------------------------#!
#print(deck1,deck2,deck3,deck4,deck5,deck6,deck7,up_pile,sep= ",")
deck1 = ['♠ K']
deck2 = ['♣ A', '♡ 4']
deck3 = ['♣10', '♣ 9', '♢ 6']
deck4 = ['♣ 3', '♡ 2', '♠ J', '♣ Q']
deck5 = ['♡ 6', '♠ 5', '♢ 2', '♡10', '♡ 7']
deck6 = ['♠ 8', '♢ 7', '♢ 8', '♣ 8', '♣ 5', '♣ 2']
deck7 = ['♡ K', '♡ 5', '♠ Q', '♠ 2', '♡ A', '♢ 9', '♣ K']
up_pile = ['♣ J', '♠ 9', '♢ 3', '♡ J', '♡ 8','♠ 3', '♠ 4', '♢ K', '♠ 6', '♣ 4', '♢ 5', '♣ 6', '♣ 7', '♢ 4', '♠ 7', '♢ A', '♢10', '♠10', '♡ 9', '♡ 3', '♡ Q', '♢ J', '♠ A', '♢ Q']
slot1 = slot2 = slot3 = slot4 = []

#card_layout = " ____\n|    |\n| eQ |\n|____|"
ltop,lup,lmid,ldown = " _____","|     |","| eQ |","|_____|" #!REPLACE eQ by % for C-like tuple formatting later
card_parts = [ltop,lup,lmid,ldown]
upper_cards_assembler= lambda x: "    " + x + "         " + "   ".join([" "+ x if x == ltop else x for _ in range(4)])
upper_board = list(map(upper_cards_assembler,card_parts))#args,but need default instance and modified instance (upper and lower board def values)

lower_cards_assembler = lambda x: "   ".join([" "+ x if x == ltop and count != 0 else x for count in range(7)])
lower_board = list(map(lower_cards_assembler,card_parts))
def create_print(_arr):
    a = _arr
    carriage = (len(_arr)-2)*"{}\r\n"
    foo = '{}\n' + carriage + '{}\n'
    f_string = foo.format(a[0],a[1],a[2],a[3])
    bar = "".join(f_string.splitlines(True))
    return bar


def board_generator_test():
    global upper_board
    global lower_board
    
    title = uw.execute("Solitaire")
    credits = "by Ant_Ender"
    player = "PLAYING: {}".format("username_id")

    return title + "\t" + credits + "\t\t" + player + "\n\t" +  str(color) + "\n" + create_print(upper_board) + 2*"\n" + create_print(lower_board)
board = board_generator_test()
board = str(re.sub("eQ","%s",board))
board = board % (up_pile[0],"<1>","<2>","<3>","<4>",deck1[0],deck2[0],deck3[0],deck4[0],deck5[0],deck6[0],deck7[0]) #?zeros are intially empty slot1,slot2,slot3,slot4
#print(re.sub("n","%d",board) % )
print(board)
#!function(card,moveto) example: 
#print(deck1,deck2,deck3,deck4,deck5,deck6,deck7,up_pile)
