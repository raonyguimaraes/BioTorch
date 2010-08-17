#!/usr/bin/python

#get a list of SNPs and insert at the database

import sys
import os


#database connection
execfile('database.py')



#for arg in sys.argv: 
filename = sys.argv[1]

f = open(filename, "r")
text = f.read()
snps = text.split(',')
for x in snps:
   sql = "INSERT INTO %s (snpid) VALUES ('%s')" % ('snpedia', x) 
   cursor.execute(sql)
    #print x+'\n'
    
#insert SNPs at the database


cursor.close ()
conn.commit ()
conn.close ()
