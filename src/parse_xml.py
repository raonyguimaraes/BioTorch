#!/usr/bin/python
#parse xml files from SNPedia

import xml.dom.minidom
from xml.dom.minidom import Node
import re


filename = "/home/raony/biotorch/data/medical_conditions/Alzheimer's_disease.xml"
doc = xml.dom.minidom.parse(filename)
#get a string and include a link to  pubmed if it has any reference Ex. 
def pubmed_link_insert(string):
   p = re.compile('PMID \d+')
   matches = p.findall(string)
   for x in matches:
     text_link = x.split()
     text_link = text_link[1][0:len(text_link[1])]
     new_text = "<a href=\"http://www.ncbi.nlm.nih.gov/pubmed/"+text_link+"?dopt=Abstract\">"+x+"</a>"
     string = string.replace(x, new_text)
   return string

def get_description(description):
  description = ""
  for node in doc.getElementsByTagName("para"):
      #print node.nodeType
      for node2 in node.childNodes:
	if node2.nodeType == node.TEXT_NODE:
	  string = pubmed_link_insert(node2.data)
	  
	  description = description + string
	else:
	  get_description(description)
	  
	  #link = node2.getAttribute("url")
	  #for node3 in node2.childNodes:
	    #text_link = node3.nodeValue
	    #print unicode(text_link).encode("utf-8")
	    #description = description + blah
  return description	    

#print get_description("")


