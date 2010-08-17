#!/usr/bin/python

#parse results VCF Files @ 1000 genomes and insert individuals, SNPs and Genotypes to the database.

import os

#parse VCF files and insert to database

path = '/home/raony/biotorch/data/2010-04-03/pilot3/vcf/'

#
os.chdir(path)

#database connection
execfile('database.py')


#cursor.execute('INSERT INTO individual (idindividual,sample_id) VALUES (1, "test")')
#cursor.execute("SELECT VERSION()")
# Fetch a single row using fetchone() method.
#data = cursor.fetchone()

#print "Database version : %s " % data

indivs = {}

#con = MySQLdb.connect('localhost', 'root', '') # conecta no servidor
#con.select_db('') # seleciona o banco de dados
#cursor = con.cursor() # e preciso ter um cursor para se trabalhar
contsnp = 0
contgenotype = 0
for file in os.listdir(path):
  fh = open(file,"r")
  igot = fh.readlines()

  for line in igot:
	  if line.startswith("#") == 0:
		  about = line.split()
		  #print indivs
		  #insert snps at database table 1000genomes_snp
		  sql = "INSERT INTO %s (CHROM, POS, ID, REF, ALT, QUAL, FILTER, INFO) VALUES ('%s','%s','%s','%s','%s','%s','%s','%s')" % ('1000genomes_snp', about[0], about[1], about[2], about[3], about[4], about[5], about[6], about[7]) 
		  cursor.execute(sql)
		  #contsnp = contsnp +1
		  ##insert array format - genotype
		  snpid = conn.insert_id()
		  #print snpid
		  #insert genotypes at database table -> genotype
		  format = about[8].split(':')
		  for i in range(9, len(about)):
		    genotype = about[i].split(':')
		    #contgenotype = contgenotype +1
		    sql = "INSERT INTO %s (GT, DP,individual_idindividual, 1000genomes_id1000genomes) VALUES ('%s','%s','%s','%s')" % ('genotype', genotype[0], genotype[1], indivs[title[i]], snpid) 
		    #print sql
		    cursor.execute(sql)
		    #print indivs[title[i]], 
		    #print genotype
		    
		    #GT DP
		  
		  
		  #print about[0]
  #cur.execute('INSERT INTO data (time,temp,sat) VALUES (currtime,currtemp,currsat)')
  #cursor.execute('ALGUM SQL') # faz alguma query sql

		  #print about[2],
		  #print about[3]
	  else:
	    if line.startswith("#CHROM") > 0:
		  title = line.split()
		  for i in range(9, len(title)):
		    ind = title[i]
		    sql = "INSERT INTO %s (sample_id) VALUES ('%s')" % ('individual', ind) 
		    ##print sql,
		    cursor.execute(sql)
		    indivs[ind] = conn.insert_id()
		    #cursor.execute("  """)

		    #cursor.execute('INSERT INTO individual (sample_id) VALUES (2)')
		    #print title[i], 

  # Note - trailing comma on print to supress new line
  # Extra print statement to add a new line after the report
cursor.close ()
conn.commit ()
conn.close ()
print contsnp
print contgenotype
