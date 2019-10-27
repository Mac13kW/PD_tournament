# -*- coding: utf-8 -*-
"""
Prisoner's Dilemma Tournament

This is a recreation of the Axelrod's (1984) tournament. I prepared this code
for a PhD class at ESSEC. It helps students to understand the tournament and
gain intuition for the game and why tit-for-tat performs so well.

I highly recommend reading the Robert Axelrod's excellent book
"The Evolution of Cooperation". It is an excellent piece. Such a simple
idea and yet it explains so much about the world - particularly the social
sphere. If you were looking for mathematical foundations of morality, you
will find them in this book.

@ Maciej Workiewicz (2019)
https://github.com/Mac13kW
"""

import numpy as np
import matplotlib.pyplot as plt

# =============================================================================
# The Payoff Function:
# {cooperation [3, 3]; sucker's profit [5, 0]; and last [1, 1]}
#
#      cooperate   defect
#    +----------+----------+
#    |       3  |       5  |
#  c |  3       |  0       |
#    +----------+----------+
#    |       0  |       1  |
#  d |  5       |  1       |
#    +----------+----------+
# 
# Define players' strategies. You can add more if you which to. I only added
# the key strategies and none of the very complex ones.

# 0 tit_for_tat;
# 1-punisher;
# 2 random 20%;
# 3 random 50%;
# 4 always defect
# 5 always cooperate;
# 6 tit for two tats;
# 7 tester;
# 8 tit for 2 tats;
# 9 tit if 3 tats
# =============================================================================

#Here is where you input the strategies that the players will be following
player1 = 1
player2 = 2

iterations = 1000  # number of iterations we will run the tournament for
rounds = 200  # number of rounds for each game. Here we don't make it
              # probabilistic, but may need to if we use a code that knows
              # the number of time periods. We simply assume that the 
              # people that submitted strategies did not know the number of
              # periods.

# DEFINE PLAYERS
def tit_for_tat(actions_of_other):  #0
    # the tit for tat strategy
    if len(actions_of_other)>0:
        last_action = actions_of_other[-1]
    else:
        last_action = 0  # start with cooperation

    if last_action==0:  # if partner cooperated...
        my_action = 0  # I cooperate as well
    elif last_action==1:  # if partner defected...
        my_action=1  # I defect as well
    return(my_action)


def punisher(actions_of_other):  #1
    # the grim trigger strategy. Starts nice, buto once you cross this player,
    # he defects forever
    if 1 in actions_of_other:
        my_action = 1  # defect
    else:
        my_action = 0  # cooperate
    return(my_action)


def random_defector20():  #2
    # defects with 20% probability
    if np.random.rand() < 0.2:
        my_action = 1  # defect 20% of the time
    else:
        my_action = 0
    return(my_action)
    
    
def random_defector50():  # 3
    # defects half the time at random
    if np.random.rand() < 0.5:
        my_action = 1  # defect 20% of the time
    else:
        my_action = 0
    return(my_action)
    
    
def always_defect():  # 4
    # as name suggests
    my_action = 1  # defect 100% of the time
    return(my_action)
    

def always_cooperate():  # 5
    # most naive of strategies
    my_action = 0  # defect 100% of the time
    return(my_action)
    
    
def tit_for_2tats(actions_of_other):  #6
    # the tit for two tats player
    if len(actions_of_other)<2:
        my_action = 0
    elif len(actions_of_other)>=2:
        if actions_of_other[-1] == 1 and actions_of_other[-2] == 1:
            my_action = 1
        else:
            my_action = 0
    return(my_action)


def tester(actions_of_other):  #7
    # test who is it playing against
    if len(actions_of_other)==0:
        my_action = 1  # let's defect and see who we play against
    elif len(actions_of_other)==1 or len(actions_of_other)==2:
        my_action = 0  # then let's see if the other agent retailated
    elif len(actions_of_other)>2:
        if actions_of_other[1]==1:  # if I got punished, I play tit for tat
            if actions_of_other[-1]==0:  # if partner cooperated...
                my_action = 0  # I cooperate as well
            elif actions_of_other[-1]==1:  # if partner defected...
                my_action=1  # I defect as well
        elif actions_of_other[1]==0:  # if it didn't retailate
            if (len(actions_of_other)%2) == 0:  # I defect each second round
                my_action = 1
            else:
                my_action = 0
    return(my_action)


def tit_if_2tats(actions_of_other):  #8
    # Defect if partner defected at least once within last two rounds
    if len(actions_of_other)<2:
        my_action = 0  # cooperate
    elif len(actions_of_other)>=2:
        if actions_of_other[-1] == 1 or actions_of_other[-2] == 1:
            my_action = 1
        else:
            my_action = 0
    return(my_action)


def tit_for_3tats(actions_of_other):  #9
    # defect if three defections in a row
    if len(actions_of_other)<3:
        my_action = 0
    elif len(actions_of_other)>=3:
        if actions_of_other[-1] == 1 and actions_of_other[-2] and actions_of_other[-3]== 1:
            my_action = 1
        else:
            my_action = 0
    return(my_action)
    

    
# START THE GAME ===========================================================

Profits1 = np.zeros((iterations, rounds))
Profits2 = np.zeros((iterations, rounds))
Actions = np.zeros((iterations, rounds))  # to record history
# 0 is both cooperate; 1 first defects; 2 second defects; 3 both defect 


for i in np.arange(iterations):
    actions1 = []
    actions2 = []
    for t in np.arange(rounds):  # as per the original tournament
        if player1 ==0:
            action1 = tit_for_tat(actions2)
        elif player1==1:
            action1 = punisher(actions2)
        elif player1==2:
            action1 = random_defector20()
        elif player1==3:
            action1 = random_defector50()
        elif player1==4:
            action1 = always_defect()
        elif player1==5:
            action1 = always_cooperate()
        elif player1==6:
            action1 = tit_for_2tats(actions2)
        elif player1==7:
            action1 = tester(actions2)
        elif player1==8:
            action1 = tit_for_3tats(actions2)
        elif player1==9:
            action1 = tit_if_2tats(actions2)
        else:
            print('Input out of range. Try again')
        
        if player2 ==0:
            action2 = tit_for_tat(actions1)
        elif player2==1:
            action2 = punisher(actions1)
        elif player2==2:
            action2 = random_defector20()
        elif player2==3:
            action2 = random_defector50()
        elif player2==4:
            action2 = always_defect()
        elif player2==5:
            action2 = always_cooperate()
        elif player2==6:
            action2 = tit_for_2tats(actions1)
        elif player2==7:
            action2 = tester(actions1)
        elif player2==8:
            action2 = tit_for_3tats(actions1)
        elif player2==9:
            action2 = tit_if_2tats(actions1)
        else:
            print('Input out of range. Try again')
    
        actions1.append(action1)
        actions2.append(action2)
        # payoff
        if action1==0:
            if action2==0:  # both cooperate
                profit1 = 3
                profit2 = 3
                Actions[i, t] = 0
            else:  # second player defects
                profit1 = 0
                profit2 = 5
                Actions[i, t] = 2
        else:  # first player defects
            if action2==0:
                profit1 = 5
                profit2 = 0
                Actions[i, t] = 1
            else:  # both defect
                profit1 = 1
                profit2 = 1
                Actions[i, t] = 3
        Profits1[i, t] = profit1
        Profits2[i, t] = profit2

profits1 = np.average(np.sum(Profits1, axis=1))
profits2 = np.average(np.sum(Profits2, axis=1))

print('profit of player 1 = ', str(profits1), '\n', 'profit of player 2 = ', str(profits2))
 

# PLOT THE FIGURE =============================================================

# Here we want to see the first 25 rounds of the first game to see if the
# code is working as it should and how the game is played.

plt.figure(1, facecolor='white', figsize=(8, 6), dpi=150)
plt.plot(Profits1[0, :25], color='blue', linewidth=2, label='player 1')
plt.plot(Profits2[0, :25], color='red', linewidth=2, label='player 2')
plt.legend(loc=4,prop={'size':10})
plt.title('Results of the tournament 1 - the first 25 rounds', size=12)
plt.xlabel('time periods', size=12)
plt.xticks(np.arange(0, 25, step=1), fontsize=8)
plt.ylabel('payoff', size=12)  
plt.show()

# END OF LINE
