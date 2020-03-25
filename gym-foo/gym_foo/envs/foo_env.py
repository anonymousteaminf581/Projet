import gym
from gym import error, spaces, utils
from gym.utils import seeding
import numpy


class Player:
    """
    A class used to represent a player.
    
    Attributes
    ----------
    name : str
        the name of the player
    balance : int
        the total reward a player has earned
    alpha : float
        a parameter for the utility function
        
    Methods
    -------
    decision(verbose = True)
        Ask a human player to enter a choice regarding the decision of sharing or not, enabling him or her to play.
    """
    def __init__(self, name, alpha):
        """
        Parameter
        ---------
        name : str
            the name of the player
        """
        self.name = name
        self.balance = 0
        self.alpha = alpha

    def decision(self, verbose = True):
        """
        Ask a human player to enter a choice.
        If 1 is entered, the player is choosing the personal reward.
        If 0 is entered, the common reward is chosen.
        
        If verbose is set to True, the input will be introduced by a formatted string.
        """
        if verbose:
            print(self.name + "'s turn ! Put 1 if you want to share. Otherwise put 0.")
        return int(input())
    
    def utility(self,score,scores):
        """
        All the agents do not necessarily have the same goal.
        Some may want to maximize their reward, others may want to earn more than the average.
        We introduce this utility function in case we want to differentiate the players and the strategies.  
        """
        bonus = score-numpy.mean(scores)
        if bonus <= 0:
            return score**self.alpha
        return score**self.alpha * bonus**(1-self.alpha)


class FooEnv(gym.Env):
    """
    A class representing the environment of the game.
    
    Attributes
    ----------
    collective_reward : int
        the reward earned by each player for each player deciding to share
    personal_reward : int
        the reward earned by only by players for decide not to share
    num_of_players : int
        the number of players in the game
    num_of_games : int
        the number of turns in each game
    player : list of Player
        a list containing all players
    historical : array of int
        an array of size(num_of_games, num_of_players) used to store the actions of each turn.
    iteration : int
        the current turn of the game
    
    Methods
    -------
    step(actions)
        Play a turn according to the actions choosen by the players.
    render(mode)
        Print the the historical and the current scores.
    reset()
        Prepare the environment for a new game.
    close()
        Print the result of the game.
    
    GENERAL DESCRIPTION OF THE GAME
    """
    metadata = {'render.modes': ['human']}

    def __init__(self, cr = 7, pr = 10, np = 2, ng = 20, alphas = None):
        """
            Attributes
            ----------
            collective_reward : int
                the reward earned by each player for each player deciding to share
            personal_reward : int
                the reward earned by only by players for decide not to share
            num_of_players : int
                the number of players in the game
            num_of_games : int
                the number of turns in each game
            player : list of Player
                a list containing all players
            historical : array of int
                an array of size(num_of_games, num_of_players) used to store the actions of each turn.
            iteration : int
                the current turn of the game
            alphas : array of floats
                an array of floats used for the utility functions
        """
        self.collective_reward = cr
        self.personal_reward = pr
        self.num_of_players = np
        if alphas is None:
            alphas = [1 for i in range(np)]
        self.player = [Player(f'p{i+1}', alphas[i]) for i in range(np)]
        self.num_of_games = ng


        self.historical = numpy.zeros((ng,np), dtype = 'int')
        self.iteration = 0

    def step(self, actions):
        """
        Given the actions chosen by the players, returns the observation (last actions played), the rewards, whether the game is done or not, and info (TO DEFINE)
        It also returns the reward earned by each player from the last turn.
        """
        
        self.historical[self.iteration,:] = actions #update historical with the last chosen actions
        observation = self.historical[self.iteration,:] #could be changed
        self.iteration += 1
        
        # Computing rewards. We calculate what the players earn collectively and then what they earn separately.
        nb_collective_rewards = self.num_of_players - numpy.sum(actions) 
        collective_rewards = numpy.multiply(nb_collective_rewards,[self.collective_reward for player in self.player])
        personal_rewards = numpy.multiply(self.personal_reward,actions)
        rewards = numpy.add(collective_rewards, personal_rewards)
        
        # Updating the total reward
        for reward,player in zip(rewards,self.player):
            player.balance += reward
        
        if self.iteration >= self.num_of_games:
            done = True
        else:
            done = False
            
        info = ""
        
        return observation, rewards, done, info

    def reset(self):
        """
        Reset the environment for a new game.
        
        historical, iteration and the balances are cleaned.
        """
        self.historical = numpy.zeros((self.num_of_games, self.num_of_players), dtype = "int")
        self.iteration = 0
        for player in self.player:
            player.balance = 0
        
        return []
    
    def render(self, mode='human'):
        """
        Print the current state of the game, with all the actions taken and the current scores and the results of the utility functions.
        """
        
        # We use a lot of formatting to print a clean table
        player_names = ["{:^4}".format(player.name) for player in self.player] # Prepare a string "p1 | p2 | ..."
        print("|".join([" iter "]+player_names))
        
        # Print each line of the historical array
        for i in range(self.iteration):
            actions = ["{:^4}".format(action) for action in self.historical[i,:]] # Prepare a string "action p1 | action p2 | ..."
            print("|".join(["{:6}".format(i+1)]+actions))
        
        # Print the scores (current total rewards)
        scores = [player.balance for player in self.player]
        scores_string = ["{:^4}".format(player.balance) for player in self.player] # Prepare a string "score1 | ..."
        print("|".join(["scores"]+scores_string))
        
        # Print the results of the utility functions
        utilities = ["{:^4.0f}".format(player.utility(player.balance,scores)) for player in self.player] # Prepare a string "utility1 | ..."
        print("|".join([" util "]+utilities))
        print("")
            
    def close(self):
        """
        Print the result of the game.
        """
        
        print(f"End of the {self.num_of_games} turns.")
        self.render()
        leader = numpy.argmax([player.balance for player in self.player])
        print(f"{self.player[leader].name} has won !")
        

