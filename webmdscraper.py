
from bs4 import BeautifulSoup as soup
import urllib2
import requests
import sqlite3

# Let's connect SQLite and initialize json
conn = sqlite3.connect('example.db')
# result = '['

# opening up connection, grabs page
my_url = 'https://www.webmd.com/a-to-z-guides/health-topics?pg=a'
uClient = urllib2.urlopen(my_url)
page_html = uClient.read()
uClient.close()

page_soup = soup(page_html, "html.parser")

groups = page_soup.findAll("div", {"class": "az-index-results-group"})

with open('webmd_diseases.csv', 'a') as the_file:

# filename = "medline_diseases.csv"
# f = open(filename, "w")

	headers = "disease, disease_url, summary\n"
	the_file.write(headers)
# f.write(headers)

#Grabs each name and link under each section
	for group in groups:
		topics = group.findAll("a")
		for topic in topics:
			disease = topic.text
			print "disease: " + disease
			disease_url = topic['href']
			
			# or write a function for getting the soup of the disease_url
			disClient = urllib2.urlopen(disease_url)
			dis_html = disClient.read()
			disClient.close()
			dis_soup = soup(dis_html, "html.parser")

			
			summary_container = dis_soup.findAll("div", {"class": "article-page active-page"})
			summary = summary_container[0].p.text
			print "summary: " + summary

		# print "disease_url: " + disease_url

			summary = ''.join(s for s in summary if ord(s)>31 and ord(s)<126).replace(",", ";").rstrip().encode('utf-8')

			the_file.write(disease.encode('utf-8') + "," + disease_url.encode('utf-8') + "," + summary + "\n")

the_file.close()