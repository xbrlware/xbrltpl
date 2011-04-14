from base import TestCase
from datas.matrix import Matrix

import random

class MatrixTest(TestCase):
	def setUp(self):
		self.m = Matrix()
	
	def test_default(self):
		self.assertEqual(self.m[0,0], None)
		self.m.default = 0
		self.assertEqual(self.m[0,0], 0)

	def test_sets(self):
		#perform 1000 random index lookups
		indicies = set([])
		while len(indicies) < 1000:
			indicies.add(( random.randint(0,1000), random.randint(0, 1000) ))
		for e, (a,b) in enumerate(indicies):
			self.assertEqual(self.m[a,b], None)
			self.m[a,b] = e
			self.assertEqual(self.m[a,b], e)
	
	def test_negative_fails(self):
		for function in ['get', 'del']:
			attr = getattr(self.m, '__%sitem__' % function)
			self.assertRaises(IndexError, attr, (-1, 2))
			self.assertRaises(IndexError, attr, (2, -1))
			self.assertRaises(IndexError, attr, (-2, 5))
		
		self.assertRaises(IndexError, self.m.__setitem__, (-1, 2), 0)
		self.assertRaises(IndexError, self.m.__setitem__, (2, -1), 0)
		self.assertRaises(IndexError, self.m.__setitem__, (-2, 5), 0)