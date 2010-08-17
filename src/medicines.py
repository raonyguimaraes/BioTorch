#!/usr/bin/python

from wikitools import wiki
from wikitools import api
from wikitools import page
from wikitools import category
import urllib2
from BeautifulSoup import BeautifulStoneSoup
from BeautifulSoup import BeautifulSoup, SoupStrainer
import re
import os
import xml.dom.minidom
from xml.dom.minidom import Node

url= "http://www.snpedia.com/index.php"

#database connection
execfile('database.py')


# create a Wiki object
site = wiki.Wiki("http://www.snpedia.com/api.php") 

def get_all_medicines():
  # create a Wiki object
  site = wiki.Wiki("http://www.snpedia.com/api.php") 
  # define the params for the query
  cat = category.Category(site, "Is_a_medicine")
  medicines = cat.getAllMembers(namespaces=[0], titleonly=True)
  for x in medicines:
    x = x.replace("'", "\\'")
    sql = "INSERT INTO %s (name) VALUES ('%s')" % ('medicine', x) 
    cursor.execute(sql)
    conn.commit ()

def get_all_pages():
  folder= "../../data/medicines"
  sql = "SELECT name FROM medicine"
  cursor.execute(sql)
  result = cursor.fetchall()
  for x in result:
    medicine = x[0]
    medicine = medicine.replace(" ","_")
    command= "mw-render --config=http://www.snpedia.com/api --writer=docbook --output=%s/%s.xml %s" % (folder, medicine, medicine)
    os.system(command)
  return

    
#get a list of snps from DB
def get_snps_from_db():
  snps = {}
  sql = "SELECT idsnp,name FROM snp"
  cursor.execute(sql)
  result = cursor.fetchall()
  for x in result:
    snps[x['name'].lower()] = x['idsnp']
  #print snps
  return snps

#get a list of snps related with each medicine
def populate_medicine_has_snp_table():
  sql = "SELECT idmedicine, name FROM medicine WHERE has_snp=0"
  cursor.execute(sql)
  medicines = cursor.fetchall()
  snps = get_snps_from_db()
  total_medicines = len(medicines)
  print "Medicines Total: "+str(total_medicines)
  #print medical_conditions
  for x in medicines:
    print "Medicines remaining: "+str(total_medicines)
    total_medicines = total_medicines - 1
    #list of snps related with genes
    found_snps = []
    #list of snps that exists at SNpedia
    snps_snpedia = []
    medicine = x['name']
    medicine_id = x['idmedicine']
    print "medicine_id: "+str(medicine_id)+" medicine: "+str(medicine)
    #medical_condition = "ABO blood group"
    pagename = medicine.replace(" ","_")
    path = "%s/%s" % (url,pagename)
    page = urllib2.urlopen(path)
    #soup = BeautifulSoup(page)
    linkstosnpedia = SoupStrainer('a', title=re.compile('^I\d|^Rs\d'))
    tags =  BeautifulSoup(page, parseOnlyThese=linkstosnpedia)
    
    
    #check if there is SNPS related with this medicine
    if(len(tags)>0):
      #for each SNP FOUND
      print "has snps!"
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
	sql = "INSERT INTO %s (medicine_idmedicine, snp_idsnp) VALUES ('%s', '%s')" % ('medicine_has_snp', medicine_id, snpid)
	cursor.execute(sql)
	conn.commit()
      sql = "UPDATE medicine SET snps='%s' WHERE idmedicine = %s" % (all_snps, medicine_id) 
      cursor.execute(sql)
      sql = "UPDATE medicine SET has_snp='1' WHERE idmedicine = %s" % (medicine_id) 
      cursor.execute(sql)
      conn.commit()
      #print all_snps
    #if there is no snp related with that disease
    else:
      print "has no snps!"
      #update has_snp
      sql = "UPDATE medicine SET has_snp='2' WHERE idmedicine = %s" % (medicine_id)
      cursor.execute(sql)
      conn.commit()

#get_all_medicines()
#get_all_pages()
#populate_medicine_has_snp_table()
def populate_db():
  get_all_medicines()
  populate_medicine_has_snp_table()

populate_db()

cursor.close ()
conn.commit ()
conn.close ()

