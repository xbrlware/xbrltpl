from template import Template
from collections import defaultdict
from datas.fact import Fact
from lxml_helpers.helpers import xml_namespace
#Chart object contains the data for a specific chart.

class Chart(object):
	"""Chart class holds a template and data to go in it"""

	def __init__(self, with_template=None, with_data=None):
		if with_template is not None:
			self._template = with_template
		else:
			self._template = Template()
		
		self._data = defaultdict(lambda: None)

	def pickle(self):
		import pickle
		return pickle.dumps(self)
	
	@property
	def role(self):
		return self._template.role
	
	def make_loc_fact(self):
		"""Return a Fact object that represents the base of this chart"""
		return Fact(**{
			'label': 'label',
			'href': 'href',
			'title': 'title',
		})
	
	@property
	def data_stream(self):
		"""Yields tuples:
			(fact, unit), context data"""
		for index in self._template.rows:
			for context in self._template.contexts:
				data = self._data[(index, context)]
				if data is not None:
					yield (index, context, data)
	
	def walk_tree(self):
		#pass through to underlying template
		for parent, child in self._template.walk_tree():
			yield parent, child

	@property
	def contexts(self):
		return self._template.contexts
	
	@property
	def facts(self):
		return self._template.facts
	
	@property
	def calculation_facts(self):
		return [fact for fact in self._template.facts if fact.is_calc]
	
	@property
	def has_calculation_facts(self):
		return len(self.calculation_facts) > 0
	
	@property
	def units(self):
		return self._template.units
	
	def transform_index(self, index):
		row, col = index
		
		try:
			row = self._template.ordered_tree()[row]
		except TypeError:
			pass
		try:
			col = self._template.contexts[col]
		except TypeError:
			pass
		return row, col

	
	def __getitem__(self, index):
		index = self.transform_index(index)
		return self._data[index]
	
	def __setitem__(self, index, data):
		index = self.transform_index(index)
		self._data[index] = data
	
	def __delitem__(self, index):
		index = self.transform_index(index)
		self._data[index] = None