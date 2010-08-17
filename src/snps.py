#!/usr/bin/python
#class to parse SNPS

from wikitools import wiki
from wikitools import api
from wikitools import page
from wikitools import category
import urllib2
from BeautifulSoup import BeautifulSoup
from BeautifulSoup import BeautifulStoneSoup
import re
import os
import xml.dom.minidom
from xml.dom.minidom import Node

filename = "Rs1801133"
url= "http://www.snpedia.com/index.php"
#path = "%s/%s" % (url,filename)
##doc = xml.dom.minidom.parse(path)

#page = urllib2.urlopen(path)
#soup = BeautifulSoup(page)

#soup = BeautifulStoneSoup(doc.toxml())


#database connection
execfile('database.py')


# create a Wiki object
site = wiki.Wiki("http://www.snpedia.com/api.php") 

# get a list of SNPs from SNPedia
def get_all_snps():
  # create a Wiki object
  site = wiki.Wiki("http://www.snpedia.com/api.php") 
  # define the params for the query
  cat = category.Category(site, "Is_a_snp")
  snps = cat.getAllMembers(namespaces=[0], titleonly=True)
  for x in snps:
    sql = "INSERT INTO %s (name) VALUES ('%s')" % ('snp', x) 
    cursor.execute(sql)

#download pages of SNPs from SNPEdia in XML files
def download_all_pages():
  folder= "../../data/snps"
  sql = "SELECT name FROM snp"
  cursor.execute(sql)
  result = cursor.fetchall()
  for x in result:
    snp = x[0]
    snp = snp.replace(" ","_")
    snp = snp.replace("'", "\\'")
    command= "mw-render --config=http://www.snpedia.com/api --writer=docbook --output=%s/%s.xml %s" % (folder, snp, snp)
    os.system(command)
  return

# get a list of snps from database
def get_snps_from_db():
  snps = []
  sql = "SELECT name FROM snp"
  cursor.execute(sql)
  result = cursor.fetchall()
  for x in result:
    snps.append(x[0])
  return snps

def parse_xml(snp_xml):
  print "Inicio"
  informal_table = snp_xml.getElementsByTagName("informaltable")
  get_genotypes(informal_table)
  print "Fim"

def printText(tags):
  text = ''
  for tag in tags:
    if tag.__class__ == NavigableString:
      text = text + ' ' + tag.strip()
    else:
      text = text + ' ' + tag.string
  return text

# find genotypes for the snps downloaded from SNPedia
def get_genotypes():
  snps = []
  #get all snps
  sql = "SELECT idsnp,name FROM snp WHERE idsnp NOT IN (SELECT snp_id FROM snp_genotype) AND has_genotype = 0"
  cursor.execute(sql)
  result = cursor.fetchall()
  total = len(result)
  print "Snps: "+str(total)
  for x in result:
    print "Total: "+str(total)
    
    total = total - 1
    #snps.append(x[0])
    snpid = x['idsnp']
    snp = x['name']
    print "snp_id: "+str(snpid)+" snp_name: "+str(snp)
    #snp = "Rs7495174"
    #print snp
    path = "%s/%s" % (url,snp)
    page = urllib2.urlopen(path)
    soup = BeautifulSoup(page)
    table = soup.find('table', id="querytable4")
    if (table is None):
      sql = "UPDATE snp SET has_genotype='2' WHERE idsnp = %s" % (snpid) 
      cursor.execute(sql)
      conn.commit()
      print "has no genotype"
    else:
      ##find headers
      #header = table.findAll("tr")[:1]
      #header_names = header[0].findAll("th")
      #for x in header_names:
	#teste = x.contents[0].string
	##print teste
      ##find contents
      contents = table.findAll("tr")[1:]
      for row in contents:
	gens = row.findAll("td")
	genotype = ""
	magnitude = ""
	summary = ""
	if(len(gens[0].contents) > 0):
	  genotype = gens[0].contents[0].string.replace(snp,"")
	if(len(gens[1].contents) > 0):
	  #print gens[1].contents
	  magnitude = gens[1].contents[0].string
	if(len(gens[2].contents) > 0):
	  summary = gens[2].contents[0].string
	  summary = MySQLdb.escape_string(summary)
	
	print "genotype: "+genotype+"magnitude: "+magnitude+"summary: "+summary
	sql = "UPDATE snp SET has_genotype='1' WHERE idsnp = %s" % (snpid) 
	cursor.execute(sql)
	sql = "INSERT INTO %s (genotype, magnitude, summary, snp_id) VALUES ('%s', '%s', '%s', '%s')" % ('snp_genotype', genotype, magnitude, summary, snpid)
	cursor.execute(sql)
	conn.commit()
def populate_db():
  #get_all_snps()
  get_genotypes()


populate_db()

cursor.close ()
conn.commit ()
conn.close ()