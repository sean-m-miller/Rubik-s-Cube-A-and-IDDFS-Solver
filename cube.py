# All code written by Sean Miller, 5/12/18
# CS 351 Final Project, Rubik's Cube solver

from random import randint
from copy import deepcopy
from math import sqrt
from queue import PriorityQueue
from time import sleep

def dist(pt1, pt2):

	# Using pythagorean 3D distance formula, passing in two tuples of (x, y, z) coordinates. Gets called in the non-admissable heuristic.

	return sqrt((pt2[0] - pt1[0])**2 + (pt2[1] - pt1[1])**2 + (pt2[2] - pt1[2])**2)

class cube:

	# Every cube object has 6 sides. At construction, the cube is at a solved state

	def __init__(self):
		self.side0 = self.side(0)
		self.side1 = self.side(1)
		self.side2 = self.side(2)
		self.side3 = self.side(3)
		self.side4 = self.side(4)
		self.side5 = self.side(5)
	
	# Hash considers tuple of every cubie in cube, will be used for hashable explored set in A*

	def __hash__(self):
		return hash((

			self.side0.matrix[0][0],
			self.side0.matrix[0][1],
			self.side0.matrix[0][2],
			self.side0.matrix[1][0],
			self.side0.matrix[1][1],
			self.side0.matrix[1][2],
			self.side0.matrix[2][0],
			self.side0.matrix[2][1],
			self.side0.matrix[2][2],

			self.side1.matrix[0][0],
			self.side1.matrix[0][1],
			self.side1.matrix[0][2],
			self.side1.matrix[1][0],
			self.side1.matrix[1][1],
			self.side1.matrix[1][2],
			self.side1.matrix[2][0],
			self.side1.matrix[2][1],
			self.side1.matrix[2][2],

			self.side2.matrix[0][0],
			self.side2.matrix[0][1],
			self.side2.matrix[0][2],
			self.side2.matrix[1][0],
			self.side2.matrix[1][1],
			self.side2.matrix[1][2],
			self.side2.matrix[2][0],
			self.side2.matrix[2][1],
			self.side2.matrix[2][2],

			self.side3.matrix[0][0],
			self.side3.matrix[0][1],
			self.side3.matrix[0][2],
			self.side3.matrix[1][0],
			self.side3.matrix[1][1],
			self.side3.matrix[1][2],
			self.side3.matrix[2][0],
			self.side3.matrix[2][1],
			self.side3.matrix[2][2],

			self.side4.matrix[0][0],
			self.side4.matrix[0][1],
			self.side4.matrix[0][2],
			self.side4.matrix[1][0],
			self.side4.matrix[1][1],
			self.side4.matrix[1][2],
			self.side4.matrix[2][0],
			self.side4.matrix[2][1],
			self.side4.matrix[2][2],

			self.side5.matrix[0][0],
			self.side5.matrix[0][1],
			self.side5.matrix[0][2],
			self.side5.matrix[1][0],
			self.side5.matrix[1][1],
			self.side5.matrix[1][2],
			self.side5.matrix[2][0],
			self.side5.matrix[2][1],
			self.side5.matrix[2][2],

		))

	# comparisons below are required to put cube objects in priority queue... I only care about __eq__ and __ne__.

	def __lt__(self, other):
		return 0 < 1

	def __le__(self, other):
		return 0 <= 1

	def __gt__(self, other):
		return 0 > 1

	def __ge__(self, other):
		return 0 >= 1

	#this method only gets run when using python3
	def __eq__(self, other):
		return (self.side0.matrix == other.side0.matrix and self.side1.matrix == other.side1.matrix and self.side2.matrix == other.side2.matrix and self.side3.matrix == other.side3.matrix and self.side4.matrix == other.side4.matrix and self.side5.matrix == other.side5.matrix)
	
	def __ne__(self, other):
		return not (self.side0.matrix == other.side0.matrix and self.side1.matrix == other.side1.matrix and self.side2.matrix == other.side2.matrix and self.side3.matrix == other.side3.matrix and self.side4.matrix == other.side4.matrix and self.side5.matrix == other.side5.matrix)
	
	# this method only gets run when using python2	
	def __cmp__(self,other):
		return (self.side0.matrix == other.side0.matrix and self.side1.matrix == other.side1.matrix and self.side2.matrix == other.side2.matrix and self.side3.matrix == other.side3.matrix and self.side4.matrix == other.side4.matrix and self.side5.matrix == other.side5.matrix)

	def heuristic(self, coordinates): 

	# 3D manhattan distance - sum up all distances between every corner cubie and the correct center cubie (same color)

	# do the same for edge cubies

	# THIS HEURISTIC IS NOT ADMISSABLE - very often, A* search with this heuristic enters cycles where it switches between 2 - 5 states.
	# even with an explored state, there are many situations where this heuristic would have to do 
	# hours of searching before finding the correct move

		# list of (corner cubie, "static location") - the "static location" gets mapped 
		# to an (x, y, z) coordinate through the passed in dictionary 'coordinates'

		corners = [

			(self.side0.matrix[0][0], (0, 0, 0)),
			(self.side0.matrix[0][2], (0, 0, 2)),
			(self.side0.matrix[2][0], (0, 2, 0)),
			(self.side0.matrix[2][2], (0, 2, 2)),

			(self.side1.matrix[0][0], (1, 0, 0)),
			(self.side1.matrix[0][2], (1, 0, 2)),
			(self.side1.matrix[2][0], (1, 2, 0)),
			(self.side1.matrix[2][2], (1, 2, 2)),

			(self.side2.matrix[0][0], (2, 0, 0)),
			(self.side2.matrix[0][2], (2, 0, 2)),
			(self.side2.matrix[2][0], (2, 2, 0)),
			(self.side2.matrix[2][2], (2, 2, 2)),

			(self.side3.matrix[0][0], (3, 0, 0)),
			(self.side3.matrix[0][2], (3, 0, 2)),
			(self.side3.matrix[2][0], (3, 2, 0)),
			(self.side3.matrix[2][2], (3, 2, 2)),

			(self.side4.matrix[0][0], (4, 0, 0)),
			(self.side4.matrix[0][2], (4, 0, 2)),
			(self.side4.matrix[2][0], (4, 2, 0)),
			(self.side4.matrix[2][2], (4, 2, 2)),

			(self.side5.matrix[0][0], (5, 0, 0)),
			(self.side5.matrix[0][2], (5, 0, 2)),
			(self.side5.matrix[2][0], (5, 2, 0)),
			(self.side5.matrix[2][2], (5, 2, 2))

		]

		# list of (edge cubie, "static location")

		edges = [ 

			(self.side0.matrix[0][1], (0, 0, 1)),
			(self.side0.matrix[1][0], (0, 1, 0)),
			(self.side0.matrix[1][2], (0, 1, 2)),
			(self.side0.matrix[2][1], (0, 2, 1)),

			(self.side1.matrix[0][1], (1, 0, 1)),
			(self.side1.matrix[1][0], (1, 1, 0)),
			(self.side1.matrix[1][2], (1, 1, 2)),
			(self.side1.matrix[2][1], (1, 2, 1)),

			(self.side2.matrix[0][1], (2, 0, 1)),
			(self.side2.matrix[1][0], (2, 1, 0)),
			(self.side2.matrix[1][2], (2, 1, 2)),
			(self.side2.matrix[2][1], (2, 2, 1)),

			(self.side3.matrix[0][1], (3, 0, 1)),
			(self.side3.matrix[1][0], (3, 1, 0)),
			(self.side3.matrix[1][2], (3, 1, 2)),
			(self.side3.matrix[2][1], (3, 2, 1)),

			(self.side4.matrix[0][1], (4, 0, 1)),
			(self.side4.matrix[1][0], (4, 1, 0)),
			(self.side4.matrix[1][2], (4, 1, 2)),
			(self.side4.matrix[2][1], (4, 2, 1)),

			(self.side5.matrix[0][1], (5, 0, 1)),
			(self.side5.matrix[1][0], (5, 1, 0)),
			(self.side5.matrix[1][2], (5, 1, 2)),
			(self.side5.matrix[2][1], (5, 2, 1))

		]

		# list of all center cubies and their static locations

		centers = [

			(self.side0.matrix[1][1], (0, 1, 1)),
			(self.side1.matrix[1][1], (1, 1, 1)),
			(self.side2.matrix[1][1], (2, 1, 1)),
			(self.side3.matrix[1][1], (3, 1, 1)),
			(self.side4.matrix[1][1], (4, 1, 1)),
			(self.side5.matrix[1][1], (5, 1, 1))

		]

		corner_total = 0
		edge_total = 0
		total = 0
		for i in corners:
			for j in centers:
				if(i[0] == j[0]): # if the colors match - first argument in the tuples in the lists above get dereferenced to the colors at that location
					corner_total += dist(coordinates[i[1]], coordinates[j[1]]) # calculate 3d distance using coordinates between corner cubie and center, add to sum
		total += corner_total
		for i in edges:
			for j in centers:
				if(i[0] == j[0]): # if the colors match
					edge_total += dist(coordinates[i[1]], coordinates[j[1]]) # calculate 3d distance using coordinates between edge cubie and center, add to sum
		total += edge_total 

		# I added the code below to try to make the heuristic admissable. This code handles a basic situation where 3D distance must get worse
		# before it can get better. I make this situation highly desirable by greatly reducing the heuristic. From this position, 
		# the best next move is a win state, which gets chosen next everytime the code below runs.
		# While this does not make it admissable in all cases, it did help some situations when the cube was only shuffled twice.

		if self.side0.matrix[0] == self.side0.matrix[2] and self.side1.matrix[0] == self.side1.matrix[2] and self.side2.matrix[0] == self.side2.matrix[2] and self.side3.matrix[0] == self.side3.matrix[2]:
			total -= 50
		elif self.side0.matrix[0][0] == self.side0.matrix[0][2] and self.side0.matrix[1][0] == self.side0.matrix[0][0] and self.side0.matrix[2][0] == self.side0.matrix[0][0] and self.side0.matrix[0][0] == self.side0.matrix[1][2] and self.side0.matrix[0][0] == self.side0.matrix[2][2]:
			total -= 50

		return total

	# This is the second heuristic I tried. Instead of calculating 3D distance, it just compares every edge and corner cubie to the center cubie 
	# with the same color, and adds the number of sides bewteen both elements in each pair. A cubie adds either 0 (same side as the center cubie), 
	# 1 (the 4 sides touching that side), or 2 (the side on the opposite side of the cube) to the sum. 
	# While it is admissable, it still takes an incredibly long time in some situations. 

	def heuristic2(self):

		edges = [

			self.side0.matrix[0][1],
			self.side0.matrix[1][0],
			self.side0.matrix[1][2],
			self.side0.matrix[2][1],

			self.side1.matrix[0][1],
			self.side1.matrix[1][0],
			self.side1.matrix[1][2],
			self.side1.matrix[2][1],

			self.side2.matrix[0][1],
			self.side2.matrix[1][0],
			self.side2.matrix[1][2],
			self.side2.matrix[2][1],

			self.side3.matrix[0][1],
			self.side3.matrix[1][0],
			self.side3.matrix[1][2],
			self.side3.matrix[2][1],

			self.side4.matrix[0][1],
			self.side4.matrix[1][0],
			self.side4.matrix[1][2],
			self.side4.matrix[2][1],

			self.side5.matrix[0][1],
			self.side5.matrix[1][0],
			self.side5.matrix[1][2],
			self.side5.matrix[2][1]

		]

		corners = [

			self.side0.matrix[0][0],
			self.side0.matrix[0][2],
			self.side0.matrix[2][0],
			self.side0.matrix[2][2],

			self.side1.matrix[0][0],
			self.side1.matrix[0][2],
			self.side1.matrix[2][0],
			self.side1.matrix[2][2],

			self.side2.matrix[0][0],
			self.side2.matrix[0][2],
			self.side2.matrix[2][0],
			self.side2.matrix[2][2],

			self.side3.matrix[0][0],
			self.side3.matrix[0][2],
			self.side3.matrix[2][0],
			self.side3.matrix[2][2],

			self.side4.matrix[0][0],
			self.side4.matrix[0][2],
			self.side4.matrix[2][0],
			self.side4.matrix[2][2],

			self.side5.matrix[0][0],
			self.side5.matrix[0][2],
			self.side5.matrix[2][0],
			self.side5.matrix[2][2]
		]

		centers = [

			self.side0.matrix[1][1],
			self.side1.matrix[1][1],
			self.side2.matrix[1][1],
			self.side3.matrix[1][1],
			self.side4.matrix[1][1],
			self.side5.matrix[1][1]

		]

		edge_total = 0
		for i in range(len(edges)):
			if i < 4: # side 0 edge, 
				for j in range(len(centers)):
					if edges[i] == centers[j]:
						if j == 1 or j == 3 or j == 4 or j == 5:
							edge_total += 1
						if j == 2:
							edge_total += 2
			if 4 <= i and i < 8: # side 1 edge
				for j in range(len(centers)):
					if edges[i] == centers[j]:
						if j == 0 or j == 2 or j == 4 or j == 5:
							edge_total += 1
						if j == 3:
							edge_total += 2
			if 8 <= i and i < 12: # side 2 edge
				for j in range(len(centers)):
					if edges[i] == centers[j]:
						if j == 1 or j == 3 or j == 4 or j == 5:
							edge_total += 1
						if j == 0:
							edge_total += 2
			if 12 <= i and i < 16: # side 3 edge
				for j in range(len(centers)):
					if edges[i] == centers[j]:
						if j == 0 or j == 2 or j == 4 or j == 5:
							edge_total += 1
						if j == 1:
							edge_total += 2
			if 16 <= i and i < 20: # side 4 edge
				for j in range(len(centers)):
					if edges[i] == centers[j]:
						if j == 0 or j == 1 or j == 2 or j == 3:
							edge_total += 1
						if j == 5:
							edge_total += 2
			if 20 <= i: # side 5 edge
				for j in range(len(centers)):
					if edges[i] == centers[j]:
						if j == 0 or j == 1 or j == 2 or j == 3:
							edge_total += 1
						if j == 4:
							edge_total += 2

		corner_total = 0
		for i in range(len(corners)):
			if i < 4: # side 0 corner, 
				for j in range(len(centers)):
					if corners[i] == centers[j]:
						if j == 1 or j == 3 or j == 4 or j == 5:
							corner_total += 1
						if j == 2:
							corner_total += 2
			if 4 <= i and i < 8: # side 1 corner
				for j in range(len(centers)):
					if corners[i] == centers[j]:
						if j == 0 or j == 2 or j == 4 or j == 5:
							edge_total += 1
						if j == 3:
							corner_total += 2
			if 8 <= i and i < 12: # side 2 corner
				for j in range(len(centers)):
					if corners[i] == centers[j]:
						if j == 1 or j == 3 or j == 4 or j == 5:
							corner_total += 1
						if j == 0:
							edge_total += 2
			if 12 <= i and i < 16: # side 3 corner
				for j in range(len(centers)):
					if corners[i] == centers[j]:
						if j == 0 or j == 2 or j == 4 or j == 5:
							corner_total += 1
						if j == 1:
							corner_total += 2
			if 16 <= i and i < 20: # side 4 corner
				for j in range(len(centers)):
					if corners[i] == centers[j]:
						if j == 0 or j == 1 or j == 2 or j == 3:
							corner_total += 1
						if j == 5:
							corner_total += 2
			if 20 <= i: # side 5 corner
				for j in range(len(centers)):
					if corners[i] == centers[j]:
						if j == 0 or j == 1 or j == 2 or j == 3:
							corner_total += 1
						if j == 4:
							corner_total += 2
		return corner_total + edge_total
			

	# Checks if win state.

	def isWin(self):
		first = self.side0.matrix[0][0]
		if not ((self.side0.matrix[0].count(first) == 3) and (self.side0.matrix[1].count(first) == 3) and (self.side0.matrix[2].count(first) == 3)):
			return False
		first = self.side1.matrix[0][0]
		if not ((self.side1.matrix[0].count(first) == 3) and (self.side1.matrix[1].count(first) == 3) and (self.side1.matrix[2].count(first) == 3)):
			return False
		first = self.side2.matrix[0][0]
		if not ((self.side2.matrix[0].count(first) == 3) and (self.side2.matrix[1].count(first) == 3) and (self.side2.matrix[2].count(first) == 3)):
			return False
		first = self.side3.matrix[0][0]
		if not ((self.side3.matrix[0].count(first) == 3) and (self.side3.matrix[1].count(first) == 3) and (self.side3.matrix[2].count(first) == 3)):
			return False
		first = self.side4.matrix[0][0]
		if not ((self.side4.matrix[0].count(first) == 3) and (self.side4.matrix[1].count(first) == 3) and (self.side4.matrix[2].count(first) == 3)):
			return False
		first = self.side5.matrix[0][0]
		if not ((self.side5.matrix[0].count(first) == 3) and (self.side5.matrix[1].count(first) == 3) and (self.side5.matrix[2].count(first) == 3)):
			return False
		else:
			return True

	# The awful, very thoroughly tested matrix functions to model the cube's possible moves.

	def side0_rot_horiz(self, index, direction): # column index/row index, "left"/"right"
		if index == 0: #top row, transpose side1
			if direction == "right":
				self.side4.trans_l()
				temp = self.side0.matrix[0]
				self.side0.matrix[0] = self.side3.matrix[0]
				self.side3.matrix[0] = self.side2.matrix[0]
				self.side2.matrix[0] = self.side1.matrix[0]
				self.side1.matrix[0] = temp
			elif direction == "left":
				self.side4.trans_r()
				temp = self.side0.matrix[0]
				self.side0.matrix[0] = self.side1.matrix[0]
				self.side1.matrix[0] = self.side2.matrix[0]
				self.side2.matrix[0] = self.side3.matrix[0]
				self.side3.matrix[0] = temp
			else:
				print("invalid direction: 'up' or 'down' only")
		elif index == 1:
			if direction == "right":
				temp = self.side0.matrix[1]
				self.side0.matrix[1] = self.side3.matrix[1]
				self.side3.matrix[1] = self.side2.matrix[1]
				self.side2.matrix[1] = self.side1.matrix[1]
				self.side1.matrix[1] = temp
			elif direction == "left":
				temp = self.side0.matrix[1]
				self.side0.matrix[1] = self.side1.matrix[1]
				self.side1.matrix[1] = self.side2.matrix[1]
				self.side2.matrix[1] = self.side3.matrix[1]
				self.side3.matrix[1] = temp
			else:
				print("invalid direction: 'up' or 'down' only")
		elif index == 2:
			if direction == "right":
				self.side5.trans_r()
				temp = self.side0.matrix[2]
				self.side0.matrix[2] = self.side3.matrix[2]
				self.side3.matrix[2] = self.side2.matrix[2]
				self.side2.matrix[2] = self.side1.matrix[2]
				self.side1.matrix[2] = temp
			elif direction == "left":
				self.side5.trans_l()
				temp = self.side0.matrix[2]
				self.side0.matrix[2] = self.side1.matrix[2]
				self.side1.matrix[2] = self.side2.matrix[2]
				self.side2.matrix[2] = self.side3.matrix[2]
				self.side3.matrix[2] = temp
			else:
				print("invalid direction: 'up' or 'down' only")
		else:
			print("invalid index: 0, 1, or 2 only")

	def side0_rot_vert(self, index, direction):
		if index == 0: #first column, index 0 of each row

			temp0 = self.side0.matrix[0][0]
			temp1 = self.side0.matrix[1][0]
			temp2 = self.side0.matrix[2][0]

			if direction == "up":
				self.side3.trans_l()

				self.side0.matrix[0][0] = self.side5.matrix[2][0]
				self.side0.matrix[1][0] = self.side5.matrix[2][1]
				self.side0.matrix[2][0] = self.side5.matrix[2][2]

				self.side5.matrix[2][0] = self.side2.matrix[2][2]
				self.side5.matrix[2][1] = self.side2.matrix[1][2]
				self.side5.matrix[2][2] = self.side2.matrix[0][2]

				self.side2.matrix[0][2] = self.side4.matrix[0][0]
				self.side2.matrix[1][2] = self.side4.matrix[0][1]
				self.side2.matrix[2][2] = self.side4.matrix[0][2]

				self.side4.matrix[0][2] = temp0
				self.side4.matrix[0][1] = temp1
				self.side4.matrix[0][0] = temp2
			elif direction == "down":
				self.side3.trans_r()

				self.side0.matrix[0][0] = self.side4.matrix[0][2]
				self.side0.matrix[1][0] = self.side4.matrix[0][1]
				self.side0.matrix[2][0] = self.side4.matrix[0][0]

				self.side4.matrix[0][2] = self.side2.matrix[2][2]
				self.side4.matrix[0][1] = self.side2.matrix[1][2]
				self.side4.matrix[0][0] = self.side2.matrix[0][2]

				self.side2.matrix[0][2] = self.side5.matrix[2][2]
				self.side2.matrix[1][2] = self.side5.matrix[2][1]
				self.side2.matrix[2][2] = self.side5.matrix[2][0]

				self.side5.matrix[2][0] = temp0
				self.side5.matrix[2][1] = temp1
				self.side5.matrix[2][2] = temp2
			else:
				print("invalid direction: 'up' or 'down' only")

		elif index == 1:

			temp0 = self.side0.matrix[0][1]
			temp1 = self.side0.matrix[1][1]
			temp2 = self.side0.matrix[2][1]

			if direction == "up":
				self.side0.matrix[0][1] = self.side5.matrix[1][0]
				self.side0.matrix[1][1] = self.side5.matrix[1][1]
				self.side0.matrix[2][1] = self.side5.matrix[1][2]

				self.side5.matrix[1][0] = self.side2.matrix[2][1]
				self.side5.matrix[1][1] = self.side2.matrix[1][1]
				self.side5.matrix[1][2] = self.side2.matrix[0][1]

				self.side2.matrix[0][1] = self.side4.matrix[1][0]
				self.side2.matrix[1][1] = self.side4.matrix[1][1]
				self.side2.matrix[2][1] = self.side4.matrix[1][2]

				self.side4.matrix[1][2] = temp0
				self.side4.matrix[1][1] = temp1
				self.side4.matrix[1][0] = temp2

			elif direction == "down":
				self.side0.matrix[0][1] = self.side4.matrix[1][2]
				self.side0.matrix[1][1] = self.side4.matrix[1][1]
				self.side0.matrix[2][1] = self.side4.matrix[1][0]

				self.side4.matrix[1][0] = self.side2.matrix[0][1]
				self.side4.matrix[1][1] = self.side2.matrix[1][1]
				self.side4.matrix[1][2] = self.side2.matrix[2][1]

				self.side2.matrix[0][1] = self.side5.matrix[1][2]
				self.side2.matrix[1][1] = self.side5.matrix[1][1]
				self.side2.matrix[2][1] = self.side5.matrix[1][0]

				self.side5.matrix[1][0] = temp0
				self.side5.matrix[1][1] = temp1
				self.side5.matrix[1][2] = temp2
			else:
				print("invalid direction: 'up' or 'down' only")

		elif index == 2:

			temp0 = self.side0.matrix[0][2]
			temp1 = self.side0.matrix[1][2]
			temp2 = self.side0.matrix[2][2]

			if direction == "up":
				self.side1.trans_r()
				self.side0.matrix[0][2] = self.side5.matrix[0][0]
				self.side0.matrix[1][2] = self.side5.matrix[0][1]
				self.side0.matrix[2][2] = self.side5.matrix[0][2]

				self.side5.matrix[0][0] = self.side2.matrix[2][0]
				self.side5.matrix[0][1] = self.side2.matrix[1][0]
				self.side5.matrix[0][2] = self.side2.matrix[0][0]

				self.side2.matrix[0][0] = self.side4.matrix[2][0]
				self.side2.matrix[1][0] = self.side4.matrix[2][1]
				self.side2.matrix[2][0] = self.side4.matrix[2][2]

				self.side4.matrix[2][2] = temp0
				self.side4.matrix[2][1] = temp1
				self.side4.matrix[2][0] = temp2

			elif direction == "down":
				self.side1.trans_l()
				self.side0.matrix[0][2] = self.side4.matrix[2][2]
				self.side0.matrix[1][2] = self.side4.matrix[2][1]
				self.side0.matrix[2][2] = self.side4.matrix[2][0]

				self.side4.matrix[2][0] = self.side2.matrix[0][0]
				self.side4.matrix[2][1] = self.side2.matrix[1][0]
				self.side4.matrix[2][2] = self.side2.matrix[2][0]

				self.side2.matrix[0][0] = self.side5.matrix[0][2]
				self.side2.matrix[1][0] = self.side5.matrix[0][1]
				self.side2.matrix[2][0] = self.side5.matrix[0][0]

				self.side5.matrix[0][0] = temp0
				self.side5.matrix[0][1] = temp1
				self.side5.matrix[0][2] = temp2
			else:
				print("invalid direction: 'up' or 'down' only")
		else:
			print("invalid index: 0, 1, or 2 only")

	def side1_rot_vert(self, index, direction):
		if index == 0:

			temp0 = self.side1.matrix[0][0]
			temp1 = self.side1.matrix[1][0]
			temp2 = self.side1.matrix[2][0]

			if direction == "up":
				self.side0.trans_l()
				self.side1.matrix[0][0] = self.side5.matrix[0][0]
				self.side1.matrix[1][0] = self.side5.matrix[1][0]
				self.side1.matrix[2][0] = self.side5.matrix[2][0]

				self.side5.matrix[0][0] = self.side3.matrix[2][2]
				self.side5.matrix[1][0] = self.side3.matrix[1][2]
				self.side5.matrix[2][0] = self.side3.matrix[0][2]

				self.side3.matrix[0][2] = self.side4.matrix[2][0]
				self.side3.matrix[1][2] = self.side4.matrix[1][0]
				self.side3.matrix[2][2] = self.side4.matrix[0][0]

				self.side4.matrix[0][0] = temp0
				self.side4.matrix[1][0] = temp1
				self.side4.matrix[2][0] = temp2
			elif direction == "down":
				self.side0.trans_r()
				self.side1.matrix[0][0] = self.side4.matrix[0][0]
				self.side1.matrix[1][0] = self.side4.matrix[1][0]
				self.side1.matrix[2][0] = self.side4.matrix[2][0]

				self.side4.matrix[0][0] = self.side3.matrix[2][2]
				self.side4.matrix[1][0] = self.side3.matrix[1][2]
				self.side4.matrix[2][0] = self.side3.matrix[0][2]

				self.side3.matrix[2][2] = self.side5.matrix[0][0]
				self.side3.matrix[1][2] = self.side5.matrix[1][0]
				self.side3.matrix[0][2] = self.side5.matrix[2][0]

				self.side5.matrix[0][0] = temp0
				self.side5.matrix[1][0] = temp1
				self.side5.matrix[2][0] = temp2
			else:
				print("invalid direction: 'up' or 'down' only")
		elif index == 1:

			temp0 = self.side1.matrix[0][1]
			temp1 = self.side1.matrix[1][1]
			temp2 = self.side1.matrix[2][1]

			if direction == "up":
				self.side1.matrix[0][1] = self.side5.matrix[0][1]
				self.side1.matrix[1][1] = self.side5.matrix[1][1]
				self.side1.matrix[2][1] = self.side5.matrix[2][1]

				self.side5.matrix[0][1] = self.side3.matrix[2][1]
				self.side5.matrix[1][1] = self.side3.matrix[1][1]
				self.side5.matrix[2][1] = self.side3.matrix[0][1]

				self.side3.matrix[0][1] = self.side4.matrix[2][1]
				self.side3.matrix[1][1] = self.side4.matrix[1][1]
				self.side3.matrix[2][1] = self.side4.matrix[0][1]

				self.side4.matrix[0][1] = temp0
				self.side4.matrix[1][1] = temp1
				self.side4.matrix[2][1] = temp2
			elif direction == "down":
				self.side1.matrix[0][1] = self.side4.matrix[0][1]
				self.side1.matrix[1][1] = self.side4.matrix[1][1]
				self.side1.matrix[2][1] = self.side4.matrix[2][1]

				self.side4.matrix[0][1] = self.side3.matrix[2][1]
				self.side4.matrix[1][1] = self.side3.matrix[1][1]
				self.side4.matrix[2][1] = self.side3.matrix[0][1]

				self.side3.matrix[2][1] = self.side5.matrix[0][1]
				self.side3.matrix[1][1] = self.side5.matrix[1][1]
				self.side3.matrix[0][1] = self.side5.matrix[2][1]

				self.side5.matrix[0][1] = temp0
				self.side5.matrix[1][1] = temp1
				self.side5.matrix[2][1] = temp2
			else:
				print("invalid direction: 'up' or 'down' only")
		elif index == 2:

			temp0 = self.side1.matrix[0][2]
			temp1 = self.side1.matrix[1][2]
			temp2 = self.side1.matrix[2][2]

			if direction == "up":
				self.side2.trans_r()
				self.side1.matrix[0][2] = self.side5.matrix[0][2]
				self.side1.matrix[1][2] = self.side5.matrix[1][2]
				self.side1.matrix[2][2] = self.side5.matrix[2][2]

				self.side5.matrix[0][2] = self.side3.matrix[2][0]
				self.side5.matrix[1][2] = self.side3.matrix[1][0]
				self.side5.matrix[2][2] = self.side3.matrix[0][0]

				self.side3.matrix[0][0] = self.side4.matrix[2][2]
				self.side3.matrix[1][0] = self.side4.matrix[1][2]
				self.side3.matrix[2][0] = self.side4.matrix[0][2]

				self.side4.matrix[0][2] = temp0
				self.side4.matrix[1][2] = temp1
				self.side4.matrix[2][2] = temp2
			elif direction == "down":
				self.side2.trans_l()
				self.side1.matrix[0][2] = self.side4.matrix[0][2]
				self.side1.matrix[1][2] = self.side4.matrix[1][2]
				self.side1.matrix[2][2] = self.side4.matrix[2][2]

				self.side4.matrix[0][2] = self.side3.matrix[2][0]
				self.side4.matrix[1][2] = self.side3.matrix[1][0]
				self.side4.matrix[2][2] = self.side3.matrix[0][0]

				self.side3.matrix[2][0] = self.side5.matrix[0][2]
				self.side3.matrix[1][0] = self.side5.matrix[1][2]
				self.side3.matrix[0][0] = self.side5.matrix[2][2]

				self.side5.matrix[0][2] = temp0
				self.side5.matrix[1][2] = temp1
				self.side5.matrix[2][2] = temp2
			else:
				print("invalid direction: 'up' or 'down' only")
		else:
			print("invalid index: 0, 1, or 2 only")

	def shuffle(self, times):
		for i in range(0, times):
			s = randint(0, 17)
			if s == 0:
				self.side0_rot_vert(0, "up")
				print("side0_rot_vert(0, up)")
			elif s == 1:
				self.side0_rot_vert(1, "up")
				print("side0_rot_vert(1, up)")
			elif s == 2:
				self.side0_rot_vert(2, "up")
				print("side0_rot_vert(2, up)")
			elif s == 3:
				self.side0_rot_vert(2, "down")
				print("side0_rot_vert(2, down)")
			elif s == 4:
				self.side0_rot_vert(1, "down")
				print("side0_rot_vert(1, down)")
			elif s == 5:
				self.side0_rot_vert(0, "down")
				print("side0_rot_vert(0, down)")
			elif s == 6:
				self.side0_rot_horiz(0, "left")
				print("side0_rot_horiz(0, left)")
			elif s == 7:
				self.side0_rot_horiz(1, "left")
				print("side0_rot_horiz(1, left)")
			elif s == 8:
				self.side0_rot_horiz(2, "left")
				print("side0_rot_horiz(2, left)")
			elif s == 9:
				self.side0_rot_horiz(2, "right")
				print("side0_rot_horiz(2, right)")
			elif s == 10:
				self.side0_rot_horiz(1, "right")
				print("side0_rot_horiz(1, right)")
			elif s == 11:
				self.side0_rot_horiz(0, "right")
				print("side0_rot_horiz(0, right)")
			elif s == 12:
				self.side1_rot_vert(0, "up")
				print("side1_rot_vert(0, up)")
			elif s == 13:
				self.side1_rot_vert(1, "up")
				print("side1_rot_vert(1, up)")
			elif s == 14:
				self.side1_rot_vert(2, "up")
				print("side1_rot_vert(2, up)")
			elif s == 15:
				self.side1_rot_vert(0, "down")
				print("side1_rot_vert(0, down)")
			elif s == 16:
				self.side1_rot_vert(1, "down")
				print("side1_rot_vert(1, down)")
			else:
				self.side1_rot_vert(2, "down")
				print("side1_rot_vert(2, down)")


	# prints the matrix

	def print_cube(self):
		self.side0.print_side()
		self.side1.print_side()
		self.side2.print_side()
		self.side3.print_side()
		self.side4.print_side()
		self.side5.print_side()

	class side:

		def __init__(self, val):
			self.matrix = [[], [], []] #[row1, row2, row3], row = [col1, col2, col3]
			self.val = val
			count = 0
			if val == 0:
				for i in self.matrix:
					for j in range(3):
						i.append("white")
					count+=1
				return
			if val == 1:
				for i in self.matrix:
					for j in range(3):
						i.append("green")
					count+=1
				return
			if val == 2:
				for i in self.matrix:
					for j in range(3):
						i.append("yellow")
					count+=1
				return
			if val == 3:
				for i in self.matrix:
					for j in range(3):
						i.append("blue")
					count+=1
				return
			if val == 4:
				for i in self.matrix:
					for j in range(3):
						i.append("red")
					count+=1
				return
			if val == 5:
				for i in self.matrix:
					for j in range(3):
						i.append("orange")
					count+=1
				return

		def trans_l(self): # a left transpose of the 3x3 matrix
			newMatrix = deepcopy(self.matrix)		# deep copy. Prevents duplication of colors
			newMatrix[0][0] = self.matrix[0][2]
			newMatrix[1][0] = self.matrix[0][1]
			newMatrix[2][0] = self.matrix[0][0]

			newMatrix[2][1] = self.matrix[1][0]
			newMatrix[2][2] = self.matrix[2][0]

			newMatrix[1][2] = self.matrix[2][1]
			newMatrix[0][2] = self.matrix[2][2]

			newMatrix[0][1] = self.matrix[1][2]
			self.matrix = newMatrix

		def trans_r(self): # a right transpose of the 3x3 matrix
			newMatrix = deepcopy(self.matrix)
			newMatrix[0][0] = self.matrix[2][0]
			newMatrix[1][0] = self.matrix[2][1]
			newMatrix[2][0] = self.matrix[2][2]

			newMatrix[0][1] = self.matrix[1][0]
			newMatrix[0][2] = self.matrix[0][0]

			newMatrix[1][2] = self.matrix[0][1]
			newMatrix[2][2] = self.matrix[0][2]

			newMatrix[2][1] = self.matrix[1][2]
			self.matrix = newMatrix

		def print_side(self): # helper function for print_cube()
			print("side ", self.val)
			print(self.matrix)

coordinates = {

	# The 3D coordinates of every cubie

	# this is an example of why I probably should have had a cubie class nested in the side class... 
	# I have to index into this dictionary to retrieve a 3D coordinate, 

	# (side number, row, col) : (x-coordinate, y-coordinate, z-coordinate)

	# I use negative values to denote cubies facing in directions "down" and "towards the user (side0)" and "to the left". 
	# This will not cause errors when calculating 3d distances since the sum of all 2d distances is square-rooted only after every 2d distance is squared (made 0 or posotive)

	(0, 0, 0) : (0, 0, -1),
	(0, 0, 1) : (0, 1, -1),
	(0, 0, 2) : (0, 2, -1),
	(0, 1, 0) : (1, 0, -1),
	(0, 1, 1) : (1, 1, -1),
	(0, 1, 2) : (1, 2, -1),
	(0, 2, 0) : (2, 0, -1),
	(0, 2, 1) : (2, 1, -1),
	(0, 2, 2) : (2, 2, -1),

	(1, 0, 0) : (0, 3, 0),
	(1, 0, 1) : (0, 3, 1),
	(1, 0, 2) : (0, 3, 2),
	(1, 1, 0) : (1, 3, 0),
	(1, 1, 1) : (1, 3, 1),
	(1, 1, 2) : (1, 3, 2),
	(1, 2, 0) : (2, 3, 0),
	(1, 2, 1) : (2, 3, 1),
	(1, 2, 2) : (2, 3, 2),

	(2, 0, 0) : (0, 2, 3),
	(2, 0, 1) : (0, 1, 3),
	(2, 0, 2) : (0, 0, 3),
	(2, 1, 0) : (1, 2, 3),
	(2, 1, 1) : (1, 1, 3),
	(2, 1, 2) : (1, 0, 3),
	(2, 2, 0) : (2, 2, 3),
	(2, 2, 1) : (2, 1, 3),
	(2, 2, 2) : (2, 0, 3),

	(3, 0, 0) : (0, -1, 2),
	(3, 0, 1) : (0, -1, 1),
	(3, 0, 2) : (0, -1, 0),
	(3, 1, 0) : (1, -1, 2),
	(3, 1, 1) : (1, -1, 1),
	(3, 1, 2) : (1, -1, 0),
	(3, 2, 0) : (2, -1, 2),
	(3, 2, 1) : (2, -1, 1),
	(3, 2, 2) : (2, -1, 0),

	(4, 0, 0) : (-1, 0, 0),
	(4, 0, 1) : (-1, 0, 1),
	(4, 0, 2) : (-1, 0, 2),
	(4, 1, 0) : (-1, 1, 0),
	(4, 1, 1) : (-1, 1, 1),
	(4, 1, 2) : (-1, 1, 2),
	(4, 2, 0) : (-1, 2, 0),
	(4, 2, 1) : (-1, 2, 1),
	(4, 2, 2) : (-1, 2, 2),

 	(5, 0, 0) : (3, 2, 0),
	(5, 0, 1) : (3, 2, 1),
	(5, 0, 2) : (3, 2, 0),
	(5, 1, 0) : (3, 1, 0),
	(5, 1, 1) : (3, 1, 1),
	(5, 1, 2) : (3, 1, 2),
	(5, 2, 0) : (3, 0, 0),
	(5, 2, 1) : (3, 0, 1),
	(5, 2, 2) : (3, 0, 2)

}


def astar(difficulty): # using non-admissible heuristic
	mycube = cube()
	mycube.shuffle(difficulty)
	explored = set()
	frontier = PriorityQueue()
	frontier.put((mycube.heuristic(coordinates), deepcopy(mycube))) # all tuples in priority queue are of the form (heuristic value, deepcopy of object). It first sorts by heuristic.
	explored.add(deepcopy(mycube))
	while(not frontier.empty()):
		parent = frontier.get()[1] # the cube object associated with each heuristic
		if parent.isWin():
			print("WOOOO WE FOUND IT!")
			return
		child0 = deepcopy(parent)
		child0.side0_rot_vert(0, "up")
		if child0 not in explored:
			frontier.put((child0.heuristic(coordinates), deepcopy(child0)))
			explored.add(deepcopy(child0))

		child1 = deepcopy(parent)
		child1.side0_rot_vert(1, "up")
		if child1 not in explored:
			frontier.put((child1.heuristic(coordinates), deepcopy(child1)))
			explored.add(deepcopy(child1))

		child2 = deepcopy(parent)
		child2.side0_rot_vert(2, "up")
		if child2 not in explored:
			frontier.put((child2.heuristic(coordinates), deepcopy(child2)))
			explored.add(deepcopy(child2))

		child3 = deepcopy(parent)
		child3.side0_rot_vert(2, "down")
		if child3 not in explored:
			frontier.put((child3.heuristic(coordinates), deepcopy(child3)))
			explored.add(deepcopy(child3))

		child4 = deepcopy(parent)
		child4.side0_rot_vert(1, "down")
		if child4 not in explored:
			frontier.put((child4.heuristic(coordinates), deepcopy(child4)))
			explored.add(deepcopy(child4))

		child5 = deepcopy(parent)
		child5.side0_rot_vert(0, "down")
		if child5 not in explored:
			frontier.put((child5.heuristic(coordinates), deepcopy(child5)))
			explored.add(deepcopy(child5))

		child6 = deepcopy(parent)
		child6.side0_rot_horiz(0, "left")
		if child6 not in explored:
			frontier.put((child6.heuristic(coordinates), deepcopy(child6)))
			explored.add(deepcopy(child6))

		child7 = deepcopy(parent)
		child7.side0_rot_horiz(1, "left")
		if child7 not in explored:
			frontier.put((child7.heuristic(coordinates), deepcopy(child7)))
			explored.add(deepcopy(child7))

		child8 = deepcopy(parent)
		child8.side0_rot_horiz(2, "left")
		if child8 not in explored:
			frontier.put((child8.heuristic(coordinates), deepcopy(child8)))
			explored.add(deepcopy(child8))

		child9 = deepcopy(parent)
		child9.side0_rot_horiz(2, "right")
		if child9 not in explored:
			frontier.put((child9.heuristic(coordinates), deepcopy(child9)))
			explored.add(deepcopy(child9))

		child10 = deepcopy(parent)
		child10.side0_rot_horiz(1, "right")
		if child10 not in explored:
			frontier.put((child10.heuristic(coordinates), deepcopy(child10)))
			explored.add(deepcopy(child10))

		child11 = deepcopy(parent)
		child11.side0_rot_horiz(0, "right")
		if child11 not in explored:
			frontier.put((child11.heuristic(coordinates), deepcopy(child11)))
			explored.add(deepcopy(child11))

		child12 = deepcopy(parent)
		child12.side1_rot_vert(2, "up")
		if child12 not in explored:
			frontier.put((child12.heuristic(coordinates), deepcopy(child12)))
			explored.add(deepcopy(child12))

		child13 = deepcopy(parent)
		child13.side1_rot_vert(1, "up")
		if child13 not in explored:
			frontier.put((child13.heuristic(coordinates), deepcopy(child13)))
			explored.add(deepcopy(child13))

		child14 = deepcopy(parent)
		child14.side1_rot_vert(0, "up")
		if child14 not in explored:
			frontier.put((child14.heuristic(coordinates), deepcopy(child14)))
			explored.add(deepcopy(child14))

		child15 = deepcopy(parent)
		child15.side1_rot_vert(2, "down")
		if child15 not in explored:
			frontier.put((child15.heuristic(coordinates), deepcopy(child15)))
			explored.add(deepcopy(child15))

		child16 = deepcopy(parent)
		child16.side1_rot_vert(1, "down")
		if child16 not in explored:
			frontier.put((child16.heuristic(coordinates), deepcopy(child16)))
			explored.add(deepcopy(child16))

		child17 = deepcopy(parent)
		child17.side1_rot_vert(0, "down")
		if child17 not in explored:
			frontier.put((child17.heuristic(coordinates), deepcopy(child17)))
			explored.add(deepcopy(child17))
	print("couldn't find it :(")


def astar2(difficulty): # using admissible heuristic
	mycube = cube()
	mycube.shuffle(difficulty)
	explored = set()
	frontier = PriorityQueue()
	frontier.put((mycube.heuristic2(), deepcopy(mycube))) 
	explored.add(deepcopy(mycube))
	while(not frontier.empty()):
		parent = frontier.get()[1] # the cube object associated with each heuristic
		if parent.isWin():
			print("WOOOO WE FOUND IT!")
			return
		child0 = deepcopy(parent)
		child0.side0_rot_vert(0, "up")
		if child0 not in explored:
			frontier.put((child0.heuristic2(), deepcopy(child0)))
			explored.add(deepcopy(child0))

		child1 = deepcopy(parent)
		child1.side0_rot_vert(1, "up")
		if child1 not in explored:
			frontier.put((child1.heuristic2(), deepcopy(child1)))
			explored.add(deepcopy(child1))

		child2 = deepcopy(parent)
		child2.side0_rot_vert(2, "up")
		if child2 not in explored:
			frontier.put((child2.heuristic2(), deepcopy(child2)))
			explored.add(deepcopy(child2))

		child3 = deepcopy(parent)
		child3.side0_rot_vert(2, "down")
		if child3 not in explored:
			frontier.put((child3.heuristic2(), deepcopy(child3)))
			explored.add(deepcopy(child3))

		child4 = deepcopy(parent)
		child4.side0_rot_vert(1, "down")
		if child4 not in explored:
			frontier.put((child4.heuristic2(), deepcopy(child4)))
			explored.add(deepcopy(child4))

		child5 = deepcopy(parent)
		child5.side0_rot_vert(0, "down")
		if child5 not in explored:
			frontier.put((child5.heuristic2(), deepcopy(child5)))
			explored.add(deepcopy(child5))

		child6 = deepcopy(parent)
		child6.side0_rot_horiz(0, "left")
		if child6 not in explored:
			frontier.put((child6.heuristic2(), deepcopy(child6)))
			explored.add(deepcopy(child6))

		child7 = deepcopy(parent)
		child7.side0_rot_horiz(1, "left")
		if child7 not in explored:
			frontier.put((child7.heuristic2(), deepcopy(child7)))
			explored.add(deepcopy(child7))

		child8 = deepcopy(parent)
		child8.side0_rot_horiz(2, "left")
		if child8 not in explored:
			frontier.put((child8.heuristic2(), deepcopy(child8)))
			explored.add(deepcopy(child8))

		child9 = deepcopy(parent)
		child9.side0_rot_horiz(2, "right")
		if child9 not in explored:
			frontier.put((child9.heuristic2(), deepcopy(child9)))
			explored.add(deepcopy(child9))

		child10 = deepcopy(parent)
		child10.side0_rot_horiz(1, "right")
		if child10 not in explored:
			frontier.put((child10.heuristic2(), deepcopy(child10)))
			explored.add(deepcopy(child10))

		child11 = deepcopy(parent)
		child11.side0_rot_horiz(0, "right")
		if child11 not in explored:
			frontier.put((child11.heuristic2(), deepcopy(child11)))
			explored.add(deepcopy(child11))

		child12 = deepcopy(parent)
		child12.side1_rot_vert(2, "up")
		if child12 not in explored:
			frontier.put((child12.heuristic2(), deepcopy(child12)))
			explored.add(deepcopy(child12))

		child13 = deepcopy(parent)
		child13.side1_rot_vert(1, "up")
		if child13 not in explored:
			frontier.put((child13.heuristic2(), deepcopy(child13)))
			explored.add(deepcopy(child13))

		child14 = deepcopy(parent)
		child14.side1_rot_vert(0, "up")
		if child14 not in explored:
			frontier.put((child14.heuristic2(), deepcopy(child14)))
			explored.add(deepcopy(child14))

		child15 = deepcopy(parent)
		child15.side1_rot_vert(2, "down")
		if child15 not in explored:
			frontier.put((child15.heuristic2(), deepcopy(child15)))
			explored.add(deepcopy(child15))

		child16 = deepcopy(parent)
		child16.side1_rot_vert(1, "down")
		if child16 not in explored:
			frontier.put((child16.heuristic2(), deepcopy(child16)))
			explored.add(deepcopy(child16))

		child17 = deepcopy(parent)
		child17.side1_rot_vert(0, "down")
		if child17 not in explored:
			frontier.put((child17.heuristic2(), deepcopy(child17)))
			explored.add(deepcopy(child17))
	print("couldn't find it :(")


# iterative deepening helper

def deephelp(cube, depth, count):
	if cube.isWin(): # goal state found
		return (True, count)
	if depth == 0: # we've hit the depth limit and no goal state found
		return (False, None)

	# spawn off 18 children - one for each possible move

	child0 = deepcopy(cube)
	child0.side0_rot_vert(0, "up")
	if child0.isWin(): # this is necessary since otherwise it searches one extra ply
		return (True, count + 1)
	c0 = deephelp(child0, depth - 1, count + 1)

	child1 = deepcopy(cube)
	child1.side0_rot_vert(1, "up")
	c1 = deephelp(child1, depth - 1, count + 1)

	child2 = deepcopy(cube)
	child2.side0_rot_vert(2, "up")
	c2 = deephelp(child2, depth - 1, count + 1)

	child3 = deepcopy(cube)
	child3.side0_rot_vert(2, "down")
	c3 = deephelp(child3, depth - 1, count + 1)

	child4 = deepcopy(cube)
	child4.side0_rot_vert(1, "down")
	c4 = deephelp(child4, depth - 1, count + 1)
	
	child5 = deepcopy(cube)
	child5.side0_rot_vert(0, "down")
	c5 = deephelp(child5, depth - 1, count + 1)
	
	child6 = deepcopy(cube)
	child6.side0_rot_horiz(0, "left")
	c6 = deephelp(child6, depth - 1, count + 1)
	
	child7 = deepcopy(cube)
	child7.side0_rot_horiz(1, "left")
	c7 = deephelp(child7, depth - 1, count + 1)
	
	child8 = deepcopy(cube)
	child8.side0_rot_horiz(2, "left")
	c8 = deephelp(child8, depth - 1, count + 1)
	
	child9 = deepcopy(cube)
	child9.side0_rot_horiz(2, "right")
	c9 = deephelp(child9, depth - 1, count + 1)
	
	child10 = deepcopy(cube)
	child10.side0_rot_horiz(1, "right")
	c10 = deephelp(child10, depth - 1, count + 1)

	child11 = deepcopy(cube)
	child11.side0_rot_horiz(0, "right")
	c11 = deephelp(child11, depth - 1, count + 1)
	
	child12 = deepcopy(cube)
	child12.side1_rot_vert(2, "up")
	c12 = deephelp(child12, depth - 1, count + 1)
	
	child13 = deepcopy(cube)
	child13.side1_rot_vert(1, "up")
	c13 = deephelp(child13, depth - 1, count + 1)
	
	child14 = deepcopy(cube)
	child14.side1_rot_vert(0, "up")
	c14 = deephelp(child14, depth - 1, count + 1)
	
	child15 = deepcopy(cube)
	child15.side1_rot_vert(2, "down")
	c15 = deephelp(child15, depth - 1, count + 1)
	
	child16 = deepcopy(cube)
	child16.side1_rot_vert(1, "down")
	c16 = deephelp(child16, depth - 1, count + 1)
	
	child17 = deepcopy(cube)
	child17.side1_rot_vert(0, "down")
	c17 = deephelp(child17, depth - 1, count + 1)

	# the return statement below is saying:

	# if any child recursively found a goal state, return (True, depth it was found at)

	return ((c1[0] or c2[0] or c3[0] or c4[0] or c5[0] or c6[0] or c7[0] or c8[0] or c9[0] or c10[0] or c11[0] or c12[0] or c13[0] or c14[0] or c15[0] or c16[0] or c17[0]), (c1[1] or c2[1] or c3[1] or c4[1] or c5[1] or c6[1] or c7[1] or c8[1] or c9[1] or c10[1] or c11[1] or c12[1] or c13[1] or c14[1] or c15[1] or c16[1] or c17[1]))


def itdeep(difficulty, depth): # iterative deepening, user determines the difficulty (number of shuffles) and the depth that it can look to inclusive
	mycube = cube()
	mycube.shuffle(difficulty)
	for i in range(1, depth + 2): # + 2 to account for the fact that in helper, depth gets reduced before win state checked
		result = deephelp(mycube, i, 0)
		if result[0]:
			print("found at depth ", result[1])
			return
	print("not found within depth", depth)


def test(): # demonstrates iterative deepening and astar.
	print("Iterative deepening with a difficulty (number of shuffles) of 3, looking to a maximum depth of 4:\n\n")
	itdeep(3, 4)
	print("\nIterative deepening with a difficulty of 5, looking to a maximum depth of 2\n\n")
	itdeep(5, 2)
	print("\nA* with non admissable heuristic solving puzzle of difficulty 2\n\n")
	astar(2)
	print("\nA* with an admissable heuristic solving puzzle of difficulty 2\n\n")
	astar2(2)

test()


