# INF581_Project
RL project

Report link (Overleaf): https://www.overleaf.com/8946242343yxqbynfbnppy

Description:

The game is played between several players. Initially the number of rounds is fixed.
During each round, players simultaneously choose either to keep or share.
Each player's win depends on their choice but also on the choice of the other players.
If a player chooses to share:
Everyone win an additional minimum reward.
Otherwise, he wins an additional maximal which is not shared.

/*
He wins a collective reward if all other players make the same choice. Otherwise he wins a minimal reward (possibly 0).
If the player chooses to keep. He wins a maximum reward if all the others choose to share. He wins 0 otherwise.
*/ -> I changed it so that it fits the game we have played.


You have several players, in each round, one player chooses either to share and in this case everyone wins a collective reward.
or to keep and in this case the reward depends on the choice of the other players. The goal is to maximize your winnings, knowing that if you play personally the others will do the same and in the end you will win less.

Each player's goal is to maximize their final win.

