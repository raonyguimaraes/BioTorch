#!/usr/bin/python

#get a list of SNPs and insert at the database

import sys
import MySQLdb
import os

#connect to the database
conn = MySQLdb.connect (host = "localhost",
			user = "biotorch",
			passwd = "p4m3d1c1n3",
			db = "biotorch")
cursor = conn.cursor()


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
