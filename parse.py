# -*- coding: utf-8 -*-
from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup
import sys
import re

f = open("portraits_qs.txt", "w")
counter = 0
raw_html = open('portrait2015.html').read()
html = BeautifulSoup(raw_html, 'html.parser')
for item in html.select('li.live-item'):
	url = item.select("h3 a")[0]['href'].strip().encode("utf8")
	titre = item.select("h3 a")[0].text.strip().encode("utf8")
	date = item.select("p.live-datetime")[0].text.strip().encode("utf8")
	try:
		rubrique = item.select("a.slug")[0].text.strip().encode("utf8")
	except:
		rubrique = "Undefined"

	if rubrique == "Portrait" or rubrique == "portrait":
		counter = counter + 1
		f.write("CREATE\n")
		f.write('LAST\tLfr\t"%s"\n' % titre)
		f.write('LAST\tDfr\t"Portrait paru dans Libération"\n')
		f.write("LAST\tP31\tQ5707594\n") # Nature : article de presse
		f.write("LAST\tP361\tQ30091381\n") # Partie de : portrait de Libération
		f.write("LAST\tP407\tQ150\n") # Langue : français
		f.write("LAST\tP1433\tQ13717\n") # Publié dans : Libération
		f.write('LAST\tP953\t"%s"\n' % url) # Texte intégral disponible à
		f.write('LAST\tP1476\tfr:"%s"\n' % titre) # Texte intégral disponible à
		dateFormatted = re.sub(r"^(\d{2})\.(\d{2})\.(\d{2})$", r'+20\3-\2-\1T00:00:00Z/11', date)
		f.write('LAST\tP577\t%s\n' % dateFormatted) # Texte intégral disponible à

		f.write("\n")

		print "%s - %s" % (counter, date)

	else:
		print "%s non traité" % rubrique
