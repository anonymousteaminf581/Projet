
import numpy as np

class Player:
	# neural net with 3 layers and 2 nodes per layer
	# input layer has one node w/ ratio of players who shared on previous round and one memory node
	# output layer has one node for output 1 for share, 0 for keep and one node for memory to serve as input on the next round
	
	#	round n 	 XX%	  m
	#				  ↓       ↓
	#				Input	Memory
	#				  ↓   ⤩   ↓
	#			    Node     Node
	#				  ↓   ⤩   ↓
	#				Output	Memory
	#				          ↓
	#				 XX%      ↓
	#				  ↓       ↓
	#	round n+1	Input	Memory
	#				  ↓   ⤩   ↓
	#			    Node     Node
	#				  ↓   ⤩   ↓
	#				Output	Memory

	def __init__(self, memory, matrix1, matrix2):
		self.balance = 0
		self.memory = memory
		self.matrix1 = matrix1
		self.matrix2 = matrix2

	def choice(self, input):
		vector = np.array([input, self.memory, 1])
		vector = np.dot(self.matrix1, vector) > 0
		vector = np.dot(self.matrix2, vector) > 0
		
		self.memory = vector[1]
		
		return vector[0]

	def clone(self):
		return Player(self.memory, self.matrix1, self.matrix2)


class Environment:
	def __init__(self, reward_keep, reward_share, *players):
		self.keep = reward_keep or (lambda n: 3 * n)			# reward functions depend on choice taken and number of players who shared
		self.share = reward_share or (lambda n: 3 * n - 4)		# default rewards: sharing costs 1 and gives 3 to everyone else, keeping costs 0 and gives 0 to everyone else
		self.players = [*players]
		self.last = 1

	def add(self, player):
		self.players.append(player)

	def round(self):
		choices = [player.choice(self.last) for player in self.players]
		
		n = sum(choices)
		
		keep = self.keep(n)
		share = self.share(n)
		
		for i in range(len(self.players)):
			self.players[i].balance += share if choices[i] else keep
		
		self.last = n / len(self.players)


if __name__ == "__main__":
	# names are from https://ncase.me/trust/
	copier = Player(0, np.array([[ 2,  0, -1], [ 0,  0,  0], [0, 0, 1]]), np.array([[ 1,  0,  0], [ 0,  0,  0]])) # share if at least 50% shared at previous turn else keep
	sharer = Player(0, np.array([[ 0,  0,  0], [ 0,  0,  0], [0, 0, 1]]), np.array([[ 0,  0, +1], [ 0,  0,  0]])) # always share
	keeper = Player(0, np.array([[ 0,  0,  0], [ 0,  0,  0], [0, 0, 1]]), np.array([[ 0,  0, -1], [ 0,  0,  0]])) # always keep
	grudge = Player(1, np.array([[ 2,  2, -3], [ 0,  0,  0], [0, 0, 1]]), np.array([[ 1,  0,  0], [ 1,  0,  0]])) # always share until at least 50% keep then always keep
	kitten = Player(1, np.array([[ 2,  0, -1], [ 0,  1,  0], [0, 0, 1]]), np.array([[ 1,  1,  0], [ 1,  0,  0]])) # keep if at least 50% kept on two previous turns, else share
	simple = Player(1, np.array([[-3,  3,  2], [-3,  3, -1], [0, 0, 1]]), np.array([[ 1, -2,  0], [ 1, -2,  0]])) # repeat previous action if at least 33% shared else do opposite action

	players = []
	
	counts = [10, 2, 20, 10, 5, 10]
	types = [copier, sharer, keeper, grudge, kitten, simple]
	names = ["copier", "sharer", "keeper", "grudge", "kitten", "simple"]
	
	for i in range(len(types)):
		for j in range(counts[i]):
			players.append(types[i].clone())

	env = Environment(None, None, *players)

	for i in range(100):
		env.round()

	for i in range(len(types)):
		if counts[i]:
			print(names[i], "(x", counts[i], ") :", players[sum(counts[:i])].balance)

