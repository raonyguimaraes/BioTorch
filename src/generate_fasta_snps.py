#!/usr/bin/python

#get all sequences in FASTA format from DbSNP present in SNPedia

import os
# Biopython library
from Bio import Entrez

#database connection
execfile('database.py')


Entrez.email = "raonyguimaraes@gmail.com"     # Always tell NCBI who you are
filename = "all_snps.fasta"

FILE = open(filename,"w")
#Get all SNPs from Database
sql = "SELECT name FROM snp WHERE name LIKE 'RS%'"
cursor.execute(sql)
result = cursor.fetchall()
total = len(result)

# iterate through SNPs
for record in result:
  snp = x = record[0][2:]
  print total, snp
  total = total-1
  get_snp=False
  while get_snp != True:
    try:
        handle = Entrez.efetch(db="snp", id=snp, rettype="fasta", retmode="text")
    except IOError:
        print 'cannot get', snp
    else:
        get_snp=True

  #handle = Entrez.efetch(db="snp", id=snp, rettype="fasta", retmode="text")
  #remove 2 first lines from result
  handle.readline(),
  handle.readline()
  #remove blank lines from the end of the result
  contents = handle.read()
  new_string = ''

  for line in contents.split('\n'):
	  if line.strip():
		  new_string += line + '\n'
  FILE.writelines(new_string)
  
  #print new_string,

FILE.close() 

