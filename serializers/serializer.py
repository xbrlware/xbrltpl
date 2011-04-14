from filing import Filing
from calculation import calculation_serializer
from definition import definition_serializer
from instance import instance_serializer
from label import label_serializer
from presentation import presentation_serializer
from schema import schema_serializer

from datetime import date

import lxml

#Serializer determines which files need to be serialized and dispatches
#to the appropriate objects that serialize that type of file with a
#specific Filing object

#Documents:
#	Instance
#	Schema
#	Calculation Linkbase
#	Definition Linkbase
#	Label Linkbase
#	Presentation Linkbase

NAME_MAP = {
	'Instance': instance_serializer,
	'Schema': schema_serializer,
	'Calculation': calculation_serializer,
	'Definition': definition_serializer,
	'Label': label_serializer,
	'Presentation': presentation_serializer,
}

def lxml_to_text(nodes):
	"""Takes the lxml nodes and turns it into text"""
	return ''

class Serializer(object):
	def __init__(self, filing):
		assert isinstance(filing, Filing)
		self.filing = filing
	
	def format_date(self, given_date):
		if given_date is None:
			given_date = date.today()
		
		return '%d%d%d' % given_date.timetuple()[:3]
	
	def document_name(self, document, company, date=None):
		#Determined by SEC on http://sec.gov/info/edgar/edgarfm-vol2-v16.pdf
		#page 221 (6-5), section 6.6.3
		template_map = {
			'Instance': '%s-%s.xml',
			'Schema': '%s-%s.xsd',
			'Calculation': '%s-%s_cal.xml',
			'Definition': '%s-%s_def.xml',
			'Label': '%s-%s_lab.xml',
			'Presentation': '%s-%s_pre.xml',
		}

		template = template_map[document]
		return template % (company.ticker, self.format_date(date))

	def determine_files(self):
		"""Determines the documents that must be created
		for a valid sec filing."""
	
	def serialize(self, company, document, formatter=lxml_to_text):
		"""Returns the serialized xml data in the specified format.

		arguments:
			name:		type	description
			company:	Company	Company object (django model)
			document:	string	Name of document to be serialized (returned by determine_files)
			formatter:	(func)	Formatter. Should take lxml nodes as input, and return whatever. If you want lxml nodes, use (lambda x: x)
		"""

		document_serializer = NAME_MAP[document]
		data = document_serializer(filing=self.filing, company=company)

		return formatter(data)
	
	def serialized_docs(self, company, formatter=lxml_to-text, date=None):
		for document in self.determine_files():
			yield self.document_name(document, date), self.serialize(company, document, formatter=formatter)
