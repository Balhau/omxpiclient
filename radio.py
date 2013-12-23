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
		radios=doc.xpath("//table[@id='thetable3']//td[1]//a")
		lines=doc.xpath("//table[@id='thetable3']//td[4]")
		channels=[]
		for line in lines:
			channels.append(line.findall("a"))
		return [radios,channels]
		
r=RadioService()
#c=r.getCountries()
p=r.getCountryRadio('portugal.html')

#print p[1]
#for radio in p:
#	print html.tostring(radio)

#for radio in p[0]:
#	print radio.attrib['href']
#	print radio.text_content()
#	print html.tostring(radio)
