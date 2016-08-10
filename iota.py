#!/usr/bin/env python
# (c) Jan Dlabal, 2016.
#
# Simple scoring script for the iota board game, because scoring by hand
# sucks.
# Usage: python iota.py.
# If desired, modify the player names below.
#
# To enter a turn, enter all the numbers that you would normally have to sum
# up, without spaces. If there was a multiplier involved, enter the numbers
# to sum, and then xN where N is the multiplier.
# You can also undo a move by typing undo, or quit the game with done.
#
# Example inputs:
#   432 -> will give the current player 9 points.
#   432x2 -> will give the current player 18 points.
#   1111x4 -> will give the current player 16 points.

import subprocess
from random import randint

def parse_score(inp):
    if len(inp) > 0:
        if 'x' in inp:
            split = inp.split('x')
            multiplier = int(split[1])
            score = sum(map(int, list(split[0])))
        else:
            multiplier = 1
            score = sum(map(int, list(inp)))

        return multiplier * score
    else:
        return 0

def previous_player(curr, num_players):
    if curr - 1 < 0:
        return num_players - 1
    else:
        return curr - 1

def next_player(curr, num_players):
    if curr + 1 >= num_players:
        return 0
    else:
        return curr + 1

def main():
    # Modify names (and count) if desired.
    players = ["Turtle", "Pineapple", "Suspension Bridge"]

    num_players = len(players)
    scores = [0] * num_players
    whose_turn = randint(0, num_players - 1)

    last_score = 0
    prompt = "start"
    undo_ok = False

    while prompt != "done":
        # Change (or remove) if not on OS X.
        subprocess.call("clear", shell=True)

        if prompt == "undo":
            if not undo_ok:
                print "Can't undo more."
            else:
                undo_ok = False
                scores[previous_player(whose_turn, num_players)] -= last_score
                whose_turn = previous_player(whose_turn, num_players)
        elif prompt == "start":
            pass
        else:
            try:
                last_score = parse_score(prompt)
                scores[whose_turn] += last_score
                whose_turn = next_player(whose_turn, num_players)
                undo_ok = True
            except:
                print "Invalid input -- read the source for format info."

        print "\n\t%s" % "".join(["%s: %i\t" % (p,s) for p,s in zip(players, scores)])
        prompt = raw_input("\t%s's turn: " % (players[whose_turn]))

if __name__ == '__main__':
    main()
