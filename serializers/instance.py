from lxml.builder import ElementMaker
from lxml_helpers.helpers import xml_namespace, convert_attribs
from common import gen_nsmap
import datetime

def instance_serializer(serializer):
	#looks like
	#<xbrli:xbrl [namespaces]>
	#<link:schemaRef to xsd document>
	#[<contexts>]
	#[<units>]
	#[<facts>]
	#</xbrli:xbrl>
	filing = serializer.filing
	date = filing.date
	company = filing.company
	nsmap = gen_nsmap(filing, 'Instance')
	maker = ElementMaker(namespace=nsmap['xbrli'], nsmap=nsmap)

	xbrl = maker.xbrl()
	with xml_namespace(maker, 'link'):
		schemaRef = maker.schemaRef(**convert_attribs({
			'xlink:type': 'simple',
			'xlink:href': serializer.document_name('Schema'),
		}, nsmap))
	
	xbrl.append(schemaRef)

	#Loop over contexts, appending to xbrl
	for context in set(filing.contexts):
		xbrl.append(context.serialize(maker, company.cik))
	
	#Loop over units, appending to xbrl
	for unit in set(filing.units):
		xbrl.append(unit.serialize(maker))
	
	#Loop over facts appending to xbrl
	for (fact, unit), context, value in filing.data_stream:
		xbrl.append(fact.serialize(value, unit, context, maker))

	return xbrl
