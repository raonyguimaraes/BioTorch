#!/usr/bin/perl -w

#in order to execute this script you will need three software: MAQ, Samtools and Genome Unifier
#the genome reference file (ref.fasta) was downloaded from here http://hgdownload.cse.ucsc.edu/goldenPath/hg18/chromosomes/
#the example reads used was downloaded from ftp://ftp.1000genomes.ebi.ac.uk/vol1/ ftp/data/NA20792/
# the file dbsnp ROD was downloaded from here http://hgdownload.cse.ucsc.edu/goldenPath/hg18/database/snp129.txt.gz

# create a list of all fastq files in the current directory 
opendir(DIR, "/media/0bd6ddcf-bc1f-4c5 3-9708-33a9e45735fc/genome/sequence_read/");
@files = grep(/\_1.filt.fastq$/,readdir(DIR));
closedir(DIR);

#create a bin file from a reference genome
$maq_reference = "maq fasta2bfa ref.fasta ref.bfa";
system($maq_reference)
my @all_reads;

# print all the filenames in our array
foreach $file (@files) {
    print "$file\n";
    @name = split(/_/, $file);
    
    #create bin files from reads to align with the reference genome
    $maq_reads_1 = "maq fastq2bfq ".$name[0]."_1.filt.fastq.gz ".$name[0]."_reads_1.bfq";
    system($maq_reads_1);
    $maq_reads_2 = "maq fastq2bfq ".$name[0]."_2.filt.fastq.gz ".$name[0]."_reads_2.bfq";
    system($maq_reads_2);
    # align the reads with the reference genome
    $maq_align = "maq match ".$name[0]."_out.map ref.bfa ".$name[0]."_reads_1.bfq ".$name[0]."_reads_2.bfq";
    system($maq_align);
    push(@all_reads, "$name[0]_out.map");
    
}
# print "@all_reads\n";

#join all reads in one out.map file
$maq_merge = "maq mapmerge out.map @all_reads";
system($maq_merge);
#convert out.map to SAM and BAM

#Convert the .map file to .sam:
$maq2sam = "maq2sam-long out.map > assembly.sam";
system($maq2sam);

#If reference data is to be included, it must first be indexed from an input .fasta file:
$sam_index_ref = "samtools faidx ref.fasta";
system($sam_index_ref);

#generate BAM file
$sam2bam = "samtools view -b -S -t ref.fasta.fai -o assembly.bam assembly.sam";
system($sam2bam);

#To work efficiently, the .bam file must also be sorted
$sort_bam = "samtools sort assembly.bam assembly_sorted.bam";
system($sort_bam);

#The final step is to index the .bam file
$index_bam = "samtools index assembly_sorted.bam";
system($index_bam);

#Genome Unifier
$genome_unifier = "java -Xmx2048m –jar GenomeAnalysisTK.jar
-R ref.fasta
-T VariantFiltration
-B variant,VCF,individual.raw.vcf
-D dbsnp_129_b36.rod
--clusterWindowSize 10
--filterExpression “AB > 0.75 || DP > 300 || MQ0 > 40 || SB > -0.10”
-l INFO
-o individual.filtered.vcf";
system($genome_unifier);

# after this commmands you should get a file individual.filtered.vcf with all the SNPs identified for the individual
#to include at the database you have to run the script parse_vcf_files.py