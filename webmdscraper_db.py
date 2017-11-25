
from bs4 import BeautifulSoup as soup
import urllib2
import requests
import sqlite3
import pdb

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

	headers = "disease, disease_url, disease_header, disease_content\n"
	the_file.write(headers)
# f.write(headers)

#Grabs each name and link under each section
	for group in groups:
		topics = group.findAll("a")
		for topic in topics:
			disease = topic.text
			print "disease: " + disease
			disease_url = topic['href']
			print "disease_url: " + disease_url
			
			# or write a function for getting the soup of the disease_url
			disClient = urllib2.urlopen(disease_url)
			dis_html = disClient.read()
			disClient.close()
			dis_soup = soup(dis_html, "html.parser")

			new_soup = dis_soup.find("div", {"class":"article-body"})
			contents = new_soup.findAll(["p","section"])

			for content in contents:

				# pdb.set_trace()
				if (content.name == "section" and len(content.text.strip())>0):
					disease_header = content.text.strip()
					print "section: " + disease_header		
				if (content.name == "p" and len(content.text.strip())>0):
					disease_content = content.text.strip()
					print "content: " + disease_content
					#how to mass combine contents instead of creating a new line / "content" for each one

			disease_content = ''.join(c for c in disease_content if ord(c)>31 and ord(c)<126).replace(",", ";").rstrip().encode('utf-8')

			#need to fix this so it matches -- multiple content per section and multiple sections per diseases
			the_file.write(disease.encode('utf-8') + "," + disease_url.encode('utf-8') + "," + disease_header.encode('utf-8') + "," + disease_content.encode('utf-8') + "\n")

the_file.close()

#Need to also add this to mongodb