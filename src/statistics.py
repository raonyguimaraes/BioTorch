#!/usr/bin/python

#database connection
execfile('database.py')


def get_frequency():
    sql = "SELECT * FROM snp WHERE has_genotype=1"
    cursor.execute(sql)
    snps = cursor.fetchall()
    for snp in snps:
	#print x['idsnp']
	snp_id = snp['idsnp']
	snp_name = snp['name']
	#print snp_name
	#get genotypes for each snp
	sql = "SELECT * FROM snp_genotype WHERE snp_id=%s" % (snp_id)
	cursor.execute(sql)
	snp_genotypes = cursor.fetchall()
	
	
	#get snp_id in 1000genomes
	sql = "SELECT * FROM 1000genomes_snpedia WHERE snpedia_snpid=%s" % (snp_id)
	cursor.execute(sql)
	snp_id_1000_genomes = cursor.fetchall()
	
	#if this snp is at the 1000 genoomes
	if len(snp_id_1000_genomes) > 0:
	    #for each SNP
	    for snp_1000 in snp_id_1000_genomes:
		
		print snp_name
		
		snp_id_10000 = snp_1000['1000genomes_snpid']
		
		#find snp 1000 genomes reference
		sql = "SELECT * FROM 1000genomes_snp WHERE id1000genomes_snp=%s" % (snp_id_10000)
		cursor.execute(sql)
		snp_1000_genotype = cursor.fetchall()
		
		#for each genotype find statistics about this genotypes
		for snp_genotype in snp_genotypes:
		    print snp_genotype['genotype']
		    print "Magnitude: "+snp_genotype['magnitude']
		    print "Summary: "+snp_genotype['summary']
		    print "Frequency: ",
		    
		    genotype_1 = snp_genotype['genotype'][1]
		    genotype_2 = snp_genotype['genotype'][3]
		    
		    
		    
		    #check all the possible genotypes
		    if (genotype_1 == snp_1000_genotype[0]['REF']) and (genotype_2 == snp_1000_genotype[0]['REF']):
			#genotype 00
			genotype_pattern = "0%0"
			#find frequency for this genotype
			sql = "SELECT * FROM genotype WHERE GT LIKE '%s' AND 1000genomes_id1000genomes = '%s'" % (genotype_pattern, snp_id_10000)
			cursor.execute(sql)
			genotype_statistics = cursor.fetchall()
			print len(genotype_statistics)
			
			##genotype 00
		    elif (genotype_1 == snp_1000_genotype[0]['REF']) and (genotype_2 == snp_1000_genotype[0]['ALT']):
			#genotype 01
			genotype_pattern = "0%1"
			#find frequency for this genotype
			sql = "SELECT * FROM genotype WHERE GT LIKE '%s' AND 1000genomes_id1000genomes = '%s'" % (genotype_pattern, snp_id_10000)
			cursor.execute(sql)
			genotype_statistics = cursor.fetchall()
			print len(genotype_statistics)
			
		    elif (genotype_1 == snp_1000_genotype[0]['ALT']) and (genotype_2 == snp_1000_genotype[0]['REF']):
			#genotype 10
			genotype_pattern = "1%0"
			#find frequency for this genotype
			sql = "SELECT * FROM genotype WHERE GT LIKE '%s' AND 1000genomes_id1000genomes = '%s'" % (genotype_pattern, snp_id_10000)
			cursor.execute(sql)
			genotype_statistics = cursor.fetchall()
			print len(genotype_statistics)
			
		    elif (genotype_1 == snp_1000_genotype[0]['ALT']) and (genotype_2 == snp_1000_genotype[0]['ALT']):
			#genotype 11
			genotype_pattern = "1%1"
			#find frequency for this genotype
			sql = "SELECT * FROM genotype WHERE GT LIKE '%s' AND 1000genomes_id1000genomes = '%s'" % (genotype_pattern, snp_id_10000)
			cursor.execute(sql)
			genotype_statistics = cursor.fetchall()
			print len(genotype_statistics)
		    else:
			print "0"
			
			
		    #print genotype_1
		    #print genotype_2
		
		
		#print snp_genotypes
		#print snp_1000_genotype
		
		#for each genotype found at snpedia search frequency in genotype
		
    
    
get_frequency()