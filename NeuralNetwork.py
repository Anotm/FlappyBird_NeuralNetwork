import numpy as np
import random as rand
import copy


class NeuralNetwork:
	def __init__(self, node_counts: list=None, input_layers: list=None, input_links: list=None, input_bias: list=None):
		'''
			input: [2,3,2]

			Neural Network:
					|0|
				|0|     |0|
				   >|0|<
				|0|     |0|
					|0|
			-input on left
			-hidden layers middle
			-output on right
		'''

		if node_counts == None and input_layers != None and input_links != None and input_bias != None:
			self.layers = input_layers
			self.links = input_links
			self.bias = input_bias
			return

		elif node_counts == None:
			return


		self.layers = []
		self.links = []
		self.bias = []

		# --------------------------------- Layers ---------------------------------

		for i in range(len(node_counts)):
			self.layers.append([])
			for j in range(node_counts[i]): self.layers[i].append(0);

		# --------------------------------- Links ---------------------------------

		for i in range(len(self.layers)):
		    self.links.append([])
		    for j in range(len(self.layers[i])):
		        if i == 0:
		            self.links[i].append([None])
		        else:
		            self.links[i].append([])
		            for k in range(len(self.layers[i-1])):
		                self.links[i][j].append(0)

		# --------------------------------- Bias ---------------------------------

		for i in range(len(node_counts)):
			self.bias.append([])
			for j in range(node_counts[i]): self.bias[i].append(0);

	def set_input(self, input_list: list):
		'''
			input: [1,2]

			Neural Network:
					|0|
				|1|     |0|
				   >|0|<
				|2|     |0|
					|0|
		'''
		for index, num in enumerate(input_list):
			self.layers[0][index] = num

	def skew_links_bias(self, link_range_round: list, bias_range_round: list):
		'''
		link_range_round = [lower bound, upper bound, how many decimals]
		bias_range_round = [lower bound, upper bound, how many decimals]

		the random number generated will be added to the already existing values
		'''
		# --------------------------------- Links ---------------------------------
		for i in range(len(self.links)):
			for j in range(len(self.links[i])):
				for k in range(len(self.links[i][j])):
					if self.links[i][j][k] != None:
						self.links[i][j][k] += round(rand.uniform(link_range_round[0], link_range_round[1]), link_range_round[2])

		# --------------------------------- Bias ---------------------------------
		for i in range(len(self.bias)):
			for j in range(len(self.bias[i])):
				self.bias[i][j] += round(rand.uniform(bias_range_round[0], bias_range_round[1]), bias_range_round[2])

	def forward_pass(self, result_round: int):
		'''
			round = number of decimals in node


			[n1] -w1-

			[n2] -w2- [n4] b1

			[n3] -w3-

			The node "n4" will be calculated by the dot product 
			of [n1,n2,n3] and [w1,w2,w3] plus b1. Then the ReLU
			activation function will be applied. 

			example:
			[-1] -2-

			[0] -1- [-5] -4

			[1] -1-

			2(-1) + 1(0) + 1(1) + (-4) = -5

			ReLU(-5) = 0

		'''
		for i in range(1, len(self.layers)):
			for j in range(len(self.layers[i])):
				self.layers[i][j] = max(round(np.dot(self.layers[i-1], self.links[i][j]) + self.bias[i][j], result_round), 0)

	def get_output(self):
		return self.layers[-1]

	def prob_dis(self):
		exp_output_sum = sum([np.exp(i) for i in self.layers[-1]])
		return [np.exp(i)/exp_output_sum for i in self.layers[-1]]

	def get_children(self, children_num, link_range_round: list, bias_range_round: list):
		l = []
		for i in range(children_num):
			l.append(self)
			l[i].skew_links_bias(link_range_round, bias_range_round)
			# print(l[i])
			# print()
		return l

	def copy(self):
		n = NeuralNetwork(
			None,
			copy.deepcopy(self.layers),
			copy.deepcopy(self.links),
			copy.deepcopy(self.bias)
		)
		return n

	def __repr__(self):
		return "NeuralNetwork()"
	
	def __str__(self):
		return "Layers = " + str(self.layers) + "\n" + "Links = " + str(self.links) + "\n" + "Bias = " + str(self.bias)


def main():
	n = NeuralNetwork([2,3,2])
	print(n)
	print()

	n.set_input([5,5])
	n.skew_links_bias([-2.0,2.1,2], [-0.5,0.51,3])
	n.forward_pass(3)
	print(n)
	print(n.get_output())
	print()
	print()

	l = n.get_children(2, [-0.01,0.01,3], [-0.05,0.05,3])

if __name__ == '__main__':
	main()