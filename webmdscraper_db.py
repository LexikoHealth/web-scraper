
from bs4 import BeautifulSoup as soup
import urllib2
import requests
import sqlite3
import pdb
import pymongo

# Let's connect to MongoDB
client = pymongo.MongoClient()
db = client.test
webmd_diseases = db.webmd_diseases
# result = '['

# opening up connection, grabs page
my_url = 'https://www.webmd.com/a-to-z-guides/health-topics?pg=a'
uClient = urllib2.urlopen(my_url)
page_html = uClient.read()
uClient.close()

page_soup = soup(page_html, "html.parser")

groups = page_soup.findAll("div", {"class": "az-index-results-group"})

# Grabs each name and link under each section
for group in groups:
		topics = group.findAll("a")
		for topic in topics:
			disease = topic.text
			print "disease: " + disease
			disease_url = topic['href']
			print "disease_url: " + disease_url
			
			# Or write a function for getting the soup of the disease_url
			disClient = urllib2.urlopen(disease_url)
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
								
			webmd_diseases.insert(
				# {
				# 	"name": disease
				# },
				{
					"name": disease,
					"url": disease_url,
					"sections": disease_container
					
				})


# To do:
# Need to also add this to mongodb
# Need to add letters B-Z