#!/usr/bin/env python3
"""Print the before/after table from two ai_read.py outputs.

  python3 ai_report.py before.txt after.txt
"""
import sys

TRIALS = 256   # AI_TEST_TRIALS in test_ai.inc
# (description, the AI's four moves, how many of them to report); same order as sAiTestScenarios.
# The unreported moves are filler.
SCENARIOS = [
    ('vs Gengar-like (Ghost/Poison, Sp. Atk > Attack)', ['Reflect', 'Light Screen', 'Growl', 'Tackle'], 3),
    ('vs Gyarados-like (Water/Flying, Attack > Sp. Atk)', ['Reflect', 'Light Screen', 'Growl', 'Tackle'], 3),
    ('after the target used Shadow Ball (now special)', ['Counter', 'Tackle', 'Growl', 'Tail Whip'], 1),
    ('after the target used Crunch (now physical)', ['Mirror Coat', 'Tackle', 'Growl', 'Tail Whip'], 1),
    ('after the target used Crunch (now physical)', ['Counter', 'Tackle', 'Growl', 'Tail Whip'], 1),
    ('after the target used Shadow Ball (now special)', ['Mirror Coat', 'Tackle', 'Growl', 'Tail Whip'], 1),
]

def load(path):
    return [[int(x) for x in line.split()] for line in open(path) if line.strip()]

before, after = load(sys.argv[1]), load(sys.argv[2])
print('Average change to each move\'s score from the AI\'s viability script')
print('(%d runs each; higher = the AI likes the move more)\n' % TRIALS)
print('| Situation | Move | Before | After |')
print('|---|---|---|---|')
for i, (desc, moves, shown) in enumerate(SCENARIOS):
    for j, move in enumerate(moves[:shown]):
        b, a = before[i][j] / TRIALS - 100, after[i][j] / TRIALS - 100
        print('| %s | %s | %+.2f | %+.2f |' % (desc, move, b, a))
