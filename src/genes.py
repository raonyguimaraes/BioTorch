#!/usr/bin/python
#class to parse SNPS

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

#get genes from Snpedia using wikitools
def get_genes_from_snpedia():
  # create a Wiki object
  site = wiki.Wiki("http://www.snpedia.com/api.php") 
  # define the params for the query
  cat = category.Category(site, "Is_a_gene")
  genes = cat.getAllMembers(namespaces=[0], titleonly=True)
  return genes

#populate gene table of database
def populate_gene_table():
  genes = get_genes_from_snpedia()
  for x in genes:
    #print x
    x = x.replace("'", "\\'")
    sql = "INSERT INTO %s (name) VALUES ('%s')" % ('gene', x) 
    cursor.execute(sql)
    conn.commit ()
    
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

#get a list of snps related with each gene
def populate_gene_has_snp_table():
  sql = "SELECT idgene, name FROM gene WHERE has_snp=0"
  cursor.execute(sql)
  genes = cursor.fetchall()
  snps = get_snps_from_db()
  total_genes = len(genes)
  print "Genes Total: "+str(total_genes)
  #print medical_conditions
  for x in genes:
    print "Genes remaining: "+str(total_genes)
    total_genes = total_genes - 1
    #list of snps related with genes
    found_snps = []
    #list of snps that exists at SNpedia
    snps_snpedia = []
    gene = x['name']
    gene_id = x['idgene']
    print "gene_id: "+str(gene_id)+" gene: "+str(gene)
    #medical_condition = "ABO blood group"
    pagename = gene.replace(" ","_")
    path = "%s/%s" % (url,pagename)
    page = urllib2.urlopen(path)
    #soup = BeautifulSoup(page)
    linkstosnpedia = SoupStrainer('a', title=re.compile('^I\d|^Rs\d'))
    tags =  BeautifulSoup(page, parseOnlyThese=linkstosnpedia)
    
    
    #check if there is SNPS related with this disease
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
	sql = "INSERT INTO %s (gene_idgene, snp_idsnp) VALUES ('%s', '%s')" % ('gene_has_snp', gene_id, snpid)
	cursor.execute(sql)
	conn.commit()
      sql = "UPDATE gene SET snps='%s' WHERE idgene = %s" % (all_snps, gene_id) 
      cursor.execute(sql)
      sql = "UPDATE gene SET has_snp='1' WHERE idgene = %s" % (gene_id) 
      cursor.execute(sql)
      conn.commit()
      #print all_snps
    #if there is no snp related with that disease
    else:
      print "has no snps!"
      #update has_snp
      sql = "UPDATE gene SET has_snp='2' WHERE idgene = %s" % (gene_id) 
      cursor.execute(sql)
      conn.commit()
def populate_db():
  populate_gene_table()
  populate_gene_has_snp_table()
  
populate_db()

  