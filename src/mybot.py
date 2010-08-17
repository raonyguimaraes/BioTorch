#!/usr/bin/python
# -*- coding: utf-8 -*-
mydir = "./"
pwbdir = mydir + "pywikipedia/"
import sys
sys.path.append(pwbdir)
from wikipedia import *

language = "en"
family = "snpedia"
site = getSite(language,family)
pagename = "Rs1815739"
page = Page(site,pagename)
pagetext = page.get()
print pagetext
