#!/usr/bin/python

import os
import xml.dom.minidom
from xml.dom.minidom import Node


#database connection
execfile('database.py')


#get a page in xml from SNPedia
def get_page(pagename, folder):
  #string="Alcohol_dependence"
  command= "mw-render --config=http://www.snpedia.com/api --writer=docbook --output=%s/%s.xml %s" % (folder, pagename, pagename)
  os.system(command)
  return

#parse an xml file from SNPedia
def parse_xml():
  return
  
def find_snps():
  tags = []
  snps = []
  sql = "SELECT snpid FROM snpedia"
  cursor.execute(sql)
  result = cursor.fetchall()
  for snp in result:
    snps.append(snp[0].lower())
  filename = "ABO_blood_group.xml"
  folder= "/home/raony/biotorch/data/medical_conditions"
  path = "%s/%s" % (folder,filename)
  doc = xml.dom.minidom.parse(path)
  for node in doc.getElementsByTagName("ulink"):
    for node2 in node.childNodes:
      tags.append(node2.data)
  matches = [x for x in tags if x in snps]
  print matches
  return

def get_medical_conditions():
  filename= "../all_medical_conditions"
  folder= "/home/raony/biotorch/data/medical_conditions"
  f = open(filename, "r")
  text = f.read()
  medical_conditions = text.split(',')
  for x in medical_conditions:
    x = x.replace(" ","_")
    pagename=x
    get_page(pagename, folder)
  return
  
def get_medicines():
  return
  
#get_medical_conditions()
find_snps()