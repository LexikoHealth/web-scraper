
from bs4 import BeautifulSoup as soup
import urllib2
import requests
import sqlite3
import pdb
import pymongo

# opening up connection, grabs page
			
			# Or write a function for getting the soup of the disease_url
disClient = urllib2.urlopen("https://www.webmd.com/lung/alpha-1-antitrypsin-deficiency-rare")
dis_html = disClient.read()
disClient.close()
dis_soup = soup(dis_html, "html.parser")

new_soup = dis_soup.find("div", {"class":"article-body"})
contents = new_soup.findAll(["p","section","ul"])

disease_content_container = []
disease_container = []

section_name = "Overview"

for content in contents:

	# pdb.set_trace()
	if (content.name == "section" and len(content.text.strip())>0):

		disease_header = section_name
		section_name = content.text.strip()
		#print "section: " + disease_header
		
		# disease_container = disease_header
		disease_container.append({
			"name": disease_header,
			"content": disease_content_container
		})
		print disease_header
		print disease_content_container

		#disease_container[disease_header].append(disease_content_container)
		disease_content_container = []
		
	if (content.name == "p" or content.name == "ul" and len(content.text.strip())>0):
		disease_content = content.text.strip()
		#print "content: " + disease_content
		disease_content_container.append(disease_content)
		

		# How to mass combine contents instead of creating a new line / "content" for each one

# Need to fix this so it matches -- multiple content per section and multiple sections per diseases
# the_file.write(disease.encode('utf-8') + "," + disease_url.encode('utf-8') + "," + disease_header.encode('utf-8') + "," + disease_content.encode('utf-8') + "\n")

# Write upsert function if needed?: webmd_diseases.update(disease, url, {upsert:true})

# the_file.close()

# To do:
# Need to also add this to mongodb
# Need to add letters B-Z