#!/usr/bin/env python

from lxml import html
#print html.parse('http://someurl.at.domain').xpath('//body')[0].text_content()

class RadioService:

	def __init__(self):
		self.url='http://www.listenlive.eu/'

	def getCountries(self):
		doc=html.parse(self.url+'/index.html')
		links=doc.xpath("//table[@id='thetable']//a")
		return links
	
	def getCountryRadio(self,countryPage):
		doc=html.parse(self.url+'/'+countryPage)
		lines=doc.xpath("//table[@id='thetable3']//a")
		return lines
		
#r=RadioService()
#c=r.getCountries()
#p=r.getCountryRadio('portugal.html')

#for radio in p:
#	print html.tostring(radio)

#for country in c:
#	print country.attrib['href']
#	print country.text_content()
#	print html.tostring(country)
