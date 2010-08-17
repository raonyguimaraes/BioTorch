#!/usr/bin/python

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

#get a list of all individuals
def get_individuals_from_db():
  individuals = []
  sql = "SELECT idindividual, sample_id FROM individual"
  cursor.execute(sql)
  result = cursor.fetchall()
  return result
  #for x in result:
    #individuals.append(x[0])
  #return individuals
  
#get a list of snps from 1000 genomes that are present at snpedia
def get_snps_from_1000genomes_at_snpedia():
  sql = "SELECT * from 1000genomes_snpedia"
  cursor.execute(sql)
  result = cursor.fetchall()
  return result

def populate_table_1000genomes_snpedia():
  snps_snpedia = {}
  sql = "SELECT idsnp, LOWER(name) as name from snp"
  cursor.execute(sql)
  result = cursor.fetchall()
  for x in result:
    #print x
    snps_snpedia[x['name']] = x['idsnp']
  sql = "SELECT id1000genomes_snp, ID FROM 1000genomes_snp WHERE ID IN (SELECT LOWER(name) FROM snp)"
  cursor.execute(sql)
  snps_1000genomes = cursor.fetchall()
  for snp in snps_1000genomes:
    snp_name = snp['ID']
    snpid_1000genomes = snp['id1000genomes_snp']
    snpid_snpedia = snps_snpedia[snp_name]
    sql = "INSERT INTO %s (1000genomes_snpid, snpedia_snpid) VALUES ('%s', '%s')" % ('1000genomes_snpedia', snpid_1000genomes, snpid_snpedia) 
    cursor.execute(sql)
    conn.commit ()
  
def find_snps_for_individuals():
  snps_1000genomes = {}
  snps_1000genomes_ids = []
  individuals = get_individuals_from_db()
  snps_snpedia = get_snps_from_1000genomes_at_snpedia()
  for x in snps_snpedia:
      snps_1000genomes_ids.append(str(x['1000genomes_snpid']))
  snps_1000 = "'"+"', '".join(snps_1000genomes_ids)+"'"
  sql = "SELECT ID, id1000genomes_snp FROM 1000genomes_snp WHERE id1000genomes_snp IN (%s)" % (snps_1000)
  cursor.execute(sql)
  result = cursor.fetchall()
  for x in result:
    snps_1000genomes[x['id1000genomes_snp']] = x['ID']
  #print snps_1000genomes
  for individual in individuals:
    id_individual = individual['idindividual']
    sampleid_individual = individual['sample_id']
    sql = "SELECT * from genotype WHERE individual_idindividual = '%s' AND 1000genomes_id1000genomes IN (%s) " % (id_individual, snps_1000)
    cursor.execute(sql)
    result = cursor.fetchall()
    
    print ">individuo:"+str(sampleid_individual)
    print "snps:"
    snp_individual = []
    for snp in result:
      #print snp['1000genomes_id1000genomes']
      #print genotype for that SNP !!!
      snp=snps_1000genomes[snp['1000genomes_id1000genomes']]
      snp_individual.append(snp) #print snp_name,
    print snp_individual
    #generate a list of snps_names for each individual
    snps_for_individual = ", ".join(snp_individual)
    sql = "UPDATE individual SET snps='%s' WHERE idindividual = %s" % (snps_for_individual, id_individual) 
    cursor.execute(sql)
    conn.commit()

def populate_db():
  populate_table_1000genomes_snpedia()
  find_snps_for_individuals()

#populate_db()

def find_medicalconditions_for_individuals():
    folder = "/home/raony/biotorch/data/reports/"
    sql = "SELECT * FROM individual"
    cursor.execute(sql)
    individuals = cursor.fetchall()
    sql = "SELECT * FROM medical_condition"
    cursor.execute(sql)
    medical_conditions = cursor.fetchall()
    for individual in individuals:
	
	individual_file_name = individual['sample_id']
	
	filename = individual_file_name+".txt"
	path = folder+filename
	file = open(path, 'w')
	
	print individual['sample_id']
	
	file.write(individual['sample_id']+"\n\n")
	id_individual = individual['idindividual']
	
	
	#sql = "SELECT * FROM genotype WHERE individual_idindividual = '%s'" % (individual['idindividual'])
	#cursor.execute(sql)
	#individual_snp_genotypes = cursor.fetchall()
	#print individual_genotype['1000genomes_id1000genomes']
	individual_snps = individual['snps'].split(', ')
	#print individual['snps']
	# find snps related with diseases
	
	#for each snp of the individual
	#for each medical condition
	for medical_condition in medical_conditions:
	    #if snp_individual in medical_condition['snps']
		#print snp genotype and snp magnitude
	    if medical_condition['snps'] is not None:
		##print medical_condition['snps']
		##print medical_condition['name']
		medical_condition_snps = medical_condition['snps'].split(', ')
		matches = [x for x in individual_snps if x in medical_condition_snps]
		#print matches
		if len(matches) > 0:
		   ##find genotype and magnitude = 
		   file.write("Medical Condition: "+medical_condition['name']+"\n\n")
		   print medical_condition['name'] 
		   #print matches
		   for snp in matches:
		       # find snp id in 1000genomes and snpedia
		        sql = "SELECT * FROM genotype INNER JOIN 1000genomes_snp ON `genotype`.`1000genomes_id1000genomes` = `1000genomes_snp`.`id1000genomes_snp` WHERE individual_idindividual = '%s' AND `1000genomes_snp`.ID = '%s'"  % (id_individual, snp) 
		        #print sql
		        
		        cursor.execute(sql)
			results = cursor.fetchall()
			#print len(results)
			for result in results:
			    #find snpedia snp id
			    file.write("Snp: "+result['ID']+"\t")
			    print "Snp: ",
			    print result['ID']
			    
			    #find genotype
			    snp_genotype = result['GT']
			    snp_genotype = snp_genotype.replace("0",result['REF'])
			    snp_genotype = snp_genotype.replace("1",result['ALT'])
			    
			    file.write("Snp Genotype: "+snp_genotype+"\n")
			    file.write("CHROM: "+str(result['CHROM'])+"\t")
			    file.write("POS: "+str(result['POS'])+"\n")
			    print "snp genotype: ",
			    print snp_genotype
			    
			    snp_1000_id = result['id1000genomes_snp']
			    sql = "SELECT * FROM 1000genomes_snpedia WHERE 1000genomes_snpid = %s" % (snp_1000_id)
			    #print sql
			    cursor.execute(sql)
			    snpedia_result = cursor.fetchall()
			    #print snpedia_result[0]
			    genotype_search = "("+snp_genotype+")"
			    genotype_search = genotype_search.replace("/",";")
			    #print genotype_search
			    
			    snpedia_id = snpedia_result[0]['snpedia_snpid']
			    #print "snpedia ID: "
			    #print snpedia_id
			    sql = "SELECT * FROM  `snp_genotype` WHERE snp_id = %s AND genotype = '%s'" % (snpedia_id, genotype_search)
			    cursor.execute(sql)
			    snp_genotype_result = cursor.fetchall()
			    if len(snp_genotype_result) > 0:
				file.write("Magnitude: "+snp_genotype_result[0]['magnitude']+"\n")
				file.write("Summary: "+snp_genotype_result[0]['summary']+"\n")
				print "Magnitude: ",
				print snp_genotype_result[0]['magnitude']
				
				print "Summary: ",
				print snp_genotype_result[0]['summary']
			    #print snp_genotype_result
			file.write("**************************************\n")
	file.close()

#find_medicalconditions_for_individuals()
find_medicalconditions_for_individuals()