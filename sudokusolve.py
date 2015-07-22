import numpy as np

class SudokuMatrix(object):
	def __init__(self, puzzle):
		self.original = np.array(puzzle).reshape(9,9)
		self.puzzle = np.array(puzzle).reshape(9,9)
		self.possibles = [[set() for i in range(9)] for i in range(9)]

	def cell(self, x, y):
		return self.puzzle[x,y]

	def row(self, n):
		return self.puzzle[n,:]

	def col(self, n):
		return self.puzzle[:,n]

	def area(self, x, y):
		x_pos, y_pos = (x//3)*3, (y//3)*3
		return self.puzzle[x_pos:x_pos+3, y_pos:y_pos+3]

	def _is_answer(self, x, y, deduce=False):
		if len(self.possibles[x][y]) == 1:
			answer = list(self.possibles[x][y])[0]
			self.commit_num_to_cell(x,y,answer)
		elif len(self.possibles[x][y]) == 0:
			pass
		else:
			if deduce:
				# rows
				pos = self.possibles[x][y] - set().union(*self.possibles[x])
				pos = pos - set().union(*[self.possibles[i][y] for i in xrange(0,9,1)]) # cols
				# area
				x_pos, y_pos = (x//3)*3, (y//3)*3
				for i in [x_pos + i for i in range(3)]:
					for j in [y_pos + i for i in range(3)]:
						pos = pos - self.possibles[i][j]

				if len(pos) == 1:
					answer = list(self.possibles[x][y])[0]
					self.commit_num_to_cell(x, y, answer)


	def _update_pos(self, x, y, num):
		self.possibles[x][y] = self.possibles[x][y] - set([num])
		self._is_answer(x,y)

	def _update_row_pos(self, x, num):
		for y in xrange(0,9,1):
			self._update_pos(x, y, num)

	def _update_col_pos(self, y, num):
		for x in xrange(0,9,1):
			self._update_pos(x, y, num)

	def _update_area_pos(self, x, y, num):
		x_pos, y_pos = (x//3)*3, (y//3)*3
		for x in [x_pos + i for i in range(3)]:
			for y in [y_pos + i for i in range(3)]:
				self._update_pos(x, y, num)

	def _calculate_unfilled(self, x, y):
		rowp = set(self.row(x))
		colp = set(self.col(y))
		areap = set(self.area(x, y).reshape(9))
		unfilled = set(xrange(1,10,1))
		final = unfilled - rowp - colp - areap
		return final

	def _commit_num_to_cell(self, x, y, num):
		self.puzzle[x,y] = num
		self.possibles[x][y] = set()
		self._update_row_pos(x, num)
		self._update_col_pos(y, num)
		self._update_area_pos(x, y, num)


	def solve_puzzle(self, maxiters=100000):
		for i in xrange(9):
			for j in xrange(9):
				if self.cell(i,j) == 0:
					self.possibles[i][j] = self.calculate_unfilled(i,j)
		
		iters = 0
		while len(self.puzzle[np.where( self.puzzle == 0 )]) > 0 and iters < maxiters:
			iters += 1
			# print iters
			for i in xrange(9):
				for j in xrange(9):
					self._is_answer(i, j, deduce=True)
		return self.puzzle


if __name__=="__main__":
	puzzle = [3,0,2,0,4,0,5,0,8,0,0,0,3,0,7,0,0,0,0,6,0,0,0,0,0,4,0,0,9,1,0,0,0,4,5,0,2,3,0,1,0,4,0,8,6,0,4,5,0,0,0,3,1,0,0,2,0,0,0,0,0,6,0,0,0,0,8,0,9,0,0,0,9,0,4,0,6,0,7,0,5]

	sk = SudokuMatrix(puzzle)
	sk.solve_puzzle()

	print sk.original
	print sk.puzzle
