import random
import tkinter as tk
from tkinter.constants import DISABLED
from PIL import ImageTk, Image

cardvalue = {'A' : 13, 'K' : 12, 'Q' : 11, 'J' : 10, '1' : 9, '9' : 8, '8' : 7, '7' : 6, '6' : 5, '5' : 4, '4' : 3, '3' : 2, '2' : 1}

deck = ['AS', 'AD', 'AC', 'AH',
        'KS', 'KD', 'KC', 'KH',
        'QS', 'QD', 'QC', 'QH',
        'JS', 'JD', 'JC', 'JH',
        '10S', '10D', '10C', '10H',
        '9S', '9D', '9C', '9H',
        '8S', '8D', '8C', '8H',
        '7S', '7D', '7C', '7H',
        '6S', '6D', '6C', '6H',
        '5S', '5D', '5C', '5H',
        '4S', '4D', '4C', '4H',
        '3S', '3D', '3C', '3H',
        '2S', '2D', '2C', '2H']

money = 100
bet = 1
cardimages = []
cardlabels = []
hand = []
exchangeset = set()

root = tk.Tk()
root.title('DUECES WILD TRAINER')
root.geometry('800x320')

handpanel = tk.Label(root, bg='green')
handpanel.pack(side='top', fill='x', ipady=15)

handevaluator = tk.Label(handpanel, text='', bg='green')
handevaluator.pack(side='bottom', pady=(0, 15))

controlpanel = tk.Label(root)
controlpanel.pack(side='bottom', fill='both', expand=True)

cardback = ImageTk.PhotoImage(Image.open('JPEG/Red_back.jpg').resize((140, 200)))

for i in range(5):
    # cant bind markcard to cards in this loop for some reason
    card = tk.Label(handpanel, image=cardback, bd=0)
    card.pack(side='left', padx=(10, 10))
    cardlabels.append(card)

def exchange():
    exchangebtn['state'] = 'disabled'
    replaceindex = 5
    for index in exchangeset:
        hand[index] = hand[replaceindex]
        cardlabels[index].configure(image=cardimages[replaceindex])
        cardlabels[index].image=cardimages[replaceindex]
        replaceindex += 1
    evaluatehand()

def markcard(event, cardnum):
    if exchangebtn["state"] == "disabled":
        return
    if cardnum in exchangeset:
        exchangeset.remove(cardnum)
        cardlabels[cardnum].configure(image=cardimages[cardnum])
        cardlabels[cardnum].image=cardimages[cardnum]
    else:
        exchangeset.add(cardnum)
        cardlabels[cardnum].configure(image=cardback)
        cardlabels[cardnum].image=cardback

cardlabels[0].bind('<Button-1>', lambda event: markcard(event, 0))
cardlabels[1].bind('<Button-1>', lambda event: markcard(event, 1))
cardlabels[2].bind('<Button-1>', lambda event: markcard(event, 2))
cardlabels[3].bind('<Button-1>', lambda event: markcard(event, 3))
cardlabels[4].bind('<Button-1>', lambda event: markcard(event, 4))

def deal():
    global money
    exchangebtn['state'] = 'normal'
    hand.clear()
    cardimages.clear()
    exchangeset.clear()

    random.seed()
    handset = set()
    while len(hand) < 10:
        cardindex = random.randint(0, 51)
        if cardindex not in handset:
            hand.append(deck[cardindex])
            handset.add(cardindex)

    cardimages.append(ImageTk.PhotoImage(Image.open('JPEG/' + hand[0] + '.jpg').resize((140,200))))
    cardimages.append(ImageTk.PhotoImage(Image.open('JPEG/' + hand[1] + '.jpg').resize((140,200))))
    cardimages.append(ImageTk.PhotoImage(Image.open('JPEG/' + hand[2] + '.jpg').resize((140,200))))
    cardimages.append(ImageTk.PhotoImage(Image.open('JPEG/' + hand[3] + '.jpg').resize((140,200))))
    cardimages.append(ImageTk.PhotoImage(Image.open('JPEG/' + hand[4] + '.jpg').resize((140,200))))
    cardimages.append(ImageTk.PhotoImage(Image.open('JPEG/' + hand[5] + '.jpg').resize((140,200))))
    cardimages.append(ImageTk.PhotoImage(Image.open('JPEG/' + hand[6] + '.jpg').resize((140,200))))
    cardimages.append(ImageTk.PhotoImage(Image.open('JPEG/' + hand[7] + '.jpg').resize((140,200))))
    cardimages.append(ImageTk.PhotoImage(Image.open('JPEG/' + hand[8] + '.jpg').resize((140,200))))
    cardimages.append(ImageTk.PhotoImage(Image.open('JPEG/' + hand[9] + '.jpg').resize((140,200))))

    cardlabels[0].configure(image=cardimages[0])
    cardlabels[0].image=cardimages[0]

    cardlabels[1].configure(image=cardimages[1])
    cardlabels[1].image=cardimages[1]

    cardlabels[2].configure(image=cardimages[2])
    cardlabels[2].image=cardimages[2]

    cardlabels[3].configure(image=cardimages[3])
    cardlabels[3].image=cardimages[3]

    cardlabels[4].configure(image=cardimages[4])
    cardlabels[4].image=cardimages[4]

    money -= bet
    moneycounter.config(text="Money: " + str(money))

def evaluatehand():
    for i in range(5):
        for j in range(i, 5):
            if cardvalue[hand[j][0]] < cardvalue[hand[i][0]]:
                temp = hand[i]
                hand[i] = hand[j]
                hand[j] = temp

    twocount = 0
    for i in range(5):
        if hand[i][0] == '2':
            twocount += 1

    if twocount == 4:
        changetext('four dueces')
        return

    li = len(hand[0]) - 1
    flush = True
    for i in range(twocount, 4):
        if hand[i][len(hand[i]) - 1] != hand[i + 1][len(hand[i + 1]) - 1]:
            flush = False
            break
    straight = cardvalue[hand[4][0]] - cardvalue[hand[twocount][0]] < 5

    if flush and straight and cardvalue[hand[4][0]] >= 9:
        if cardvalue[hand[4][0]] >= 9:
            if twocount == 0:
                changetext('natural royal flush')
            else:
                changetext('royal flush')
        else:
            changetext('straight flush')
        return

    cardcounts = dict()
    maxcount = 1
    for i in range(twocount, 5):
        if hand[i][0] in cardcounts:
            cardcounts[hand[i][0]] += 1
            if cardcounts[hand[i][0]] > maxcount:
                maxcount = cardcounts[hand[i][0]]
        else:
            cardcounts[hand[i][0]] = 1

    uniquecards = len(cardcounts)

    if twocount == 0:
        if maxcount == 4:
            changetext('four of a kind')
        elif maxcount == 3:
            if uniquecards == 2:
                changetext('full house')
            else:
                changetext('three of a kind')
        elif maxcount == 2:
            changetext('nothing')
        else:
            if flush:
                changetext('flush')
            elif straight:
                changetext('straight')
            else:
                changetext('nothing')
    elif twocount == 1:
        if maxcount == 4:
            changetext('five of a kind')
        elif maxcount == 3:
            changetext('four of a kind')
        elif maxcount == 2:
            if uniquecards == 2:
                changetext('full house')
            else:
                changetext('three of a kind')
        else:
            if flush:
                changetext('flush')
            elif straight:
                changetext('straight')
            else:
                changetext('nothing')
    elif twocount == 2:
        if maxcount == 3:
            changetext('five of a kind')
        elif maxcount == 2:
            changetext('four of a kind')
        else:
            if flush:
                changetext('flush')
            elif straight:
                changetext('straight')
            else:
                changetext('three of a kind')
    else:
        if maxcount == 2:
            changetext('five of a kind')
        else:
            changetext('four of a kind')

def changetext(hand):
    global money
    handevaluator.config(text=hand)
    if hand == 'nothing':
        return
    elif hand == 'three of a kind':
        money += bet
        moneycounter.config(text="Money: " + str(money)) 
    elif hand == 'straight' or hand == 'flush':
        money += 2 * bet
        moneycounter.config(text="Money: " + str(money))
    elif hand == 'full house':
        money += 3 * bet
        moneycounter.config(text="Money: " + str(money))
    elif hand == 'four of a kind':
        money += 5 * bet
        moneycounter.config(text="Money: " + str(money))
    elif hand == 'straight flush':
        money += 9 * bet
        moneycounter.config(text="Money: " + str(money))
    elif hand == 'five of a kind':
        money += 15 * bet
        moneycounter.config(text="Money: " + str(money))
    elif hand == 'royal flush':
        money += 25 * bet
        moneycounter.config(text="Money: " + str(money))
    elif hand == 'four dueces':
        money += 200 * bet
        moneycounter.config(text="Money: " + str(money))
    elif hand == 'natural royal flush':
        money += 800 * bet
        moneycounter.config(text="Money: " + str(money))

exchangebtn = tk.Button(controlpanel, text='Exchange', command=exchange, bd=0, state='disabled')
exchangebtn.pack(side='left', padx=(20,10))

dealbtn = tk.Button(controlpanel, text='Deal', command=deal, bd=0)
dealbtn.pack(side='left', padx=(10, 10))

moneycounter = tk.Label(controlpanel, text="Money: " + str(money))
moneycounter.pack(side='left', padx=(10, 10))

root.mainloop()