#!/usr/bin/python
#class to parse Medical Conditions

from wikitools import wiki
from wikitools import api
from wikitools import page
from wikitools import category
import xml.dom.minidom
from xml.dom.minidom import Node
import os

import urllib2
#from BeautifulSoup import BeautifulSoup
from BeautifulSoup import BeautifulStoneSoup
from BeautifulSoup import BeautifulSoup, SoupStrainer
import re


#database connection
execfile('database.py')


# create a Wiki object
site = wiki.Wiki("http://www.snpedia.com/api.php") 
url= "http://www.snpedia.com/index.php"

def get_medical_conditions_from_db():
  
  medical_conditions = {}
  sql = "SELECT idmedical_condition, name FROM medical_condition"
  cursor.execute(sql)
  result = cursor.fetchall()
  #print result
  #for x in result:
    #medical_conditions[x['name']] = x['idmedical_condition']
  return result

def get_snps_from_db():
  snps = {}
  sql = "SELECT idsnp,name FROM snp"
  cursor.execute(sql)
  result = cursor.fetchall()
  for x in result:
    snps[x['name'].lower()] = x['idsnp']
  #print snps
  return snps

def get_all_medical_conditions():
  # create a Wiki object
  site = wiki.Wiki("http://www.snpedia.com/api.php") 
  # define the params for the query
  cat = category.Category(site, "Is_a_medical_condition")
  snps = cat.getAllMembers(namespaces=[0], titleonly=True)
  for x in snps:
    x = x.replace("'", "\\'")
    sql = "INSERT INTO %s (name) VALUES ('%s')" % ('medical_condition', x) 
    cursor.execute(sql)
    conn.commit ()

def get_all_pages():
  folder= "../../data/medical_conditions"
  sql = "SELECT name FROM medical_condition"
  cursor.execute(sql)
  result = cursor.fetchall()
  for x in result:
    medical_condition = x[0]
    medical_condition = medical_condition.replace(" ","_")
    medical_condition = medical_condition.replace("'", "\\'")
    command= "mw-render --config=http://www.snpedia.com/api --writer=docbook --output=%s/%s.xml %s" % (folder, medical_condition, medical_condition)
    os.system(command)
  return

def find_snps():
  tags = []
  snps = []
  result = get_snps_from_db()
  for snp in result:
    snps.append(snp.lower())
  medical_conditions = get_medical_conditions_from_db()
  for medical_condition in medical_conditions:
    filename = medical_condition.replace(" ","_") + ".xml" 
    folder= "/home/raony/biotorch/data/medical_conditions"
    path = "%s/%s" % (folder,filename)
    doc = xml.dom.minidom.parse(path)
    for node in doc.getElementsByTagName("ulink"):
      for node2 in node.childNodes:
	tags.append(node2.data)
    matches = [x for x in tags if x in snps]
    #print matches
    for node in doc.getElementsByTagName("para"):
      #print node.childNodes[0].nodeValue
      for node2 in node.childNodes:
	if node2.nodeType == node.TEXT_NODE:
	  print node2.nodeValue
	  #link = node3.getAttribute("url")
	  #print link
	for node3 in node2.childNodes:
	  print node3.getAttribute("url")	 
  return

def find_snps_from_snpedia():
  #medical_conditions = {}
  sql = "SELECT idmedical_condition, name FROM medical_condition WHERE has_snp=0"
  cursor.execute(sql)
  medical_conditions = cursor.fetchall()
  
#get_all_medical_conditions()
#get_all_pages()
#find_snps()

#find_snps_from_snpedia()

#test = get_medical_conditions_from_db()
#print len(test)
#print test['High blood pressure']
  snps = get_snps_from_db()
  total_medical_conditions = len(medical_conditions)
  print "Medical Condition Total: "+str(total_medical_conditions)
  #print medical_conditions
  for x in medical_conditions:
    print "Medical Condition: "+str(total_medical_conditions)
    total_medical_conditions = total_medical_conditions - 1
    #snps related with the medical condition
    found_snps = []
    #snps that exists at SNpedia
    snps_snpedia = []
    medical_condition = x['name']
    medical_condition_id = x['idmedical_condition']
    print "medical_condition_id: "+str(medical_condition_id)+" medical_condition: "+str(medical_condition)
    #medical_condition = "ABO blood group"
    pagename = medical_condition.replace(" ","_")
    path = "%s/%s" % (url,pagename)
    page = urllib2.urlopen(path)
    #soup = BeautifulSoup(page)
    linkstosnpedia = SoupStrainer('a', title=re.compile('^I\d|^Rs\d'))
    tags =  BeautifulSoup(page, parseOnlyThese=linkstosnpedia)
    
    
    #check if there is SNPS related with this disease
    if(len(tags)>0):
      #for each SNP FOUND
      print "has snps"
      for link in tags:
	snp = link.contents[0]
	found_snps.append(snp)
	#check if SNP is present at the database
	if snp in snps.keys():
	  #print "SNP Id"+str()
	  snpid = snps[snp]
	  snps_snpedia.append(snp)
      all_snps = ", ".join(found_snps)
      print "SNPS found: " + str(len(found_snps))
      snps_snpedia = list(set(snps_snpedia))
      for snp in snps_snpedia:
	snpid = snps[snp]
	sql = "INSERT INTO %s (medical_condition_idmedical_condition, snp_idsnp) VALUES ('%s', '%s')" % ('medical_condition_has_snp', medical_condition_id, snpid)
	cursor.execute(sql)
	conn.commit()
      sql = "UPDATE medical_condition SET snps='%s' WHERE idmedical_condition = %s" % (all_snps, medical_condition_id) 
      cursor.execute(sql)
      sql = "UPDATE medical_condition SET has_snp='1' WHERE idmedical_condition = %s" % (medical_condition_id) 
      cursor.execute(sql)
      conn.commit()
      #print all_snps
    #if there is no snp related with that disease
    else:
      print "has no snps"
      #update has_snp
      sql = "UPDATE medical_condition SET has_snp='2' WHERE idmedical_condition = %s" % (medical_condition_id) 
      cursor.execute(sql)
      conn.commit()
    
def populate_db():
  #get_all_medical_conditions()
  find_snps_from_snpedia()
  

populate_db()

cursor.close ()
conn.commit ()
conn.close ()

